import re
import shlex
import subprocess
from functools import cache

from host_inspector.gpu.application.dtos import GPUInfoDTO
from host_inspector.gpu.application.dtos import GPUPayloadDTO

from .common import clean_gpu_name


@cache
def _get_gpu():
    """Safely get GPU."""
    try:
        cmd = "system_profiler SPDisplaysDataType"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError:  # pragma: no cover
        return None


@cache
def _get_model() -> str:
    """Get GPU chipset model."""
    if result := _get_gpu():
        for line in result.split("\n"):
            if "Chipset Model" in line:
                return clean_gpu_name(
                    re.sub(r"\s+Chipset Model:\s+", "", line, count=1)
                )
    return "--"  # pragma: no cover


@cache
def _get_vram() -> str:
    """Get GPU VRAM."""
    if result := _get_gpu():
        for line in result.split("\n"):
            if "VRAM" in line:
                return line.split(":")[1].strip()
    return "--"  # pragma: no cover


@cache
def _get_resolution() -> str:
    """Get resolution."""
    if result := _get_gpu():
        regex = r"(\d+) x (\d+)"
        if match := re.search(regex, result):
            return f"{match[1]} x {match[2]}"
    return "--"  # pragma: no cover


@cache
def _get_refresh_rate() -> str:
    """Get refresh rate."""
    pattern = re.compile(r"@ (\d+\.\d+)Hz")
    output = _get_gpu()
    if output:
        match = pattern.search(output)
        if match:
            return f"{match.group(1)} Hz"
    return "--"  # pragma: no cover


class MacGPUCollector:
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
