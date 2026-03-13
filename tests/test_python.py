from host_inspector.python import get_python_info
from host_inspector.python.application.service import PythonService


class StubProbe:
    def version(self) -> str:
        return "3.13.1"

    def executable_path(self) -> str:
        return "/usr/bin/python3"


def test_get_python_info_shape():
    info = get_python_info()
    assert isinstance(info, dict)
    assert set(info.keys()) == {"version", "path"}
    assert isinstance(info["version"], str)
    assert isinstance(info["path"], str)


def test_python_service_output():
    service = PythonService(probe=StubProbe())
    assert service.get_python_info() == {
        "version": "3.13.1",
        "path": "/usr/bin/python3",
    }
