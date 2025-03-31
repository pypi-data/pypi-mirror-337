import pytest
import asyncio
from qink.lib.config import Config
from qink.lib.org_config_store import OrgConfigStore
from qink.lib.qink import Qink
from qink.lib.qink_azure_storage_provider import (
    QinkAzureStorageProvider,
)
from qink.lib.logger import setup_logger
from qink.lib.qink_kafka_source import QinkKafkaSource

logger = setup_logger(__name__)


@pytest.mark.asyncio
async def test_entry():
    logger.info("Starting...")

    config = Config.from_env()

    OrgConfigStore(
        core_api_key=config.CORE_API_KEY,
        core_api_url=config.CORE_API_URL,
        redis_host=config.REDIS_HOST,
        redis_port=config.REDIS_PORT,
        redis_password=config.REDIS_PASSWORD,
        redis_config_topic=config.REDIS_CONFIG_TOPIC,
        redis_ssl=config.REDIS_SSL,
        logger=logger,
    )

    (
        Qink(
            logger=logger,
            storage_provider=QinkAzureStorageProvider.from_env(logger),
        )
        .source(QinkKafkaSource.from_env(logger))
        .start()
    )

    await asyncio.sleep(10)

    (
        Qink(
            logger=logger,
            storage_provider=QinkAzureStorageProvider.from_env(logger),
        )
        .source(QinkKafkaSource.from_env(logger))
        .start()
    )

    while True:
        await asyncio.sleep(1)
