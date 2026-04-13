"""Command provider for help functionality."""

from __future__ import annotations

from motion.tui.palette.providers.base import SimpleSingleCommandProvider


class HelpCommandProvider(SimpleSingleCommandProvider):
    """Command provider for help command."""

    COMMAND_NAME = "Help"
    COMMAND_HELP = "Show keybindings and usage instructions"
    COMMAND_CALLBACK_NAME = "search_help"
