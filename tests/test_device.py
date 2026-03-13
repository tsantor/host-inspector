from host_inspector import get_device_info
from host_inspector.device.application.service import DeviceService


def test_get_device_info():
    device_dict = get_device_info()
    assert isinstance(device_dict, dict)

    expected_keys = {"os", "platform", "network", "gpu", "display"}
    missing_keys = [key for key in expected_keys if key not in device_dict]
    assert not missing_keys, f"Missing keys: {missing_keys}"

    # assert set(device_info.keys()) == {"os", "platform", "network", "gpu", "display"}

    assert isinstance(device_dict["os"], dict)
    assert isinstance(device_dict["platform"], dict)
    assert isinstance(device_dict["network"], dict)
    assert isinstance(device_dict["gpu"], dict | list)
    assert isinstance(device_dict["display"], list)


class StubProbe:
    def os_info(self) -> dict:
        return {"name": "macOS"}

    def platform_info(self) -> dict:
        return {"system": "Darwin"}

    def network_info(self) -> dict:
        return {"ip_address": "127.0.0.1"}

    def gpu_info(self) -> dict:
        return {"model": "GPU"}

    def display_info(self) -> list[dict]:
        return [{"name": "Display"}]


def test_device_service_output():
    service = DeviceService(probe=StubProbe())
    assert service.get_device_info() == {
        "os": {"name": "macOS"},
        "platform": {"system": "Darwin"},
        "network": {"ip_address": "127.0.0.1"},
        "gpu": {"model": "GPU"},
        "display": [{"name": "Display"}],
    }
