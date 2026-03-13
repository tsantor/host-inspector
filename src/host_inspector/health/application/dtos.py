from dataclasses import dataclass


@dataclass(frozen=True)
class HealthInputDTO:
    cpu: dict
    mem: dict
    disk: dict
    uptime: dict
    local_datetime: dict
