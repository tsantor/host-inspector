from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceInputDTO:
    os: dict
    platform: dict
    network: dict
    gpu: dict | list
    display: list[dict]
