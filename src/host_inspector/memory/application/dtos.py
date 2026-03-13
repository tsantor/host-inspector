from dataclasses import dataclass


@dataclass(frozen=True)
class MemorySnapshotDTO:
    total: int
    used: int
    available: int
    percent: float
