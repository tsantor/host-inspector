import logging

from .cpu import get_cpu_info
from .date_time import get_datetime_info
from .device import get_device_info
from .disk import get_disk_info
from .display import get_display_info
from .firewall import get_firewall_info
from .gpu import get_gpu_info
from .health import get_health_info
from .memory import get_mem_info
from .network import get_network_info
from .os import get_os_info
from .platform import get_platform_info
from .uptime import get_uptime_info

# Basic logger setup; users of this package can configure logging as needed
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

__version__ = "0.2.4"

__all__ = [
    "get_cpu_info",
    "get_datetime_info",
    "get_device_info",
    "get_disk_info",
    "get_display_info",
    "get_firewall_info",
    "get_gpu_info",
    "get_health_info",
    "get_mem_info",
    "get_network_info",
    "get_os_info",
    "get_platform_info",
    "get_uptime_info",
]
