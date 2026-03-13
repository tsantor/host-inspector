import re
import shlex
import subprocess
from functools import cache

from host_inspector.gpu.application.dtos import GPUInfoDTO
from host_inspector.gpu.application.dtos import GPUPayloadDTO


@cache
def _get_gpu():
    """Safely get GPU."""
    try:
        cmd = "vcgencmd get_config int"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


@cache
def _get_model() -> str:
    """Get GPU chipset model."""
    model_map = {
        "bcm2835": "Broadcom VideoCore IV",
        "bcm2836": "Broadcom VideoCore IV",
        "bcm2837": "Broadcom VideoCore IV",
        "bcm2711": "Broadcom VideoCore VI",
        "bcm2710A1": "Broadcom VideoCore VI",
    }
    try:
        cmd = "cat /sys/firmware/devicetree/base/gpu/compatible"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        for model_key, model in model_map.items():
            if model_key in result:
                return model
        return "Unknown GPU Model"
    except subprocess.CalledProcessError:
        pass

    try:
        result = subprocess.run(
            ["/usr/bin/bash", "-c", 'DISPLAY=:0 glxinfo | grep "OpenGL renderer"'],
            capture_output=True,
            text=True,
            check=True,
        )
        gpu_info = result.stdout.strip()
        return gpu_info.split(":")[1].strip()
    except subprocess.CalledProcessError:
        return "--"


@cache
def _get_vram() -> str:
    """Safely get GPU VRAM."""
    try:
        cmd = "vcgencmd get_mem gpu"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        return result.replace("gpu=", "").replace("M", " MB")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "--"


@cache
def _get_resolution() -> str:
    """Safely get resolution."""
    try:
        cmd = "xrandr -display :0.0"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        regex = r"current (\d+) x (\d+)"
        if match := re.search(regex, result):
            return f"{match[1]} x {match[2]}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "--"

    return "--"


@cache
def _get_refresh_rate() -> str:
    """Safely get refresh rate."""
    if result := _get_gpu():
        for line in result.splitlines():
            if line.startswith("lcd_framerate="):
                return f"{int(line.split('=')[1])} Hz"
    return "--"


class LinuxGPUCollector:
    def gpu_info(self) -> GPUPayloadDTO:
        """Return a dict of GPU info."""
        return GPUPayloadDTO(
            adapters=[
                GPUInfoDTO(
                    model=_get_model(),
                    vram=_get_vram(),
                    resolution=_get_resolution(),
                    refresh_rate=_get_refresh_rate(),
                )
            ],
            as_list=False,
        )
