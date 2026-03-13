from dataclasses import dataclass

from .ports import HealthProbePort


@dataclass(frozen=True)
class HealthService:
    probe: HealthProbePort

    def get_health_info(self) -> dict:
        snapshot = self.probe.snapshot()
        return {
            "cpu": snapshot.cpu,
            "mem": snapshot.mem,
            "disk": snapshot.disk,
            "uptime": snapshot.uptime,
            "local_datetime": snapshot.local_datetime,
        }
