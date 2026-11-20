"""Hand over the v3 front page for news-image-20261119.

The entry is a single picture that sums up Thursday 19 November
2026: 42 stories checked against the day's reporting, led by the
first Trump-Xi-Putin meeting in Shenzhen, the worldwide GTA VI
launch, and Anthropic's record $81.3bn IPO, with a grid of smaller
stories, a world map, a numbered brief list, and a box that names the
big stories which actually broke on Wednesday 18 November, so none
of them is presented as today's news.

The picture was composed in advance and sits next to this script as
entry.png. Nothing here draws or downloads anything: the script
inspects those bytes, confirms they form one whole JPEG within the
competition's limits, and places an unchanged copy in the output
directory. There is no network use, no clock, and no randomness, so
running it twice produces identical bytes both times.
"""

from __future__ import annotations

import os
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().with_name("entry.png")
TARGET_NAME = "entry.png"
FILE_LIMIT = 1_048_576
EDGE_LIMIT = 1024
JPEG_START = b"\xff\xd8"
JPEG_END = b"\xff\xd9"
FRAME_KINDS = frozenset((0xC0, 0xC1, 0xC2))
LONE_MARKERS = frozenset((0x01, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7))


class BadPicture(Exception):
    """Raised when the shipped picture fails any validation step."""


def read_image() -> bytes:
    """Load the shipped picture, rejecting anything malformed."""
    try:
        blob = SOURCE.read_bytes()
    except FileNotFoundError:
        raise BadPicture("entry.png is not present beside main.py")
    if len(blob) > FILE_LIMIT:
        raise BadPicture("entry.png exceeds the 1 MiB cap")
    if blob[:2] != JPEG_START:
        raise BadPicture("entry.png does not start with a JPEG SOI marker")
    if blob[-2:] != JPEG_END:
        raise BadPicture("entry.png does not end with a JPEG EOI marker")
    return blob


def segment_length(blob: bytes, at: int) -> int:
    """Return how many bytes a marker segment occupies, header included."""
    return 2 + struct.unpack(">H", blob[at + 2:at + 4])[0]


def find_frame_size(blob: bytes) -> tuple[int, int]:
    """Measure the picture from its JPEG frame header.

    Steps through the marker segments from the start, jumping over
    each one by its declared size, until a frame segment reports the
    dimensions. A segment that overruns the file, or a file with no
    frame segment, is rejected. The walk stops at the scan segment:
    compressed data follows it until the EOI marker that read_image
    already confirmed is the file's last two bytes.
    """
    offset = 2
    size: tuple[int, int] | None = None
    while offset + 9 <= len(blob):
        if blob[offset] != 0xFF:
            raise BadPicture("entry.png has a broken JPEG segment")
        kind = blob[offset + 1]
        if kind in FRAME_KINDS:
            tall, wide = struct.unpack(">HH", blob[offset + 5:offset + 9])
            size = (wide, tall)
        if kind in (0xD9, 0xDA):
            break
        if kind in LONE_MARKERS:
            offset += 2
            continue
        jump = segment_length(blob, offset)
        if offset + jump > len(blob):
            raise BadPicture("entry.png has a cut-off JPEG segment")
        offset += jump
    if size is None:
        raise BadPicture("entry.png carries no JPEG frame header")
    if size[0] <= 0 or size[1] <= 0:
        raise BadPicture("entry.png reports a zero side")
    return size


def place_image(blob: bytes) -> None:
    """Confirm the size, then copy the picture to the output folder."""
    wide, tall = find_frame_size(blob)
    if wide > EDGE_LIMIT or tall > EDGE_LIMIT:
        raise BadPicture("entry.png is wider or taller than 1024 pixels")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / TARGET_NAME
    destination.write_bytes(blob)
    if destination.read_bytes() != blob:
        raise BadPicture("the copied entry.png differs from the validated one")
    delivered_wide, delivered_tall = find_frame_size(destination.read_bytes())
    if (delivered_wide, delivered_tall) != (wide, tall):
        raise BadPicture("the copied entry.png measures differently from the validated one")


def run() -> int:
    """Validate the picture and deliver it, reporting problems plainly."""
    try:
        blob = read_image()
        place_image(blob)
    except BadPicture as problem:
        print(f"error: {problem}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
