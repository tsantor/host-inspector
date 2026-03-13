from typing import Protocol


class GPUCollectorPort(Protocol):
    def gpu_info(self) -> dict | list[dict]:
        """Return GPU info payload for the current platform."""
