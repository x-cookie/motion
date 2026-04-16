"""XDG Base Directory utilities for motion.

Implements the XDG Base Directory Specification:
https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""

import os
from pathlib import Path

from motion_core.shared.constants.file_management import CONFIG_FILE_NAME


class XDGDirectories:
    """XDG Base Directory helper for motion."""

    APP_NAME = "motion"

    @classmethod
    def get_data_home(cls, create: bool = True) -> Path:
        """Get XDG_DATA_HOME directory for motion.

        Returns:
            Path to $XDG_DATA_HOME/motion (default: ~/.local/share/motion)

        Args:
            create: Create directory if it doesn't exist (default: True)
        """
        base_dir = os.getenv("XDG_DATA_HOME", str(Path("~/.local/share").expanduser()))
        data_dir = Path(base_dir) / cls.APP_NAME

        if create:
            data_dir.mkdir(parents=True, exist_ok=True)

        return data_dir

    @classmethod
    def get_config_home(cls, create: bool = True) -> Path:
        """Get XDG_CONFIG_HOME directory for motion.

        Returns:
            Path to $XDG_CONFIG_HOME/motion (default: ~/.config/motion)

        Args:
            create: Create directory if it doesn't exist (default: True)
        """
        base_dir = os.getenv("XDG_CONFIG_HOME", str(Path("~/.config").expanduser()))
        config_dir = Path(base_dir) / cls.APP_NAME

        if create:
            config_dir.mkdir(parents=True, exist_ok=True)

        return config_dir

    @classmethod
    def get_config_file(cls) -> Path:
        """Get path to config.toml file.

        Returns:
            Path to config.toml in config directory
        """
        return cls.get_config_home() / CONFIG_FILE_NAME
