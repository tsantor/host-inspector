from host_inspector.disk.application.service import DiskService

from .probe import PsutilDiskProbe


def build_disk_service() -> DiskService:
    return DiskService(probe=PsutilDiskProbe())
