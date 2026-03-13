from host_inspector.display import get_display_info
from host_inspector.gpu import get_gpu_info
from host_inspector.network import get_network_info
from host_inspector.os import get_os_info
from host_inspector.platform import get_platform_info


class DeviceProbe:
    def os_info(self) -> dict:
        return get_os_info()

    def platform_info(self) -> dict:
        return get_platform_info()

    def network_info(self) -> dict:
        return get_network_info()

    def gpu_info(self) -> dict | list:
        return get_gpu_info()

    def display_info(self) -> list[dict]:
        return get_display_info()
