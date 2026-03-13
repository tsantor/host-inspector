import importlib
import sys

from host_inspector.cpu.application.service import CPUService

from .metrics import PsutilCPUMetrics


def build_cpu_service() -> CPUService:
    """Build a CPU service wired with the current platform collector."""
    if sys.platform == "darwin":
        module_name = "host_inspector.cpu.infrastructure.mac"
        class_name = "MacCPUPlatform"
    elif sys.platform == "win32":
        module_name = "host_inspector.cpu.infrastructure.windows"
        class_name = "WindowsCPUPlatform"
    elif sys.platform == "linux":
        module_name = "host_inspector.cpu.infrastructure.linux"
        class_name = "LinuxCPUPlatform"
    else:
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg)

    platform_module = importlib.import_module(module_name)
    platform_cls = getattr(platform_module, class_name)
    return CPUService(metrics=PsutilCPUMetrics(), platform=platform_cls())
