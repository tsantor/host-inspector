from functools import cache

from .infrastructure import build_firewall_service

__all__ = ["get_firewall_info"]


@cache
def _get_firewall_service():
    return build_firewall_service()


def get_firewall_info(
    ports=None,
    direction=None,
    enabled_only: bool = False,
    exclude_any_ports: bool = False,
) -> dict:
    return _get_firewall_service().get_firewall_info(
        ports=ports,
        direction=direction,
        enabled_only=enabled_only,
        exclude_any_ports=exclude_any_ports,
    )


def is_firewall_enabled() -> bool:
    return _get_firewall_service().is_firewall_enabled()
