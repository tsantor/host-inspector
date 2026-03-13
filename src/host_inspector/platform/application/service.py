from dataclasses import dataclass

from .ports import PlatformCollectorPort


@dataclass(frozen=True)
class PlatformService:
    collector: PlatformCollectorPort

    def get_platform_info(self) -> dict:
        return self.collector.platform_info().to_dict()
