from host_inspector import get_cpu_info
from host_inspector.cpu.application.service import CPUService


class StubMetrics:
    def __init__(self, *, physical: int, logical: int, freq_mhz: float, percent: float):
        self._physical = physical
        self._logical = logical
        self._freq_mhz = freq_mhz
        self._percent = percent

    def physical_count(self) -> int:
        return self._physical

    def logical_count(self) -> int:
        return self._logical

    def max_frequency_mhz(self) -> float:
        return self._freq_mhz

    def usage_percent(self) -> float:
        return self._percent


class StubPlatform:
    def __init__(self, *, processor: str, temperature: dict):
        self._processor = processor
        self._temperature = temperature

    def processor_name(self) -> str:
        return self._processor

    def temperature_info(self) -> dict:
        return self._temperature


def test_get_cpu_info():
    cpu_info = get_cpu_info()

    assert isinstance(cpu_info, dict)
    assert set(cpu_info.keys()) == {
        "count",
        "logical",
        "percent",
        "percent_str",
        "processor",
        "frequency",
        "frequency_str",
        "temperature",
    }

    # If you want to check that the values are not None
    for key, value in cpu_info.items():
        assert value is not None, f'Key "{key}" is None.'


def test_cpu_service_get_cpu_info_formats_output():
    service = CPUService(
        metrics=StubMetrics(physical=8, logical=16, freq_mhz=3200.0, percent=12.5),
        platform=StubPlatform(
            processor="Apple M4 Pro",
            temperature={"celsius": 51.0, "fahrenheit": 123.8},
        ),
    )

    assert service.get_cpu_info() == {
        "count": 8,
        "logical": 16,
        "percent": 12.5,
        "percent_str": "12.5%",
        "processor": "Apple M4 Pro",
        "frequency": 3.2,
        "frequency_str": "3.2 GHz",
        "temperature": {"celsius": 51.0, "fahrenheit": 123.8},
    }


def test_cpu_service_mhz_to_ghz():
    service = CPUService(
        metrics=StubMetrics(physical=1, logical=1, freq_mhz=1000.0, percent=0.0),
        platform=StubPlatform(processor="Test CPU", temperature={}),
    )

    expected_ghz = 2.8
    assert service.mhz_to_ghz(2800.0) == expected_ghz
