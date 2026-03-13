from typing import Protocol

from .dtos import FirewallRulesDTO
from .dtos import FirewallStatusDTO


class FirewallCollectorPort(Protocol):
    def enabled_status(self) -> FirewallStatusDTO:
        """Return platform-specific enabled status."""

    def rules(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> FirewallRulesDTO:
        """Return platform-specific firewall rules."""
