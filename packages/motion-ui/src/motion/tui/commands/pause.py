"""Pause task command for TUI."""

from motion.tui.commands.batch_command_base import BatchCommandBase
from motion_core.application.dto.bulk_operation_output import BulkOperationOutput
from motion_core.application.dto.task_operation_output import TaskOperationOutput


class PauseCommand(BatchCommandBase):
    """Command to pause the selected task(s)."""

    def execute_single(self, task_id: int) -> TaskOperationOutput:
        return self.context.api_client.pause_task(task_id)

    def execute_bulk(self, task_ids: list[int]) -> BulkOperationOutput:
        """Pause tasks via Bulk API."""
        return self.context.api_client.bulk_pause(task_ids)
