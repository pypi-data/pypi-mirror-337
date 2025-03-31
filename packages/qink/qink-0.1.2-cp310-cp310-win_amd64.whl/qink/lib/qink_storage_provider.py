import abc


class QinkStorageProvider(abc.ABC):
    def __init__(self, prefix: str = ""):
        """Initialize the storage provider with an optional prefix
        for all file paths."""
        self.prefix = prefix
        if self.prefix and not self.prefix.endswith("/"):
            self.prefix += "/"

    @abc.abstractmethod
    async def get_file_contents_async(self, file_path: str) -> bytes:
        pass

    @abc.abstractmethod
    async def set_file_contents_async(self, file_path: str, content: bytes):
        pass
