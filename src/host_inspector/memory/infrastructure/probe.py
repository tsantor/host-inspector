import psutil

from host_inspector.memory.application.ports import MemorySnapshot


class PsutilMemoryProbe:
    def snapshot(self) -> MemorySnapshot:
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "used": memory.used,
            "available": memory.available,
            "percent": memory.percent,
        }
