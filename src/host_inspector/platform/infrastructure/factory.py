import importlib
import sys

from host_inspector.platform.application.service import PlatformService


def build_platform_service() -> PlatformService:
    if sys.platform == "darwin":
        module_name = "host_inspector.platform.infrastructure.mac"
        class_name = "MacPlatformCollector"
    elif sys.platform == "win32":
        module_name = "host_inspector.platform.infrastructure.windows"
        class_name = "WindowsPlatformCollector"
    elif sys.platform == "linux":
        module_name = "host_inspector.platform.infrastructure.linux"
        class_name = "LinuxPlatformCollector"
    else:
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg)

    collector_module = importlib.import_module(module_name)
    collector_cls = getattr(collector_module, class_name)
    return PlatformService(collector=collector_cls())
