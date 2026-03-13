from datetime import datetime

from host_inspector.utils.datetimeutils import human_date
from host_inspector.utils.datetimeutils import human_date_short
from host_inspector.utils.datetimeutils import human_delta
from host_inspector.utils.datetimeutils import human_time


def date_as_string(dt: datetime) -> str:
    """Return boot time date as string."""
    return dt.strftime("%Y-%m-%d")


def time_as_string(dt: datetime, *, military: bool = False) -> str:
    """Return boot time as string."""
    return dt.strftime("%H:%M") if military else human_time(dt)


def date_as_day(dt: datetime) -> str:
    """Return boot time as day string."""
    return human_date(dt)


def date_as_day_short(dt: datetime) -> str:
    """Return boot time as day string."""
    return human_date_short(dt)


def uptime_as_string(seconds: int) -> str:
    """Return uptime as string."""
    return human_delta(seconds)
