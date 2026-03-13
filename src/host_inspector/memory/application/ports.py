from typing import Protocol

from .dtos import MemorySnapshotDTO


class MemoryProbePort(Protocol):
    def snapshot(self) -> MemorySnapshotDTO:
        """Return a memory snapshot."""
