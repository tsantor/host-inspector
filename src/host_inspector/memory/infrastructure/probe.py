import psutil

from host_inspector.memory.application.dtos import MemorySnapshotDTO


class PsutilMemoryProbe:
    def snapshot(self) -> MemorySnapshotDTO:
        memory = psutil.virtual_memory()
        return MemorySnapshotDTO(
            total=memory.total,
            used=memory.used,
            available=memory.available,
            percent=memory.percent,
        )
