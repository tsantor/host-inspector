import psutil

SAMPLE_INTERVAL_SECONDS = 0.3


class PsutilCPUMetrics:
    def physical_count(self) -> int:
        return psutil.cpu_count(logical=False)

    def logical_count(self) -> int:
        return psutil.cpu_count()

    def max_frequency_mhz(self) -> float:
        return psutil.cpu_freq().max

    def usage_percent(self) -> float:
        # Sample over a short interval and derive usage from idle time to align
        # more closely with OS-reported "user + system" style CPU usage.
        idle = psutil.cpu_times_percent(interval=SAMPLE_INTERVAL_SECONDS).idle
        usage = 100.0 - idle
        return round(max(0.0, min(100.0, usage)), 1)
