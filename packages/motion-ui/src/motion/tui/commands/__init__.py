"""TUI command classes for action handling."""

from motion.tui.commands.add import AddCommand
from motion.tui.commands.audit import AuditCommand
from motion.tui.commands.base import TUICommandBase
from motion.tui.commands.cancel import CancelCommand
from motion.tui.commands.done import DoneCommand
from motion.tui.commands.edit import EditCommand
from motion.tui.commands.export import ExportCommand
from motion.tui.commands.fix_actual import FixActualCommand
from motion.tui.commands.hard_delete import HardDeleteCommand
from motion.tui.commands.help import ShowHelpCommand
from motion.tui.commands.note import NoteCommand
from motion.tui.commands.optimize import OptimizeCommand
from motion.tui.commands.pause import PauseCommand
from motion.tui.commands.refresh import RefreshCommand
from motion.tui.commands.reopen import ReopenCommand
from motion.tui.commands.rm import RmCommand
from motion.tui.commands.show import ShowCommand
from motion.tui.commands.start import StartCommand
from motion.tui.commands.stats import StatsCommand

COMMANDS: dict[str, type[TUICommandBase]] = {
    "add": AddCommand,
    "audit": AuditCommand,
    "cancel": CancelCommand,
    "done": DoneCommand,
    "edit": EditCommand,
    "export": ExportCommand,
    "fix_actual": FixActualCommand,
    "hard_delete": HardDeleteCommand,
    "show_help": ShowHelpCommand,
    "note": NoteCommand,
    "optimize": OptimizeCommand,
    "pause": PauseCommand,
    "refresh": RefreshCommand,
    "reopen": ReopenCommand,
    "rm": RmCommand,
    "show": ShowCommand,
    "start": StartCommand,
    "stats": StatsCommand,
}

__all__ = ["COMMANDS"]
