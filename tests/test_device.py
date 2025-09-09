from host_inspector import get_device_info


def test_get_device_info():
    device_info = get_device_info()

    assert isinstance(device_info, dict)
    assert set(device_info.keys()) == {"os", "platform", "network", "gpu", "display"}

    assert isinstance(device_info["os"], dict)
    assert isinstance(device_info["platform"], dict)
    assert isinstance(device_info["network"], dict)
    assert isinstance(device_info["gpu"], dict | list)
    assert isinstance(device_info["display"], list)
