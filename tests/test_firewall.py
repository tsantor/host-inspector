import sys

import pytest

from host_inspector import get_firewall_info
from host_inspector.firewall import is_firewall_enabled
from host_inspector.firewall.application.dtos import FirewallRulesDTO
from host_inspector.firewall.application.dtos import FirewallStatusDTO
from host_inspector.firewall.application.service import FirewallService
from host_inspector.firewall.domain import extract_ports_from_rule
from host_inspector.firewall.domain import parse_linux_firewall_output
from host_inspector.firewall.domain import parse_windows_rule_block


@pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
@pytest.mark.parametrize(
    ("ports", "direction", "enabled_only", "exclude_any_ports"),
    [
        ([80], "in", True, False),
        ([22, 443], "out", False, True),
        ([], "in", False, False),
    ],
)
def test_get_firewall_info(ports, direction, enabled_only, exclude_any_ports):
    firewall_info = get_firewall_info(
        ports=ports,
        direction=direction,
        enabled_only=enabled_only,
        exclude_any_ports=exclude_any_ports,
    )
    assert isinstance(firewall_info, dict)
    assert "status" in firewall_info
    assert "rules" in firewall_info
    assert isinstance(firewall_info["rules"], list)


@pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
def test_get_firewall_info_empty_ports():
    firewall_info = get_firewall_info(ports=[])
    assert isinstance(firewall_info, dict)
    assert "status" in firewall_info
    assert "rules" in firewall_info


def test_ensure_rules_not_empty():
    if not is_firewall_enabled():
        pytest.skip("Firewall is not enabled; skipping test.")
    firewall_info = get_firewall_info()
    assert isinstance(firewall_info, dict)
    assert "rules" in firewall_info
    assert isinstance(firewall_info["rules"], list)
    assert len(firewall_info["rules"]) > 0, "Firewall rules should not be empty"


def test_parse_linux_firewall_output():
    output = """Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
"""
    rules = parse_linux_firewall_output(output)
    expected_rule_count = 2
    assert len(rules) == expected_rule_count
    assert rules[0]["name"] == "SSH"
    assert rules[1]["protocol"] == "TCP"


def test_parse_windows_rule_block():
    block = """Rule Name:                            Test Rule
----------------------------------------------------------------------
Enabled:                              Yes
Direction:                            In
Profiles:                             Domain
Grouping:
LocalIP:                              Any
RemoteIP:                             Any
Protocol:                             TCP
LocalPort:                            443
RemotePort:                           Any
Edge traversal:                       No
Action:                               Allow
"""
    parsed = parse_windows_rule_block(block)
    expected_port = 443
    assert parsed is not None
    assert parsed["name"] == "Test Rule"
    assert parsed["protocol"] == "TCP"
    assert parsed["port"] == expected_port
    assert parsed["enabled"] is True


def test_extract_ports_from_rule():
    assert extract_ports_from_rule("80,443") == [80, 443]
    assert extract_ports_from_rule("1000-1002") == [1000, 1001, 1002]


class StubCollector:
    def __init__(self, status, rules):
        self._status = status
        self._rules = rules

    def enabled_status(self):
        return FirewallStatusDTO(overall=bool(self._status.get("overall", False)))

    def rules(
        self, ports=None, direction=None, enabled_only=False, exclude_any_ports=False
    ):
        del ports, direction, enabled_only, exclude_any_ports
        return FirewallRulesDTO(items=[])


def test_firewall_service_normalizes_dict_status():
    service = FirewallService(
        collector=StubCollector(
            status={"domain": False, "private": False, "public": True, "overall": True},
            rules=[],
        )
    )
    info = service.get_firewall_info()
    assert info["enabled"] is True
    assert info["status"] == "ON"


# @pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
# def test_check_firewall_status():
#     result = check_firewall_status()
#     assert isinstance(result, bool)


# @pytest.mark.skipif(sys.platform == "darwin", reason="Not implemented on macOS")
# def test_is_firewall_enabled():
#     enabled = is_firewall_enabled()
#     assert isinstance(enabled, bool)
