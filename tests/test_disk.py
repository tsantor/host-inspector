from host_inspector import get_disk_info
from host_inspector.disk.application.dtos import DiskSnapshotDTO
from host_inspector.disk.application.service import DiskService
from host_inspector.disk.domain import disk_physical
from host_inspector.disk.domain import disk_physical_str


class StubProbe:
    def snapshot(self, path: str = "/"):
        del path
        gib = 1024 * 1024 * 1024
        return DiskSnapshotDTO(
            total=16 * gib,
            used=8 * gib,
            free=8 * gib,
            percent=50.0,
        )


def test_get_disk_info_shape():
    info = get_disk_info()
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


def test_disk_domain_formatting():
    gib = 1024 * 1024 * 1024
    total_bytes = 16 * gib
    expected_physical_gb = 18
    assert disk_physical(total_bytes) == expected_physical_gb
    assert disk_physical_str(total_bytes) == f"{expected_physical_gb} GB"


def test_disk_service_output():
    expected_physical_gb = 18
    expected_percent = 50.0
    service = DiskService(probe=StubProbe())
    info = service.get_disk_info()
    assert info["physical"] == expected_physical_gb
    assert info["percent"] == expected_percent
    assert info["percent_str"] == f"{expected_percent}%"
