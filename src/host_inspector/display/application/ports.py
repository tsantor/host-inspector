from typing import Protocol


class DisplayCollectorPort(Protocol):
    def display_info(self) -> list[dict]:
        """Return display info for the current platform."""
