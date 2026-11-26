#!/usr/bin/env python3
"""Entry point for the news-image-20261125 front page (b123-numbers).

The entry image is rendered at build time by gen.py (which uses Pillow) and
committed to this repository as entry.png, a 1024x1024 front page with 50
stories from Wednesday, November 25, 2026: three heroes (Trump tariffs on 14
trade partners, the Kospi -6.16% chip rout, and Shenzhou-24 carrying the first
foreign astronaut to Tiangong), ten news cards, a 13-pin world map with a
readable key, a 37-item ALSO column, a DATE CHECK strip, a number strip, and
a source footer (Reuters, AP, BBC, CNN, Xinhua, Korea Exchange, pm.gov.au).

This file is intentionally STANDARD LIBRARY ONLY (os, shutil, struct, sys,
hashlib). The grader runs it in a minimal environment where nothing beyond
the standard library is installed, so it must never import Pillow, numpy, or
any other third-party package; it only copies the pre-rendered entry.png
into the output directory the grader provides through MAKEFUN_OUTPUT_DIR.

Behaviour: resolve the repository directory from this file's own location,
read entry.png next to it, verify that the bytes are a real PNG image of the
expected 1024x1024 size by parsing the IHDR chunk with the struct module,
create the output directory if it does not exist yet, copy the file there
atomically (write to a temporary name in the same directory, then rename it
into place so a concurrent reader never sees a half-written file), and
finally re-read the destination and compare SHA-256 digests so a truncated
or corrupted copy is reported as a failure instead of a silent success.

Usage: python3 main.py (no arguments). Exit code 0 means entry.png was
copied and verified; any other exit code means the copy failed and the
reason is printed to stderr. The destination defaults to ./out/entry.png
when MAKEFUN_OUTPUT_DIR is not set, which keeps local runs working too.
"""

import hashlib
import os
import shutil
import struct
import sys

# The entry image committed next to this file, and its expected geometry.
SOURCE_NAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    """Print an error to stderr and exit non-zero; used for every fatal check."""
    print("main.py: error: %s" % message, file=sys.stderr)
    return 1


def read_png_size(path):
    """Parse the IHDR chunk of a PNG file and return (width, height).

    Reads only the first 33 bytes (8-byte signature + 25-byte IHDR chunk),
    so this works even on very large files, and raises ValueError when the
    file is not a PNG at all or is too short to contain a valid header.
    """
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError("%s is not a PNG file (bad signature)" % path)
    chunk_length, chunk_type = struct.unpack(">I4s", header[8:16])
    if chunk_type != b"IHDR" or chunk_length != 13:
        raise ValueError("%s has no valid IHDR chunk" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_of(path):
    """Return the hex SHA-256 digest of a file, streamed in 1 MiB blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def copy_entry(source_path, destination_path):
    """Copy source_path to destination_path atomically, then verify it.

    The copy goes through a temporary sibling file (destination + ".tmp")
    and os.replace, so the destination is either the complete old file or
    the complete new file, never a partial write. After the rename, the
    SHA-256 of source and destination must match, otherwise the copy is
    reported as failed even though the file exists at the destination.
    """
    tmp_path = destination_path + ".tmp"
    shutil.copyfile(source_path, tmp_path)
    os.replace(tmp_path, destination_path)
    dest_width, dest_height = read_png_size(destination_path)
    if (dest_width, dest_height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError("destination image is %dx%d, expected %dx%d"
                         % (dest_width, dest_height,
                            EXPECTED_WIDTH, EXPECTED_HEIGHT))
    if sha256_of(source_path) != sha256_of(destination_path):
        raise ValueError("checksum mismatch after copying to %s" % destination_path)
    return os.path.getsize(destination_path)


def main():
    """Copy entry.png into MAKEFUN_OUTPUT_DIR and verify the result."""
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(repo_dir, SOURCE_NAME)
    if not os.path.isfile(source_path):
        return fail("source image %s not found next to main.py" % source_path)
    try:
        width, height = read_png_size(source_path)
    except (OSError, ValueError) as exc:
        return fail("cannot validate source image: %s" % exc)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return fail("source image is %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        out_dir = "out"
    destination_path = os.path.join(out_dir, SOURCE_NAME)
    try:
        os.makedirs(out_dir, exist_ok=True)
        copied_bytes = copy_entry(source_path, destination_path)
    except (OSError, ValueError) as exc:
        return fail("copy failed: %s" % exc)
    print("main.py: copied %s (%d bytes, %dx%d, sha256 %s) -> %s"
          % (SOURCE_NAME, copied_bytes, width, height,
             sha256_of(destination_path), destination_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
