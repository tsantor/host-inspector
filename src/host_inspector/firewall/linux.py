import logging
import subprocess

logger = logging.getLogger(__name__)


def check_firewall_status():
    """
    Checks the status of common firewall services and returns if any are active.
    """
    # Prefer ufw and firewalld as they're the high-level managers.
    firewall_managers = ["ufw", "firewalld"]

    for manager in firewall_managers:
        try:
            # Use `systemctl is-active` for a definitive, machine-readable status
            command = ["sudo", "systemctl", "is-active", manager]
            result = subprocess.run(command, capture_output=True, text=True, check=True)  # noqa: S603
            # The command returns 0 for active, non-zero for inactive
            if result.returncode == 0:
                return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If the command is not found or returns an error, that firewall manager isn't active
            continue
    return False


def is_firewall_enabled() -> bool:
    """
    Checks the status of the firewall using common Linux commands.
    """
    # commands = {
    #     "ufw": ["ufw", "status"],
    #     "firewalld": ["firewall-cmd", "--state"],
    #     "iptables": ["iptables", "-L", "-n"],
    # }

    # # Check for each firewall manager in a preferred order
    # for args in commands.values():
    #     try:
    #         process = subprocess.run(args, capture_output=True, text=True, check=True)
    #         output = process.stdout.strip().lower()

    #         if "active" in output or "running" in output:
    #             return True
    #         if "inactive" in output:
    #             return False
    #         return False

    #     except subprocess.CalledProcessError:
    #         pass
    #     except FileNotFoundError:
    #         pass

    # return False
    return check_firewall_status()


def get_firewall_rules(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
):
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
        return parse_firewall_output(
            result.stdout, ports, enabled_only, exclude_any_ports
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        logger.exception("Error executing command")
        return []


def parse_firewall_output(
    output, ports_filter=None, enabled_only=False, exclude_any_ports=False
):
    lines = output.strip().split("\n")
    rules = []

    # Find the line that marks the beginning of the rules table
    start_index = -1
    for i, line in enumerate(lines):
        if "To" in line and "Action" in line and "From" in line:
            start_index = i + 2  # Skip the header line and separator line
            break

    if start_index == -1:
        return rules  # No rules found or output format is different

    rule_lines = lines[start_index:]

    for line in rule_lines:
        line = line.strip()  # noqa: PLW2901
        if not line or line.startswith("--"):  # Skip empty lines and separator lines
            continue

        # Split the line into parts, but be careful with whitespace
        parts = line.split()
        if len(parts) < 3:  # noqa: PLR2004
            continue

        # The format is: To | Action | From
        # Example: "22/tcp                     ALLOW IN    Anywhere"
        #          "1883,9001/tcp              ALLOW IN    Anywhere"
        to_part = parts[
            0
        ]  # This contains port/protocol like "22/tcp" or "1883,9001/tcp"
        action_part = parts[1]  # This is "ALLOW" or "DENY"
        direction_part = parts[2] if len(parts) > 2 else "IN"  # noqa: PLR2004

        # Parse the "To" field which contains port/protocol
        protocol = "ANY"
        port = None

        if "/" in to_part:
            port_proto = to_part.split("/")
            port_part = port_proto[0]  # Could be "22" or "1883,9001"
            protocol = port_proto[1].upper()
            port = port_part  # Keep comma-separated ports as-is
        else:
            # Handle cases where there's no protocol specified
            port = to_part if to_part else None

        # Standardize action and direction
        action = "ALLOW" if "ALLOW" in action_part.upper() else "DENY"
        direction = (
            "INBOUND" if "IN" in direction_part or "OUT" not in line else "OUTBOUND"
        )

        # Create single rule
        rule = {
            "name": None,
            "direction": direction,
            "action": action,
            "protocol": protocol,
            "enabled": True,
            "local_port": port,
            "remote_port": "ANY",
        }
        rules.append(rule)

    return rules


def get_firewall_info(
    interested_ports=None,
    direction=None,
    enabled_only=False,
    exclude_any_ports=False,
) -> dict:
    """Return a dict of firewall info."""
    enabled = is_firewall_enabled()
    return {
        "enabled": enabled,
        "status": "ON" if enabled else "OFF",
        "rules": get_firewall_rules(
            ports=interested_ports,
            direction=direction,
            enabled_only=enabled_only,
            exclude_any_ports=exclude_any_ports,
        ),
    }


# sudo ufw allow 22/tcp
# sudo ufw allow 1883,9001/tcp
