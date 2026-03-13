from dataclasses import dataclass

from .ports import GPUCollectorPort


@dataclass(frozen=True)
class GPUService:
    collector: GPUCollectorPort

    def get_gpu_info(self) -> dict | list[dict]:
        """Return GPU info payload from the collector."""
        return self.collector.gpu_info()
