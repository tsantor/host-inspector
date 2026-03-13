import psutil

from host_inspector.disk.application.dtos import DiskSnapshotDTO


class PsutilDiskProbe:
    def snapshot(self, path: str = "/") -> DiskSnapshotDTO:
        disk = psutil.disk_usage(path)
        return DiskSnapshotDTO(
            total=disk.total,
            used=disk.used,
            free=disk.free,
            percent=disk.percent,
        )
