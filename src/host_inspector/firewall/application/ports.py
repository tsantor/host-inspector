from typing import Protocol


class FirewallCollectorPort(Protocol):
    def enabled_status(self) -> bool | dict:
        """Return platform-specific enabled status."""

    def rules(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> list[dict]:
        """Return platform-specific firewall rules."""
