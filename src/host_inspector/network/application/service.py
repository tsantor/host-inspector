from dataclasses import dataclass

from host_inspector.network.domain import format_node_as_mac
from host_inspector.network.domain import normalize_mac_address
from host_inspector.network.domain import strip_ipv6_scope

from .ports import NetworkProbePort


@dataclass(frozen=True)
class NetworkService:
    probe: NetworkProbePort

    def get_network_info(self) -> dict:
        snapshot = self.probe.snapshot()
        return {
            "hostname": snapshot.hostname,
            "ip_address": snapshot.ip_address,
            "ipv6_address": strip_ipv6_scope(snapshot.ipv6_address),
            "node_address": format_node_as_mac(snapshot.node_value),
            "mac_address": normalize_mac_address(snapshot.mac_address),
            "interface": snapshot.interface,
        }
