"""Command providers for sort functionality."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, ClassVar

from motion.tui.palette.providers.base import (
    BaseListProvider,
    SimpleSingleCommandProvider,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from motion.tui.app import motionTUI


class SortCommandProvider(SimpleSingleCommandProvider):
    """Command provider for the main 'Sort' command."""

    COMMAND_NAME = "Sort"
    COMMAND_HELP = "Change sort order for tasks and Gantt chart"
    COMMAND_CALLBACK_NAME = "search_sort"


class SortOptionsProvider(BaseListProvider):
    """Command provider for sort options (second stage)."""

    # Sort options: (sort_key, option_name, description)
    SORT_OPTIONS: ClassVar = [
        ("deadline", "Deadline", "Urgency-based (earlier deadline first)"),
        ("planned_start", "Planned Start", "Timeline-based (chronological order)"),
        ("priority", "Priority", "Importance-based (higher priority first)"),
        ("estimated_duration", "Duration", "Effort-based (shorter tasks first)"),
        ("id", "ID", "Creation order (lower ID first)"),
        ("name", "Name", "Alphabetically (A-Z)"),
        (
            "status",
            "Status",
            "State-based (CANCELED → COMPLETED → IN_PROGRESS → PENDING)",
        ),
    ]

    def get_options(self, app: motionTUI) -> list[tuple[str, Callable[[], None], str]]:
        """Return sort options with callbacks.

        Args:
            app: motionTUI application instance

        Returns:
            List of (option_name, callback, description) tuples
        """
        return [
            (option_name, partial(app.set_sort_order, sort_key), description)
            for sort_key, option_name, description in self.SORT_OPTIONS
        ]
