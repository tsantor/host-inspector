from host_inspector import get_gpu_info
from host_inspector.gpu.application.dtos import GPUInfoDTO
from host_inspector.gpu.application.dtos import GPUPayloadDTO
from host_inspector.gpu.application.service import GPUService


class StubCollector:
    def __init__(self, payload: dict | list[dict]):
        self.payload = payload

    def gpu_info(self) -> GPUPayloadDTO:
        if isinstance(self.payload, list):
            return GPUPayloadDTO(
                adapters=[GPUInfoDTO(**item) for item in self.payload], as_list=True
            )
        return GPUPayloadDTO(adapters=[GPUInfoDTO(**self.payload)], as_list=False)


def test_get_gpu_info():
    gpu_info = get_gpu_info()
    assert isinstance(gpu_info, dict | list)

    expected_keys = {"model", "vram", "resolution", "refresh_rate"}

    assert isinstance(gpu_info, dict | list)
    if isinstance(gpu_info, dict):
        assert set(gpu_info.keys()) == expected_keys
    elif isinstance(gpu_info, list):
        for item in gpu_info:
            assert isinstance(item, dict)
            assert set(item.keys()) == expected_keys


def test_gpu_service_dict_passthrough():
    payload = {
        "model": "Apple M4 GPU",
        "vram": "8 GB",
        "resolution": "3024 x 1964",
        "refresh_rate": "120.0 Hz",
    }
    service = GPUService(collector=StubCollector(payload=payload))
    assert service.get_gpu_info() == payload


def test_gpu_service_list_passthrough():
    payload = [
        {
            "model": "NVIDIA RTX",
            "vram": "16 GB",
            "resolution": "3840 x 2160",
            "refresh_rate": "144 Hz",
        }
    ]
    service = GPUService(collector=StubCollector(payload=payload))
    assert service.get_gpu_info() == payload
