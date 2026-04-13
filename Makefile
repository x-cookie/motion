.PHONY: help test test-core test-server test-ui test-client test-mcp test-all \
        install install-dev install-hooks install-core install-server install-ui install-client install-mcp \
        install-ui-only install-server-only reinstall \
        tool-install-ui tool-install-server check-deps \
        clean lint format typecheck spell check \
        lint-core lint-client lint-server lint-ui lint-mcp \
        typecheck-core typecheck-client typecheck-server typecheck-ui typecheck-mcp \
        bump-version show-version

.DEFAULT_GOAL := help

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    PLATFORM := linux
endif
ifeq ($(UNAME_S),Darwin)
    PLATFORM := macos
endif

help: ## Show this help message
	@echo "╔════════════════════════════════════════════════════════╗"
	@echo "║           Motion Makefile - Available Targets         ║"
	@echo "╚════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 Installation:"
	@grep -E '^(install|reinstall|tool-install).*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🧪 Testing:"
	@grep -E '^test.*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "✨ Code Quality:"
	@grep -E '^(lint|format|typecheck|check).*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🧹 Cleanup:"
	@grep -E '^clean.*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🏷️  Version:"
	@grep -E '^(bump-version|show-version).*:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# Installation Targets
# ============================================================================

check-deps: ## Check if required tools are installed
	@echo "Checking required dependencies..."
	@command -v uv >/dev/null 2>&1 || { echo "❌ Error: uv is not installed. Install it from https://github.com/astral-sh/uv"; exit 1; }
	@echo "✓ uv is installed"
ifeq ($(PLATFORM),linux)
	@command -v systemctl >/dev/null 2>&1 || { echo "❌ Error: systemctl is not installed"; exit 1; }
	@echo "✓ systemctl is installed"
else ifeq ($(PLATFORM),macos)
	@command -v launchctl >/dev/null 2>&1 || { echo "❌ Error: launchctl is not installed"; exit 1; }
	@echo "✓ launchctl is installed"
endif
	@echo "✓ All dependencies are installed"
	@echo ""

install: check-deps ## Install all commands globally with uv tool (recommended)
	@echo "Installing motion-server globally..."
	cd packages/motion-server && uv tool install --force --reinstall .
	@echo "Installing motion globally..."
	cd packages/motion-ui && uv tool install --force --reinstall .
	@echo "Installing motion-mcp globally..."
	cd packages/motion-mcp && uv tool install --force --reinstall .
	@echo ""
ifeq ($(PLATFORM),linux)
	@echo "Setting up systemd user service..."
	@mkdir -p ~/.local/share/motion
	@mkdir -p ~/.config/systemd/user
	@cp contrib/systemd/motion-server.service ~/.config/systemd/user/
	@systemctl --user daemon-reload
	@systemctl --user enable motion-server.service
	@echo ""
	@echo "✓ All commands installed successfully!"
	@echo ""
	@echo "Available commands:"
	@echo "  - motion          (CLI/TUI)"
	@echo "  - motion-server   (API server)"
	@echo "  - motion-mcp      (MCP server for Claude Desktop)"
	@echo ""
	@echo "Systemd service installed and enabled:"
	@echo "  - Start:  systemctl --user start motion-server"
	@echo "  - Status: systemctl --user status motion-server"
	@echo "  - Logs:   journalctl --user -u motion-server -f"
	@echo ""
	@echo "See contrib/README.md for more details."
	@echo ""
else ifeq ($(PLATFORM),macos)
	@echo "Setting up launchd service..."
	@mkdir -p ~/Library/LaunchAgents
	@mkdir -p ~/Library/Logs
	@sed 's|%USER%|$(USER)|g' contrib/launchd/motion-server.plist > ~/Library/LaunchAgents/com.github.kohei-wada.motion-server.plist
	@launchctl load ~/Library/LaunchAgents/com.github.kohei-wada.motion-server.plist 2>/dev/null || true
	@echo ""
	@echo "✓ All commands installed successfully!"
	@echo ""
	@echo "Available commands:"
	@echo "  - motion          (CLI/TUI)"
	@echo "  - motion-server   (API server)"
	@echo "  - motion-mcp      (MCP server for Claude Desktop)"
	@echo ""
	@echo "Launchd service installed and enabled:"
	@echo "  - Start:  launchctl start com.github.kohei-wada.motion-server"
	@echo "  - Stop:   launchctl stop com.github.kohei-wada.motion-server"
	@echo "  - Status: launchctl list | grep motion-server"
	@echo "  - Logs:   tail -f ~/Library/Logs/motion-server.log"
	@echo ""
