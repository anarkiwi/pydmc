"""SID register write logs (the shared py* ``iter_register_writes`` convention).

A register log is the player's output flattened to timed chip writes: one
:class:`RegWrite` per SID register write, with an absolute clock in C64 CPU
cycles.  The DMC player emits one tight write burst per VBI play call; successive
calls are one VBI period (``cycles_per_frame``) apart, and within a call the
writes are spaced ``write_spacing`` cycles -- the same shape the other py* libs
(pymusicassembler / pygoattracker) expose, so deplayroutine's cross-check harness
can frame and byte-compare them.
"""

from typing import Iterator, NamedTuple

from pydmc import constants
from pydmc.player import iter_frames
from pydmc.reader import Song

DEFAULT_WRITE_SPACING = 16


class RegWrite(NamedTuple):
    """One SID register write at an absolute CPU clock (in cycles)."""

    clock: int
    reg: int
    val: int


def iter_register_writes(
    song: Song,
    max_frames: int = 50 * 60,
    cycles_per_frame: int = constants.PAL_CYCLES_PER_FRAME,
    write_spacing: int = DEFAULT_WRITE_SPACING,
    subtune: int = 0,
) -> Iterator[RegWrite]:
    """Yield :class:`RegWrite` for ``song``, frame by frame (VBI play calls).

    ``max_frames`` bounds the (looping) player; writes within a frame are
    ``write_spacing`` cycles apart, frames ``cycles_per_frame`` apart.
    """
    for frame, writes in enumerate(
        iter_frames(song, max_frames=max_frames, subtune=subtune)
    ):
        clock = frame * cycles_per_frame
        for offset, (reg, val) in enumerate(writes):
            yield RegWrite(clock + offset * write_spacing, reg, val)
