from host_inspector import get_mem_info
from host_inspector.memory.application.service import MemoryService
from host_inspector.memory.domain import mem_physical
from host_inspector.memory.domain import mem_physical_str


class StubProbe:
    def snapshot(self):
        gib = 1024 * 1024 * 1024
        return {
            "total": 16 * gib,
            "used": 8 * gib,
            "available": 8 * gib,
            "percent": 50.0,
        }


def test_get_mem_info_shape():
    info = get_mem_info()
    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "physical",
        "physical_str",
        "used",
        "used_str",
        "avail",
        "avail_str",
        "percent",
        "percent_str",
    }


def test_memory_domain_formatting():
    gib = 1024 * 1024 * 1024
    total_bytes = 16 * gib
    expected_physical_gb = 18
    assert mem_physical(total_bytes) == expected_physical_gb
    assert mem_physical_str(total_bytes) == f"{expected_physical_gb} GB"


def test_memory_service_output():
    expected_physical_gb = 18
    expected_percent = 50.0
    service = MemoryService(probe=StubProbe())
    info = service.get_mem_info()
    assert info["physical"] == expected_physical_gb
    assert info["percent"] == expected_percent
    assert info["percent_str"] == f"{expected_percent}%"
