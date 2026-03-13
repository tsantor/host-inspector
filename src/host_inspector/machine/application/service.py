from dataclasses import dataclass

from host_inspector.machine.domain import normalize_machine_id

from .ports import MachineIdProbePort


@dataclass(frozen=True)
class MachineService:
    probe: MachineIdProbePort

    def get_machine_id(self) -> str:
        return normalize_machine_id(self.probe.machine_id())
