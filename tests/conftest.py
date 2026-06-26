"""Shared test fixtures: tune access + the committed byte-exact oracle grids.

DMC ``.sid`` tunes are HVSC copyright works, never committed.  ``tune_path``
FETCHES + CACHES the tune on demand (HVSC mirror, honouring a local ``$HVSC``
tree) into the gitignored cache and the byte-exact tests RUN for real -- they do
not skip (a fetch failure is a test failure).  The ground-truth per-frame
register grids are committed frozen (``fixtures/*.grid.txt``), framed per VBI
play call (the DMC framing), so no emulator binary is needed.
"""

import sys
from pathlib import Path

import pytest

from helpers import TUNES, load_grid

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import fetch_tunes  # noqa: E402  (after sys.path tweak)


@pytest.fixture(params=sorted(TUNES))
def tune_id(request):
    """Parametrize over each DMC test tune id."""
    return request.param


@pytest.fixture
def tune_path(tune_id):
    """Path to a DMC test tune, FETCHED + CACHED on demand (never skipped).

    The byte-exact validation requires the tune, so it is fetched from the HVSC
    mirror into the gitignored cache (honouring a local ``$HVSC`` tree) and the
    test runs for real -- a fetch failure is a test failure, not a skip.
    """
    rel, _grid = TUNES[tune_id]
    return str(fetch_tunes.fetch(rel))


@pytest.fixture
def oracle_grid(tune_id):
    """The committed frozen per-call register grid for ``tune_id``."""
    return load_grid(tune_id)
