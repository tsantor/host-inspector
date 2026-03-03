from .cpu import get_cpu_info
from .date_time import get_datetime_info
from .disk import get_disk_info
from .memory import get_mem_info
from .uptime import get_uptime_info


def get_health_info() -> dict:
    """Return overall health information. CPU, Mem, Disk, Uptime."""
    return {
        "cpu": get_cpu_info(),
        "mem": get_mem_info(),
        "disk": get_disk_info(),
        "uptime": get_uptime_info(),
        "local_datetime": get_datetime_info(),
    }
