from dataclasses import dataclass

from .ports import FirewallCollectorPort


@dataclass(frozen=True)
class FirewallService:
    collector: FirewallCollectorPort

    def is_firewall_enabled(self) -> bool:
        return self.collector.enabled_status().overall

    def get_firewall_info(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> dict:
        enabled = self.is_firewall_enabled()
        return {
            "enabled": enabled,
            "status": "ON" if enabled else "OFF",
            "rules": [
                rule.data
                for rule in self.collector.rules(
                    ports=ports,
                    direction=direction,
                    enabled_only=enabled_only,
                    exclude_any_ports=exclude_any_ports,
                ).items
            ],
        }
