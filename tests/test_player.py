"""Byte-exact playback: the DMC player reproduces the committed oracle grids.

Frames the player's per-VBI-play-call write bursts (the first burst = the init
baseline, every subsequent burst = one play call) into a forward-filled 25-register
grid and asserts it equals the committed frozen oracle grid byte-for-byte (lead
aligned over the leading silent call).  This is the player's correctness gate.
"""

import pydmc
from helpers import NREG, PW_HI_REGS, load_grid

SID_BASE = 0xD400


def _grid_from_calls(song, nframes):
    """Forward-fill the player's per-call write bursts into a per-frame grid.

    The first burst (init) forms the frame-0 baseline; each later burst is a row.
    """
    cur = [0] * NREG
    rows = []
    for frame, writes in enumerate(pydmc.iter_frames(song, max_frames=nframes)):
        for reg, val in writes:
            if 0 <= reg < NREG:
                cur[reg] = (val & 0x0F) if reg in PW_HI_REGS else val
        if frame == 0:  # init burst = baseline, not a row
            continue
        rows.append(cur[:])
    return rows


def _lead_aligned_equal(oracle, rendered):
    """True if some lead in 0..4 makes ``rendered`` reproduce ``oracle`` exactly."""
    if not rendered:
        return False
    baseline = rendered[0]
    for lead in range(5):
        if lead and (lead > len(rendered) or rendered[lead - 1] != baseline):
            break
        aligned = rendered[lead : lead + len(oracle)]
        if len(aligned) >= len(oracle) and aligned[: len(oracle)] == oracle:
            return True
    return False


def test_is_dmc(tune_path):
    """A DMC tune carries the player JMP-table signature."""
    song = pydmc.read(tune_path)
    assert song.is_dmc()
    assert song.load == 0x1000


def test_byte_exact_vs_oracle(tune_id, tune_path):
    """The player reproduces the committed per-call oracle grid byte-exact."""
    oracle = load_grid(tune_id)
    song = pydmc.read(tune_path)
    rendered = _grid_from_calls(song, len(oracle) + 8)
    assert _lead_aligned_equal(oracle, rendered), (
        "player diverges from oracle for %r" % tune_id
    )


def test_frames_are_register_writes(tune_path):
    """Each yielded frame is a list of ``(reg, val)`` with reg in 0..24."""
    song = pydmc.read(tune_path)
    frames = list(pydmc.iter_frames(song, max_frames=4))
    assert frames
    for writes in frames:
        for reg, val in writes:
            assert 0 <= reg < NREG
            assert 0 <= val <= 0xFF
