from typing import Protocol

from .dtos import PlatformInfoDTO


class PlatformCollectorPort(Protocol):
    def platform_info(self) -> PlatformInfoDTO:
        """Return platform information for the current OS."""
