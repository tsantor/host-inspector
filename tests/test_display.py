from host_inspector import get_display_info


def test_get_display_info():
    displays = get_display_info()
    assert isinstance(displays, list)
    for display in displays:
        assert isinstance(display, dict)
        assert set(display.keys()) == {
            "name",
            "display_id",
            "resolution_actual",
            "pixel_resolution",
            "refresh_hz",
        }
        assert isinstance(display["name"], str)
        assert isinstance(display["display_id"], int)
        assert isinstance(display["resolution_actual"], dict)
        assert isinstance(display["pixel_resolution"], dict)
        assert isinstance(display["refresh_hz"], int | float)
        for res_key in ["width", "height"]:
            assert res_key in display["resolution_actual"]
            assert res_key in display["pixel_resolution"]
            assert isinstance(display["resolution_actual"][res_key], int)
            assert isinstance(display["pixel_resolution"][res_key], int)
