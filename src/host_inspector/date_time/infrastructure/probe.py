import time
from datetime import datetime


class SystemDateTimeProbe:
    def now(self) -> datetime:
        return datetime.now().astimezone()

    def is_dst(self) -> bool:
        return time.localtime().tm_isdst == 1
