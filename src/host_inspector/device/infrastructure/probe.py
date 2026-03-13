from host_inspector.device.application.dtos import DeviceInputDTO
from host_inspector.display import get_display_info
from host_inspector.gpu import get_gpu_info
from host_inspector.network import get_network_info
from host_inspector.os import get_os_info
from host_inspector.platform import get_platform_info


class DeviceProbe:
    def snapshot(self) -> DeviceInputDTO:
        return DeviceInputDTO(
            os=get_os_info(),
            platform=get_platform_info(),
            network=get_network_info(),
            gpu=get_gpu_info(),
            display=get_display_info(),
        )
