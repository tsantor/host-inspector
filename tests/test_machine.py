from host_inspector.machine import get_machine_id
from host_inspector.machine.application.service import MachineService
from host_inspector.machine.domain import normalize_machine_id


def test_get_machine_id():
    if machine_id := get_machine_id():
        assert len(get_machine_id()) == 36  # noqa: PLR2004
    else:
        assert machine_id is None


def test_normalize_machine_id():
    raw = "00112233-4455-6677-8899-aabbccddeeff"
    assert normalize_machine_id(raw) == raw


class StubProbe:
    def machine_id(self) -> str:
        return "00112233-4455-6677-8899-aabbccddeeff"


def test_machine_service():
    service = MachineService(probe=StubProbe())
    assert service.get_machine_id() == "00112233-4455-6677-8899-aabbccddeeff"
