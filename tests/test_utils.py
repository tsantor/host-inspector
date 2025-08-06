import datetime
from datetime import UTC

import pytest

from host_inspector.utils import datetimeutils
from host_inspector.utils.byteutils import bytes_to_gb
from host_inspector.utils.byteutils import bytes_to_gib
from host_inspector.utils.byteutils import bytes_to_mb
from host_inspector.utils.byteutils import bytes_to_mib
from host_inspector.utils.byteutils import human_readable_bytes


def test_bytes_to_mb():
    assert bytes_to_mb(1_000_000) == 1.0
    assert bytes_to_mb(5_000_000) == 5.0  # noqa: PLR2004
    assert bytes_to_mb(0) == 0.0


def test_bytes_to_mib():
    assert bytes_to_mib(1_048_576) == 1.0
    assert bytes_to_mib(5_242_880) == 5.0  # noqa: PLR2004
    assert bytes_to_mib(0) == 0.0


def test_bytes_to_gb():
    assert bytes_to_gb(1_000_000_000) == 1.0
    assert bytes_to_gb(5_000_000_000) == 5.0  # noqa: PLR2004
    assert bytes_to_gb(0) == 0.0


def test_bytes_to_gib():
    assert bytes_to_gib(1_073_741_824) == 1.0
    assert bytes_to_gib(5_368_709_120) == 5.0  # noqa: PLR2004
    assert bytes_to_gib(0) == 0.0


@pytest.mark.parametrize(
    ("b", "metric", "expected"),
    [
        (0, True, "0 B"),
        (999, True, "999 B"),
        (1000, True, "1.0 KB"),
        (1536, True, "1.54 KB"),
        (1_000_000, True, "1.0 MB"),
        (1_000_000_000, True, "1.0 GB"),
        (1023, False, "1023 B"),
        (1024, False, "1.0 KB"),
        (1536, False, "1.5 KB"),
        (1_048_576, False, "1.0 MB"),
        (1_073_741_824, False, "1.0 GB"),
    ],
)
def test_human_readable_bytes(b, metric, expected):
    assert human_readable_bytes(b, metric) == expected


def test_human_date():
    dt = datetime.datetime(2024, 8, 6, tzinfo=UTC)
    assert datetimeutils.human_date(dt) == "Tuesday, August 06, 2024"


def test_human_time():
    dt = datetime.datetime(2024, 8, 6, 15, 30, tzinfo=UTC)
    assert datetimeutils.human_time(dt) == "03:30 PM"


def test_human_datetime():
    dt = datetime.datetime(2024, 8, 6, 15, 30, tzinfo=UTC)
    assert datetimeutils.human_datetime(dt) == "Tuesday, August 06, 2024 03:30 PM"


def test_human_delta():
    # Example: 3661 seconds = "1 hour, 1 minute"
    result = datetimeutils.human_delta(3661)
    assert "hour" in result or "minute" in result
