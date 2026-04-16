"""Refresh command for TUI."""

from motion.tui.commands.base import TUICommandBase


class RefreshCommand(TUICommandBase):
    """Command to refresh the task list."""

    def execute_impl(self) -> None:
        """Execute the refresh command."""
        self.reload_tasks()
        self.notify_success("Tasks refreshed")
