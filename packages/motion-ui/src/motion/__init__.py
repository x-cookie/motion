"""motion - CLI task management tool"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("motion-ui")
except PackageNotFoundError:
    __version__ = "unknown"
