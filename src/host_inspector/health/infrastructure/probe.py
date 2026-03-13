from host_inspector.cpu import get_cpu_info
from host_inspector.date_time import get_datetime_info
from host_inspector.disk import get_disk_info
from host_inspector.memory import get_mem_info
from host_inspector.uptime import get_uptime_info


class HealthProbe:
    def cpu_info(self) -> dict:
        return get_cpu_info()

    def mem_info(self) -> dict:
        return get_mem_info()

    def disk_info(self) -> dict:
        return get_disk_info()

    def uptime_info(self) -> dict:
        return get_uptime_info()

    def datetime_info(self) -> dict:
        return get_datetime_info()
