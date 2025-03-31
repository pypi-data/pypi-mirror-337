import asyncio
from typing import List, Optional
from logging import Logger
from redis import asyncio as aioredis
from redis.backoff import ConstantBackoff
from redis.exceptions import TimeoutError, ConnectionError
from redis.retry import Retry
from .core_api_client import (
    CoreAPIClient,
    CoreAPIConfig,
    Org,
    Processor,
)


class OrgConfigStore:
    def __init__(
        self,
        redis_host: str,
        redis_port: int,
        redis_password: str,
        redis_config_topic: str,
        core_api_url: str,
        core_api_key: str,
        logger: Logger,
        redis_ssl: bool = False,
    ):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.redis_config_topic = redis_config_topic
        self.core_api_url = core_api_url
        self.core_api_key = core_api_key
        self.orgs: List[Org] = []
        self.processors: List[Processor] = []
        self.redis: Optional[aioredis.Redis] = None
        self.sub_task: Optional[asyncio.Task] = None
        self.redis_ssl = redis_ssl
        self.logger = logger
        self.sub_task = asyncio.create_task(self._create_redis_subscription())

    async def _create_redis_subscription(self):
        """Handle incoming Redis messages with automatic reconnection."""
        while True:
            try:
                redis = await aioredis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    ssl=self.redis_ssl,
                    retry=Retry(ConstantBackoff(1), retries=0),
                    retry_on_error=[
                        ConnectionError,
                        TimeoutError,
                        ConnectionResetError,
                    ],
                    password=self.redis_password,
                    encoding="utf-8",
                    decode_responses=True,
                )

                pubsub = redis.pubsub()

                await pubsub.subscribe(self.redis_config_topic)

                await self._load_config()

                self.logger.info(
                    f"Subscribed to Redis topic: {self.redis_config_topic}"
                )

                async for message in pubsub.listen():
                    if message["type"] == "message":
                        await self._load_config()
            except Exception as e:
                self.logger.error(
                    f"Error subscribing to Redis or disconnected: {e}"
                )
                await redis.aclose()
                await asyncio.sleep(1)

    async def _load_config(self):
        """Load organizations and processors from the Core API."""
        api_config = CoreAPIConfig(
            base_url=self.core_api_url, api_key=self.core_api_key, timeout=5
        )

        async with CoreAPIClient(api_config) as client:
            self.orgs = await client.get_orgs()
            self.processors = await client.get_processors()

            self.logger.info(
                f"Loaded {len(self.orgs)} organizations and "
                f"{len(self.processors)} processors",
            )

    async def close(self):
        """Clean up resources."""
        if self.redis:
            await self.redis.aclose()

        if self.sub_task:
            self.sub_task.cancel()
            try:
                await self.sub_task
            except asyncio.CancelledError:
                pass

    def get_org(self, org_id: str) -> Optional[Org]:
        """Get an organization by ID."""
        return next((org for org in self.orgs if org._id == org_id), None)

    def get_processor(self, processor_id: str) -> Optional[Processor]:
        """Get a processor by ID."""
        return next(
            (proc for proc in self.processors if proc._id == processor_id),
            None,
        )
