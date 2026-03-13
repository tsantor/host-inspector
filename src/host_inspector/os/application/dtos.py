from dataclasses import dataclass


@dataclass(frozen=True)
class OSDataDTO:
    platform: str
    name: str
    version: str | int | None
    edition: str | None
    build: str | int | None
    display_version: str | None = None
