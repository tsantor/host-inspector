import importlib
import sys

from host_inspector.os.application.service import OSService


def build_os_service() -> OSService:
    """Build an OS service wired with the current platform collector."""
    if sys.platform == "darwin":
        module_name = "host_inspector.os.infrastructure.mac"
        class_name = "MacOSCollector"
    elif sys.platform == "win32":
        module_name = "host_inspector.os.infrastructure.windows"
        class_name = "WindowsOSCollector"
    elif sys.platform == "linux":
        module_name = "host_inspector.os.infrastructure.linux"
        class_name = "LinuxOSCollector"
    else:
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg)

    collector_module = importlib.import_module(module_name)
    collector_cls = getattr(collector_module, class_name)
    return OSService(collector=collector_cls())
