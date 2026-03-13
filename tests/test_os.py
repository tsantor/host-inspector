from host_inspector.os import get_os_info
from host_inspector.os.application.service import OSService
from host_inspector.os.domain import get_macos_edition


class StubCollector:
    def __init__(self, payload: dict):
        self.payload = payload

    def collect(self) -> dict:
        return self.payload


def test_get_os_info():
    os_info = get_os_info()

    assert isinstance(os_info, dict)

    required_keys = {"name", "version", "edition", "build"}
    assert required_keys.issubset(os_info.keys())

    # If you want to check that the values are not None
    for key, value in os_info.items():
        assert value is not None, f'Key "{key}" is None.'


def test_get_mac_os_edition():
    assert get_macos_edition("10.15") == "Catalina"
    assert get_macos_edition("11") == "Big Sur"
    assert get_macos_edition("12") == "Monterey"
    assert get_macos_edition("13") == "Ventura"
    assert get_macos_edition("14") == "Sonoma"
    assert get_macos_edition("15") == "Sequoia"
    assert get_macos_edition("26") == "Tahoe"
    assert get_macos_edition("26.1") == "Tahoe"
    assert get_macos_edition("27") == "macOS"
    assert get_macos_edition("27.0.1") == "macOS"
    assert get_macos_edition("not-a-version") == "--"


def test_os_service_mac_edition_resolution():
    service = OSService(
        collector=StubCollector(
            {
                "platform": "darwin",
                "name": "macOS",
                "version": "26.1",
                "edition": "--",
                "build": "24A123",
            }
        )
    )

    assert service.get_os_info() == {
        "name": "macOS",
        "version": "26.1",
        "edition": "Tahoe",
        "build": "24A123",
    }


def test_os_service_linux_passthrough():
    service = OSService(
        collector=StubCollector(
            {
                "platform": "linux",
                "name": "Ubuntu",
                "version": "24.04",
                "edition": "noble",
                "build": "--",
            }
        )
    )

    assert service.get_os_info() == {
        "name": "Ubuntu",
        "version": "24.04",
        "edition": "noble",
        "build": "--",
    }


def test_os_service_windows_display_version_passthrough():
    service = OSService(
        collector=StubCollector(
            {
                "platform": "win32",
                "name": "Windows",
                "version": 11,
                "edition": "Professional",
                "build": 26100,
                "display_version": "24H2",
            }
        )
    )

    assert service.get_os_info() == {
        "name": "Windows",
        "version": 11,
        "edition": "Professional",
        "build": 26100,
        "display_version": "24H2",
    }
