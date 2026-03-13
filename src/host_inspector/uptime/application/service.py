from dataclasses import dataclass

from host_inspector.uptime.domain import date_as_day
from host_inspector.uptime.domain import date_as_day_short
from host_inspector.uptime.domain import date_as_string
from host_inspector.uptime.domain import time_as_string
from host_inspector.uptime.domain import uptime_as_string

from .ports import UptimeProbePort


@dataclass(frozen=True)
class UptimeService:
    probe: UptimeProbePort

    def uptime_in_seconds(self) -> int:
        """Return uptime in seconds."""
        return int(self.probe.now_timestamp() - self.probe.boot_timestamp())

    def get_uptime_info(self) -> dict:
        dt = self.probe.boot_time()
        seconds = self.uptime_in_seconds()
        return {
            "day": date_as_day(dt),
            "day_short": date_as_day_short(dt),
            "date": date_as_string(dt),
            "time": time_as_string(dt),
            "military_time": time_as_string(dt, military=True),
            "uptime": uptime_as_string(seconds),
            "seconds": seconds,
        }
