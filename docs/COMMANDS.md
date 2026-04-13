# CLI Commands Reference

Complete reference for all Motion CLI commands.

## Table of Contents

- [Task Creation & Updates](#task-creation--updates)
- [Task Management](#task-management)
- [Dependencies](#dependencies)
- [Tags Management](#tags-management)
- [Time Tracking](#time-tracking)
- [Optimization](#optimization)
- [Visualization](#visualization)
- [Analytics](#analytics)
- [Notes & TUI](#notes--tui)
- [Task States](#task-states)
- [Tags](#tags)

## Task Creation & Updates

### add - Create a new task

```bash
motion add "Task name" [-p PRIORITY] [--fixed] [-d DEP_ID] [-t TAG]
```

Create a new task with optional priority, dependencies, and tags. Multiple `-d` and `-t` flags are allowed.

**Examples:**

```bash
motion add "Design phase" -p 150
motion add "Implementation" -p 100 -d 1 -t backend -t api
motion add "Team meeting" --fixed  # Won't be rescheduled
```

### update - Multi-field update

```bash
motion update ID [--name NAME] [--priority N] [--status STATUS] [--planned-start DATE] [--planned-end DATE] [--deadline DATE] [--estimated-duration HOURS]
```

Update multiple task fields at once.

**Examples:**

```bash
motion update 1 --priority 200 --deadline 2025-10-25
motion update 2 --name "New task name"
```

## Task Management

### start - Start tasks

```bash
motion start ID...
```

Start one or more tasks. Records actual start time and changes status to IN_PROGRESS.

**Examples:**

```bash
motion start 1
motion start 2 3 4  # Batch operation
```

### done - Complete tasks

```bash
motion done ID...
```

Mark tasks as completed. Records actual end time.

**Examples:**

```bash
motion done 1
motion done 2 3 4  # Batch operation
```

### pause - Pause tasks

```bash
motion pause ID...
```

Pause tasks and reset to PENDING status. Clears timestamps.

**Examples:**

```bash
motion pause 1
motion pause 2 3  # Batch operation
```

### cancel - Cancel tasks

```bash
motion cancel ID...
```

Mark tasks as CANCELED.

**Examples:**

```bash
motion cancel 1
motion cancel 2 3  # Batch operation
```

### reopen - Reopen tasks

```bash
motion reopen ID...
```

Reopen completed or canceled tasks. Resets to PENDING status.

**Examples:**

```bash
motion reopen 1
motion reopen 2 3  # Batch operation
```

### rm - Remove tasks

```bash
motion rm ID... [--hard]
```

Remove tasks. Default is soft delete (sets is_archived=true). Use `--hard` for permanent deletion.

**Examples:**

```bash
motion rm 1        # Soft delete (can be restored)
motion rm 2 --hard # Permanent deletion
```

### restore - Restore soft-deleted tasks

```bash
motion restore ID...
```

Restore previously archived (soft-deleted) tasks.

**Examples:**

```bash
motion restore 1
motion restore 2 3  # Batch operation
```

## Dependencies

### add-dependency - Add task dependency

```bash
motion add-dependency TASK_ID DEPENDS_ON_ID
```

Add a dependency relationship. Includes circular dependency detection.

**Examples:**

```bash
motion add-dependency 2 1  # Task 2 depends on task 1
```

### remove-dependency - Remove task dependency

```bash
motion remove-dependency TASK_ID DEP_ID
```

Remove a dependency relationship.

**Examples:**

```bash
motion remove-dependency 2 1
```

## Tags Management

### tags - Manage tags

```bash
motion tags              # List all tags with counts
motion tags ID           # Show tags for a task
motion tags ID TAG1...   # Set tags for a task (replaces existing)
```

**Examples:**

```bash
motion tags                    # List all tags
motion tags 1                  # Show task 1's tags
motion tags 1 urgent backend   # Set tags for task 1
```

## Optimization

### optimize - Auto-schedule tasks

```bash
motion optimize [--start-date DATE] [--max-hours-per-day N] [-a ALGORITHM] [-f]
```

Auto-generate optimal task schedules based on priorities, deadlines, and dependencies.

**Available Algorithms:**

- `greedy` (default) - Schedule highest priority tasks first
- `balanced` - Distribute workload evenly across days
- `backward` - Schedule from deadline backwards
- `priority_first` - Strict priority ordering
- `earliest_deadline` - Schedule tasks with earliest deadlines first
- `round_robin` - Rotate through tasks to minimize context switching
- `dependency_aware` - Prioritize tasks that unblock others
- `genetic` - Use genetic algorithm for optimization
- `monte_carlo` - Use Monte Carlo simulation

**Features:**

- Respects fixed tasks and dependencies
- Distributes workload across weekdays
- Avoids weekend scheduling
- Honors max_hours_per_day constraint

**Examples:**

```bash
motion optimize
motion optimize --start-date 2025-10-22 --max-hours-per-day 8
motion optimize -a balanced
motion optimize -f  # Force re-optimization
```

## Visualization

### table - Table view

```bash
motion table [OPTIONS]
```

Display tasks in table format with filtering and sorting.

**Options:**

- `-s/--sort FIELD` - Sort by: id, priority, deadline, name, status, planned_start
- `-r/--reverse` - Reverse sort order
- `-a/--all` - Include archived tasks (default: non-archived only)
- `-f/--fields LIST` - Custom field selection
- `--status STATUS` - Filter by status: pending, in_progress, completed, canceled
- `-t/--tag TAG` - Filter by tags (multiple tags use OR logic)
- `--start-date DATE` - Filter by planned start date (from)
- `--end-date DATE` - Filter by planned end date (to)

**Examples:**

```bash
motion table
motion table -s priority -r
motion table --status pending --tag backend
motion table -a  # Show archived tasks too
```

### gantt - Gantt chart

```bash
motion gantt [OPTIONS]
```

Display visual timeline with workload analysis. Supports same filter/sort options as table.

**Features:**

- Visual timeline with daily hours
- Status symbols (◆)
- Weekend coloring
- Workload summary
- Strikethrough for finished tasks

**Examples:**

```bash
motion gantt
motion gantt -s deadline
motion gantt --start-date 2025-10-20 --end-date 2025-10-30
```

### show - Task details

```bash
motion show ID [--raw]
```

Show detailed information for a task, including notes. Notes are rendered as markdown by default.

**Examples:**

```bash
motion show 1
motion show 1 --raw  # Show raw markdown
```

### export - Export tasks

```bash
motion export [OPTIONS]
```

Export tasks to JSON or CSV format. Exports non-archived tasks by default.

**Options:**

- `--format FORMAT` - json (default), csv, or markdown
- `-o/--output FILE` - Output file path
- `-f/--fields LIST` - Custom field selection
- `-a/--all` - Include archived tasks
- `--status STATUS` - Filter by status
- `-t/--tag TAG` - Filter by tags
- `--start-date DATE` - Filter by date range
- `--end-date DATE` - Filter by date range

**Examples:**

```bash
motion export
motion export --format csv -o tasks.csv
motion export --format markdown -o tasks.md
motion export --status pending -t backend
```

## Analytics

### stats - Task statistics

```bash
motion stats [--period PERIOD] [--focus FOCUS]
```

Display task statistics and analytics.

**Options:**

- `-p/--period` - all (default), 7d, 30d
- `-f/--focus` - all (default), basic, time, estimation, deadline, priority, trends

**Examples:**

```bash
motion stats
motion stats -p 7d -f time
motion stats --period 30d --focus trends
```

## Notes & TUI

### note - Edit task notes

```bash
motion note ID
```

Edit markdown notes for a task using `$EDITOR`.

**Examples:**

```bash
motion note 1
```

### tui - Interactive TUI

```bash
motion tui
```

Launch full-screen interactive terminal user interface.

**Key features:**

- Real-time task search and filtering
- Keyboard shortcuts for quick operations
- Sort by deadline, priority, planned start, or ID
- Visual status indicators with colors
- Task details panel with dependencies

See [Interactive TUI](../README.md#interactive-tui) section in README for full keyboard shortcuts.

## Task States

Tasks can be in one of four states:

- **PENDING**: Not started (yellow)
- **IN_PROGRESS**: Being worked on (blue)
- **COMPLETED**: Finished (green)
- **CANCELED**: Won't be done (red)

**Note**: Archived tasks (soft-deleted) retain their original status and can be restored with `motion restore`.

## Tags

Tasks can be organized with tags for better categorization and filtering.

**Examples:**

```bash
# Add task with tags
motion add "Backend API" --tag backend --tag api

# Manage tags
motion tags                    # List all tags with counts
motion tags 1                  # Show tags for task 1
motion tags 1 urgent backend   # Set tags (replaces existing)

# Filter by tags
motion table --tag backend     # Show tasks with 'backend' tag
motion table --tag api --tag db  # OR logic: tasks with 'api' OR 'db'
```

**Tag behavior:**

- Tags are case-sensitive
- Multiple tags can be assigned to a task
- Tags are automatically created when first used
- Filtering with multiple tags uses OR logic
- Empty or whitespace-only tags are not allowed
