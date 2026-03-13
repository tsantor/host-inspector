from dataclasses import dataclass

from .ports import HealthProbePort


@dataclass(frozen=True)
class HealthService:
    probe: HealthProbePort

    def get_health_info(self) -> dict:
        return {
            "cpu": self.probe.cpu_info(),
            "mem": self.probe.mem_info(),
            "disk": self.probe.disk_info(),
            "uptime": self.probe.uptime_info(),
            "local_datetime": self.probe.datetime_info(),
        }
