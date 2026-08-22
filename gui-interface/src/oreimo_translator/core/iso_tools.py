"""
ISO-level helpers: locate RES.DAT inside a raw PSP ISO file, read it, and
patch a same-size RES.DAT back into a clone of the ISO without a full
rebuild.

Pure Python, no OS-specific tools (no mounting) and no assumption about
the ISO9660 filesystem layout - RES.DAT is found by scanning the raw
bytes for the GPDA container format's own magic/size header. Works
identically on macOS, Windows, and Linux.

Why binary-patch instead of rebuilding the ISO from scratch: see the
sibling reverse-engineering project's documentation/FORMAT_NOTES.md §13 —
a full `xorriso` rebuild silently broke the game (a module failed to load,
infinite hang). Binary-patching RES.DAT in place, keeping everything else
byte-identical to the original disc, works perfectly and is what this
project uses in production.
"""
import platform
import shutil
import struct
import subprocess
from pathlib import Path


class IsoError(RuntimeError):
    pass


def _find_res_dat_span(data: bytes) -> tuple[int, int]:
    """Locates RES.DAT's (offset, size) within a raw ISO byte buffer by
    scanning for every 'GPDA' magic occurrence and picking the one with
    the largest self-declared size (the 4-byte field immediately after
    the magic). This works without mounting the ISO or parsing its
    filesystem: RES.DAT is itself built of many smaller nested GPDA blobs
    (one per scene, etc - all of which also start with the same magic and
    are necessarily smaller since they're contained within it), and
    first.dat (the only other top-level GPDA file on this disc) is
    ~1.7MB vs RES.DAT's ~205MB - so the single largest declared size
    unambiguously identifies RES.DAT's own top-level header."""
    best_offset, best_size = None, -1
    idx = 0
    while True:
        idx = data.find(b"GPDA", idx)
        if idx == -1:
            break
        if idx + 8 <= len(data):
            declared_size = struct.unpack_from("<I", data, idx + 4)[0]
            if declared_size > best_size and idx + declared_size <= len(data):
                best_offset, best_size = idx, declared_size
        idx += 1
    if best_offset is None:
        raise IsoError("no GPDA blob found in this file - is it a valid ISO for this game?")
    return best_offset, best_size


def read_res_dat(iso_path: str) -> bytes:
    """Reads RES.DAT's bytes directly out of the raw ISO file."""
    data = Path(iso_path).read_bytes()
    offset, size = _find_res_dat_span(data)
    return data[offset:offset + size]


def locate_res_dat_offset(iso_path: str, expected_size: int | None = None) -> int:
    """Returns RES.DAT's byte offset within the ISO. If expected_size is
    given, raises if the found blob's declared size doesn't match (a
    sanity check for callers that already know the size independently)."""
    data = Path(iso_path).read_bytes()
    offset, size = _find_res_dat_span(data)
    if expected_size is not None and size != expected_size:
        raise IsoError(
            f"expected a RES.DAT of size {expected_size}, found one of size "
            f"{size} at offset {offset} instead"
        )
    return offset


def _clone_file(source_path: str, dest_path: str):
    """Copies source_path to dest_path. Uses an APFS clonefile (instant,
    no extra disk space) on macOS when possible; falls back to a regular
    copy everywhere else (Windows, Linux, or if cloning isn't supported
    on the source volume)."""
    if platform.system() == "Darwin":
        try:
            subprocess.run(["/bin/cp", "-c", source_path, dest_path], check=True, capture_output=True)
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    shutil.copy2(source_path, dest_path)


def patch_res_dat_into_iso(source_iso_path: str, new_res_dat: bytes, output_iso_path: str):
    """Clones source_iso_path to output_iso_path, then overwrites the
    RES.DAT region in place with new_res_dat. Refuses if new_res_dat isn't
    the exact same size as the RES.DAT currently in the source ISO —
    writing a different size would corrupt whatever data follows RES.DAT
    on disc (confirmed non-zero/real data, not padding)."""
    original_res_dat = read_res_dat(source_iso_path)
    if len(new_res_dat) != len(original_res_dat):
        raise IsoError(
            f"refusing to patch: new RES.DAT is {len(new_res_dat)} bytes, "
            f"original is {len(original_res_dat)} bytes. Writing a different "
            f"size would overwrite real data adjacent to RES.DAT on the disc."
        )

    offset = locate_res_dat_offset(source_iso_path, len(original_res_dat))

    _clone_file(source_iso_path, output_iso_path)

    with open(output_iso_path, "r+b") as f:
        f.seek(offset)
        magic = f.read(4)
        if magic != b"GPDA":
            raise IsoError(f"expected GPDA magic at offset {offset} in the clone, got {magic!r}")
        f.seek(offset)
        f.write(new_res_dat)
