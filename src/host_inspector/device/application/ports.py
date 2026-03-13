from typing import Protocol

from .dtos import DeviceInputDTO


class DeviceProbePort(Protocol):
    def snapshot(self) -> DeviceInputDTO:
        """Return device aggregate input."""
