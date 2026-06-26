"""Read a DMC tune from a ``.sid`` (PSID/RSID) or raw ``.prg``/image.

The DMC ``.sid`` IS the player + the per-tune song data (the player binary is
resident, and the song tables are relocated into it).  :func:`read` loads the C64
memory image and its load address; the player walks the resident tables directly.
"""

import struct
from dataclasses import dataclass
from pathlib import Path

from pydmc import constants
from pydmc.errors import SidParseError


@dataclass
class Song:
    """A loaded DMC tune: the C64 RAM image + load address + subtune count."""

    mem: bytearray  # 64K C64 memory with the tune resident
    load: int  # load address
    image_len: int  # bytes of the loaded image
    songs: int  # subtune count (PSID header)
    start_song: int  # default subtune (1-based in the header)
    name: str = ""
    author: str = ""

    def is_dmc(self) -> bool:
        """Whether the resident binary carries the DMC JMP-table signature."""
        sig = bytes(self.mem[self.load : self.load + len(constants.DMC_SIGNATURE)])
        return sig == constants.DMC_SIGNATURE


def parse(data: bytes) -> Song:
    """Parse SID/PRG ``data`` bytes into a :class:`Song`."""
    if data[:4] in (b"PSID", b"RSID"):
        data_off = struct.unpack_from(">H", data, 6)[0]
        load = struct.unpack_from(">H", data, 8)[0]
        songs = struct.unpack_from(">H", data, 0x0E)[0]
        start = struct.unpack_from(">H", data, 0x10)[0]
        body = data[data_off:]
        if load == 0:
            if len(body) < 2:
                raise SidParseError("PSID body too short for embedded load address")
            load = body[0] | (body[1] << 8)
            body = body[2:]
        name = data[0x16:0x36].split(b"\x00", 1)[0].decode("latin-1")
        author = data[0x36:0x56].split(b"\x00", 1)[0].decode("latin-1")
    else:  # raw .prg: first two bytes = load address
        if len(data) < 2:
            raise SidParseError("PRG too short")
        load = data[0] | (data[1] << 8)
        body = data[2:]
        songs = 1
        start = 1
        name = author = ""
    mem = bytearray(0x10000)
    end = min(load + len(body), 0x10000)
    mem[load:end] = body[: end - load]
    song = Song(
        mem=mem,
        load=load,
        image_len=end - load,
        songs=songs,
        start_song=start,
        name=name,
        author=author,
    )
    if not song.is_dmc():
        raise SidParseError("image does not carry the DMC player signature")
    return song


def read(path) -> Song:
    """Read a DMC tune from a ``.sid``/``.prg`` file path."""
    return parse(Path(path).read_bytes())
