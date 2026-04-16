"""Use case for completing a task."""

from motion_core.application.dto.base import SingleTaskInput
from motion_core.application.use_cases.status_change_use_case import (
    StatusChangeUseCase,
)
from motion_core.domain.entities.task import TaskStatus


class CompleteTaskUseCase(StatusChangeUseCase[SingleTaskInput]):
    """Use case for completing a task.

    Sets task status to COMPLETED and records actual end time.

    This use case inherits common status change logic from StatusChangeUseCase
    and only specifies the target status.
    """

    def _get_target_status(self) -> TaskStatus:
        """Return COMPLETED as the target status.

        Returns:
            TaskStatus.COMPLETED
        """
        return TaskStatus.COMPLETED
