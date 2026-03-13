from dataclasses import dataclass

from .ports import DisplayCollectorPort


@dataclass(frozen=True)
class DisplayService:
    collector: DisplayCollectorPort

    def get_display_info(self) -> list[dict]:
        return self.collector.display_info()
