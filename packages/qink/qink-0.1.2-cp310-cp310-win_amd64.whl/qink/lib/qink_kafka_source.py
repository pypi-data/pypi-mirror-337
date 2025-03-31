import logging
from typing import Optional, Set
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from aiokafka.abc import ConsumerRebalanceListener
from aiokafka.structs import TopicPartition
from .qink_assignment_listener import QinkAssignmentListener
from .qink_source import QinkSource
from .models import PartitionState
from .qink_source import Message


class QinkKafkaSource(QinkSource):

    @staticmethod
    def from_env(logger: logging.Logger) -> "QinkKafkaSource":
        from qink.lib.config import Config

        config = Config.from_env()

        return QinkKafkaSource(
            kafka_bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            kafka_group_id=config.KAFKA_GROUP_ID,
            kafka_topic=config.KAFKA_TOPIC,
            kafka_sasl_mechanism=config.KAFKA_SASL_MECHANISM,
            kafka_security_protocol=config.KAFKA_SECURITY_PROTOCOL,
            kafka_sasl_username=config.KAFKA_SASL_USERNAME,
            kafka_sasl_password=config.KAFKA_SASL_PASSWORD,
            logger=logger,
        )

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        kafka_group_id: str,
        kafka_topic: str,
        kafka_sasl_mechanism: str,
        kafka_security_protocol: str,
        kafka_sasl_username: str,
        kafka_sasl_password: str,
        logger: logging.Logger,
    ):
        super().__init__(logger)

        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_group_id = kafka_group_id
        self.kafka_topic = kafka_topic
        self.kafka_sasl_mechanism = kafka_sasl_mechanism
        self.kafka_security_protocol = kafka_security_protocol
        self.kafka_sasl_username = kafka_sasl_username
        self.kafka_sasl_password = kafka_sasl_password
        self.logger = logger
        self._consumer: Optional[AIOKafkaConsumer] = None

    async def stop(self):
        if self._consumer is not None:
            self._consumer.stop()
            self._consumer = None

    async def seek(self, state: PartitionState):
        self._consumer.seek(
            partition=TopicPartition(
                topic=self.kafka_topic, partition=state.partition
            ),
            offset=state.offset + 1,
        )

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            group_id=self.kafka_group_id,
            sasl_mechanism=self.kafka_sasl_mechanism or "PLAINTEXT",
            security_protocol=self.kafka_security_protocol or "PLAINTEXT",
            sasl_plain_username=self.kafka_sasl_username,
            sasl_plain_password=self.kafka_sasl_password,
            enable_auto_commit=False,
            consumer_timeout_ms=-1,  # Never timeout
        )

        self._consumer.subscribe(
            [self.kafka_topic],
            listener=self.KafkaAssignmentListener(
                self.logger,
                self._listener,
            ),
        )

        await self._consumer.start()

    async def get_many(self, partition: int):
        records: dict[TopicPartition, list[ConsumerRecord]] = (
            await self._consumer.getmany(
                TopicPartition(topic=self.kafka_topic, partition=partition),
                timeout_ms=1_000,
                max_records=1_000,
            )
        )

        # Return only messages
        return [
            Message(
                key=record.key,
                value=record.value,
                timestamp=record.timestamp,
                offset=record.offset,
            )
            for record in records[
                TopicPartition(topic=self.kafka_topic, partition=partition)
            ]
        ]

    class KafkaAssignmentListener(ConsumerRebalanceListener):

        def __init__(
            self,
            logger: logging.Logger,
            listener: QinkAssignmentListener,
        ):
            self.logger = logger
            self._listener = listener

        async def on_partitions_revoked(self, revoked: Set[TopicPartition]):
            self._listener.on_partitions_revoked(
                [partition.partition for partition in revoked]
            )

        async def on_partitions_assigned(self, assigned: Set[TopicPartition]):
            self._listener.on_partitions_assigned(
                [partition.partition for partition in assigned]
            )
