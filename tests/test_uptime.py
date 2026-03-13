from datetime import datetime

from host_inspector import get_uptime_info
from host_inspector.uptime.application.service import UptimeService
from host_inspector.uptime.domain import date_as_string
from host_inspector.uptime.domain import time_as_string
from host_inspector.uptime.domain import uptime_as_string


class StubProbe:
    def __init__(self):
        self._boot = datetime.fromisoformat("2026-03-13T08:15:00+00:00")

    def boot_time(self) -> datetime:
        return self._boot

    def now_timestamp(self) -> float:
        return 2000.0

    def boot_timestamp(self) -> float:
        return 1000.0


def test_get_uptime_info_shape():
    info = get_uptime_info()
    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "day",
        "day_short",
        "date",
        "time",
        "military_time",
        "uptime",
        "seconds",
    }


def test_uptime_domain_formatting():
    dt = datetime.fromisoformat("2026-03-13T08:15:00+00:00")
    assert date_as_string(dt) == "2026-03-13"
    assert time_as_string(dt, military=True) == "08:15"
    assert isinstance(uptime_as_string(3600), str)


def test_uptime_service_builds_output():
    expected_seconds = 1000
    service = UptimeService(probe=StubProbe())
    info = service.get_uptime_info()
    assert info["date"] == "2026-03-13"
    assert info["military_time"] == "08:15"
    assert info["seconds"] == expected_seconds
