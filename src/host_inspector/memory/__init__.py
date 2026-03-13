from functools import cache

from .infrastructure import build_memory_service


@cache
def _get_memory_service():
    return build_memory_service()


def get_mem_info() -> dict:
    """Return memory info as a dict."""
    return _get_memory_service().get_mem_info()
