"""Shared test fixtures for motion packages.

This module provides reusable test utilities that can be shared across
motion-core, motion-server, and motion-ui test suites.

Usage in conftest.py:
    from fixtures import TaskFactory, InMemoryNotesRepository
    from fixtures.pytest_fixtures import (
        task_factory,
        sample_task,
        pending_task,
        ...
    )
"""

from fixtures.factories import TaskFactory
from fixtures.repositories import InMemoryNotesRepository

__all__ = [
    "InMemoryNotesRepository",
    "TaskFactory",
]
