# pydmc

Pure-Python reader and player for **DMC (Demo Music Creator)** SID tunes — the
C64 player by Brian/Graffity ("`-PLAYER (C) BRIAN/GRAFFITY!`").

A DMC `.sid` is the player binary plus the per-tune song data resident in the same
image. `pydmc` loads the image, locates the per-tune table bases from the player
code operands (no baked addresses — a differently-sized tune relocates its tables),
and runs a faithful integer transcription of the 6502 play routine, exposing the
per-frame SID register writes.

## Usage

```python
import pydmc

song = pydmc.read("tune.sid")
for w in pydmc.iter_register_writes(song, max_frames=50 * 60):
    print(w.clock, w.reg, w.val)   # absolute CPU cycle, $D4xx reg offset, value
```

`iter_register_writes` follows the shared py* register-log convention
(`pygoattracker` / `pymusicassembler`): one `RegWrite(clock, reg, val)` per SID
write, frames `cycles_per_frame` apart. The DMC player emits one tight write burst
per VBI play call.

## What it models

Tempo divider, per-voice orderlist walk (transpose / loop / stop), pattern walk
(note / instrument-select / duration / effect / gate), stride-11 instrument records
driving PW init + a 16-bit PW sweep, the `$FF`-arp wavetable, triangle vibrato,
glide, the pitch-slide effect and a 6-step filter sweep, the hard-restart window,
and the final per-voice frequency compose. Transcribed from the DMC disassembly.

## License

Apache-2.0.
