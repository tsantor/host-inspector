from functools import cache

from .infrastructure import build_os_service


@cache
def get_os_info() -> dict:
    """Return OS info as dict."""
    return build_os_service().get_os_info()
