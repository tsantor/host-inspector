import machineid


class MachineIdProbe:
    def machine_id(self) -> str:
        return machineid.id()
