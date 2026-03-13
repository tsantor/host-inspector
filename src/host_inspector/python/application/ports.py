from typing import Protocol


class PythonInfoProbePort(Protocol):
    def version(self) -> str:
        """Return Python version string."""

    def executable_path(self) -> str:
        """Return Python executable path."""
