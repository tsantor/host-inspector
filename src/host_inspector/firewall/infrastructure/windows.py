import logging
import re
import subprocess

from host_inspector.firewall.application.dtos import FirewallRuleDTO
from host_inspector.firewall.application.dtos import FirewallRulesDTO
from host_inspector.firewall.application.dtos import FirewallStatusDTO
from host_inspector.firewall.domain import parse_windows_firewall_output

logger = logging.getLogger(__name__)


class WindowsFirewallCollector:
    def enabled_status(self) -> FirewallStatusDTO:
        command = ["netsh", "advfirewall", "show", "allprofiles"]
        try:
            result = subprocess.run(  # noqa: S603
                command,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            output = result.stdout
        except subprocess.CalledProcessError:
            return FirewallStatusDTO(overall=False)

        profiles = {"domain": False, "private": False, "public": False}
        for profile in profiles:
            match = re.search(
                rf"{profile}\s*profile settings:.*?state\s*on",
                output,
                re.IGNORECASE | re.DOTALL,
            )
            profiles[profile] = bool(match)
        profiles["overall"] = any(profiles.values())
        return FirewallStatusDTO(overall=any(profiles.values()))

    def rules(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> FirewallRulesDTO:
        command = ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"]
        if direction:
            command.extend([f"dir={direction}"])

        try:
            result = subprocess.run(  # noqa: S603
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=30,
            )
            return FirewallRulesDTO(
                items=[
                    FirewallRuleDTO(data=rule)
                    for rule in parse_windows_firewall_output(
                        result.stdout,
                        ports_filter=ports,
                        enabled_only=enabled_only,
                        exclude_any_ports=exclude_any_ports,
                    )
                ]
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            logger.exception("Error executing command")
            return FirewallRulesDTO(items=[])
