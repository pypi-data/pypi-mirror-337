import asyncio
from typing import Dict, Optional
from enum import Enum
import logging
from .qink_source import QinkSource
from .models import PartitionState
from .qink_storage import QinkStorage
from .qink_storage_provider import QinkStorageProvider
from .qink_assignment_listener import QinkAssignmentListener


class Qink:
    State = Enum("State", ["STOPPED", "CONNECTING", "CONSUMING"])

    def __init__(
        self,
        logger: logging.Logger,
        storage_provider: QinkStorageProvider,
    ):
        self._state = Qink.State.STOPPED
        self._state_task: Optional[asyncio.Task] = None
        self._logger = logger
        self._partition_consumers: Dict[int, Qink.PartitionConsumer] = {}
        self._storage = QinkStorage(storage_provider, logger)
        self._source: Optional[QinkSource] = None

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
                    )
                )

    class PartitionConsumer:

        def __init__(
            self,
            partition: int,
            source: QinkSource,
            storage: QinkStorage,
            logger: logging.Logger,
        ):
            self._partition = partition
            self._source = source
            self._storage = storage
            self._logger = logger
            self._task = asyncio.create_task(self._run())

        def dispose(self):
            self._task.cancel()

        async def _run(self):
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

            await self._source.seek(state)

            while True:
                messages = await self._source.get_many(self._partition)

                if len(messages) > 0:
                    self._logger.info(
                        f"[p{self._partition}] "
                        f"Received {len(messages)} messages"
                    )
