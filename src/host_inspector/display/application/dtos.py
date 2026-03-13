from dataclasses import asdict
from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayInfoDTO:
    name: str
    display_id: int | None
    resolution_actual: str
    resolution: str
    refresh_rate: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class DisplayCollectionDTO:
    items: list[DisplayInfoDTO]
