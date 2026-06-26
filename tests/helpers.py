"""Shared test helpers (constants + frozen-grid loader)."""

from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NREG = 25
PW_HI_REGS = {0x03, 0x0A, 0x11}

TUNES = {
    "ode": ("MUSICIANS/A/Ass_It/Ode_to_Music.sid", "Ode_to_Music.grid.txt"),
    "faces": ("DEMOS/A-F/Faces.sid", "Faces.grid.txt"),
    "fear": ("DEMOS/A-F/Fear_Me.sid", "Fear_Me.grid.txt"),
    "wladca": ("GAMES/S-Z/Wladca.sid", "Wladca.grid.txt"),
}


def load_grid(tune_id):
    """Load the committed frozen per-call oracle grid for ``tune_id``."""
    _rel, grid = TUNES[tune_id]
    rows = []
    with open(FIXTURES / grid, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                rows.append([int(tok, 16) for tok in line.split()])
    return rows
