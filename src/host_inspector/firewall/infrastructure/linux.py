import logging
import subprocess

from host_inspector.firewall.domain import parse_linux_firewall_output

logger = logging.getLogger(__name__)


class LinuxFirewallCollector:
    def enabled_status(self) -> bool:
        commands = {
            "ufw": "sudo ufw status",
        }
        for command in commands.values():
            try:
                process = subprocess.run(  # noqa: S602
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                output = process.stdout.strip().lower()
                if "inactive" in output:
                    return False
                return bool("active" in output or "running" in output)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        return False

    def rules(
        self,
        ports=None,
        direction=None,
        enabled_only: bool = False,
        exclude_any_ports: bool = False,
    ) -> list[dict]:
        del direction
        command = ["sudo", "ufw", "status", "verbose"]
        try:
            result = subprocess.run(  # noqa: S603
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=30,
            )
            return parse_linux_firewall_output(
                result.stdout,
                ports_filter=ports,
                enabled_only=enabled_only,
                exclude_any_ports=exclude_any_ports,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            logger.warning("Error executing command %s", command)
            return []
