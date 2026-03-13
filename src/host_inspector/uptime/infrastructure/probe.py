import time
from datetime import datetime
from functools import cache

import psutil


@cache
def _boot_time() -> datetime:
    return datetime.fromtimestamp(psutil.boot_time()).astimezone()


@cache
def _boot_timestamp() -> float:
    return psutil.boot_time()


class PsutilUptimeProbe:
    def boot_time(self) -> datetime:
        """Return datetime of CPU boot time."""
        return _boot_time()

    def now_timestamp(self) -> float:
        return time.time()

    def boot_timestamp(self) -> float:
        return _boot_timestamp()
