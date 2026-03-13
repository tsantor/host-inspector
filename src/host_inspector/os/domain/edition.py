from functools import cache

MACOS_EDITIONS = {
    # OS X
    "10.0": "Cheetah",
    "10.1": "Puma",
    "10.2": "Jaguar",
    "10.3": "Panther",
    "10.4": "Tiger",
    "10.5": "Leopard",
    "10.6": "Snow Leopard",
    "10.7": "Lion",
    "10.8": "Mountain Lion",
    "10.9": "Mavericks",
    "10.10": "Yosemite",
    "10.11": "El Capitan",
    "10.12": "Sierra",
    "10.13": "High Sierra",
    "10.14": "Mojave",
    "10.15": "Catalina",
    # macOS
    "11": "Big Sur",
    "12": "Monterey",
    "13": "Ventura",
    "14": "Sonoma",
    "15": "Sequoia",
    "26": "Tahoe",
}


@cache
def get_macos_edition(version) -> str:
    """Resolve the macOS codename from a version string."""
    if not isinstance(version, str):
        return "--"

    if version in MACOS_EDITIONS:
        return MACOS_EDITIONS[version]

    major = version.split(".")[0]
    if major in MACOS_EDITIONS:
        return MACOS_EDITIONS[major]

    try:
        major_num = int(major)
    except ValueError:
        return "--"

    if major_num >= 11:  # noqa: PLR2004
        return "macOS"

    return "--"
