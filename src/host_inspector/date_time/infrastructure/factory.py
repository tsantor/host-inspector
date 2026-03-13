from host_inspector.date_time.application.service import DateTimeService

from .probe import SystemDateTimeProbe


def build_datetime_service() -> DateTimeService:
    return DateTimeService(probe=SystemDateTimeProbe())
