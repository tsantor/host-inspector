from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkSnapshotDTO:
    hostname: str
    ip_address: str
    node_value: int
    interface: str
    mac_address: str | None
    ipv6_address: str | None
