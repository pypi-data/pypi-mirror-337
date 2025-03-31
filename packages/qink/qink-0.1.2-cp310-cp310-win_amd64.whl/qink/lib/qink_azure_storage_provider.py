import logging
from typing import Optional, List
from dataclasses import dataclass
from azure.storage.blob import BlobServiceClient
from azure.storage.blob.aio import BlobServiceClient as AsyncBlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from .qink_storage_provider import QinkStorageProvider


@dataclass
class AzureStorageConfig:
    """Configuration for Azure Storage client."""

    connection_string: str
    container_name: str
    prefix: str = ""


class QinkAzureStorageProvider(QinkStorageProvider):
    """Client for Azure Blob Storage operations."""

    @staticmethod
    def from_env(logger: logging.Logger) -> "QinkAzureStorageProvider":
        from qink.lib.config import Config

        config = Config.from_env()

        return QinkAzureStorageProvider(
            config=AzureStorageConfig(
                connection_string=config.AZURE_STORAGE_CONNECTION_STRING,
                container_name=config.AZURE_STORAGE_CONTAINER_NAME,
                prefix=config.AZURE_STORAGE_PREFIX,
            ),
            logger=logger,
        )

    def __init__(
        self,
        config: AzureStorageConfig,
        logger: Optional[logging.Logger] = None,
    ):
        """Initialize the Azure Storage client with configuration."""
        super().__init__(config.prefix)

        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self._blob_service_client = BlobServiceClient.from_connection_string(
            self.config.connection_string
        )
        self._container_client = (
            self._blob_service_client.get_container_client(
                self.config.container_name
            )
        )

    async def list_files_async(self, directory: str = "") -> List[str]:
        """
        List all files in a given directory asynchronously.

        Args:
            directory: Directory path within the container (optional).

        Returns:
            List of file paths.
        """
        async with AsyncBlobServiceClient.from_connection_string(
            self.config.connection_string
        ) as blob_service_client:
            container_client = blob_service_client.get_container_client(
                self.config.container_name
            )

            try:
                # Ensure directory path ends with a slash if not empty
                if directory and not directory.endswith("/"):
                    directory += "/"

                # Get blobs with the specified prefix
                files = []
                async for blob in container_client.list_blobs(
                    name_starts_with=directory
                ):
                    files.append(blob.name)

                return files
            except Exception as e:
                self.logger.error(
                    f"Error listing files in directory '{directory}': {e}"
                )
                raise

    async def get_file_contents_async(self, file_path: str) -> bytes:
        """
        Get the contents of a file as bytes asynchronously.

        Args:
            file_path: Path to the file within the container.

        Returns:
            File contents as bytes.

        Raises:
            ResourceNotFoundError: If the file doesn't exist.
        """
        async with AsyncBlobServiceClient.from_connection_string(
            self.config.connection_string
        ) as blob_service_client:
            container_client = blob_service_client.get_container_client(
                self.config.container_name
            )
            blob_client = container_client.get_blob_client(
                self.prefix + file_path
            )

            try:
                download_stream = await blob_client.download_blob()
                data = await download_stream.readall()

                return data
            except ResourceNotFoundError:
                self.logger.error(f"File not found: {self.prefix + file_path}")
                return None
            except Exception as e:
                self.logger.error(
                    f"Error reading file '{self.prefix + file_path}': {e}"
                )
                raise

    async def set_file_contents_async(
        self, file_path: str, content: bytes
    ) -> None:
        """
        Set the contents of a file asynchronously.

        Args:
            file_path: Path to the file within the container.
            content: Content to write to the file (string or bytes).

        Raises:
            Exception: If there's an error writing to the file.
        """
        async with AsyncBlobServiceClient.from_connection_string(
            self.config.connection_string
        ) as blob_service_client:
            container_client = blob_service_client.get_container_client(
                self.config.container_name
            )
            blob_client = container_client.get_blob_client(
                self.prefix + file_path
            )

            try:
                # Convert string to bytes if necessary
                if isinstance(content, str):
                    content = content.encode("utf-8")

                await blob_client.upload_blob(content, overwrite=True)
            except Exception as e:
                self.logger.error(
                    f"Error writing to file '{self.prefix + file_path}': {e}"
                )
                raise
