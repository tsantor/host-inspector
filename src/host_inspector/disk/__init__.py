from functools import cache

from .infrastructure import build_disk_service


@cache
def _get_disk_service():
    return build_disk_service()


def get_disk_info(path: str = "/") -> dict:
    """Return disk usage info as dict."""
    return _get_disk_service().get_disk_info(path=path)
