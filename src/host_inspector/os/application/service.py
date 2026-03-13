from dataclasses import dataclass

from host_inspector.os.domain import get_macos_edition

from .ports import OSCollector


@dataclass(frozen=True)
class OSService:
    collector: OSCollector

    def get_os_info(self) -> dict:
        """Get OS info using the configured collector."""
        data = self.collector.collect()

        info = {
            "name": data.name,
            "version": data.version,
            "edition": data.edition,
            "build": data.build,
        }

        if data.platform == "darwin":
            info["edition"] = get_macos_edition(data.version)

        display_version = data.display_version
        if display_version is not None:
            info["display_version"] = display_version

        return info
