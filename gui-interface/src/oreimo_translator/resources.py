"""Locates bundled data files (currently just the app icon) whether the
app is running from source or frozen by PyInstaller, which unpacks
everything in the spec's `datas` into a temp dir and points
`sys._MEIPASS` at it."""
import sys
from pathlib import Path


def resource_path(relative: str) -> Path:
    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir is not None:
        return Path(bundle_dir) / relative
    # src/oreimo_translator/resources.py -> gui-interface/
    return Path(__file__).resolve().parents[2] / relative


def app_icon_path() -> Path | None:
    """Returns the master PNG icon, or None if it hasn't been added yet -
    the app is expected to run fine without one rather than crash."""
    path = resource_path("assets/icon.png")
    return path if path.exists() else None
