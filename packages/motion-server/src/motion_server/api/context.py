"""API context for dependency injection."""

from dataclasses import dataclass, field

from sqlalchemy.engine import Engine

from motion_core.controllers.audit_log_controller import AuditLogController
from motion_core.controllers.bulk_task_controller import BulkTaskController
from motion_core.controllers.query_controller import QueryController
from motion_core.controllers.task_analytics_controller import TaskAnalyticsController
from motion_core.controllers.task_crud_controller import TaskCrudController
from motion_core.controllers.task_lifecycle_controller import TaskLifecycleController
from motion_core.controllers.task_relationship_controller import (
    TaskRelationshipController,
)
from motion_core.domain.repositories.notes_repository import NotesRepository
from motion_core.domain.repositories.task_repository import TaskRepository
from motion_core.domain.services.holiday_checker import IHolidayChecker
from motion_core.domain.services.time_provider import ITimeProvider
from motion_core.shared.config_manager import Config


@dataclass
class ApiContext:
    """Context object for API endpoints containing shared dependencies.

    Attributes:
        repository: Task repository for data access
        config: Application configuration
        notes_repository: Notes repository for notes file operations
        query_controller: Controller for task read operations
        lifecycle_controller: Controller for task lifecycle operations (start, complete, etc.)
        relationship_controller: Controller for task relationships (dependencies, tags, hours)
        analytics_controller: Controller for analytics operations (statistics, optimization)
        crud_controller: Controller for CRUD operations (create, update, archive, etc.)
        holiday_checker: Holiday checker for workday validation (optional)
        time_provider: Time provider for current time (optional, defaults to SystemTimeProvider)
        audit_log_controller: Controller for audit log operations
        engine: Shared SQLAlchemy engine (owned by this context)
    """

    repository: TaskRepository
    config: Config
    notes_repository: NotesRepository
    query_controller: QueryController
    lifecycle_controller: TaskLifecycleController
    relationship_controller: TaskRelationshipController
    analytics_controller: TaskAnalyticsController
    crud_controller: TaskCrudController
    holiday_checker: IHolidayChecker | None
    time_provider: ITimeProvider
    audit_log_controller: AuditLogController
    bulk_controller: BulkTaskController
    engine: Engine | None = field(default=None, repr=False)

    def close(self) -> None:
        """Dispose the shared engine to release database connections."""
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
