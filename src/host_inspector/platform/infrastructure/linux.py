import contextlib
import platform
import re
import shlex
import subprocess
from functools import cache

from host_inspector.platform.application.dtos import PlatformInfoDTO


@cache
def _get_model() -> str:
    """Safely get model."""
    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "cat /sys/firmware/devicetree/base/model"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip().rstrip("\x00")

    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "sudo dmidecode -s system-family"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    return "--"


@cache
def _get_manufacturer() -> str:
    """Safely get manufacturer."""
    if "Raspberry Pi" in _get_model():
        return "Raspberry Pi Ltd."

    try:
        cmd = "sudo dmidecode -s system-manufacturer"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        return "--"


@cache
def _get_serial() -> str:
    """Safely get serial number."""
    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "cat /proc/cpuinfo"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        result = proc.stdout.strip()
        regex = r"(Serial\s+:)(.+)"
        if match := re.search(regex, result):
            return match[2]

    with contextlib.suppress(subprocess.CalledProcessError):
        cmd = "sudo dmidecode -s system-serial-number"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    return "--"


class LinuxPlatformCollector:
    def platform_info(self) -> PlatformInfoDTO:
        uname = platform.uname()
        return PlatformInfoDTO(
            system=uname.system,
            release=uname.release,
            machine=uname.machine,
            architecture=platform.architecture()[0],
            manufacturer=_get_manufacturer(),
            model=_get_model(),
            serial=_get_serial(),
        )
