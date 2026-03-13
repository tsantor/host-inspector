from host_inspector.device.application.service import DeviceService

from .probe import DeviceProbe


def build_device_service() -> DeviceService:
    return DeviceService(probe=DeviceProbe())
