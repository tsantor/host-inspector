from functools import cache

from .infrastructure import build_health_service

__all__ = ["get_health_info"]


@cache
def _get_health_service():
    return build_health_service()


def get_health_info() -> dict:
    """Return overall health information."""
    return _get_health_service().get_health_info()
