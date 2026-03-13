from typing import Protocol

from .dtos import NetworkSnapshotDTO


class NetworkProbePort(Protocol):
    def snapshot(self) -> NetworkSnapshotDTO:
        """Return network snapshot data."""
