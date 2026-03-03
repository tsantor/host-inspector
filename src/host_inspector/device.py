from .display import get_display_info
from .gpu import get_gpu_info
from .network import get_network_info
from .os import get_os_info
from .platform import get_platform_info


def get_device_info() -> dict:
    """Return device information."""
    return {
        "os": get_os_info(),
        "platform": get_platform_info(),
        "network": get_network_info(),
        "gpu": get_gpu_info(),
        # "firewall": get_firewall_info(),
        "display": get_display_info(),
    }
