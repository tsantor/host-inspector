from functools import cache

from .infrastructure import build_cpu_service


def mhz_to_ghz(m) -> float:
    """Convert MHz to GHz."""
    return _get_cpu_service().mhz_to_ghz(m)


@cache
def cpu_physical_count() -> int:
    """Get the number of physical CPUs on the system."""
    return _get_cpu_service().cpu_physical_count()


@cache
def cpu_logical_count() -> int:
    """Get the number of logical CPUs on the system."""
    return _get_cpu_service().cpu_logical_count()


@cache
def cpu_freq() -> float:
    """Get the maximum frequency of the CPU in GHz."""
    return _get_cpu_service().cpu_freq()


def cpu_percent() -> float:
    """Get the current CPU usage percentage."""
    return _get_cpu_service().cpu_percent()


def get_processor_name() -> str:
    """Safely get processor name."""
    return _get_cpu_service().get_processor_name()


def get_temp_info() -> dict:
    """Return current temperature information."""
    return _get_cpu_service().get_temp_info()


@cache
def _get_cpu_service():
    return build_cpu_service()


def get_cpu_info() -> dict:
    """Return CPU info as a dict."""
    return _get_cpu_service().get_cpu_info()
