import json
import platform
import shlex
import subprocess
from functools import cache

from host_inspector.platform.application.dtos import PlatformInfoDTO


@cache
def _get_hardware():
    """Safely get hardware."""
    try:
        cmd = "system_profiler -json SPHardwareDataType"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(proc.stdout.strip())
        if "SPHardwareDataType" in result:
            return result["SPHardwareDataType"][0]
    except subprocess.CalledProcessError:  # pragma: no cover
        return None
    return None


@cache
def _get_model() -> str:
    return result.get("machine_name") if (result := _get_hardware()) else ""


@cache
def _get_serial() -> str:
    return result.get("serial_number") if (result := _get_hardware()) else ""


class MacPlatformCollector:
    def platform_info(self) -> PlatformInfoDTO:
        uname = platform.uname()
        return PlatformInfoDTO(
            system=uname.system,
            release=uname.release,
            machine=uname.machine,
            architecture=platform.architecture()[0],
            manufacturer="Apple Inc.",
            model=_get_model(),
            serial=_get_serial(),
        )
