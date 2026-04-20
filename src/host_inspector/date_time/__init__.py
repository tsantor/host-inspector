from functools import cache

from .infrastructure import build_datetime_service

__all__ = ["get_datetime_info"]


@cache
def _get_datetime_service():
    return build_datetime_service()


def get_datetime_info() -> dict:
    """Get date/time information as a dict."""
    return _get_datetime_service().get_datetime_info()
