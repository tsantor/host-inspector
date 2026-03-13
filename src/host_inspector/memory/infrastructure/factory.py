from host_inspector.memory.application.service import MemoryService

from .probe import PsutilMemoryProbe


def build_memory_service() -> MemoryService:
    return MemoryService(probe=PsutilMemoryProbe())
