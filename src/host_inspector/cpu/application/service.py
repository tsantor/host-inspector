from dataclasses import dataclass

from .ports import CPUMetricsPort
from .ports import CPUPlatformPort


@dataclass(frozen=True)
class CPUService:
    metrics: CPUMetricsPort
    platform: CPUPlatformPort

    @staticmethod
    def mhz_to_ghz(mhz: float) -> float:
        """Convert MHz to GHz."""
        return round(mhz / 1000, 2)

    def cpu_physical_count(self) -> int:
        """Get the number of physical CPUs on the system."""
        return self.metrics.physical_count()

    def cpu_logical_count(self) -> int:
        """Get the number of logical CPUs on the system."""
        return self.metrics.logical_count()

    def cpu_freq(self) -> float:
        """Get the maximum frequency of the CPU in GHz."""
        return self.mhz_to_ghz(self.metrics.max_frequency_mhz())

    def cpu_percent(self) -> float:
        """Get the current CPU usage percentage."""
        return self.metrics.usage_percent()

    def get_processor_name(self) -> str:
        """Safely get processor name."""
        return self.platform.processor_name()

    def get_temp_info(self) -> dict:
        """Return current temperature information."""
        return self.platform.temperature_info()

    def get_cpu_info(self) -> dict:
        """Return CPU info as a dict."""
        cpu_usage = self.cpu_percent()
        cpu_ghz = self.cpu_freq()
        return {
            "count": self.cpu_physical_count(),
            "logical": self.cpu_logical_count(),
            "percent": cpu_usage,
            "percent_str": f"{cpu_usage}%",
            "processor": self.get_processor_name(),
            "frequency": cpu_ghz,
            "frequency_str": f"{cpu_ghz} GHz",
            "temperature": self.get_temp_info(),
        }
