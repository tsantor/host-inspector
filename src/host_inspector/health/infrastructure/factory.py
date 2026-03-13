from host_inspector.health.application.service import HealthService

from .probe import HealthProbe


def build_health_service() -> HealthService:
    return HealthService(probe=HealthProbe())
