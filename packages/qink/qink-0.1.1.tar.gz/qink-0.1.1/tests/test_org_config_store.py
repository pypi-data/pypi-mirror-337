import asyncio
import logging
import pytest
from unittest.mock import patch
from redis import asyncio as aioredis
from qink.lib.config import Config
from qink.lib.org_config_store import OrgConfigStore
from qink.lib.core_api_client import CoreAPIConfig, Org, Processor
from tests.test_utils import MockCoreAPIClient
from redis.backoff import ConstantBackoff
from redis.exceptions import TimeoutError, ConnectionError
from redis.retry import Retry


@pytest.fixture
def config():
    return Config.from_env()


@pytest.fixture
def initial_orgs():
    return [
        Org(_id="org1", name="Test Org 1"),
        Org(_id="org2", name="Test Org 2"),
    ]


@pytest.fixture
def updated_orgs():
    return [
        Org(_id="org1", name="Updated Org 1"),
        Org(_id="org2", name="Updated Org 2"),
        Org(_id="org3", name="New Org 3"),
    ]


@pytest.fixture
def processors():
    return [
        Processor(
            _id="proc1",
            orgId="org1",
            title="Test Processor",
            processor="test",
            options={},
            isEnabled=True,
            dependsOn=None,
        )
    ]


@pytest.mark.asyncio
async def test_redis_message_reloads_config(
    config, initial_orgs, updated_orgs, processors
):
    # Create a mock Redis server
    redis_url = f"redis://{config.REDIS_HOST}" f":{config.REDIS_PORT}"
    redis = await aioredis.from_url(
        redis_url,
        password=config.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
    )

    # Create a mock CoreAPIClient that returns different data on
    # subsequent calls
    mock_client = MockCoreAPIClient(
        CoreAPIConfig(
            base_url=config.CORE_API_URL, api_key=config.CORE_API_KEY
        ),
        initial_orgs,
        processors,
    )

    # Create the store with our mock client
    store = OrgConfigStore(
        core_api_key=config.CORE_API_KEY,
        core_api_url=config.CORE_API_URL,
        redis_host=config.REDIS_HOST,
        redis_port=config.REDIS_PORT,
        redis_password=config.REDIS_PASSWORD,
        redis_config_topic=config.REDIS_CONFIG_TOPIC,
        logger=logging.getLogger("test"),
    )

    # Patch the CoreAPIClient to use our mock
    with patch(
        "qink.lib.org_config_store.CoreAPIClient", return_value=mock_client
    ):
        await asyncio.sleep(1)

        # Verify initial state
        assert len(store.orgs) == 2
        assert store.orgs[0].name == "Test Org 1"
        assert store.orgs[1].name == "Test Org 2"

        # Update the mock client to return different data
        mock_client._orgs = updated_orgs

        # Publish a message to Redis to trigger reload
        await redis.publish(config.REDIS_CONFIG_TOPIC, "config_updated")

        # Give some time for the message to be processed
        await asyncio.sleep(0.1)

        # Verify the store was updated with new data
        assert len(store.orgs) == 3
        assert store.orgs[0].name == "Updated Org 1"
        assert store.orgs[1].name == "Updated Org 2"
        assert store.orgs[2].name == "New Org 3"

    # Cleanup
    if store.sub_task:
        store.sub_task.cancel()
        try:
            await store.sub_task
        except asyncio.CancelledError:
            pass
    await store.close()
    await redis.aclose()
    await asyncio.sleep(0.1)  # Give time for connections to close properly


@pytest.mark.asyncio
async def test_org_store_recovers_after_redis_disconnect(
    config, initial_orgs, updated_orgs, processors
):
    """Test that OrgConfigStore recovers after Redis connection is restored."""
    from tests.test_utils import TCPProxy

    # Create a proxy pointing to Redis
    proxy = TCPProxy(
        target_host=config.REDIS_HOST, target_port=config.REDIS_PORT
    )
    proxy_port = await proxy.start()

    # Create a mock Redis server through the proxy
    redis = await aioredis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
        retry=Retry(ConstantBackoff(1), retries=-1),
        retry_on_error=[
            ConnectionError,
            TimeoutError,
            ConnectionResetError,
        ],
    )

    # Create a mock CoreAPIClient
    mock_client = MockCoreAPIClient(
        CoreAPIConfig(
            base_url=config.CORE_API_URL, api_key=config.CORE_API_KEY
        ),
        initial_orgs,
        processors,
    )

    # Create the store with our mock client
    store = OrgConfigStore(
        core_api_key=config.CORE_API_KEY,
        core_api_url=config.CORE_API_URL,
        redis_host=config.REDIS_HOST,
        redis_port=proxy_port,
        redis_password=config.REDIS_PASSWORD,
        redis_config_topic=config.REDIS_CONFIG_TOPIC,
        logger=logging.getLogger("test"),
    )

    try:
        # Patch the CoreAPIClient to use our mock
        with patch(
            "qink.lib.org_config_store.CoreAPIClient", return_value=mock_client
        ):
            await asyncio.sleep(2)

            # Verify initial state
            assert len(store.orgs) == 2
            assert store.orgs[0].name == "Test Org 1"
            assert store.orgs[1].name == "Test Org 2"

            await redis.publish(config.REDIS_CONFIG_TOPIC, "1")
            await asyncio.sleep(0.1)

            # Stop the proxy to simulate disconnection
            await proxy.stop()

            # Update the mock client to return different data
            mock_client._orgs = updated_orgs

            # Publish a message to Redis to trigger reload
            await redis.publish(config.REDIS_CONFIG_TOPIC, "1")

            # Give some time for the message to be processed
            await asyncio.sleep(0.1)

            # Verify the store wasn't updated while disconnected
            assert len(store.orgs) == 2
            assert store.orgs[0].name == "Test Org 1"
            assert store.orgs[1].name == "Test Org 2"

            # Restart the proxy with a new port
            proxy = TCPProxy(
                target_host=config.REDIS_HOST,
                target_port=config.REDIS_PORT,
                listen_port=proxy_port,
            )

            await proxy.start()

            # Wait a bit for the store to reconnect
            await asyncio.sleep(1)

            # Publish a message after reconnection
            await redis.publish(config.REDIS_CONFIG_TOPIC, "1")

            # Give more time for the message to be processed
            await asyncio.sleep(1)

            # Verify the store was updated after reconnection
            assert len(store.orgs) == 3
            assert store.orgs[0].name == "Updated Org 1"
            assert store.orgs[1].name == "Updated Org 2"
            assert store.orgs[2].name == "New Org 3"
    finally:
        await store.close()
        await redis.aclose()
        await proxy.stop()