else
	@echo "✓ All commands installed successfully!"
	@echo ""
	@echo "Available commands:"
	@echo "  - motion          (CLI/TUI)"
	@echo "  - motion-server   (API server)"
	@echo "  - motion-mcp      (MCP server for Claude Desktop)"
	@echo ""
	@echo "Note: Automatic service management not supported on this platform."
	@echo "Start the server manually: motion-server --host 127.0.0.1 --port 8000"
	@echo ""
endif

install-dev: ## Install all packages with development dependencies (for development)
	@echo "Installing all packages with dev dependencies..."
	cd packages/motion-core && uv pip install -e ".[dev]"
	cd packages/motion-client && uv pip install -e ".[dev]"
	cd packages/motion-server && uv pip install -e ".[dev]"
	cd packages/motion-ui && uv pip install -e ".[dev]"
	cd packages/motion-mcp && uv pip install -e ".[dev]"
	$(MAKE) install-hooks
	@echo ""
	@echo "✓ Development environment ready!"
	@echo ""

install-hooks: ## Install pre-commit hooks via uv
	uv run pre-commit install --install-hooks
	uv run pre-commit install --hook-type commit-msg
	uv run pre-commit install --hook-type pre-push
	uv run pre-commit install --hook-type post-merge

install-core: ## Install motion-core package only (for development)
	@echo "Installing motion-core..."
	cd packages/motion-core && uv pip install -e .

install-server: install-core ## Install motion-server with pip (for development)
	@echo "Installing motion-server..."
	cd packages/motion-server && uv pip install -e .

install-client: install-core ## Install motion-client with pip (for development)
	@echo "Installing motion-client..."
	cd packages/motion-client && uv pip install -e .

install-ui: install-client ## Install motion-ui with pip (for development)
	@echo "Installing motion-ui..."
	cd packages/motion-ui && uv pip install -e .

install-mcp: install-client ## Install motion-mcp with pip (for development)
	@echo "Installing motion-mcp..."
	cd packages/motion-mcp && uv pip install -e .

install-local: install-core install-client install-server install-ui install-mcp ## Install all packages locally with pip (for development)
	@echo ""
	@echo "✓ All packages installed locally for development!"
	@echo ""

reinstall: clean install ## Clean and reinstall all commands globally
	@echo "✓ Reinstallation complete!"

# Uninstall
uninstall: ## Uninstall all commands
ifeq ($(PLATFORM),linux)
	@echo "Stopping and disabling systemd service..."
	-systemctl --user stop motion-server.service 2>/dev/null || true
	-systemctl --user disable motion-server.service 2>/dev/null || true
	-rm -f ~/.config/systemd/user/motion-server.service
	-systemctl --user daemon-reload
else ifeq ($(PLATFORM),macos)
	@echo "Stopping and unloading launchd service..."
	-launchctl unload ~/Library/LaunchAgents/com.github.kohei-wada.motion-server.plist 2>/dev/null || true
	-rm -f ~/Library/LaunchAgents/com.github.kohei-wada.motion-server.plist
endif
	@echo "Uninstalling motion commands..."
	-uv tool uninstall motion 2>/dev/null || true
	-uv tool uninstall motion-server 2>/dev/null || true
	-uv tool uninstall motion-mcp 2>/dev/null || true
	@echo "✓ Uninstalled successfully!"

# ============================================================================
# Testing Targets (recursive)
# ============================================================================

PACKAGES := motion-core motion-client motion-server motion-ui motion-mcp
ROOT_DIR := $(shell pwd)
CONFIG := $(ROOT_DIR)/pyproject.toml

