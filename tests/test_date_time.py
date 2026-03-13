from datetime import UTC
from datetime import datetime

from host_inspector import get_datetime_info
from host_inspector.date_time.application.service import DateTimeService
from host_inspector.date_time.domain import date_as_string
from host_inspector.date_time.domain import time_as_string


class StubProbe:
    def now(self) -> datetime:
        return datetime(2026, 3, 13, 8, 15, tzinfo=UTC)

    def is_dst(self) -> bool:
        return False


def test_get_datetime_info_shape():
    info = get_datetime_info()
    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "timestamp",
        "day",
        "day_short",
        "date",
        "time",
        "military_time",
        "timezone",
        "is_dst",
    }


def test_datetime_domain_formatting():
    now = datetime(2026, 3, 13, 8, 15, tzinfo=UTC)
    assert date_as_string(now) == "2026-03-13"
    assert time_as_string(now, military=True) == "08:15"


def test_datetime_service_output():
    service = DateTimeService(probe=StubProbe())
    info = service.get_datetime_info()
    assert info["date"] == "2026-03-13"
    assert info["military_time"] == "08:15"
    assert info["is_dst"] is False
