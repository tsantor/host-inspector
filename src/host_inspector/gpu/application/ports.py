from typing import Protocol

from .dtos import GPUPayloadDTO


class GPUCollectorPort(Protocol):
    def gpu_info(self) -> GPUPayloadDTO:
        """Return GPU info payload for the current platform."""
