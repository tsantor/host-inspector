import contextlib
import logging
import re
import subprocess

# from functools import cache

logger = logging.getLogger(__name__)


def get_firewall_rules(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
):
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
        return parse_firewall_output(
            result.stdout, ports, enabled_only, exclude_any_ports
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        logger.exception("Error executing command")
        return []


def parse_firewall_output(
    output, ports_filter=None, enabled_only=False, exclude_any_ports=False
):
    rules = []
    ports_set = {str(p) for p in ports_filter} if ports_filter else None

    rule_blocks = re.split(r"\n(?=Rule Name:)", output)
    for block in rule_blocks:
        if "Rule Name:" not in block:
            continue

        rule = parse_single_rule_block(block)
        if not rule:
            continue

        if enabled_only and (rule.get("enabled") or "").lower() != "yes":
            continue

        # Handle port filtering
        rule_port = rule.get("port")

        # Exclude "Any" ports if requested
        if exclude_any_ports and rule_port == "Any":
            continue

        # Filter by specific ports if provided
        if ports_set and rule_port != "Any":
            # Extract all numeric ports from the rule (handles ranges, lists, etc.)
            rule_ports = extract_ports_from_rule(rule_port)
            if not any(str(port) in ports_set for port in rule_ports):
                continue

        rules.append(rule)

    return rules


def extract_ports_from_rule(port_spec):  # noqa: PLR0911
    """Extract all individual ports from a port specification (ranges, lists, etc.)"""
    if not port_spec or port_spec == "Any":
        return []

    # If it's a simple integer, return it
    if isinstance(port_spec, int):
        return [port_spec]

    # If it's a string that can be converted to int, return it
    if isinstance(port_spec, str) and port_spec.isdigit():
        return [int(port_spec)]

    # Handle port ranges (e.g., "1000-2000")
    if isinstance(port_spec, str) and "-" in port_spec:
        try:
            start, end = map(int, port_spec.split("-"))
            return list(range(start, end + 1))
        except ValueError:
            return []

    # Handle comma-separated lists (e.g., "80,443,8080")
    if isinstance(port_spec, str) and "," in port_spec:
        ports = []
        for part in port_spec.split(","):
            part_stripped = part.strip()
            if part_stripped.isdigit():
                ports.append(int(part_stripped))
            elif "-" in part_stripped:  # Handle ranges within lists
                ports.extend(extract_ports_from_rule(part_stripped))
        return ports

    # If it's a service name or other non-numeric value, return empty
    return []


def parse_single_rule_block(block):
    """
    Parse a single rule block into a dictionary.
    """
    patterns = {
        "name": r"Rule Name:\s*(.+?)(?:\n|$)",
        "direction": r"Direction:\s*(.+?)(?:\n|$)",
        "action": r"Action:\s*(.+?)(?:\n|$)",
        "protocol": r"Protocol:\s*(.+?)(?:\n|$)",
        "local_port": r"LocalPort:\s*(.+?)(?:\n|$)",
        "remote_port": r"RemotePort:\s*(.+?)(?:\n|$)",
        "enabled": r"Enabled:\s*(.+?)(?:\n|$)",
    }

    rule = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, block, re.IGNORECASE)
        rule[field] = match.group(1).strip() if match else None

    # Skip if essential fields are missing
    if not all([rule["name"], rule["direction"], rule["action"], rule["protocol"]]):
        return None

    # Parse port information - check both local and remote ports
    port = "Any"
    port_candidates = [rule["local_port"], rule["remote_port"]]

    for port_candidate in port_candidates:
        if port_candidate and port_candidate.lower() != "any":
            port = port_candidate
            break

    # Try to parse as integer if it's a simple number
    if isinstance(port, str) and port.isdigit():
        with contextlib.suppress(ValueError):
            port = int(port)

    return {
        "name": rule["name"],
        "direction": rule["direction"].upper(),
        "action": rule["action"].upper(),
        "protocol": rule["protocol"].upper(),
        "enabled": rule["enabled"],
        "port": port,
        "local_port": rule["local_port"],
        "remote_port": rule["remote_port"],
    }


# Enhanced debugging function to see what ports are actually being parsed
# def debug_port_parsing():
#     """Debug function to see how ports are being parsed"""
#     command = ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"]

#     try:
#         result = subprocess.run(
#             command,
#             capture_output=True,
#             text=True,
#             encoding="utf-8",
#             check=True,
#             timeout=30,
#         )

#         rule_blocks = re.split(r"\n(?=Rule Name:)", result.stdout)
#         for block in rule_blocks:
#             if "Rule Name:" not in block:
#                 continue

#             # Look for MQTT-related rules
#             if any(keyword in block for keyword in ["1883", "9001", "MQTT", "mqtt"]):
#                 print("=" * 50)
#                 print("Found MQTT-related rule:")
#                 print(block)
#                 print("=" * 50)

#     except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
#         print(f"Error executing command: {e}")


# @cache
def get_firewall_info(
    interested_ports=None, direction=None, enabled_only=False, exclude_any_ports=False
) -> dict:
    """Return a dict of firewall info."""
    return {
        "status": "TODO",
        "rules": get_firewall_rules(
            interested_ports,
            direction=direction,
            enabled_only=enabled_only,
            exclude_any_ports=exclude_any_ports,
        ),
    }


# Example usage with performance improvements:
# if __name__ == "__main__":
#     print("Testing improved firewall rules script...")

#     # First, debug to see what MQTT rules exist
#     print("\n--- Debug: Looking for MQTT rules ---")
#     debug_port_parsing()

#     # Test with specific ports (faster)
#     print("\n--- Rules for specific ports (optimized) ---")
#     interested_ports = [80, 1883, 9001, 5432, 8081]

#     # Get only inbound rules for specific ports, excluding "Any" ports
#     inbound_rules = get_firewall_rules(
#         interested_ports, direction="in", enabled_only=True, exclude_any_ports=True
#     )
#     print(f"Found {len(inbound_rules)} enabled inbound rules with specific ports")

#     # Show rules that match our ports
#     mqtt_rules = [
#         rule
#         for rule in inbound_rules
#         if any(str(port) in str(rule.get("port", "")) for port in [1883, 9001])
#     ]

#     print(f"Found {len(mqtt_rules)} MQTT-related rules (ports 1883, 9001):")
#     for rule in mqtt_rules:
#         print(f"  - {rule['name']}: Port {rule['port']}")

#     print(json.dumps(inbound_rules, indent=2))
