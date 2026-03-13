from typing import Protocol


class DeviceProbePort(Protocol):
    def os_info(self) -> dict:
        """Return OS info."""

    def platform_info(self) -> dict:
        """Return platform info."""

    def network_info(self) -> dict:
        """Return network info."""

    def gpu_info(self) -> dict | list:
        """Return GPU info."""

    def display_info(self) -> list[dict]:
        """Return display info."""
