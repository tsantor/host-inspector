import json
import shlex
import subprocess
from functools import cache

from host_inspector.gpu.application.dtos import GPUInfoDTO
from host_inspector.gpu.application.dtos import GPUPayloadDTO
from host_inspector.utils.byteutils import bytes_to_gib

from .common import clean_gpu_name


@cache
def _get_gpu():
    """Safely get GPU."""
    try:
        cmd = "powershell Get-CimInstance -ClassName Win32_VideoController | Select-Object Name, CurrentRefreshRate, Current*Resolution, AdapterRAM | ConvertTo-Json -Compress"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def _parse_controllers(gpu_output):
    """Parse JSON GPU output into list of controller dictionaries."""
    if not gpu_output:
        return []

    try:
        data = json.loads(gpu_output)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []


def _get_model(controller):
    """Get GPU model from controller dict."""
    if name := controller.get("Name"):
        return clean_gpu_name(name)
    return "--"


def _get_vram(controller):
    """Get VRAM from controller dict."""
    if adapter_ram := controller.get("AdapterRAM"):
        try:
            return f"{bytes_to_gib(int(adapter_ram))} GB"
        except (ValueError, TypeError):
            pass
    return "--"


def _get_resolution(controller):
    """Get resolution from controller dict."""
    hres = controller.get("CurrentHorizontalResolution")
    vres = controller.get("CurrentVerticalResolution")
    if hres and vres:
        return f"{hres} x {vres}"
    return "--"


def _get_refresh_rate(controller):
    """Get refresh rate from controller dict."""
    if refresh_rate := controller.get("CurrentRefreshRate"):
        return f"{refresh_rate} Hz"
    return "--"


def _build_adapter_info(controller) -> GPUInfoDTO:
    """Build adapter info dict from controller dict."""
    return GPUInfoDTO(
        model=_get_model(controller),
        vram=_get_vram(controller),
        resolution=_get_resolution(controller),
        refresh_rate=_get_refresh_rate(controller),
    )


class WindowsGPUCollector:
    def gpu_info(self) -> GPUPayloadDTO:
        """Return info dictionaries, one for each display adapter."""
        gpu_output = _get_gpu()
        controllers = _parse_controllers(gpu_output)
        return GPUPayloadDTO(
            adapters=[_build_adapter_info(controller) for controller in controllers],
            as_list=True,
        )
