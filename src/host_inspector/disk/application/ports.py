from typing import Protocol
from typing import TypedDict


class DiskSnapshot(TypedDict):
    total: int
    used: int
    free: int
    percent: float


class DiskProbePort(Protocol):
    def snapshot(self, path: str = "/") -> DiskSnapshot:
        """Return a disk usage snapshot."""
