from datetime import datetime
from typing import Protocol


class UptimeProbePort(Protocol):
    def boot_time(self) -> datetime:
        """Return boot timestamp as timezone-aware datetime."""

    def now_timestamp(self) -> float:
        """Return the current timestamp in seconds."""

    def boot_timestamp(self) -> float:
        """Return boot timestamp in seconds."""
