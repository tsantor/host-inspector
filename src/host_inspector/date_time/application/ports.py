from datetime import datetime
from typing import Protocol


class DateTimeProbePort(Protocol):
    def now(self) -> datetime:
        """Return current local timezone-aware datetime."""

    def is_dst(self) -> bool:
        """Return whether DST is currently active."""
