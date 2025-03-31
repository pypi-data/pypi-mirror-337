import pickle
import logging
from typing import Optional
from .qink_storage_provider import QinkStorageProvider
from .models import PartitionState


class QinkStorage:

    def __init__(
        self,
        storage_provider: QinkStorageProvider,
        logger: logging.Logger,
    ):
        self.logger = logger
        self.storage_provider = storage_provider

    async def get_partition_state(
        self, partition: int
    ) -> Optional[PartitionState]:
        bytes = await self.storage_provider.get_file_contents_async(
            self.get_partition_state_file_name(partition)
        )

        if bytes is None:
            return None

        return PartitionState(**pickle.loads(bytes))

    async def set_partition_state(self, partition: int, state: PartitionState):
        await self.storage_provider.set_file_contents_async(
            self.get_partition_state_file_name(partition),
            pickle.dumps(state.__dict__),
        )

    def get_partition_state_file_name(self, partition: int) -> str:
        return f"p-{partition}.state.pkl"
