import json
import subprocess
from typing import Any

from host_inspector.display.application.dtos import DisplayCollectionDTO
from host_inspector.display.application.dtos import DisplayInfoDTO
from host_inspector.display.domain import parse_macos_display_output


class MacDisplayCollector:
    def display_info(self) -> DisplayCollectionDTO:
        try:
            command = ["system_profiler", "SPDisplaysDataType", "-json"]
            process = subprocess.run(  # noqa: S603
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            parsed: list[dict[str, Any]] = parse_macos_display_output(
                json.loads(process.stdout.strip())
            )
            return DisplayCollectionDTO(
                items=[
                    DisplayInfoDTO(
                        name=str(item["name"]),
                        display_id=item["display_id"],
                        resolution_actual=str(item["resolution_actual"]),
                        resolution=str(item["resolution"]),
                        refresh_rate=str(item["refresh_rate"]),
                    )
                    for item in parsed
                ]
            )
        except subprocess.CalledProcessError:  # pragma: no cover
            return DisplayCollectionDTO(items=[])
