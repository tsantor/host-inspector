from typing import Protocol

from .dtos import HealthInputDTO


class HealthProbePort(Protocol):
    def snapshot(self) -> HealthInputDTO:
        """Return health aggregate input."""
