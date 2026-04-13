# Motion Quick Setup Guide

Get started with Motion in 5 minutes!

## Prerequisites

- Python 3.11+ (workspace root) or 3.13+ (individual packages)
- [uv](https://github.com/astral-sh/uv) package manager

## Step 1: Install Motion (2 minutes)

```bash
# Clone the repository
git clone https://github.com/Kohei-Wada/motion.git
cd motion

# Install both CLI/TUI and API server
make install
```

This installs two commands:

- `motion` - CLI and TUI interface
- `motion-server` - API server (required for motion to work)

## Step 2: Configure Authentication (2 minutes)

Motion uses API key authentication by default. You need to configure both server and client.

### 2a. Generate API Key

```bash
# Generate a secure API key
python -c "import secrets; print(f'sk-{secrets.token_hex(24)}')"
# Example output: sk-a1b2c3d4e5f6...
```

### 2b. Configure Server

```bash
# Create config directory
mkdir -p ~/.config/motion

# Create server config with your API key
cat > ~/.config/motion/server.toml << 'EOF'
[auth]
enabled = true

[[auth.api_keys]]
name = "my-client"
key = "sk-YOUR-GENERATED-KEY-HERE"  # Replace with your key
EOF

# Secure the file (contains secrets)
chmod 600 ~/.config/motion/server.toml
```

### 2c. Configure CLI/TUI

```bash
# Create CLI config with the same API key
cat > ~/.config/motion/cli.toml << 'EOF'
[api]
host = "127.0.0.1"
port = 8000
api_key = "sk-YOUR-GENERATED-KEY-HERE"  # Same key as server.toml

[ui]
theme = "textual-dark"
EOF
```

**Important**: The `api_key` in `cli.toml` must match one of the keys in `server.toml`.

## Step 3: Start the Server (1 minute)

### Option A: Docker (Recommended for isolation)

```bash
# Build and run the container
docker build -t motion-server .
docker run -d --name motion-server -p 8000:8000 -v motion-data:/data motion-server

# Or use Docker Compose
docker compose up -d

# Verify it's running
curl http://localhost:8000/health
```

### Option B: Manual Start (Quick Test)

```bash
# Start the server in a terminal
motion-server

# Keep this terminal running
```

### Option C: Systemd Service (Linux, Recommended for local)

```bash
# Start the service
systemctl --user start motion-server

# Enable auto-start on boot
systemctl --user enable motion-server

# Check status
systemctl --user status motion-server
```

The server will now:

- Start automatically when you log in
- Restart automatically if it crashes
- Run in the background

## Step 4: Verify Everything Works (1 minute)

```bash
# In a new terminal, test the CLI
motion table

# If you see an empty table (or a list of tasks), you're ready!
```

## Quick Tour

Now that everything is set up, try these commands:

```bash
# Add your first task
motion add "Learn Motion" --priority 10

# View tasks in a table
motion table

# Start working on the task
motion start 1

# View in interactive TUI
motion tui
```

### Load Demo Data (Optional)

To quickly populate Motion with ~50 sample tasks (deadlines, dependencies, tags, notes):

```bash
docker compose exec motion-server python scripts/demo_data.py --no-confirm
```

### TUI Keyboard Shortcuts

Once in the TUI (`motion tui`):

- `a` - Add new task
- `s` - Start selected task
- `d` - Complete (done) task
- `i` - Show task details
- `q` - Quit
- `/` - Search
- `S` - Change sort order

## Common Issues & Solutions

### Error: "Cannot connect to API server"

**Problem**: Server is not running

**Solution**:

```bash
# Check if server is running
systemctl --user status motion-server

# Or manually check
curl http://127.0.0.1:8000/health

# If not running, start it (see Step 3)
motion-server
```

### Error: Connection refused

**Problem**: Port mismatch between config and server

**Solution**:

```bash
# Check what port the server is using
systemctl --user status motion-server  # Look for --port in the command

# Make sure config matches
cat ~/.config/motion/cli.toml  # Check [api] port value

# Update config if needed
nano ~/.config/motion/cli.toml
```

### Server won't start

**Problem**: Port already in use

**Solution**:

```bash
# Check what's using port 8000
ss -tlnp | grep 8000

# Use a different port
motion-server --port 8001

# Update config to match
# Edit ~/.config/motion/cli.toml: port = 8001
```

### Error: Authentication failed (401)

**Problem**: API key mismatch or missing

**Solution**:

```bash
# Check server config has the key
grep -A2 "api_keys" ~/.config/motion/server.toml

# Check CLI config has matching key
grep "api_key" ~/.config/motion/cli.toml

# Verify keys match (copy-paste to compare)
```

## MCP Server Setup (Optional)

Use Claude Desktop or other MCP-compatible AI clients to manage tasks via natural language.

### Install MCP Server

```bash
# From motion workspace root
make install-mcp

# Or install globally
uv tool install motion-mcp
```

### Configure MCP

```bash
# Create MCP config
cat > ~/.config/motion/mcp.toml << 'EOF'
[api]
host = "127.0.0.1"
port = 8000
api_key = "sk-YOUR-GENERATED-KEY-HERE"  # Same key as server.toml

[server]
name = "motion"
log_level = "INFO"
EOF
```

### Configure Claude Desktop

Add to Claude Desktop config:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "motion": {
      "command": "motion-mcp"
    }
  }
}
```

Restart Claude Desktop after configuration.

### Test MCP

Ask Claude Desktop:

- "Create a task to review the PR"
- "Start task 42"

See [motion-mcp README](../packages/motion-mcp/README.md) for more details.

## Next Steps

- Read the [full README](../README.md) for all features
- Check [CLAUDE.md](../CLAUDE.md) for architecture details
- Explore optimization algorithms: `motion optimize --help`
- Try the Gantt chart: `motion gantt`
- Add dependencies: `motion add-dependency TASK_ID DEPENDS_ON_ID`
- Set up MCP for AI-assisted task management

## Environment Variable Alternative

Instead of editing the config file, you can set environment variables:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export MOTION_API_HOST=127.0.0.1
export MOTION_API_PORT=8000
export MOTION_API_KEY=sk-your-api-key

# Or set them temporarily
MOTION_API_KEY=sk-your-key motion table
```

Note: Environment variables take precedence over config file.

## Uninstall

If you need to remove Motion:

```bash
cd /path/to/motion

# Stop and remove systemd service (if using)
systemctl --user stop motion-server
systemctl --user disable motion-server

# Uninstall commands
make uninstall

# Optional: Remove data and config
rm -rf ~/.local/share/motion
rm -rf ~/.config/motion
```

## Getting Help

- Issues: https://github.com/Kohei-Wada/motion/issues
- Documentation: See [README.md](../README.md)
- CLI help: `motion --help`
- Command help: `motion <command> --help`
