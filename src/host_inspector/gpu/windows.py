import shlex
import subprocess
from functools import cache

from host_inspector.utils.byteutils import bytes_to_gib

from .utils import clean_name


@cache
def get_gpu():
    """Safely get GPU."""
    try:
        cmd = "powershell Get-WmiObject win32_VideoController"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def _get_key_value(line):
    """Split text output and return a key, value pair."""
    parts = line.split(":")
    key = parts.pop(0).strip()
    value = ":".join(parts).strip()
    return (key, value)


def _parse_controllers(gpu_output):
    """Parse GPU output into separate controller dictionaries."""
    if not gpu_output:
        return []

    controllers = []
    current_controller = {}

    for line in gpu_output.split("\n"):
        line = line.strip()
        if not line:
            if current_controller:
                controllers.append(current_controller)
                current_controller = {}
        elif ":" in line:
            key, value = _get_key_value(line)
            current_controller[key] = value

    if current_controller:
        controllers.append(current_controller)

    return controllers


def _get_model(controller):
    """Get GPU model from controller dict."""
    if description := controller.get("Description"):
        return clean_name(description)
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


def _build_adapter_info(controller):
    """Build adapter info dict from controller dict."""
    return {
        "model": _get_model(controller),
        "vram": _get_vram(controller),
        "resolution": _get_resolution(controller),
        "refresh_rate": _get_refresh_rate(controller),
    }


@cache
def get_gpu_info() -> list[dict]:
    """Return a list of GPU info dictionaries, one for each display adapter."""
    gpu_output = get_gpu()
    controllers = _parse_controllers(gpu_output)
    return [_build_adapter_info(controller) for controller in controllers]
