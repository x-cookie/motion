# motion-core

Core business logic and infrastructure for Motion task management system.

## Overview

This package contains the core components shared by both the Motion server and UI:

- **Domain Layer**: Business entities, domain services, and interfaces
- **Application Layer**: Use cases, queries, DTOs, and business logic orchestration
- **Infrastructure Layer**: Persistence implementations, external service integrations
- **Controllers**: Business logic orchestrators used by presentation layers

## Installation

```bash
pip install motion-core
```

For development:

```bash
pip install -e ".[dev]"
```

## Architecture

Follows Clean Architecture principles:

```text
Domain (entities, services, repositories)
  ↑
Application (use cases, queries, DTOs)
  ↑
Infrastructure (SQLite, file storage)
  ↑
Controllers (orchestration layer)
```

### Key Components

**Domain Layer** (`motion_core/domain/`):

- `Task` - Core entity with status, priority, deadlines, dependencies
- `TaskStatus` - PENDING, IN_PROGRESS, COMPLETED, CANCELED
- `TimeTracker` - Records actual_start/actual_end timestamps
- `TaskNotFoundException`, `TaskValidationError` - Domain exceptions

**Application Layer** (`motion_core/application/`):

- **Use Cases**: CreateTaskUseCase, StartTaskUseCase, OptimizeScheduleUseCase, etc.
- **Validators**: TaskFieldValidatorRegistry with Status and Dependency validators
- **Services**: WorkloadAllocator, OptimizationSummaryBuilder, TaskQueryService
- **Optimization**: 9 scheduling strategies (greedy, balanced, backward, priority_first, earliest_deadline, round_robin, dependency_aware, genetic, monte_carlo)

**Infrastructure Layer** (`motion_core/infrastructure/`):

- `SqliteTaskRepository` - SQLite persistence with transactional writes
- `SqliteNotesRepository` - Database-based notes storage
- `ConfigManager` - TOML configuration loading

**Controllers** (`motion_core/controllers/`):

- `TaskCrudController` - Create, update, delete operations
- `TaskLifecycleController` - Start, complete, pause, cancel, reopen
- `TaskRelationshipController` - Dependencies and tags
- `TaskAnalyticsController` - Statistics and optimization
- `QueryController` - Read-only operations

## Usage Example

```python
from motion_core.domain.entities.task import Task, TaskStatus
from motion_core.infrastructure.persistence.database.sqlite_task_repository import SqliteTaskRepository
from motion_core.controllers.task_crud_controller import TaskCrudController
from motion_core.infrastructure.config.config_manager import ConfigManager
from motion_core.shared.utils.logger import StandardLogger

# Setup
repository = SqliteTaskRepository("sqlite:///tasks.db")
config = ConfigManager()
logger = StandardLogger("example")

# Create controller
crud_controller = TaskCrudController(repository, config, logger)

# Create a task
from motion_core.application.dto.task_request import CreateTaskRequest
request = CreateTaskRequest(name="My Task", priority=100)
task = crud_controller.create_task(request)
```

## Dependencies

- `holidays`: Holiday checking for scheduling
- `python-dateutil`: Date/time utilities
- `sqlalchemy`: Database ORM

## Related Packages

- [motion-server](../motion-server/): FastAPI REST API server using this package
- [motion-ui](../motion-ui/): CLI and TUI interfaces using this package
- [motion-client](../motion-client/): HTTP client library for API access

For detailed architecture documentation, see [CLAUDE.md](../../CLAUDE.md).

## Testing

```bash
pytest tests/
```

## License

MIT
