from host_inspector import get_network_info
from host_inspector.network.application.service import NetworkService
from host_inspector.network.domain import format_node_as_mac
from host_inspector.network.domain import normalize_mac_address
from host_inspector.network.domain import strip_ipv6_scope


class StubProbe:
    def __init__(self):
        self._ip = "192.168.1.12"

    def hostname(self) -> str:
        return "test-host"

    def current_ip_address(self) -> str:
        return self._ip

    def node_value(self) -> int:
        return 0x001122334455

    def interface_for_ip(self, ip_address: str) -> str:
        return "en0" if ip_address == self._ip else "--"

    def mac_for_ip(self, ip_address: str) -> str | None:
        if ip_address == self._ip:
            return "AA-BB-CC-DD-EE-FF"
        return None

    def ipv6_for_ip(self, ip_address: str) -> str | None:
        if ip_address == self._ip:
            return "fe80::1%en0"
        return None


def test_get_network_info_shape():
    info = get_network_info()
    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "hostname",
        "ip_address",
        "ipv6_address",
        "node_address",
        "mac_address",
        "interface",
    }


def test_network_domain_normalization():
    assert format_node_as_mac(0x001122334455) == "00:11:22:33:44:55"
    assert normalize_mac_address("AA-BB-CC-DD-EE-FF") == "aa:bb:cc:dd:ee:ff"
    assert strip_ipv6_scope("fe80::1%en0") == "fe80::1"


def test_network_service_builds_output():
    service = NetworkService(probe=StubProbe())
    assert service.get_network_info() == {
        "hostname": "test-host",
        "ip_address": "192.168.1.12",
        "ipv6_address": "fe80::1",
        "node_address": "00:11:22:33:44:55",
        "mac_address": "aa:bb:cc:dd:ee:ff",
        "interface": "en0",
    }
