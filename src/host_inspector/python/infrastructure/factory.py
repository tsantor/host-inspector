from host_inspector.python.application.service import PythonService

from .probe import SystemPythonProbe


def build_python_service() -> PythonService:
    return PythonService(probe=SystemPythonProbe())
