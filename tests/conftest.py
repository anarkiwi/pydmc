"""Shared test fixtures: tune access + the committed byte-exact oracle grids.

DMC ``.sid`` tunes are HVSC copyright works, never committed.  ``tune_path``
locates a tune from a local HVSC mirror (``$HVSC`` or the default path), skipping
the test when the tune is absent.  The ground-truth per-frame register grids are
committed frozen (``fixtures/*.grid.txt``), framed per VBI play call (the DMC
framing), so the byte-exact player tests run with no emulator binary.
"""

import os
from pathlib import Path

import pytest

from helpers import TUNES, load_grid


def _hvsc_root() -> Path:
    return Path(os.environ.get("HVSC", "/scratch/preframr/hvsc/C64Music"))


@pytest.fixture(params=sorted(TUNES))
def tune_id(request):
    """Parametrize over each DMC test tune id."""
    return request.param


@pytest.fixture
def tune_path(tune_id):
    """Path to a DMC test tune, or skip if the HVSC mirror is unavailable."""
    rel, _grid = TUNES[tune_id]
    path = _hvsc_root() / rel
    if not path.exists():
        pytest.skip("tune %r not found in HVSC mirror (set $HVSC)" % tune_id)
    return str(path)


@pytest.fixture
def oracle_grid(tune_id):
    """The committed frozen per-call register grid for ``tune_id``."""
    return load_grid(tune_id)
