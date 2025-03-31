import pytest
import redis.asyncio as redis
from tests.test_utils import TCPProxy
from qink.lib.config import Config


@pytest.mark.asyncio
async def test_redis_proxy():
    """Test that we can connect to Redis through the TCPProxy."""
    config = Config.from_env()

    # Create a proxy pointing to Redis
    proxy = TCPProxy(
        target_host=config.REDIS_HOST, target_port=config.REDIS_PORT
    )

    proxy_port = await proxy.start()

    try:
        # Connect to Redis through the proxy
        redis_client = redis.Redis(
            host="localhost",
            port=proxy_port,
            socket_timeout=5,
            decode_responses=True,
        )

        # Test basic Redis operations through the proxy
        await redis_client.set("test_key", "test_value")
        value = await redis_client.get("test_key")
        assert value == "test_value"

        # Test multiple operations
        await redis_client.hset("test_hash", mapping={"field1": "value1"})
        hash_value = await redis_client.hget("test_hash", "field1")
        assert hash_value == "value1"

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
    finally:
        await proxy.stop()


@pytest.mark.asyncio
async def test_redis_proxy_closed():
    """Test that Redis operations fail after the proxy is closed."""
    config = Config.from_env()

    # Create a proxy pointing to Redis
    proxy = TCPProxy(
        target_host=config.REDIS_HOST, target_port=config.REDIS_PORT
    )

    proxy_port = await proxy.start()

    # Connect to Redis through the proxy
    redis_client = redis.Redis(
        host="localhost",
        port=proxy_port,
        socket_timeout=5,
        decode_responses=True,
    )

    # Verify we can connect initially
    await redis_client.set("test_key", "test_value")
    value = await redis_client.get("test_key")
    assert value == "test_value"

    # Stop the proxy
    await proxy.stop()

    # Verify operations fail after proxy is closed
    with pytest.raises(Exception):
        await redis_client.get("test_key")
