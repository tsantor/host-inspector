from typing import Protocol


class MachineIdProbePort(Protocol):
    def machine_id(self) -> str:
        """Return raw machine identifier string."""
