def get_display_info() -> list[dict]:
    # TODO: Implement Windows display detection
    return [
        {
            "name": "Display",
            "display_id": 1,
            "resolution_actual": {"width": 1920, "height": 1080},
            "pixel_resolution": {"width": 1920, "height": 1080},
            "refresh_hz": 60,
        }
    ]
