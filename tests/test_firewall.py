import os

from host_inspector import get_firewall_info


def test_get_firewall_info():
    firewall_info = get_firewall_info(
        interested_ports=[8000, 80, 1883, 9001, 22, 5432, 8080, 8081],
        direction="in",
        enabled_only=True,
        exclude_any_ports=True,
    )

    # print(firewall_info)

    assert isinstance(firewall_info, dict)
    assert set(firewall_info.keys()) == {
        "status",
        "rules",
    }

    # If you want to check that the values are not None
    # for key, value in cpu_info.items():
    #     assert value is not None, f'Key "{key}" is None.'


def test_check_firewall_status():
    if os.name != "nt":
        return

    from host_inspector.firewall.windows import check_firewall_status  # noqa: PLC0415

    assert isinstance(check_firewall_status(), bool)


def test_is_firewall_enabled():
    if os.name != "nt":
        return

    from host_inspector.firewall.windows import is_firewall_enabled  # noqa: PLC0415

    status = is_firewall_enabled()
    assert isinstance(status, dict)
    assert set(status.keys()) == {"overall", "profiles"}
    assert isinstance(status["overall"], bool)
    assert isinstance(status["profiles"], dict)
    for profile, enabled in status["profiles"].items():
        assert profile in {"Domain", "Private", "Public"}
        assert isinstance(enabled, bool)
