"""Copy the pre-rendered entry image to the grader output directory.

The entry image (entry.png) sits next to this script. This program
copies it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png using only
the Python standard library, so it runs in a bare grader image where
nothing extra is installed.
"""

import os
import shutil


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, "entry.png")
    if not os.path.isfile(source):
        raise SystemExit("entry.png not found next to main.py: " + source)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)


if __name__ == "__main__":
    main()
