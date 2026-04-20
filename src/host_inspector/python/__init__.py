from functools import cache

from .infrastructure import build_python_service

__all__ = ["get_python_info"]


@cache
def _get_python_service():
    return build_python_service()


def get_python_info() -> dict:
    """Get current Python info as dict."""
    return _get_python_service().get_python_info()
