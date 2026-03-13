from dataclasses import dataclass


@dataclass(frozen=True)
class DiskSnapshotDTO:
    total: int
    used: int
    free: int
    percent: float
