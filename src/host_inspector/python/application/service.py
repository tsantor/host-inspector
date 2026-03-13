from dataclasses import dataclass

from .ports import PythonInfoProbePort


@dataclass(frozen=True)
class PythonService:
    probe: PythonInfoProbePort

    def get_python_info(self) -> dict:
        return {
            "version": self.probe.version(),
            "path": self.probe.executable_path(),
        }
