def format_node_as_mac(node_value: int) -> str:
    """Format an integer node identifier as a MAC-like string."""
    return ":".join(f"{node_value:012x}"[i : i + 2] for i in range(0, 12, 2))


def normalize_mac_address(mac_address: str | None) -> str:
    """Normalize a MAC address to lower-case with ':' separators."""
    if not mac_address or mac_address == "--":
        return "--"
    return mac_address.lower().replace("-", ":")


def strip_ipv6_scope(ipv6_address: str | None) -> str:
    """Strip scope-id suffix from IPv6 addresses."""
    if not ipv6_address or ipv6_address == "--":
        return "--"
    return ipv6_address.split("%")[0]
