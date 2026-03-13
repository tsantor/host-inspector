from host_inspector.cpu import get_cpu_info
from host_inspector.date_time import get_datetime_info
from host_inspector.disk import get_disk_info
from host_inspector.health.application.dtos import HealthInputDTO
from host_inspector.memory import get_mem_info
from host_inspector.uptime import get_uptime_info


class HealthProbe:
    def snapshot(self) -> HealthInputDTO:
        return HealthInputDTO(
            cpu=get_cpu_info(),
            mem=get_mem_info(),
            disk=get_disk_info(),
            uptime=get_uptime_info(),
            local_datetime=get_datetime_info(),
        )
