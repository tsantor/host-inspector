import re
from typing import Any

RESOLUTION_PATTERN = re.compile(
    r"^\s*(\d+)\s*x\s*(\d+)(?:\s*@\s*([\d.]+)\s*Hz)?\s*$",
    re.I,
)


def parse_resolution(
    resolution: str | None,
) -> tuple[int | None, int | None, float | None]:
    """Parse display resolution strings like '3440 x 1440 @ 60.00Hz'."""
    if not resolution or not isinstance(resolution, str):
        return None, None, None
    match = RESOLUTION_PATTERN.search(resolution)
    if not match:
        return None, None, None
    width = int(match.group(1))
    height = int(match.group(2))
    refresh_hz = float(match.group(3)) if match.group(3) else None
    return width, height, refresh_hz


def to_int_maybe(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except ValueError:  # pragma: no cover
        return None


def parse_macos_display_output(sp_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse `system_profiler SPDisplaysDataType -json` output."""
    output = []
    for gpu in sp_json.get("SPDisplaysDataType", []):
        for display in gpu.get("spdisplays_ndrvs", []) or []:
            name = display.get("_name") or "Display"

            resolution_str = (
                display.get("_spdisplays_resolution")
                or display.get("spdisplays_resolution")
                or display.get("_spdisplays_pixels")
            )
            actual_width, actual_height, refresh_hz = parse_resolution(resolution_str)

            pixel_resolution_str = display.get("_spdisplays_pixels")
            pixel_width, pixel_height, _ = parse_resolution(pixel_resolution_str)
            display_id = to_int_maybe(display.get("_spdisplays_displayID"))

            output.append(
                {
                    "name": name,
                    "display_id": display_id,
                    "resolution_actual": (
                        f"{actual_width} x {actual_height}"
                        if actual_width and actual_height
                        else "--"
                    ),
                    "resolution": (
                        f"{pixel_width} x {pixel_height}"
                        if pixel_width and pixel_height
                        else "--"
                    ),
                    "refresh_rate": f"{refresh_hz} Hz" if refresh_hz else "--",
                }
            )
    return output
