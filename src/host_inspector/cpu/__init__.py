from functools import cache

from .infrastructure import build_cpu_service

__all__ = ["get_cpu_info"]


@cache
def _get_cpu_service():
    return build_cpu_service()


def get_cpu_info() -> dict:
    """Return CPU info as a dict."""
    return _get_cpu_service().get_cpu_info()
