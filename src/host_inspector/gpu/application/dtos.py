from dataclasses import asdict
from dataclasses import dataclass


@dataclass(frozen=True)
class GPUInfoDTO:
    model: str
    vram: str
    resolution: str
    refresh_rate: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class GPUPayloadDTO:
    adapters: list[GPUInfoDTO]
    as_list: bool
