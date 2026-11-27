"""news-image-20261127: copy the entry image to the output directory.

The image (image.jpg, shipped in this repository) sums up the world news
of Friday 27 November 2026 as a newspaper front page. This program only
copies it to $MAKEFUN_OUTPUT_DIR/entry.png and validates the result:
no network, no clock, no randomness, fully deterministic.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "image.jpg")
JPEG_MAGIC = b"\xff\xd8\xff"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as src:
        magic = src.read(3)
        if magic != JPEG_MAGIC:
            print("image.jpg is not a JPEG", file=sys.stderr)
            return 1
        src.seek(-2, os.SEEK_END)
        if src.read(2) != b"\xff\xd9":
            print("image.jpg is truncated (no JPEG end marker)", file=sys.stderr)
            return 1
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    if size == 0 or size > 1048576:
        print("output size out of range: %d" % size, file=sys.stderr)
        return 1
    with open(dest, "rb") as out:
        if out.read(3) != JPEG_MAGIC:
            print("output is not a JPEG", file=sys.stderr)
            return 1
    print("wrote %s (%d bytes)" % (dest, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
