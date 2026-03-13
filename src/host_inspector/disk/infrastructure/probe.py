import psutil

from host_inspector.disk.application.ports import DiskSnapshot


class PsutilDiskProbe:
    def snapshot(self, path: str = "/") -> DiskSnapshot:
        disk = psutil.disk_usage(path)
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent,
        }
