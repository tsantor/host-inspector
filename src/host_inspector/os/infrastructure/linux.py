import re
import shlex
import subprocess
from functools import cache

from host_inspector.os.application.dtos import OSDataDTO


def _search_pattern(pattern: str, result: str) -> str | None:
    if matches := re.search(pattern, result):
        return matches[1].strip()
    return None


@cache
def _collect_linux_os_data() -> OSDataDTO:
    """Parse /etc/os-release file for name, version, and edition."""
    cmd = "cat /etc/os-release"
    proc = subprocess.run(  # noqa: S603
        shlex.split(cmd),
        check=True,
        capture_output=True,
        text=True,
    )
    result = proc.stdout.strip().replace("PRETTY_NAME", "PRETTY")

    return OSDataDTO(
        platform="linux",
        name=_search_pattern(r'NAME="(.+)"', result),
        version=_search_pattern(r'VERSION_ID="(.+)"', result),
        edition=_search_pattern(r"VERSION_CODENAME=(.+)", result),
        build="--",
    )


class LinuxOSCollector:
    def collect(self) -> OSDataDTO:
        return _collect_linux_os_data()