test: $(addprefix test-,$(PACKAGES)) ## Run all tests with coverage
	@echo ""
	@echo "✓ All tests passed!"
	@echo ""

test-all: test ## Run all tests (alias for test)

test-%: ## Run tests for a specific package (e.g., make test-motion-core)
	@echo "Running $* tests..."
	$(MAKE) -C packages/$* test

# Convenience aliases for testing
test-core: test-motion-core ## Run motion-core tests
test-client: test-motion-client ## Run motion-client tests
test-server: test-motion-server ## Run motion-server tests
test-ui: test-motion-ui ## Run motion-ui tests
test-mcp: test-motion-mcp ## Run motion-mcp tests

# ============================================================================
# Code Quality Targets (recursive)
# ============================================================================

lint: $(addprefix lint-,$(PACKAGES)) ## Check code with ruff linter
	@echo ""
	@echo "✓ Lint passed!"
	@echo ""

lint-%: ## Lint a specific package (e.g., make lint-motion-core)
	@echo "Linting $*..."
	$(MAKE) -C packages/$* lint ROOT_DIR=$(ROOT_DIR)

# Convenience aliases for linting
lint-core: lint-motion-core ## Lint motion-core
lint-client: lint-motion-client ## Lint motion-client
lint-server: lint-motion-server ## Lint motion-server
lint-ui: lint-motion-ui ## Lint motion-ui
lint-mcp: lint-motion-mcp ## Lint motion-mcp

format: $(addprefix format-,$(PACKAGES)) ## Format code with ruff and apply fixes
	@echo ""
	@echo "✓ Format complete!"
	@echo ""

format-%: ## Format a specific package (e.g., make format-taskdog-core)
	@echo "Formatting $*..."
	$(MAKE) -C packages/$* format ROOT_DIR=$(ROOT_DIR)

typecheck: $(addprefix typecheck-,$(PACKAGES)) ## Run mypy type checker on all packages
	@echo ""
	@echo "✓ Type check passed!"
	@echo ""

typecheck-%: ## Type check a specific package (e.g., make typecheck-taskdog-core)
	@echo "Type checking $*..."
	$(MAKE) -C packages/$* typecheck ROOT_DIR=$(ROOT_DIR)

# Convenience aliases for type checking
typecheck-core: typecheck-taskdog-core ## Type check taskdog-core
typecheck-client: typecheck-taskdog-client ## Type check taskdog-client
typecheck-server: typecheck-taskdog-server ## Type check taskdog-server
typecheck-ui: typecheck-taskdog-ui ## Type check taskdog-ui
typecheck-mcp: typecheck-taskdog-mcp ## Type check taskdog-mcp

spell: ## Run spell checker
	uv tool run codespell

check: lint typecheck spell ## Run all code quality checks (lint + typecheck + spell)
	@echo ""
	@echo "✓ All code quality checks passed!"
	@echo ""

# ============================================================================
# Cleanup Targets
# ============================================================================

clean: ## Clean build artifacts and cache
	@echo "Cleaning build artifacts..."
	rm -rf packages/*/build/ packages/*/dist/ packages/*/src/*.egg-info/
	rm -rf packages/*/.ruff_cache/ packages/*/.mypy_cache/
	find packages -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	uv cache clean
ifeq ($(PLATFORM),linux)
	@echo "Stopping systemd service..."
	-systemctl --user stop taskdog-server.service 2>/dev/null || true
else ifeq ($(PLATFORM),macos)
	@echo "Stopping launchd service..."
	-launchctl stop com.github.kohei-wada.taskdog-server 2>/dev/null || true
endif
	@echo "✓ Clean complete!"

# ============================================================================
# Version Management Targets
# ============================================================================

bump-version: ## Bump version (e.g., make bump-version VERSION=0.8.0)
ifndef VERSION
	$(error VERSION is required. Usage: make bump-version VERSION=0.8.0)
endif
	python scripts/bump_version.py $(VERSION)

show-version: ## Show current version
	@python scripts/bump_version.py --current
