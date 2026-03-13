from dataclasses import dataclass

from host_inspector.disk.domain import disk_avail
from host_inspector.disk.domain import disk_avail_str
from host_inspector.disk.domain import disk_percent
from host_inspector.disk.domain import disk_physical
from host_inspector.disk.domain import disk_physical_str
from host_inspector.disk.domain import disk_used
from host_inspector.disk.domain import disk_used_str

from .ports import DiskProbePort


@dataclass(frozen=True)
class DiskService:
    probe: DiskProbePort

    def get_disk_info(self, path: str = "/") -> dict:
        snapshot = self.probe.snapshot(path=path)
        return {
            "physical": disk_physical(snapshot.total),
            "physical_str": disk_physical_str(snapshot.total),
            "used": disk_used(snapshot.used),
            "used_str": disk_used_str(snapshot.used),
            "avail": disk_avail(snapshot.free),
            "avail_str": disk_avail_str(snapshot.free),
            "percent": disk_percent(snapshot.percent),
            "percent_str": f"{disk_percent(snapshot.percent)}%",
        }
