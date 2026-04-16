"""Table command - Display tasks in flat table format."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from motion.cli.commands.common_options import (
    date_range_options,
    filter_options,
    sort_options,
)
from motion.cli.commands.table_helpers import render_table
from motion.cli.error_handler import handle_command_errors

if TYPE_CHECKING:
    from datetime import datetime

    from motion.cli.context import CliContext
from motion.shared.click_types.field_list import FieldList


@click.command(
    name="table",
    help="Display tasks in flat table format (shows non-archived tasks by default).",
)
@click.option(
    "--fields",
    "-f",
    type=FieldList(),  # No validation - renderer handles unknown fields gracefully
    help="Comma-separated list of fields to display (e.g., 'id,name,note,priority,status'). "
    "Available: id, name, note, priority, status, depends_on, planned_start, planned_end, "
    "actual_start, actual_end, deadline, duration, created_at, tags",
)
@click.option(
    "--tag",
    "-t",
    multiple=True,
    type=str,
    help="Filter by tags (can be specified multiple times, uses OR logic)",
)
@date_range_options()
@sort_options(default_sort="id")
@filter_options()
@click.pass_context
@handle_command_errors("displaying tasks")
def table_command(
    ctx: click.Context,
    include_archived: bool,
    status: str | None,
    sort: str,
    reverse: bool,
    fields: list[str] | None,
    tag: tuple[str, ...],
    start_date: datetime | None,
    end_date: datetime | None,
) -> None:
    """Display tasks as a flat table.

    By default, shows non-archived tasks (all statuses except archived).
    Use -a/--all to show all tasks including archived.
    Use --status to filter by specific status.
    Use --tag to filter by tags (OR logic when multiple tags specified).
    Use --start-date and --end-date to filter by date range.

    Examples:
        motion table                              # Show non-archived tasks
        motion table -a                           # Show all tasks (including archived)
        motion table --status archived            # Show only archived tasks
        motion table --status completed           # Show only completed tasks
        motion table -t work -t urgent            # Tasks with tag "work" OR "urgent"
        motion table -s priority -r               # Sort by priority descending
        motion table --fields id,name,status      # Show specific fields only
        motion table --start-date 2025-10-01      # Tasks with dates >= Oct 1
        motion table --start-date 2025-10-01 --end-date 2025-10-31  # October tasks
    """
    ctx_obj: CliContext = ctx.obj

    # fields is already parsed by FieldList Click type (no validation)
    # Prepare filter parameters (tags use OR logic by default)
    tags = list(tag) if tag else None

    # Get filtered and sorted tasks via API client
    result = ctx_obj.api_client.list_tasks(
        include_archived=include_archived,
        status=status,
        tags=tags,
        start_date=start_date.date() if start_date else None,
        end_date=end_date.date() if end_date else None,
        sort_by=sort,
        reverse=reverse,
    )

    # Render and display
    render_table(ctx_obj, result, fields=fields)
