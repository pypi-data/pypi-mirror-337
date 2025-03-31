from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Application configuration with environment variables."""

    CORE_API_URL: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_GROUP_ID: str
    KAFKA_TOPIC: str
    CORE_API_KEY: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_CONFIG_TOPIC: str = "org_config_updates"
    REDIS_SSL: bool = False
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    KAFKA_SASL_PASSWORD: Optional[str] = None
    KAFKA_SASL_USERNAME: Optional[str] = None
    KAFKA_SASL_MECHANISM: Optional[str] = None
    KAFKA_SECURITY_PROTOCOL: Optional[str] = None
    AZURE_STORAGE_CONTAINER_NAME: Optional[str] = None
    AZURE_STORAGE_PREFIX: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        """Create Config instance from environment variables."""
        return cls(
            CORE_API_URL=os.getenv("CORE_API_URL", "http://localhost:8080"),
            KAFKA_BOOTSTRAP_SERVERS=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            KAFKA_GROUP_ID=os.getenv("KAFKA_GROUP_ID", "test-local"),
            KAFKA_TOPIC=os.getenv("KAFKA_TOPIC", "prod-post-events-request"),
            CORE_API_KEY=os.getenv("CORE_API_KEY"),
            REDIS_HOST=os.getenv("REDIS_HOST", "localhost"),
            REDIS_PORT=int(os.getenv("REDIS_PORT", "6379")),
            REDIS_PASSWORD=os.getenv("REDIS_PASSWORD"),
            REDIS_CONFIG_TOPIC=os.getenv(
                "REDIS_CONFIG_TOPIC", "org_config_updates"
            ),
            REDIS_SSL=os.getenv("REDIS_SSL", "False").lower() == "true",
            KAFKA_SASL_PASSWORD=os.getenv("KAFKA_SASL_PASSWORD"),
            KAFKA_SASL_USERNAME=os.getenv("KAFKA_SASL_USERNAME"),
            KAFKA_SASL_MECHANISM=os.getenv("KAFKA_SASL_MECHANISM"),
            KAFKA_SECURITY_PROTOCOL=os.getenv("KAFKA_SECURITY_PROTOCOL"),
            AZURE_STORAGE_CONNECTION_STRING=os.getenv(
                "AZURE_STORAGE_CONNECTION_STRING"
            ),
            AZURE_STORAGE_CONTAINER_NAME=os.getenv(
                "AZURE_STORAGE_CONTAINER_NAME"
            ),
            AZURE_STORAGE_PREFIX=os.getenv("AZURE_STORAGE_PREFIX"),
        )
