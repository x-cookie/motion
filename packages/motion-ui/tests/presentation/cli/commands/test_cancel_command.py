"""Tests for cancel command."""

from motion.cli.commands.cancel import cancel_command
from motion_core.shared.constants import StatusVerbs
from tests.presentation.cli.commands.bulk_command_test_base import BaseBulkCommandTest


class TestCancelCommand(BaseBulkCommandTest):
    """Test cases for cancel command."""

    command_func = cancel_command
    bulk_method = "bulk_cancel"
    action_verb = StatusVerbs.CANCELED
