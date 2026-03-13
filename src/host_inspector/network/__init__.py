from functools import cache

from .infrastructure import build_network_service


@cache
def _get_network_service():
    return build_network_service()


def get_network_info() -> dict:
    """Return network info as dict."""
    return _get_network_service().get_network_info()
