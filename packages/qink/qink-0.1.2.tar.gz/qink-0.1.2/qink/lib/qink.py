import asyncio
from typing import Dict, Optional, Union
from enum import Enum
import logging
from .qink_source import QinkSource
from .models import KeyState, PartitionState
from .qink_storage import QinkStorage
from .qink_storage_provider import QinkStorageProvider
from .qink_assignment_listener import QinkAssignmentListener
from multiprocessing import Process, connection
from dataclasses import dataclass
from .partitioner import DefaultPartitioner
from datetime import timedelta
from .qink_source import Message


class Qink:
    State = Enum("State", ["STOPPED", "CONNECTING", "CONSUMING"])

    def __init__(
        self,
        logger: logging.Logger,
        storage_provider: QinkStorageProvider,
        workers_per_partition: int,
        checkpoint_interval: timedelta,
    ):
        self._state = Qink.State.STOPPED
        self._state_task: Optional[asyncio.Task] = None
        self._logger = logger
        self._partition_consumers: Dict[int, Qink.PartitionConsumer] = {}
        self._storage = QinkStorage(storage_provider, logger)
        self._source: Optional[QinkSource] = None
        self._workers_per_partition = workers_per_partition
        self._checkpoint_interval = checkpoint_interval

    def source(self, source: QinkSource):
        self._source = source
        self._source.set_listener(self.AssignmentListener(self))

        return self

    def start(self):
        self._state = Qink.State.CONNECTING

        self._cancel_state_task()

        self._state_task = asyncio.create_task(self._run())

    async def stop(self):
        self._state = Qink.State.STOPPED

        self.stop_all_partition_consumers()
        self._cancel_state_task()

    def _cancel_state_task(self):
        if self._state_task is not None:
            self._state_task.cancel()

    async def _run(self):
        while self._state != Qink.State.STOPPED:
            try:
                self.stop_all_partition_consumers()

                await self._connect()
                break
            except Exception as e:
                self._logger.error(f"Error in Qink _run: {e}")
                await asyncio.sleep(1)

    async def _connect(self):
        self._logger.info("Connecting to source...")
        self._state = Qink.State.CONNECTING

        if self._source is not None:
            await self._source.stop()

        await self._source.start()

        self._state = Qink.State.CONSUMING
        self._logger.info("Source started")

    def stop_partition_consumer(self, partition: int):
        if partition in self._partition_consumers:
            self._partition_consumers[partition].dispose()
            del self._partition_consumers[partition]

    def stop_all_partition_consumers(self):
        for partition in self._partition_consumers:
            self.stop_partition_consumer(partition)

    class AssignmentListener(QinkAssignmentListener):
        def __init__(self, qink: "Qink"):
            self.qink = qink

        def on_partitions_revoked(self, revoked: list[int]):
            self.qink._logger.info(f"Partitions revoked: {len(revoked)}")

            for partition in revoked:
                self.qink.stop_partition_consumer(partition)

        def on_partitions_assigned(self, assigned: list[int]):
            self.qink._logger.info(f"Partitions assigned: {len(assigned)}")

            for partition in assigned:
                self.qink.stop_partition_consumer(partition)

                self.qink._partition_consumers[partition] = (
                    Qink.PartitionConsumer(
                        partition=partition,
                        source=self.qink._source,
                        storage=self.qink._storage,
                        logger=self.qink._logger,
                        workers_per_partition=self.qink._workers_per_partition,
                        checkpoint_interval=self.qink._checkpoint_interval,
                    )
                )

    class PartitionConsumer:

        def __init__(
            self,
            partition: int,
            source: QinkSource,
            storage: QinkStorage,
            logger: logging.Logger,
            workers_per_partition: int,
            checkpoint_interval: timedelta,
        ):
            self._partition = partition
            self._source = source
            self._storage = storage
            self._logger = logger
            self._task = asyncio.create_task(self._run())
            self._workers_per_partition = workers_per_partition
            self._checkpoint_interval = checkpoint_interval
            self._is_checkpoint_task_running = False
            self._all_workers_drained = True
            self._state: Optional[PartitionState] = None
            self._checkpoint_task = asyncio.create_task(
                self._checkpoint_loop()
            )
            self._worker_processes: list[
                "Qink.PartitionConsumer.WorkerProcess"
            ] = []

            for _ in range(workers_per_partition):
                listener = connection.Listener(address=("localhost", 0))

                process = Process(
                    target=self._worker_process,
                    args=(listener.address,),
                )

                self._worker_processes.append(
                    Qink.PartitionConsumer.WorkerProcess(
                        process=process,
                        listener=listener,
                        conn_future=asyncio.get_running_loop().run_in_executor(
                            None, listener.accept
                        ),
                    )
                )

                process.start()

        @dataclass
        class WorkerProcess:
            process: Process
            conn_future: asyncio.Future[connection.Connection]
            listener: connection.Listener

        def dispose(self):
            self._task.cancel()
            self._checkpoint_task.cancel()

            for process in self._worker_processes:
                process.process.terminate()
                process.listener.close()
                asyncio.create_task(
                    self.close_conn_future(process.conn_future)
                )

        async def close_conn_future(
            self, conn_future: asyncio.Future[connection.Connection]
        ):
            try:
                (await conn_future).close()
            except Exception:
                pass

        @staticmethod
        def _worker_process(address: tuple[str, int]):
            client = connection.Client(address)

            async def main(client: connection.Connection):
                loop = asyncio.get_running_loop()

                states: list[KeyState] = await loop.run_in_executor(
                    None, client.recv
                )

                while True:
                    try:
                        data: Union[list[Message], str] = (
                            await loop.run_in_executor(None, client.recv)
                        )

                        if data == b"collect_key_states":
                            client.send(states)
                        else:
                            # TODO: Handle data
                            print(data)

                            client.send(b"drained")
                    except Exception as e:
                        print(e)
                        await asyncio.sleep(1)

            asyncio.run(main(client))

        async def _checkpoint_loop(self):
            while True:
                await asyncio.sleep(self._checkpoint_interval.total_seconds())

                self._is_checkpoint_task_running = True

                self._logger.info(
                    f"[p{self._partition}] Checkpoint loop started"
                )

                await self._wait_all_workers_drained()

                self._logger.info(
                    f"[p{self._partition}] Collecting key states"
                )

                # 1. Collect all key states from workers
                collection_start_time = asyncio.get_event_loop().time()
                key_states = await self._collect_key_states()
                collection_end_time = asyncio.get_event_loop().time()
                collection_duration = (
                    collection_end_time - collection_start_time
                )

                self._logger.info(
                    f"[p{self._partition}] Collected {len(key_states)} key "
                    f"states in {collection_duration:.3f}s"
                )

                # 2. Add key states to partition state
                self._state.state.update(
                    {key_state.key: key_state for key_state in key_states}
                )

                # 3. Store the partition state
                save_start_time = asyncio.get_event_loop().time()
                await self._storage.set_partition_state(
                    self._partition, self._state
                )
                save_end_time = asyncio.get_event_loop().time()
                save_duration = save_end_time - save_start_time

                self._is_checkpoint_task_running = False

                self._logger.info(
                    f"[p{self._partition}] Checkpoint done - "
                    f"collected in {collection_duration:.3f}s, "
                    f"saved in {save_duration:.3f}s, "
                    f"total: {(collection_duration + save_duration):.3f}s"
                )

        async def _collect_key_states(self):
            key_states: list[KeyState] = []

            collection_tasks: list[asyncio.Task] = []

            for process in self._worker_processes:
                collection_tasks.append(
                    asyncio.create_task(
                        self.collect_key_states_from_worker(
                            process, key_states
                        )
                    )
                )

            await asyncio.gather(*collection_tasks)

            return key_states

        async def collect_key_states_from_worker(
            self,
            process: "Qink.PartitionConsumer.WorkerProcess",
            key_states: list[KeyState],
        ):
            loop = asyncio.get_running_loop()
            conn = await process.conn_future

            await loop.run_in_executor(None, conn.send, b"collect_key_states")

            key_states.extend(await loop.run_in_executor(None, conn.recv))

        async def _run(self):
            self._state = await self.get_partition_state_from_storage()

            await self.distribute_state_to_workers(self._state)

            await self._source.seek(self._state)

            while True:
                messages = await self._source.get_many(self._partition)

                await self.wait_for_checkpoint_task()

                if len(messages) > 0:
                    self._all_workers_drained = False
                    self._logger.info(f"Distributing {len(messages)} messages")

                    # Get the max offset in case list is not sorted.
                    # This has to be before _wait_all_workers_drained
                    # because _checkpoint_loop must see the latest offset.
                    self._state.offset = max(
                        message.offset for message in messages
                    )

                    await self._distribute_messages(messages)
                    await self._collect_all_workers_drained()

                    self._all_workers_drained = True

                    self._logger.info(f"Processed {len(messages)} messages")

        async def _wait_all_workers_drained(self):
            while not self._all_workers_drained:
                await asyncio.sleep(0.5)

        async def _collect_all_workers_drained(self):
            """Wait for all worker processes to drain their messages.

            This method waits for all worker processes to send a 'drained'
            message back to the main process, indicating they have
            processed all messages.
            """
            loop = asyncio.get_running_loop()

            for i in range(self._workers_per_partition):
                process = self._worker_processes[i]
                conn = await process.conn_future

                try:
                    # Wait for the worker to send a 'drained' message
                    response = await loop.run_in_executor(None, conn.recv)

                    if response != b"drained":
                        self._logger.warning(
                            f"Worker {i} sent unexpected response: {response}"
                        )
                except Exception as e:
                    self._logger.error(
                        f"Error waiting for worker {i} to drain: {e}"
                    )

        async def _distribute_messages(self, messages: list[Message]):
            key_groups: list[list[Message]] = [
                [] for _ in range(self._workers_per_partition)
            ]

            partition = DefaultPartitioner(range(self._workers_per_partition))

            loop = asyncio.get_running_loop()

            for message in messages:
                target_group = partition(message.key)

                key_groups[target_group].append(message)

            for i in range(self._workers_per_partition):
                process = self._worker_processes[i]

                conn = await process.conn_future

                await loop.run_in_executor(None, conn.send, key_groups[i])

        async def wait_for_checkpoint_task(self):
            while self._is_checkpoint_task_running:
                await asyncio.sleep(0.5)

        async def get_partition_state_from_storage(self):
            state = await self._storage.get_partition_state(self._partition)

            if state is None:
                self._logger.info(
                    f"No state for partition {self._partition}, "
                    f"starting from offset 0"
                )
                state = PartitionState(
                    partition=self._partition, offset=0, state={}
                )

                await self._storage.set_partition_state(self._partition, state)
            else:
                self._logger.info(
                    f"State found for partition {self._partition}, "
                    f"starting from offset {state.offset}"
                )

            return state

        async def distribute_state_to_workers(self, state: PartitionState):
            # Split the state into key groups
            key_groups: list[list[KeyState]] = [
                [] for _ in range(self._workers_per_partition)
            ]
            partition = DefaultPartitioner(range(self._workers_per_partition))
            loop = asyncio.get_running_loop()

            for key, value in state.state.items():
                target_group = partition(key)

                key_groups[target_group].append(KeyState(key=key, state=value))

            # Send the key states to the worker processes
            for i in range(self._workers_per_partition):
                process = self._worker_processes[i]

                conn = await process.conn_future

                await loop.run_in_executor(None, conn.send, key_groups[i])
