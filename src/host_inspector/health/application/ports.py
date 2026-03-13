from typing import Protocol


class HealthProbePort(Protocol):
    def cpu_info(self) -> dict:
        """Return CPU info."""

    def mem_info(self) -> dict:
        """Return memory info."""

    def disk_info(self) -> dict:
        """Return disk info."""

    def uptime_info(self) -> dict:
        """Return uptime info."""

    def datetime_info(self) -> dict:
        """Return local datetime info."""
