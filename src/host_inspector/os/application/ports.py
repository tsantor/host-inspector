from typing import Protocol

from .dtos import OSDataDTO


class OSCollector(Protocol):
    def collect(self) -> OSDataDTO:
        """Collect platform OS information."""
