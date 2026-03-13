import math

import humanize

from host_inspector.utils.byteutils import bytes_to_gb


def mem_physical(total_bytes: int) -> int:
    """Return physical memory in GB rounded up."""
    return math.ceil(bytes_to_gb(total_bytes))


def mem_physical_str(total_bytes: int) -> str:
    """Return physical memory as a human-readable string."""
    return f"{mem_physical(total_bytes)} GB"


def mem_used(used_bytes: int) -> float:
    """Return memory used in GB."""
    return bytes_to_gb(used_bytes)


def mem_used_str(used_bytes: int) -> str:
    """Return memory used as a human-readable string."""
    return humanize.naturalsize(used_bytes, binary=False)


def mem_avail(available_bytes: int) -> float:
    """Return memory available in GB."""
    return bytes_to_gb(available_bytes)


def mem_avail_str(available_bytes: int) -> str:
    """Return memory available as a human-readable string."""
    return humanize.naturalsize(available_bytes, binary=False)


def mem_percent(percent: float) -> float:
    """Return memory usage percentage."""
    return percent
