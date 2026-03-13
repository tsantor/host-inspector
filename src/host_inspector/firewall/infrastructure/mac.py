from host_inspector.firewall.application.dtos import FirewallRulesDTO
from host_inspector.firewall.application.dtos import FirewallStatusDTO


class MacFirewallCollector:
    def enabled_status(self) -> FirewallStatusDTO:
        return FirewallStatusDTO(overall=False)

    def rules(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> FirewallRulesDTO:
        del ports, direction, enabled_only, exclude_any_ports
        return FirewallRulesDTO(items=[])
