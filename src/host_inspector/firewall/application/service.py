from dataclasses import dataclass

from .ports import FirewallCollectorPort


@dataclass(frozen=True)
class FirewallService:
    collector: FirewallCollectorPort

    @staticmethod
    def _normalize_enabled(status: bool | dict) -> bool:
        if isinstance(status, bool):
            return status
        if isinstance(status, dict):
            if "overall" in status:
                return bool(status["overall"])
            return any(bool(value) for value in status.values())
        return False

    def is_firewall_enabled(self) -> bool:
        return self._normalize_enabled(self.collector.enabled_status())

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
            "rules": self.collector.rules(
                ports=ports,
                direction=direction,
                enabled_only=enabled_only,
                exclude_any_ports=exclude_any_ports,
            ),
        }
