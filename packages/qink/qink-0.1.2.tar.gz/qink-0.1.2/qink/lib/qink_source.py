import logging
from typing import Optional
from .qink_assignment_listener import QinkAssignmentListener
from .models import PartitionState
import abc
from dataclasses import dataclass


@dataclass
class Message:
    key: bytes
    value: bytes
    timestamp: int
    offset: int


class QinkSource(abc.ABC):
    def __init__(
        self,
        logger: logging.Logger,
    ):
        self.logger = logger
        self._listener: Optional[QinkAssignmentListener] = None

    @abc.abstractmethod
    async def stop(self):
        pass

    def set_listener(self, listener: QinkAssignmentListener):
        self._listener = listener

    @abc.abstractmethod
    async def seek(self, state: PartitionState):
        pass

    @abc.abstractmethod
    async def start(self):
        pass

    @abc.abstractmethod
    async def get_many(self, partition: int) -> list[Message]:
        pass
