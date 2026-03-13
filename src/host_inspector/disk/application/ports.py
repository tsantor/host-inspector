from typing import Protocol

from .dtos import DiskSnapshotDTO


class DiskProbePort(Protocol):
    def snapshot(self, path: str = "/") -> DiskSnapshotDTO:
        """Return a disk usage snapshot."""
