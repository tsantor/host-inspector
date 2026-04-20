from dataclasses import dataclass

from host_inspector.memory.domain import mem_avail
from host_inspector.memory.domain import mem_avail_str
from host_inspector.memory.domain import mem_percent
from host_inspector.memory.domain import mem_physical
from host_inspector.memory.domain import mem_physical_str
from host_inspector.memory.domain import mem_used
from host_inspector.memory.domain import mem_used_str

from .ports import MemoryProbePort


@dataclass(frozen=True)
class MemoryService:
    probe: MemoryProbePort

    def get_mem_info(self) -> dict:
        snapshot = self.probe.snapshot()
        used_bytes = max(snapshot.total - snapshot.available, 0)
        return {
            "physical": mem_physical(snapshot.total),
            "physical_str": mem_physical_str(snapshot.total),
            "used": mem_used(used_bytes),
            "used_str": mem_used_str(used_bytes),
            "avail": mem_avail(snapshot.available),
            "avail_str": mem_avail_str(snapshot.available),
            "percent": mem_percent(snapshot.percent),
            "percent_str": f"{mem_percent(snapshot.percent)}%",
        }
