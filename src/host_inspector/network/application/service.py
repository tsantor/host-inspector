from dataclasses import dataclass

from host_inspector.network.domain import format_node_as_mac
from host_inspector.network.domain import normalize_mac_address
from host_inspector.network.domain import strip_ipv6_scope

from .ports import NetworkProbePort


@dataclass(frozen=True)
class NetworkService:
    probe: NetworkProbePort

    def get_network_info(self) -> dict:
        ip_address = self.probe.current_ip_address()
        return {
            "hostname": self.probe.hostname(),
            "ip_address": ip_address,
            "ipv6_address": strip_ipv6_scope(self.probe.ipv6_for_ip(ip_address)),
            "node_address": format_node_as_mac(self.probe.node_value()),
            "mac_address": normalize_mac_address(self.probe.mac_for_ip(ip_address)),
            "interface": self.probe.interface_for_ip(ip_address),
        }
