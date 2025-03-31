from dataclasses import dataclass


@dataclass
class KeyState:
    key: str
    state: dict


@dataclass
class PartitionState:
    partition: int
    offset: int
    """Last successfully processed offset."""
    state: dict[str, KeyState]
