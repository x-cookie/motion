"""Infrastructure layer for motion-ui.

This module provides CLI-specific infrastructure components.
API client and WebSocket client are provided by the motion_client package.
"""

from motion.infrastructure.cli_config_manager import CliConfig, load_cli_config

__all__ = [
    "CliConfig",
    "load_cli_config",
]
