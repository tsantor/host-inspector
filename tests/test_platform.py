from host_inspector.platform import get_platform_info
from host_inspector.platform.application.service import PlatformService


def test_get_model():
    info = get_platform_info()

    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "system",
        "release",
        "machine",
        "architecture",
        "manufacturer",
        "model",
        "serial",
    }

    # If you want to check that the values are not None
    for key, value in info.items():
        assert value is not None, f'Key "{key}" is None.'


class StubCollector:
    def __init__(self, payload: dict):
        self.payload = payload

    def platform_info(self) -> dict:
        return self.payload


def test_platform_service_passthrough():
    payload = {
        "system": "Darwin",
        "release": "23.6.0",
        "machine": "arm64",
        "architecture": "64bit",
        "manufacturer": "Apple Inc.",
        "model": "MacBook Pro",
        "serial": "ABC123",
    }
    service = PlatformService(collector=StubCollector(payload))
    assert service.get_platform_info() == payload
