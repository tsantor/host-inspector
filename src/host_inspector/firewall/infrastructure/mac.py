class MacFirewallCollector:
    def enabled_status(self) -> bool:
        return False

    def rules(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> list[dict]:
        del ports, direction, enabled_only, exclude_any_ports
        return []
