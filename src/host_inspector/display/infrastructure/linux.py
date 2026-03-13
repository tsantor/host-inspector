class LinuxDisplayCollector:
    def display_info(self) -> list[dict]:
        return [
            {
                "name": "--",
                "display_id": 1,
                "resolution_actual": "--",
                "resolution": "--",
                "refresh_rate": "--",
            }
        ]
