import importlib
import sys

from host_inspector.gpu.application.service import GPUService


def build_gpu_service() -> GPUService:
    """Build a GPU service wired with the current platform collector."""
    if sys.platform == "darwin":
        module_name = "host_inspector.gpu.infrastructure.mac"
        class_name = "MacGPUCollector"
    elif sys.platform == "win32":
        module_name = "host_inspector.gpu.infrastructure.windows"
        class_name = "WindowsGPUCollector"
    elif sys.platform == "linux":
        module_name = "host_inspector.gpu.infrastructure.linux"
        class_name = "LinuxGPUCollector"
    else:
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg)

    collector_module = importlib.import_module(module_name)
    collector_cls = getattr(collector_module, class_name)
    return GPUService(collector=collector_cls())
