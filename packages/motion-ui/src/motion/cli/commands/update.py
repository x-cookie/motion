"""Update command - Update task properties."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import click

from motion.cli.error_handler import handle_task_errors

if TYPE_CHECKING:
    from datetime import datetime

    from motion.cli.context import CliContext
from motion_core.domain.entities.task import TaskStatus


# Sentinel value for "clear" - distinct from None (not provided)
CLEAR_SENTINEL = "CLEAR"


class ClearableDateTimeType(click.ParamType):
    """DateTime type that treats empty string as 'clear' command.

    Requires full datetime input (YYYY-MM-DD HH:MM:SS) for accurate timestamps.
    """

    name = "DATETIME"

    def __init__(self) -> None:
        """Initialize with click.DateTime for parsing."""
        self._inner = click.DateTime()

    def convert(
        self, value: Any, param: Any, ctx: click.Context | None
    ) -> datetime | str | None:
        """Convert value, treating empty string as clear sentinel."""
        if value is None:
            return None
        if value == "" or value == CLEAR_SENTINEL:
            return CLEAR_SENTINEL
        return cast("datetime", self._inner.convert(value, param, ctx))


def _validate_name(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    """Validate that name is not empty or whitespace-only."""
    if value is not None and not value.strip():
        raise click.BadParameter("cannot be empty or whitespace-only")
    return value


@click.command(
    name="update",
    help="Update multiple task properties at once.",
)
@click.argument("task_id", type=int)
@click.option(
    "--name",
    type=str,
    default=None,
    callback=_validate_name,
    help="New task name",
)
@click.option(
    "--priority",
    type=int,
    default=None,
    help="New priority",
)
@click.option(
    "--status",
    type=click.Choice([e.value for e in TaskStatus]),
    default=None,
    help="New status",
)
@click.option(
    "--planned-start",
    type=ClearableDateTimeType(),
    default=None,
    help='Planned start (format: YYYY-MM-DD HH:MM:SS, empty string "" to clear)',
)
@click.option(
    "--planned-end",
    type=ClearableDateTimeType(),
    default=None,
    help='Planned end (format: YYYY-MM-DD HH:MM:SS, empty string "" to clear)',
)
@click.option(
    "--deadline",
    type=ClearableDateTimeType(),
    default=None,
    help='Deadline (format: YYYY-MM-DD HH:MM:SS, empty string "" to clear)',
)
@click.option(
    "--estimated-duration",
    type=float,
    default=None,
    help="Estimated duration in hours (e.g., 2.5)",
)
@click.pass_context
@handle_task_errors("updating task")
def update_command(
    ctx: click.Context,
    task_id: int,
    name: str | None,
    priority: int | None,
    status: str | None,
    planned_start: datetime | str | None,
    planned_end: datetime | str | None,
    deadline: datetime | str | None,
    estimated_duration: float | None,
) -> None:
    """Update multiple task properties at once.

    Usage:
        motion update <TASK_ID> [OPTIONS]

    Examples:
        # Update multiple fields at once
        motion update 5 --priority 3 --deadline 2025-10-15

        # Rename a task
        motion update 10 --name "New task name"

        # Update deadline and estimated duration
        motion update 7 --deadline 2025-10-20 --estimated-duration 4.0

        # Clear planned dates (reset optimization)
        motion update 5 --planned-start "" --planned-end ""
    """
    ctx_obj: CliContext = ctx.obj
    console_writer = ctx_obj.console_writer

    # Convert status string to Enum if provided
    status_enum = TaskStatus(status) if status else None

    # Determine clear flags
    clear_planned_start = planned_start == CLEAR_SENTINEL
    clear_planned_end = planned_end == CLEAR_SENTINEL
    clear_deadline = deadline == CLEAR_SENTINEL

    # Convert sentinels to None for actual values
    final_planned_start: datetime | None = (
        None if clear_planned_start or planned_start is None else planned_start  # type: ignore[assignment]
    )
    final_planned_end: datetime | None = (
        None if clear_planned_end or planned_end is None else planned_end  # type: ignore[assignment]
    )
    final_deadline: datetime | None = (
        None if clear_deadline or deadline is None else deadline  # type: ignore[assignment]
    )

    # Update task via API client
    result = ctx_obj.api_client.update_task(
        task_id=task_id,
        name=name,
        priority=priority,
        status=status_enum,
        planned_start=final_planned_start,
        planned_end=final_planned_end,
        deadline=final_deadline,
        estimated_duration=estimated_duration,
    )

    if not result.updated_fields:
        console_writer.warning(
            "No fields to update. Use --name, --priority, --status, --planned-start, --planned-end, --deadline, or --estimated-duration"
        )
        return

    # Print updates
    console_writer.task_fields_updated(result.task, result.updated_fields)
