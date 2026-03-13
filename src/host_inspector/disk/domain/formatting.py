import math

import humanize

from host_inspector.utils.byteutils import bytes_to_gb


def disk_physical(total_bytes: int) -> int:
    """Return physical disk in GB rounded up."""
    return math.ceil(bytes_to_gb(total_bytes))


def disk_physical_str(total_bytes: int) -> str:
    """Return physical disk as a human-readable string."""
    return f"{disk_physical(total_bytes)} GB"


def disk_used(used_bytes: int) -> float:
    """Return disk used in GB."""
    return bytes_to_gb(used_bytes)


def disk_used_str(used_bytes: int) -> str:
    """Return disk used as a human-readable string."""
    return humanize.naturalsize(used_bytes, binary=False)


def disk_avail(free_bytes: int) -> float:
    """Return disk available in GB."""
    return bytes_to_gb(free_bytes)


def disk_avail_str(free_bytes: int) -> str:
    """Return disk available as a human-readable string."""
    return humanize.naturalsize(free_bytes, binary=False)


def disk_percent(percent: float) -> float:
    """Return disk usage percentage."""
    return percent
