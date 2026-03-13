from typing import Protocol

from .dtos import TemperatureInfoDTO


class CPUMetricsPort(Protocol):
    def physical_count(self) -> int:
        """Return the number of physical CPUs."""

    def logical_count(self) -> int:
        """Return the number of logical CPUs."""

    def max_frequency_mhz(self) -> float:
        """Return max CPU frequency in MHz."""

    def usage_percent(self) -> float:
        """Return current CPU usage percent."""


class CPUPlatformPort(Protocol):
    def processor_name(self) -> str:
        """Return normalized processor model name."""

    def temperature_info(self) -> TemperatureInfoDTO:
        """Return temperature information."""
