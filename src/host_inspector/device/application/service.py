from dataclasses import dataclass

from .ports import DeviceProbePort


@dataclass(frozen=True)
class DeviceService:
    probe: DeviceProbePort

    def get_device_info(self) -> dict:
        return {
            "os": self.probe.os_info(),
            "platform": self.probe.platform_info(),
            "network": self.probe.network_info(),
            "gpu": self.probe.gpu_info(),
            "display": self.probe.display_info(),
        }
