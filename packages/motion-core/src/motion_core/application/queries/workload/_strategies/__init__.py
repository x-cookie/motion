"""Internal workload calculation strategies.

This module is internal to the workload package. External code should use
the public calculators (OptimizationWorkloadCalculator, DisplayWorkloadCalculator)
instead of accessing strategies directly.
"""

from motion_core.application.queries.workload._strategies.actual_schedule import (
    ActualScheduleStrategy,
)
from motion_core.application.queries.workload._strategies.all_days import (
    AllDaysStrategy,
)
from motion_core.application.queries.workload._strategies.base import (
    WorkloadCalculationStrategy,
)
from motion_core.application.queries.workload._strategies.weekday_only import (
    WeekdayOnlyStrategy,
)

__all__ = [
    "ActualScheduleStrategy",
    "AllDaysStrategy",
    "WeekdayOnlyStrategy",
    "WorkloadCalculationStrategy",
]
