from functools import cache

from .infrastructure import build_uptime_service

all__all__ = ["get_uptime_info"]


@cache
def _get_uptime_service():
    return build_uptime_service()


def get_uptime_info() -> dict:
    """Return uptime info as a dict."""
    return _get_uptime_service().get_uptime_info()
