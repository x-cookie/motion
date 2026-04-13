"""Tests for restore command."""

from motion.cli.commands.restore import restore_command
from motion_core.shared.constants import StatusVerbs
from tests.presentation.cli.commands.bulk_command_test_base import BaseBulkCommandTest


class TestRestoreCommand(BaseBulkCommandTest):
    """Test cases for restore command."""

    command_func = restore_command
    bulk_method = "bulk_restore"
    action_verb = StatusVerbs.RESTORED
