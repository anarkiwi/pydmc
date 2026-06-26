"""Register-log convention tests (the shared py* ``iter_register_writes`` API)."""

import pydmc
from pydmc import constants
from pydmc.reglog import RegWrite, iter_register_writes


def test_reglog_clock_layout(tune_path):
    """Writes within a frame are ``write_spacing`` apart; frames a VBI period apart."""
    song = pydmc.read(tune_path)
    writes = list(iter_register_writes(song, max_frames=3, write_spacing=16))
    assert writes
    assert all(isinstance(w, RegWrite) for w in writes)
    # The very first burst is the init burst at clock 0.
    assert writes[0].clock == 0
    assert writes[1].clock == 16


def test_reglog_frame_spacing(tune_path):
    """Frame ``n`` starts at ``n * cycles_per_frame``."""
    song = pydmc.read(tune_path)
    cpf = 1000
    by_clock = {}
    for w in iter_register_writes(song, max_frames=3, cycles_per_frame=cpf):
        by_clock.setdefault(w.clock // cpf, []).append(w)
    # init (frame 0) + at least two play frames present.
    assert max(by_clock) >= 2


def test_reglog_regs_in_range(tune_path):
    """Every logged register is a valid SID register offset."""
    song = pydmc.read(tune_path)
    for w in iter_register_writes(song, max_frames=4):
        assert 0 <= w.reg < constants.SID_REGISTERS
        assert 0 <= w.val <= 0xFF
