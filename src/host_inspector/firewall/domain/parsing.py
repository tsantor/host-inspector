import contextlib
import re


def port_to_name(port: str) -> str | None:
    """Return a friendly name for a port or comma-separated ports."""
    port_map = {
        "80": "HTTP",
        "443": "HTTPS",
        "22": "SSH",
        "1883": "MQTT",
        "3000": "Node",
        "9001": "MQTT",
        "5432": "PostgreSQL",
        "8000": "HTTP",
        "8080": "HTTP",
        "8883": "MQTT",
    }
    ports = [p.strip() for p in port.split(",")] if port else []
    seen = set()
    names = []
    for current in ports:
        label = port_map.get(current, current)
        if label not in seen:
            names.append(label)
            seen.add(label)
    return ",".join(names) if names else None


def parse_linux_firewall_output(
    output: str,
    ports_filter: list[int] | None = None,
    enabled_only: bool = False,
    exclude_any_ports: bool = False,
) -> list[dict]:
    del ports_filter, enabled_only, exclude_any_ports
    lines = output.strip().split("\n")
    rules: list[dict] = []

    start_index = -1
    for i, line in enumerate(lines):
        if "To" in line and "Action" in line and "From" in line:
            start_index = i + 2
            break

    if start_index == -1:
        return rules

    for raw_line in lines[start_index:]:
        line = raw_line.strip()
        if not line or line.startswith("--") or "(v6)" in line:
            continue

        parts = line.split()
        if len(parts) < 3:  # noqa: PLR2004
            continue

        to_part = parts[0]
        action_part = parts[1]
        direction_part = parts[2] if len(parts) > 2 else "IN"  # noqa: PLR2004
        from_part = parts[3] if len(parts) > 3 else "ANY"  # noqa: PLR2004

        protocol = "ANY"
        port = None
        if "/" in to_part:
            port_part, protocol_part = to_part.split("/")
            protocol = protocol_part.upper()
            port = port_part
        else:
            port = to_part or None

        action = "ALLOW" if "ALLOW" in action_part.upper() else "DENY"
        direction = (
            "INBOUND" if "IN" in direction_part or "OUT" not in line else "OUTBOUND"
        )
        from_port = "ANY" if from_part == "Anywhere" else from_part

        rules.append(
            {
                "name": port_to_name(port) if port else None,
                "direction": direction,
                "action": action,
                "protocol": protocol,
                "enabled": True,
                "local_port": port,
                "remote_port": from_port,
            }
        )

    return rules


def extract_ports_from_rule(port_spec):  # noqa: PLR0911
    """Extract ports from a port specification."""
    if not port_spec or port_spec == "Any":
        return []
    if isinstance(port_spec, int):
        return [port_spec]
    if isinstance(port_spec, str) and port_spec.isdigit():
        return [int(port_spec)]
    if isinstance(port_spec, str) and "-" in port_spec:
        with contextlib.suppress(ValueError):
            start, end = map(int, port_spec.split("-"))
            return list(range(start, end + 1))
        return []
    if isinstance(port_spec, str) and "," in port_spec:
        ports = []
        for part in port_spec.split(","):
            stripped = part.strip()
            if stripped.isdigit():
                ports.append(int(stripped))
            elif "-" in stripped:
                ports.extend(extract_ports_from_rule(stripped))
        return ports
    return []


def parse_windows_rule_block(block: str) -> dict | None:
    """Parse a single netsh rule block into a dictionary."""
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

    if not all([rule["name"], rule["direction"], rule["action"], rule["protocol"]]):
        return None

    port = "Any"
    for port_candidate in [rule["local_port"], rule["remote_port"]]:
        if port_candidate and port_candidate.lower() != "any":
            port = port_candidate
            break

    if isinstance(port, str) and port.isdigit():
        with contextlib.suppress(ValueError):
            port = int(port)

    enabled = str(rule.get("enabled", "")).strip().upper() == "YES"

    return {
        "name": rule["name"],
        "direction": rule["direction"].upper(),
        "action": rule["action"].upper(),
        "protocol": rule["protocol"].upper(),
        "enabled": enabled,
        "port": port,
        "local_port": rule["local_port"],
        "remote_port": rule["remote_port"],
    }


def parse_windows_firewall_output(
    output: str,
    ports_filter: list[int] | None = None,
    enabled_only: bool = False,
    exclude_any_ports: bool = False,
) -> list[dict]:
    """Parse `netsh` firewall output into filtered rule dictionaries."""
    rules = []
    ports_set = {str(p) for p in ports_filter} if ports_filter else None

    for block in re.split(r"\n(?=Rule Name:)", output):
        if "Rule Name:" not in block:
            continue

        rule = parse_windows_rule_block(block)
        if not rule:
            continue
        if enabled_only and not rule.get("enabled", False):
            continue

        rule_port = rule.get("port")
        if exclude_any_ports and rule_port == "Any":
            continue
        if ports_set and rule_port != "Any":
            rule_ports = extract_ports_from_rule(rule_port)
            if not any(str(port) in ports_set for port in rule_ports):
                continue

        rules.append(rule)

    return rules
