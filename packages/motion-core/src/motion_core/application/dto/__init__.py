"""Data Transfer Objects."""

from motion_core.application.dto.base import SingleTaskInput
from motion_core.application.dto.gantt_output import GanttDateRange, GanttOutput
from motion_core.application.dto.query_inputs import (
    GetGanttDataInput,
    ListTasksInput,
    TimeRange,
)
from motion_core.application.dto.statistics_output import (
    CalculateStatisticsInput,
    DeadlineComplianceStatistics,
    EstimationAccuracyStatistics,
    PriorityDistributionStatistics,
    StatisticsOutput,
    TaskStatistics,
    TimeStatistics,
    TrendStatistics,
)
from motion_core.application.dto.status_change_output import StatusChangeOutput
from motion_core.application.dto.task_detail_output import TaskDetailOutput

__all__ = [
    "CalculateStatisticsInput",
    "DeadlineComplianceStatistics",
    "EstimationAccuracyStatistics",
    "GanttDateRange",
    "GanttOutput",
    "GetGanttDataInput",
    "ListTasksInput",
    "PriorityDistributionStatistics",
    "SingleTaskInput",
    "StatisticsOutput",
    "StatusChangeOutput",
    "TaskDetailOutput",
    "TaskStatistics",
    "TimeRange",
    "TimeStatistics",
    "TrendStatistics",
]
