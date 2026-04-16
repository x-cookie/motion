# motion-mcp

MCP (Model Context Protocol) server for Motion, enabling Claude Desktop and other MCP-compatible AI clients to interact with your task management system.

## Features

- **Task Management**: Create, read, update, delete tasks via natural language
- **Task Lifecycle**: Start, complete, pause, cancel, reopen tasks
- **Task Decomposition**: AI-assisted breakdown of large tasks into subtasks
- **Queries**: Get statistics, executable tasks, tag statistics

## Installation

```bash
# From the motion workspace root
make install-mcp

# Or install globally
uv tool install motion-mcp
```

## Configuration

Create `~/.config/motion/mcp.toml`:

```toml
[api]
host = "127.0.0.1"
port = 8000
api_key = ""  # Optional, for authenticated servers

[server]
name = "motion"
log_level = "INFO"
```

Environment variables override config file:

- `MOTION_API_HOST`
- `MOTION_API_PORT`
- `MOTION_API_KEY`
- `MOTION_MCP_NAME`
- `MOTION_MCP_LOG_LEVEL`

## Claude Desktop Setup

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "motion": {
      "command": "motion-mcp"
    }
  }
}
```

Or with uv (for development):

```json
{
  "mcpServers": {
    "motion": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/motion/packages/motion-mcp",
        "run",
        "motion-mcp"
      ]
    }
  }
}
```

## Available Tools

### Task CRUD

- `list_tasks` - List tasks with filtering
- `get_task` - Get task details
- `create_task` - Create a new task
- `update_task` - Update task fields
- `delete_task` - Delete/archive a task
- `restore_task` - Restore an archived task

### Lifecycle

- `start_task` - Start working on a task
- `complete_task` - Mark task as completed
- `pause_task` - Pause a task
- `cancel_task` - Cancel a task
- `reopen_task` - Reopen a completed/canceled task

### Queries

- `get_statistics` - Get task statistics
- `get_tag_statistics` - Get tag statistics
- `get_executable_tasks` - Get tasks AI can work on

### Decomposition & Organization

- `decompose_task` - Break down a task into subtasks
- `add_dependency` - Add dependency between tasks
- `remove_dependency` - Remove a dependency
- `set_task_tags` - Set task tags
- `update_task_notes` - Update task notes
- `get_task_notes` - Get task notes

## Usage Examples

Ask Claude Desktop:

- "Create a task to write unit tests for the API"
- "Start task 42"
- "Complete task 42"
- "Decompose task 123 into smaller subtasks for implementing the login feature"
- "What tasks can you execute for me?"

## Requirements

- `motion-server` must be running (default: `http://127.0.0.1:8000`)
- Python 3.13+

## Development

```bash
# Install in development mode
cd packages/motion-mcp
uv pip install -e .

# Run tests
PYTHONPATH=src uv run python -m pytest tests/ -v
```

## Troubleshooting

### "Cannot connect to API server"

**Problem**: MCP server can't reach motion-server

**Solutions**:

1. Check if motion-server is running:

   ```bash
   curl http://127.0.0.1:8000/health
   ```

2. Verify `~/.config/motion/mcp.toml` has correct host/port
3. Check if authentication is required:

   ```bash
   curl -H "X-Api-Key: your-key" http://127.0.0.1:8000/health
   ```

### "Authentication failed"

**Problem**: API key is invalid or missing

**Solutions**:

1. Ensure `api_key` in `mcp.toml` matches a key in `server.toml`
2. Check that auth is enabled on server (`[auth] enabled = true`)

### Claude Desktop doesn't see motion tools

**Problem**: MCP server not properly configured

**Solutions**:

1. Verify `claude_desktop_config.json` has correct path
2. Restart Claude Desktop after config changes
3. Check logs: `~/Library/Logs/Claude/mcp*.log` (macOS)

## Related Packages

- [motion-server](../motion-server/): Required API server
- [motion-core](../motion-core/): Core business logic
- [motion-client](../motion-client/): HTTP client used internally

## License

MIT
