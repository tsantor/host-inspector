from host_inspector import get_display_info
from host_inspector.display.application.service import DisplayService
from host_inspector.display.domain import parse_macos_display_output
from host_inspector.display.domain import parse_resolution


def test_get_display_info():
    displays = get_display_info()
    assert isinstance(displays, list)
    for display in displays:
        assert isinstance(display, dict)
        assert set(display.keys()) == {
            "name",
            "display_id",
            "resolution_actual",
            "resolution",
            "refresh_rate",
        }
        assert isinstance(display["name"], str)
        assert isinstance(display["display_id"], int)
        assert isinstance(display["resolution_actual"], str)
        assert isinstance(display["resolution"], str)
        assert isinstance(display["refresh_rate"], str)


def test_parse_resolution():
    expected_width = 3440
    expected_height = 1440
    expected_hz = 60.0
    width, height, hz = parse_resolution("3440 x 1440 @ 60.00Hz")
    assert width == expected_width
    assert height == expected_height
    assert hz == expected_hz


def test_parse_macos_display_output():
    expected_display_id = 12345
    parsed = parse_macos_display_output(
        {
            "SPDisplaysDataType": [
                {
                    "spdisplays_ndrvs": [
                        {
                            "_name": "Studio Display",
                            "_spdisplays_displayID": "12345",
                            "_spdisplays_resolution": "1728 x 1117 @ 60.00Hz",
                            "_spdisplays_pixels": "3456 x 2234",
                        }
                    ]
                }
            ]
        }
    )
    assert len(parsed) == 1
    assert parsed[0]["name"] == "Studio Display"
    assert parsed[0]["display_id"] == expected_display_id
    assert parsed[0]["resolution_actual"] == "1728 x 1117"
    assert parsed[0]["resolution"] == "3456 x 2234"
    assert parsed[0]["refresh_rate"] == "60.0 Hz"


class StubCollector:
    def __init__(self, payload: list[dict]):
        self.payload = payload

    def display_info(self) -> list[dict]:
        return self.payload


def test_display_service_passthrough():
    payload = [
        {
            "name": "Display",
            "display_id": 1,
            "resolution_actual": "1920 x 1080",
            "resolution": "1920 x 1080",
            "refresh_rate": "60 Hz",
        }
    ]
    service = DisplayService(collector=StubCollector(payload))
    assert service.get_display_info() == payload
