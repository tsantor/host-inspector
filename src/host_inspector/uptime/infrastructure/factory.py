from host_inspector.uptime.application.service import UptimeService

from .probe import PsutilUptimeProbe


def build_uptime_service() -> UptimeService:
    return UptimeService(probe=PsutilUptimeProbe())
