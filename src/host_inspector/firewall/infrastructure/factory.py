import importlib
import sys

from host_inspector.firewall.application.service import FirewallService


def build_firewall_service() -> FirewallService:
    if sys.platform == "darwin":
        module_name = "host_inspector.firewall.infrastructure.mac"
        class_name = "MacFirewallCollector"
    elif sys.platform == "win32":
        module_name = "host_inspector.firewall.infrastructure.windows"
        class_name = "WindowsFirewallCollector"
    elif sys.platform == "linux":
        module_name = "host_inspector.firewall.infrastructure.linux"
        class_name = "LinuxFirewallCollector"
    else:
        msg = f"Unsupported platform: {sys.platform}"
        raise ImportError(msg)

    collector_module = importlib.import_module(module_name)
    collector_cls = getattr(collector_module, class_name)
    return FirewallService(collector=collector_cls())
