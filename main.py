"""Ship the finished front page for news-image-20261119 v3.

Thursday 19 November 2026, summed up in one dense broadsheet: 42
stories checked against the day's reporting -- the first Trump-Xi-Putin
meeting in Shenzhen, the worldwide GTA VI launch, and Anthropic's
record $81.3bn IPO at the top, plus a twelve-card grid, a world map
with numbered story dots, a UTC timeline, a 27-item numbered brief
list, and a date-check box naming the big stories that actually broke
on Wednesday 18 November, so they are not passed off as today's news.

The picture was laid out beforehand and ships beside this file as
entry.png. This program draws nothing and fetches nothing: it reads
those bytes, proves they are one complete JPEG inside the
competition's limits, and copies them unchanged to the output folder.
No network, no clock, no randomness -- run it twice and the two
outputs are the same bytes.
"""

import os
import pathlib
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"

SOI = b"\xff\xd8"  # JPEG start-of-image marker
EOI = b"\xff\xd9"  # JPEG end-of-image marker
BYTE_CAP = 1_048_576  # 1 MiB, the competition's image cap
SIDE_CAP = 1024  # longest allowed side in pixels

# Markers that open a frame segment (baseline, extended, progressive).
# Every other marker is either standalone or carries a length to skip.
FRAME_MARKERS = (0xC0, 0xC1, 0xC2)


def fail(reason):
    """Stop with a clear error instead of delivering a broken picture."""
    print("error: " + reason, file=sys.stderr)
    raise SystemExit(1)


def load_picture():
    """Return the shipped picture, or stop if it is missing or unusable."""
    try:
        data = PICTURE.read_bytes()
    except FileNotFoundError:
        fail("entry.png is missing next to main.py")
    if len(data) > BYTE_CAP:
        fail("entry.png is larger than 1 MiB")
    if not data.startswith(SOI):
        fail("entry.png is not a JPEG (no SOI marker)")
    if not data.endswith(EOI):
        fail("entry.png is not a complete JPEG (no EOI marker)")
    return data


def read_dimensions(data):
    """Return (width, height) from the JPEG frame header.

    Walk the segments from the SOI marker, skipping each one by its
    declared length, until a frame segment gives the dimensions. A
    segment that claims to run past the end of the file, or a file
    with no frame segment at all, is rejected. The scan segment (SOS)
    ends the walk: entropy-coded data follows it up to the EOI marker
    that load_picture already checked sits at the very end.
    """
    pos = 2
    found = None
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            fail("entry.png has a malformed JPEG segment")
        marker = data[pos + 1]
        if marker in FRAME_MARKERS:
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            found = (width, height)
        if marker == 0xD9 or marker == 0xDA:
            break
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2  # standalone marker, no length field
            continue
        size = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if pos + 2 + size > len(data):
            fail("entry.png has a truncated JPEG segment")
        pos += 2 + size
    if found is None:
        fail("entry.png has no JPEG frame header")
    if found[0] == 0 or found[1] == 0:
        fail("entry.png has a zero dimension")
    return found


def main():
    """Check the picture, then hand it over to the output folder."""
    data = load_picture()
    width, height = read_dimensions(data)
    if width > SIDE_CAP or height > SIDE_CAP:
        fail("entry.png is larger than 1024 by 1024")
    folder = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.png"
    target.write_bytes(data)
    if target.read_bytes() != data:
        fail("the written entry.png does not match the validated picture")


if __name__ == "__main__":
    main()
