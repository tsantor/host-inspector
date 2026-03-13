from dataclasses import dataclass

from host_inspector.date_time.domain import date_as_day
from host_inspector.date_time.domain import date_as_day_short
from host_inspector.date_time.domain import date_as_string
from host_inspector.date_time.domain import local_timezone
from host_inspector.date_time.domain import time_as_string

from .ports import DateTimeProbePort


@dataclass(frozen=True)
class DateTimeService:
    probe: DateTimeProbePort

    def get_datetime_info(self) -> dict:
        now = self.probe.now()
        return {
            "timestamp": now.isoformat(),
            "day": date_as_day(now),
            "day_short": date_as_day_short(now),
            "date": date_as_string(now),
            "time": time_as_string(now),
            "military_time": time_as_string(now, military=True),
            "timezone": local_timezone(now),
            "is_dst": self.probe.is_dst(),
        }
