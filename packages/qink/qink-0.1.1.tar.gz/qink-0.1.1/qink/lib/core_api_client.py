import aiohttp
from typing import Any, Optional, List
from dataclasses import dataclass
from urllib.parse import urljoin


@dataclass
class CoreAPIConfig:
    """Configuration for Core API client."""

    base_url: str
    api_key: Optional[str] = None
    timeout: int = 30


@dataclass
class Processor:
    _id: str
    orgId: str
    title: str
    processor: str
    options: Any
    isEnabled: bool
    dependsOn: Optional[str]


@dataclass
class Org:
    _id: str
    name: str


class CoreAPIClient:
    """Async client for making HTTP calls to the Core API."""

    def __init__(self, config: CoreAPIConfig):
        """Initialize the client with configuration."""
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Create aiohttp session when entering context manager."""
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            headers=self._get_headers(),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session when exiting context manager."""
        if self._session:
            await self._session.close()

    def _get_headers(self) -> dict:
        """Get headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    async def get_orgs(self) -> List[Org]:
        """Get all organizations from the Core API."""
        url = urljoin(self.config.base_url, "/admin/system/orgs")
        async with self._session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            # Only use the fields we care about
            return [Org(_id=org["_id"], name=org["name"]) for org in data]

    async def get_processors(self) -> List[Processor]:
        """Get all processors from the Core API."""
        url = urljoin(self.config.base_url, "/admin/system/processors")
        async with self._session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            # Only use the fields we care about
            return [
                Processor(
                    _id=processor["_id"],
                    orgId=processor["orgId"],
                    title=processor["title"],
                    processor=processor["processor"],
                    options=processor["options"],
                    isEnabled=processor["isEnabled"],
                    dependsOn=processor.get("dependsOn"),
                )
                for processor in data
            ]
