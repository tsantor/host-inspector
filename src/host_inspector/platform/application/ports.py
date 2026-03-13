from typing import Protocol


class PlatformCollectorPort(Protocol):
    def platform_info(self) -> dict:
        """Return platform information for the current OS."""
