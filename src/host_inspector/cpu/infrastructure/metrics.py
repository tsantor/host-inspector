import psutil


class PsutilCPUMetrics:
    def physical_count(self) -> int:
        return psutil.cpu_count(logical=False)

    def logical_count(self) -> int:
        return psutil.cpu_count()

    def max_frequency_mhz(self) -> float:
        return psutil.cpu_freq().max

    def usage_percent(self) -> float:
        return psutil.cpu_percent()
