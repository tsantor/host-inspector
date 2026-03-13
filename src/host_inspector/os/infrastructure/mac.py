import re
import shlex
import subprocess
from functools import cache

from host_inspector.os.application.ports import OSData


def _search_pattern(pattern: str, result: str) -> str | None:
    if matches := re.search(pattern, result):
        return matches[1].strip()
    return None


@cache
def _collect_mac_os_data() -> OSData:
    cmd = "sw_vers"
    proc = subprocess.run(  # noqa: S603
        shlex.split(cmd),
        check=True,
        capture_output=True,
        text=True,
    )
    result = proc.stdout.strip()

    name = _search_pattern(r"ProductName:(.+)", result)
    version = _search_pattern(r"ProductVersion:(.+)", result)
    build = _search_pattern(r"BuildVersion:(.+)", result)

    return {
        "platform": "darwin",
        "name": name,
        "version": version,
        "edition": "--",
        "build": build,
    }


class MacOSCollector:
    def collect(self) -> OSData:
        return _collect_mac_os_data()
