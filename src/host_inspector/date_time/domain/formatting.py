from datetime import datetime

from host_inspector.utils.datetimeutils import human_date
from host_inspector.utils.datetimeutils import human_date_short
from host_inspector.utils.datetimeutils import human_time


def local_timezone(now: datetime) -> str:
    """Get local timezone string."""
    return str(now.tzinfo)


def date_as_string(now: datetime) -> str:
    """Return date as YYYY-MM-DD string."""
    return now.strftime("%Y-%m-%d")


def date_as_day(now: datetime) -> str:
    """Return full day string."""
    return human_date(now)


def date_as_day_short(now: datetime) -> str:
    """Return short day string."""
    return human_date_short(now)


def time_as_string(now: datetime, *, military: bool = False) -> str:
    """Return time as string."""
    return now.strftime("%H:%M") if military else human_time(now)
