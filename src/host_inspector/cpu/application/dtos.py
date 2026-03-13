from dataclasses import dataclass


@dataclass(frozen=True)
class TemperatureInfoDTO:
    data: dict
