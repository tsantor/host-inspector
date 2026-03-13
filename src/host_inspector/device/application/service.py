from dataclasses import dataclass

from .ports import DeviceProbePort


@dataclass(frozen=True)
class DeviceService:
    probe: DeviceProbePort

    def get_device_info(self) -> dict:
        snapshot = self.probe.snapshot()
        return {
            "os": snapshot.os,
            "platform": snapshot.platform,
            "network": snapshot.network,
            "gpu": snapshot.gpu,
            "display": snapshot.display,
        }
