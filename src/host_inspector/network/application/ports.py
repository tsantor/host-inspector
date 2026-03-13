from typing import Protocol


class NetworkProbePort(Protocol):
    def hostname(self) -> str:
        """Return host name."""

    def current_ip_address(self) -> str:
        """Return current IPv4 address."""

    def node_value(self) -> int:
        """Return node identifier suitable for MAC formatting."""

    def interface_for_ip(self, ip_address: str) -> str:
        """Return interface name for a given IP address."""

    def mac_for_ip(self, ip_address: str) -> str | None:
        """Return raw MAC address for a given IP address."""

    def ipv6_for_ip(self, ip_address: str) -> str | None:
        """Return raw IPv6 address for a given IP address."""
