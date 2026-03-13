from dataclasses import dataclass

from .ports import DisplayCollectorPort


@dataclass(frozen=True)
class DisplayService:
    collector: DisplayCollectorPort

    def get_display_info(self) -> list[dict]:
        return [item.to_dict() for item in self.collector.display_info().items]
