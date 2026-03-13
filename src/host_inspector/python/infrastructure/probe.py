import platform
import sys
from pathlib import Path


class SystemPythonProbe:
    def version(self) -> str:
        return platform.python_version()

    def executable_path(self) -> str:
        return str(Path(sys.executable))
