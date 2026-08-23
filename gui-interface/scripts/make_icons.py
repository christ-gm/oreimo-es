#!/usr/bin/env python3
"""Converts the master app icon (assets/icon.png) into the per-platform
formats PyInstaller needs: assets/icon.ico for the Windows executable and
assets/icon.icns for the macOS .app bundle.

Both outputs are COMMITTED to the repo rather than generated during CI,
because .icns generation needs macOS's `iconutil` and the Windows build
runner obviously doesn't have it. Re-run this script (on macOS) whenever
icon.png changes, and commit all three files together.

    python3 scripts/make_icons.py [--round-corners]

--round-corners applies macOS's standard rounded-square mask and margin
to the .icns only (the Windows .ico stays full-bleed, which is the
convention there). Use it when the source art is a full-bleed square;
skip it when the art already has its own shape and transparency, or the
mask will clip it.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MASTER = ASSETS / "icon.png"

# Windows .ico: every size Explorer/taskbar/alt-tab actually picks from.
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]

# macOS .iconset: Apple's required (name, pixel size) set. 1024 is the
# @2x of 512 and is what the App Store / Finder preview uses.
ICONSET = [
    ("icon_16x16.png", 16), ("icon_16x16@2x.png", 32),
    ("icon_32x32.png", 32), ("icon_32x32@2x.png", 64),
    ("icon_128x128.png", 128), ("icon_128x128@2x.png", 256),
    ("icon_256x256.png", 256), ("icon_256x256@2x.png", 512),
    ("icon_512x512.png", 512), ("icon_512x512@2x.png", 1024),
]

# Apple's icon grid: the artwork occupies ~80% of the canvas, with a
# corner radius of ~22.4% of the artwork's width.
MACOS_CONTENT_RATIO = 0.80
MACOS_CORNER_RATIO = 0.224


def apply_macos_shape(im: Image.Image) -> Image.Image:
    """Insets the artwork into the transparent margin macOS icons use and
    rounds its corners, so the app doesn't sit in the Dock as a hard
    square among rounded neighbours."""
    canvas_size = im.width
    content_size = round(canvas_size * MACOS_CONTENT_RATIO)
    radius = round(content_size * MACOS_CORNER_RATIO)

    content = im.resize((content_size, content_size), Image.LANCZOS)

    mask = Image.new("L", (content_size, content_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, content_size - 1, content_size - 1), radius=radius, fill=255
    )
    # intersect with the art's own alpha so existing transparency survives
    mask = Image.composite(content.getchannel("A"), Image.new("L", mask.size, 0), mask)
    content.putalpha(mask)

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    offset = (canvas_size - content_size) // 2
    canvas.paste(content, (offset, offset))
    return canvas


def load_master() -> Image.Image:
    if not MASTER.exists():
        sys.exit(
            f"missing {MASTER.relative_to(MASTER.parents[2])} - drop a square "
            f"1024x1024 PNG there first (see the app icon section of README.md)"
        )
    im = Image.open(MASTER).convert("RGBA")
    if im.width != im.height:
        sys.exit(f"icon.png must be square, got {im.width}x{im.height}")
    if im.width < 1024:
        print(f"warning: icon.png is only {im.width}px; 1024 is recommended so "
              f"the largest macOS/Retina sizes aren't upscaled", file=sys.stderr)
    if im.width != 1024:
        im = im.resize((1024, 1024), Image.LANCZOS)
    return im


def build_ico(im: Image.Image):
    out = ASSETS / "icon.ico"
    im.save(out, format="ICO", sizes=[(s, s) for s in ICO_SIZES])
    print(f"wrote {out.name} ({', '.join(f'{s}x{s}' for s in ICO_SIZES)})")


def build_icns(im: Image.Image):
    out = ASSETS / "icon.icns"
    if not shutil.which("iconutil"):
        # PIL can write .icns too, but only a subset of sizes and without
        # Apple's exact packing - fine as a fallback, not as the default.
        im.save(out, format="ICNS")
        print(f"wrote {out.name} via Pillow (no iconutil - run this on macOS "
              f"for a proper multi-resolution icns)")
        return

    with tempfile.TemporaryDirectory() as tmp:
        iconset = Path(tmp) / "icon.iconset"
        iconset.mkdir()
        for name, size in ICONSET:
            im.resize((size, size), Image.LANCZOS).save(iconset / name)
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset), "-o", str(out)], check=True
        )
    print(f"wrote {out.name} (16-1024px, via iconutil)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--round-corners", action="store_true",
        help="apply macOS's rounded-square mask and margin to the .icns"
    )
    args = parser.parse_args()

    master = load_master()
    build_ico(master)
    build_icns(apply_macos_shape(master) if args.round_corners else master)


if __name__ == "__main__":
    main()
