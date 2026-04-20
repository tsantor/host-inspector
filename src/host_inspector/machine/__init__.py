from functools import cache

from .infrastructure import build_machine_service

__all__ = ["get_machine_id"]


@cache
def _get_machine_service():
    return build_machine_service()


def get_machine_id() -> str:
    """Return consistent UUID format."""
    return _get_machine_service().get_machine_id()
