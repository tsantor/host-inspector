def get_firewall_rules(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
):
    # TODO: Implement Linux firewall rules parsing
    return []


def get_firewall_info(
    interested_ports=None,
    direction=None,
    enabled_only=False,
    exclude_any_ports=False,
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
