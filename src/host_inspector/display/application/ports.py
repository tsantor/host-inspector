from typing import Protocol

from .dtos import DisplayCollectionDTO


class DisplayCollectorPort(Protocol):
    def display_info(self) -> DisplayCollectionDTO:
        """Return display info for the current platform."""
