"""stopuhr: A simple tool for measuring durations in Python."""

import importlib.metadata

from stopuhr.funkuhr import FunkUhr, funkuhr
from stopuhr.stopuhr import StopUhr, stopuhr

try:
    __version__ = importlib.metadata.version("stopuhr")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["FunkUhr", "StopUhr", "funkuhr", "stopuhr"]
