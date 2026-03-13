from dataclasses import dataclass

from .ports import GPUCollectorPort


@dataclass(frozen=True)
class GPUService:
    collector: GPUCollectorPort

    def get_gpu_info(self) -> dict | list[dict]:
        """Return GPU info payload from the collector."""
        payload = self.collector.gpu_info()
        adapters = [adapter.to_dict() for adapter in payload.adapters]
        if payload.as_list:
            return adapters
        return adapters[0] if adapters else {}
