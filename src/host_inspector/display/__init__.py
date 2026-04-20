from functools import cache

from .infrastructure import build_display_service

__all__ = ["get_display_info"]


@cache
def _get_display_service():
    return build_display_service()


def get_display_info() -> list[dict]:
    return _get_display_service().get_display_info()
