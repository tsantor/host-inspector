from functools import cache

from .infrastructure import build_gpu_service


@cache
def _get_gpu_service():
    return build_gpu_service()


def get_gpu_info() -> dict | list[dict]:
    return _get_gpu_service().get_gpu_info()
