# Contributing to Motion

Thank you for your interest in contributing to Motion! We welcome contributions of all kinds, including:

- Bug reports and fixes
- Feature requests and implementations
- Documentation improvements
- Code optimizations and refactoring
- Test coverage improvements

This guide will help you get started with contributing to the project.

## Development Setup

### Prerequisites

- **Python 3.11+** (workspace root) / **Python 3.13+** (individual packages)
- **[uv](https://github.com/astral-sh/uv)** - Python package manager
- **Git**

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/cookie-may/motion.git
cd motion
```

2. **Install with development dependencies:**

```bash
make install-dev
```

This installs all packages with development dependencies in editable mode and
automatically sets up pre-commit hooks (`pre-commit`, `commit-msg`, `pre-push`,
`post-merge`) via `uv run pre-commit install`.

3. **Verify installation:**

```bash
# Run all tests
make test

# Run linter
make lint

# Run type checker
make typecheck
```

### Alternative Installation Methods

```bash
# Install locally for development (per-package editable mode)
make install-local

# Install as global commands (via uv tool)
make install
```

## Project Structure

Motion is a **UV workspace monorepo** with three packages:

```text
motion/
├── packages/
│   ├── motion-core/      # Core business logic and infrastructure
│   │   ├── src/motion_core/
│   │   │   ├── domain/           # Entities, services, exceptions
│   │   │   ├── application/      # Use cases, queries, DTOs, validators
│   │   │   ├── infrastructure/   # SQLite repository, config
│   │   │   └── controllers/      # CRUD, Lifecycle, Relationship, Analytics, Query controllers
│   │   └── tests/
│   ├── motion-server/    # FastAPI REST API server
│   │   ├── src/motion_server/
│   │   │   ├── api/              # Routers, models, dependencies
│   │   │   └── main.py           # FastAPI application
│   │   └── tests/
│   └── motion-ui/        # CLI and TUI interfaces
│       ├── src/motion/
│       │   ├── cli/              # Click commands
│       │   ├── tui/              # Textual TUI
│       │   ├── console/          # Output formatters
│       │   └── renderers/        # Table and Gantt renderers
│       └── tests/
├── pyproject.toml         # Workspace configuration
├── CLAUDE.md              # Detailed architecture documentation
└── Makefile               # Build and test automation
```

### Package Dependencies

- **motion-core**: No dependencies on other packages (pure business logic)
- **motion-server**: Depends on `motion-core` (direct access to controllers and repository)
- **motion-ui**: Depends on `motion-core` (for DTOs and types; accesses data via HTTP API)

### Communication Flow

```text
CLI/TUI (motion-ui) → HTTP API → FastAPI (motion-server) → Controllers/Repository (motion-core)
```

### Architecture

Motion follows **Clean Architecture** principles. For detailed architecture documentation, see [CLAUDE.md](CLAUDE.md).

## Coding Standards

This project enforces high code quality standards:

### Linting and Formatting

- **Linter**: Ruff
- **Formatter**: Ruff format
- **Line Length**: 88 characters
- **McCabe Complexity**: Max 10

```bash
# Run linter
make lint

# Auto-format code
make format

# Run both
make check
```

### Type Checking

- **Type Checker**: mypy (Phase 4 - strict mode)
- All code must have proper type annotations

```bash
# Run type checker
make typecheck
```

### Code Quality Commands

```bash
# Run all quality checks (lint + typecheck)
make check

# Auto-format code before committing
make format
```

## Testing

### Test Framework

- **Framework**: `unittest` (Python standard library)
- **Coverage Tool**: `coverage`

### Writing Tests

- Write tests for all new features and bug fixes
- Test structure mirrors package structure under `tests/`
- Use `unittest.mock` for dependencies
- Follow existing test patterns in the codebase

### Running Tests

```bash
# Run all tests (core + server + ui)
make test

# Run tests for specific package
make test-core
make test-server
make test-ui

# All test commands include coverage (sorted by coverage: low → high)

# Run single test file (from package directory)
cd packages/motion-core && PYTHONPATH=src uv run python -m unittest tests/test_module.py

# Run specific test method
cd packages/motion-core && PYTHONPATH=src uv run python -m unittest tests.test_module.TestClass.test_method
```

### Coverage Requirements

- Coverage reports are displayed in CI logs
- Focus on improving low-coverage areas
- All CI checks must pass before merging

## Commit Guidelines

This project uses **Conventional Commits** format:

```text
<type>: <description>

[optional body]

[optional footer]
```

### Commit Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code refactoring (no functional changes)
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks (dependencies, tooling)
- `perf:` - Performance improvements
- `style:` - Code style changes (formatting, whitespace)

### Examples

```bash
feat: Add genetic algorithm for schedule optimization
fix: Fix circular dependency detection in optimizer
docs: Update API documentation for lifecycle endpoints
refactor: Extract common validation logic to base class
test: Add tests for WorkloadCalculator edge cases
chore: Update dependencies to latest versions
```

## Pull Request Process

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/motion.git
cd motion
git remote add upstream https://github.com/cookie-may/motion.git
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/bug-description
```

### 3. Make Your Changes

- Write clean, well-documented code
- Follow the coding standards
- Add tests for your changes
- Update documentation if needed

### 4. Test Your Changes

```bash
# Run all quality checks
make check

# Run all tests with coverage
make test
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with conventional commit format
git commit -m "feat: Add my awesome feature"
```

### 6. Push to Your Fork

```bash
git push origin feature/my-feature
```

### 7. Create a Pull Request

- Go to GitHub and create a Pull Request from your branch
- Fill in the PR template (if available)
- Reference any related issues (e.g., "Closes #123")

### PR Checklist

Before submitting your PR, ensure:

- [ ] Tests pass (`make test`)
- [ ] Linter passes (`make lint`)
- [ ] Type checker passes (`make typecheck`)
- [ ] Code is formatted (`make format`)
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (if user-facing change)
- [ ] Commit messages follow conventional commit format

### CI Checks

All pull requests automatically run:

- Linting (`make lint`)
- Type checking (`make typecheck`)
- Tests with coverage (`make test`)

All checks must pass before merging.

## Development Workflow

### Per-Package Development

When working on a specific package:

```bash
# Core package
cd packages/motion-core
make install-core
make test-core

# Server package
cd packages/motion-server
make install-server
make test-server

# UI package
cd packages/motion-ui
make install-ui
make test-ui
```

### Running During Development

```bash
# Run CLI without installation
cd packages/motion-ui
PYTHONPATH=src uv run python -m motion.cli_main --help

# Run server without installation
cd packages/motion-server
PYTHONPATH=src uv run python -m motion_server.main --help
```

## Design Philosophy

Before adding new features, please review [DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md). This document explains why Motion focuses on individual task management with flat task structures, and includes guidelines for evaluating new feature proposals.

## Questions and Support

### Getting Help

- **Questions**: Open an issue with the `question` label
- **Bug Reports**: Open an issue with the `bug` label
- **Feature Requests**: Open an issue with the `enhancement` label

### Before Opening an Issue

- Search existing issues to avoid duplicates
- Check the documentation ([README.md](README.md), [CLAUDE.md](CLAUDE.md))
- Try reproducing the issue with the latest version

### Issue Templates

When opening an issue, please provide:

- **Bug Reports**: Steps to reproduce, expected vs actual behavior, environment details
- **Feature Requests**: Clear use case, proposed solution, alternatives considered
- **Questions**: Context, what you've tried, relevant code/commands

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and constructive in discussions
- Focus on the technical merits of ideas
- Welcome newcomers and help them get started
- Assume good intentions

## License

By contributing to Motion, you agree that your contributions will be licensed under the MIT License.

## Additional Resources

- [CLAUDE.md](CLAUDE.md) - Detailed architecture and development guide
- [DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md) - Design principles and rationale
- [README.md](README.md) - User documentation and features
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format
- [UV Documentation](https://github.com/astral-sh/uv) - Package manager guide

---

Thank you for contributing to Motion! 🚀
