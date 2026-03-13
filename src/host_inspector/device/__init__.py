from functools import cache

from .infrastructure import build_device_service


@cache
def _get_device_service():
    return build_device_service()


def get_device_info() -> dict:
    """Return device information."""
    return _get_device_service().get_device_info()
