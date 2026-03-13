from host_inspector.machine.application.service import MachineService

from .probe import MachineIdProbe


def build_machine_service() -> MachineService:
    return MachineService(probe=MachineIdProbe())
