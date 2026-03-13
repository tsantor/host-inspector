import importlib
import sys

from host_inspector.display.application.service import DisplayService


def build_display_service() -> DisplayService:
    if sys.platform == "darwin":
        module_name = "host_inspector.display.infrastructure.mac"
        class_name = "MacDisplayCollector"
    elif sys.platform == "win32":
        module_name = "host_inspector.display.infrastructure.windows"
        class_name = "WindowsDisplayCollector"
    elif sys.platform == "linux":
        module_name = "host_inspector.display.infrastructure.linux"
        class_name = "LinuxDisplayCollector"
    else:
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg)

    collector_module = importlib.import_module(module_name)
    collector_cls = getattr(collector_module, class_name)
    return DisplayService(collector=collector_cls())
