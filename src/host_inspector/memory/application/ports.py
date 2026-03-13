from typing import Protocol
from typing import TypedDict


class MemorySnapshot(TypedDict):
    total: int
    used: int
    available: int
    percent: float


class MemoryProbePort(Protocol):
    def snapshot(self) -> MemorySnapshot:
        """Return a memory snapshot."""
