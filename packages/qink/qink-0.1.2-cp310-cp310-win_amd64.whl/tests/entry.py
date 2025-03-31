import asyncio
from qink.lib.qink import Qink
from qink.lib.qink_azure_storage_provider import (
    QinkAzureStorageProvider,
)
from qink.lib.logger import setup_logger
from qink.lib.qink_kafka_source import QinkKafkaSource
from datetime import timedelta

logger = setup_logger(__name__)


async def main():
    logger.info("Starting...")

    (
        Qink(
            logger=logger,
            storage_provider=QinkAzureStorageProvider.from_env(logger),
            workers_per_partition=2,
            checkpoint_interval=timedelta(seconds=30),
        )
        .source(QinkKafkaSource.from_env(logger))
        .start()
    )

    await asyncio.sleep(10)

    (
        Qink(
            logger=logger,
            storage_provider=QinkAzureStorageProvider.from_env(logger),
            workers_per_partition=2,
            checkpoint_interval=timedelta(seconds=30),
        )
        .source(QinkKafkaSource.from_env(logger))
        .start()
    )

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
