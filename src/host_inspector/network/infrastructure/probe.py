import platform
import socket
import uuid
from functools import cache
from typing import Any

import psutil

AF_INET6 = [30, 10, 23]
AF_LINK = [18, 17, -1]


@cache
def _network_interface_by_ip(ip_address: str) -> tuple[str, list[Any]]:
    interfaces = psutil.net_if_addrs()
    for name, addresses in interfaces.items():
        for nic_address in addresses:
            if nic_address.address == ip_address:
                return name, addresses
    return "--", []


def _current_ip_address() -> str:
    """Safely get internal IPv4 address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:  # pragma: no cover
        return "--"


class SystemNetworkProbe:
    def hostname(self) -> str:
        return platform.node()

    def current_ip_address(self) -> str:
        return _current_ip_address()

    def node_value(self) -> int:
        return uuid.getnode()

    def interface_for_ip(self, ip_address: str) -> str:
        interface_name, _ = _network_interface_by_ip(ip_address)
        return interface_name

    def mac_for_ip(self, ip_address: str) -> str | None:
        _, addresses = _network_interface_by_ip(ip_address)
        return next(
            (addr.address for addr in addresses if addr.family in AF_LINK), None
        )

    def ipv6_for_ip(self, ip_address: str) -> str | None:
        _, addresses = _network_interface_by_ip(ip_address)
        return next(
            (addr.address for addr in addresses if addr.family in AF_INET6), None
        )
