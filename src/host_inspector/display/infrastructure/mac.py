import json
import subprocess
from typing import Any

from host_inspector.display.domain import parse_macos_display_output


class MacDisplayCollector:
    def display_info(self) -> list[dict[str, Any]]:
        try:
            command = ["system_profiler", "SPDisplaysDataType", "-json"]
            process = subprocess.run(  # noqa: S603
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            return parse_macos_display_output(json.loads(process.stdout.strip()))
        except subprocess.CalledProcessError:  # pragma: no cover
            return []
