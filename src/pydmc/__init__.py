"""Read and play DMC (Demo Music Creator) SID tunes (pure-Python)."""

from pydmc.errors import DmcError, SidParseError
from pydmc.player import Player, iter_frames
from pydmc.reader import Song, parse, read
from pydmc.reglog import RegWrite, iter_register_writes

__version__ = "0.1.0"

__all__ = [
    "DmcError",
    "Player",
    "RegWrite",
    "SidParseError",
    "Song",
    "__version__",
    "iter_frames",
    "iter_register_writes",
    "parse",
    "read",
]
