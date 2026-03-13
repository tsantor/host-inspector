from host_inspector.network.application.service import NetworkService

from .probe import SystemNetworkProbe


def build_network_service() -> NetworkService:
    return NetworkService(probe=SystemNetworkProbe())
