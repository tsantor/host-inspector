from host_inspector import get_health_info
from host_inspector.health.application.service import HealthService


def test_get_health_info():
    health_dict = get_health_info()
    assert isinstance(health_dict, dict)

    expected_keys = {"cpu", "mem", "disk", "uptime", "local_datetime"}
    missing_keys = [key for key in expected_keys if key not in health_dict]
    assert not missing_keys, f"Missing keys: {missing_keys}"

    for value in health_dict.values():
        assert isinstance(value, dict)


class StubProbe:
    def cpu_info(self) -> dict:
        return {"cpu": 1}

    def mem_info(self) -> dict:
        return {"mem": 1}

    def disk_info(self) -> dict:
        return {"disk": 1}

    def uptime_info(self) -> dict:
        return {"uptime": 1}

    def datetime_info(self) -> dict:
        return {"date": "2026-03-13"}


def test_health_service_output():
    service = HealthService(probe=StubProbe())
    assert service.get_health_info() == {
        "cpu": {"cpu": 1},
        "mem": {"mem": 1},
        "disk": {"disk": 1},
        "uptime": {"uptime": 1},
        "local_datetime": {"date": "2026-03-13"},
    }
