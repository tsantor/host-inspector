import contextlib
import platform
import sys
import winreg
from functools import cache

from host_inspector.os.application.dtos import OSDataDTO


@cache
def _get_windows_version() -> str | int:
    # Need this since Windows major.minor reports as 10.x for Windows 11.
    if int(platform.version().split(".")[2]) >= 22000:  # noqa: PLR2004
        return 11
    return platform.win32_ver()[0]


@cache
def _get_windows_display_version() -> str:
    with contextlib.suppress(FileNotFoundError):
        key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as chnd:
            return winreg.QueryValueEx(chnd, "DisplayVersion")[0]
    return "--"  # pragma: no cover


@cache
def _collect_windows_os_data() -> OSDataDTO:
    return OSDataDTO(
        platform="win32",
        name=platform.system(),
        version=_get_windows_version(),
        edition=platform.win32_edition(),
        build=sys.getwindowsversion().build,
        display_version=_get_windows_display_version(),
    )


class WindowsOSCollector:
    def collect(self) -> OSDataDTO:
        return _collect_windows_os_data()
