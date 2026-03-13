import re
import subprocess
from functools import cache

import psutil

from host_inspector.cpu.application.dtos import TemperatureInfoDTO

from .common import clean_processor_name


@cache
def _get_processor_name() -> str:
    """Safely get processor name."""
    try:
        proc = subprocess.run(
            ["lscpu"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        )
        all_info = proc.stdout.strip()
        for line in all_info.split("\n"):
            if "Model name:" in line:
                return clean_processor_name(
                    re.sub(r"Model name:\s+", "", line, count=1)
                )
        return "--"
    except subprocess.CalledProcessError:  # pragma: no cover
        return "--"


def _get_temp_info() -> TemperatureInfoDTO:
    """Get CPU temperature with psutil, then vcgencmd fallback."""
    try:
        temps = psutil.sensors_temperatures()
        if temps.get("coretemp"):
            temp = temps["coretemp"][0].current
            temp_c = round(temp, 1)
            temp_f = round(temp_c * 9 / 5 + 32, 1)
            return TemperatureInfoDTO(
                data={
                    "celsius": temp_c,
                    "fahrenheit": temp_f,
                    "celsius_str": f"{temp_c} °C",
                    "fahrenheit_str": f"{temp_f} °F",
                }
            )
    except (KeyError, AttributeError):
        pass

    try:
        result = subprocess.run(
            ["/usr/bin/vcgencmd", "measure_temp"],
            capture_output=True,
            text=True,
            check=True,
        )
        temp_c = round(float(result.stdout.split("=")[1].split("'")[0]), 1)
        temp_f = round(temp_c * 9 / 5 + 32, 1)
        return TemperatureInfoDTO(
            data={
                "celsius": temp_c,
                "fahrenheit": temp_f,
                "celsius_str": f"{temp_c} °C",
                "fahrenheit_str": f"{temp_f} °F",
            }
        )
    except (FileNotFoundError, subprocess.CalledProcessError, IndexError, ValueError):
        pass

    return TemperatureInfoDTO(data={})


class LinuxCPUPlatform:
    def processor_name(self) -> str:
        return _get_processor_name()

    def temperature_info(self) -> TemperatureInfoDTO:
        return _get_temp_info()
