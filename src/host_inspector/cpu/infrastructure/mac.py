import shlex
import subprocess
from functools import cache

from host_inspector.cpu.application.dtos import TemperatureInfoDTO

from .common import clean_processor_name


@cache
def _get_processor_name() -> str:
    try:
        cmd = "sysctl -n machdep.cpu.brand_string"
        proc = subprocess.run(  # noqa: S603
            shlex.split(cmd),
            check=True,
            capture_output=True,
            text=True,
        )
        return clean_processor_name(proc.stdout.strip())
    except subprocess.CalledProcessError:  # pragma: no cover
        return "--"


class MacCPUPlatform:
    def processor_name(self) -> str:
        return _get_processor_name()

    def temperature_info(self) -> TemperatureInfoDTO:
        # TODO: Implement temperature retrieval for MacOS.
        temp_c = 0.0
        temp_f = 0.0
        return TemperatureInfoDTO(
            data={
                "celsius": temp_c,
                "fahrenheit": temp_f,
                "celsius_str": f"{temp_c if temp_c != 0 else '--'} °C",
                "fahrenheit_str": f"{temp_f if temp_f != 0 else '--'} °F",
            }
        )
