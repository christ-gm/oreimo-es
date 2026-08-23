"""
ISO-level helpers: locate RES.DAT inside a raw PSP ISO file, read it, and
either (a) patch a same-size RES.DAT back into a clone of the ISO without
a full rebuild (fast path, no external tools), or (b) do a full rebuild
when RES.DAT changed size (needed for image edits - see
documentation/FORMAT_NOTES.md §22).

RES.DAT lookup/patching is pure Python, no OS-specific tools (no mounting)
and no assumption about the ISO9660 filesystem layout - RES.DAT is found
by scanning the raw bytes for the GPDA container format's own magic/size
header. Works identically on macOS, Windows, and Linux.

Why binary-patch instead of rebuilding the ISO from scratch whenever
possible: see the sibling reverse-engineering project's
documentation/FORMAT_NOTES.md §13 — a full `xorriso -as mkisofs` rebuild
silently broke the game (psmf.prx failed to load, infinite hang).
Binary-patching RES.DAT in place, keeping everything else byte-identical
to the original disc, works perfectly for same-size changes and is the
default this project uses.

When RES.DAT's size DOES change (routine for image edits - see §22), a
full rebuild is unavoidable. `rebuild_iso_with_new_res_dat()` does this
using `pycdlib` (pure Python) to extract every file off the original ISO,
and real `mkisofs` (cdrtools) - NOT `xorriso` - to repack it, with the
exact flag set (`-iso-level 4 -xa ...`) taken from the sibling
`FastAsyncOreimoTranslateTool` project (already used in production to
ship a full translated build of this game) and confirmed by an actual
PPSSPP boot test to reach the title screen cleanly (§22), unlike the
`xorriso` attempt. The critical, previously-missing ingredient is `-xa`
(rationalized CD-ROM XA directory attributes) - `xorriso -as mkisofs`'s
emulation mode has no `-xa` equivalent at all (checked: absent from its
`-help` output), which is the most likely reason it silently produced a
disc the PSP firmware's module loader couldn't read correctly.
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


def mkisofs_available() -> bool:
    return shutil.which("mkisofs") is not None


def _extract_iso_tree(iso_path: str, dest_dir: Path):
    """Extracts every file off iso_path into dest_dir, preserving the
    exact directory structure and filename casing (this disc has no Rock
    Ridge/Joliet - pycdlib reads the raw, non-standard-but-tolerated
    lowercase/mixed-case primary ISO9660 identifiers directly; verified
    byte-for-byte against the trusted raw-byte-scan RES.DAT reader before
    this was trusted, see FORMAT_NOTES.md §22)."""
    import pycdlib

    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    try:
        for root, _dirs, files in iso.walk(iso_path="/"):
            root_rel = root.lstrip("/")
            out_dir = dest_dir / root_rel if root_rel else dest_dir
            out_dir.mkdir(parents=True, exist_ok=True)
            for fname in files:
                entry_iso_path = f"{root}/{fname}" if root != "/" else f"/{fname}"
                with open(out_dir / fname, "wb") as f:
                    iso.get_file_from_iso_fp(f, iso_path=entry_iso_path)
    finally:
        iso.close()


def rebuild_iso_with_new_res_dat(source_iso_path: str, new_res_dat: bytes, output_iso_path: str):
    """Full rebuild path, used when new_res_dat is NOT the same size as
    the original (patch_res_dat_into_iso can't handle that case at all).
    Extracts every file off the original ISO (pycdlib), swaps in
    new_res_dat, and repacks with real mkisofs using the validated flag
    set (see module docstring). Raises IsoError if mkisofs isn't
    installed - this is an external dependency (cdrtools), unlike the
    same-size patch path which needs nothing beyond the stdlib."""
    if not mkisofs_available():
        raise IsoError(
            "mkisofs not found on PATH. Rebuilding the ISO with a resized "
            "RES.DAT (needed for this compile) requires real mkisofs from "
            "cdrtools - install it (macOS: `brew install cdrtools`; "
            "Windows/Linux: see the project README) and try again."
        )

    import tempfile

    with tempfile.TemporaryDirectory(prefix="oreimo_iso_rebuild_") as tmp:
        staging = Path(tmp) / "staging"
        _extract_iso_tree(source_iso_path, staging)

        # find the staged RES.DAT by locating whichever extracted file has
        # the same size as the ORIGINAL RES.DAT (name casing on disc is
        # "RES.DAT", but resolved via search rather than assumed, in case
        # a future disc uses different casing)
        original_size = len(read_res_dat(source_iso_path))
        res_dat_path = None
        for candidate in staging.rglob("*"):
            if candidate.is_file() and candidate.stat().st_size == original_size and candidate.name.upper() == "RES.DAT":
                res_dat_path = candidate
                break
        if res_dat_path is None:
            raise IsoError("could not locate RES.DAT in the extracted ISO tree")
        res_dat_path.write_bytes(new_res_dat)

        mkisofs = shutil.which("mkisofs")
        subprocess.run(
            [
                mkisofs,
                "-iso-level", "4", "-xa",
                "-A", "PSP GAME",
                "-V", "OreImo",
                "-sysid", "PSP GAME",
                "-volset", "OreImo",
                "-p", "", "-publisher", "",
                "-o", str(output_iso_path),
                str(staging),
            ],
            check=True, capture_output=True, text=True,
        )
