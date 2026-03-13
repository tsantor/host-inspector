from functools import cache

from .infrastructure import build_platform_service


@cache
def _get_platform_service():
    return build_platform_service()


def get_platform_info() -> dict:
    return _get_platform_service().get_platform_info()
