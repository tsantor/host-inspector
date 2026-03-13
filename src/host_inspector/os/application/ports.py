from typing import NotRequired
from typing import Protocol
from typing import TypedDict


class OSData(TypedDict):
    platform: str
    name: str
    version: str | int | None
    edition: str | None
    build: str | int | None
    display_version: NotRequired[str]


class OSCollector(Protocol):
    def collect(self) -> OSData:
        """Collect platform OS information."""
