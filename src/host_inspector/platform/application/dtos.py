from dataclasses import asdict
from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformInfoDTO:
    system: str
    release: str
    machine: str
    architecture: str
    manufacturer: str
    model: str
    serial: str

    def to_dict(self) -> dict:
        return asdict(self)
