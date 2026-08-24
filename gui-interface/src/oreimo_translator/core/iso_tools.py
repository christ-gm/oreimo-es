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
full rebuild is unavoidable - and note that such a rebuild must also
replace `first.dat`, whose embedded seekmap indexes absolute offsets into
RES.DAT and goes stale the moment anything shifts (see core/seekmap.py
and FORMAT_NOTES.md §24). `rebuild_iso_with_files()` does this
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
import io
import os
import platform
import shutil
import struct
import subprocess
import sys
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


def _mkisofs_executable() -> str | None:
    """Locates mkisofs: first on PATH, then the oreimo-es repo's own
    tool-bin copy - mkisofs.exe (standalone cygwin binary) on Windows,
    or the WSL shim wrapping it elsewhere. Walks upwards from this file
    (source checkout) and from the executable (PyInstaller build) since
    the frozen layout nests deeper than src/."""
    found = shutil.which("mkisofs")
    if found:
        return found
    # platform order matters: on POSIX the bash shim converts POSIX paths
    # for the cygwin binary; native Windows wants the .exe directly.
    names = ("mkisofs", "mkisofs.exe") if os.name != "nt" else ("mkisofs.exe", "mkisofs")
    starts = [Path(__file__).resolve()]
    if getattr(sys, "frozen", False):
        # onedir/onefile builds: PyInstaller unpacks bundled binaries here
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            starts.append(Path(meipass) / "tool-bin")  # sentinel: exact match below
        starts.append(Path(sys.executable).resolve())
    for start in starts:
        if start.name == "tool-bin":
            for name in names:
                cand = start / name
                if cand.is_file():
                    return str(cand)
            continue
        d = start.parent
        for _ in range(8):
            for name in names:
                cand = d / "tool-bin" / name
                if cand.is_file():
                    return str(cand)
            if d.parent == d:
                break
            d = d.parent
    return None


def mkisofs_available() -> bool:
    return _mkisofs_executable() is not None


def _locate_file_offset(iso_path: str, inner_path: str) -> tuple[int, int]:
    """Returns (byte_offset, length) of a file on the disc, from its
    ISO9660 directory record. Cross-checked against the independent
    raw-magic-scan locator for RES.DAT (both report 40056832 on this
    game's disc) before being trusted for in-place patching."""
    import pycdlib

    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    try:
        record = iso.get_record(iso_path=inner_path)
        return record.extent_location() * 2048, record.get_data_length()
    finally:
        iso.close()


def patch_files_into_iso(source_iso_path: str, replacements: dict[str, bytes], output_iso_path: str):
    """Clones the ISO and overwrites each replacement in place, without
    touching the filesystem structure. Every replacement must be exactly
    the same size as the file it replaces - anything else would run into
    neighbouring data on the disc. This is the fast, dependency-free path
    (no mkisofs); callers fall back to rebuild_iso_with_files when a size
    actually changed."""
    located = {}
    for inner_path, new_bytes in replacements.items():
        offset, length = _locate_file_offset(source_iso_path, inner_path)
        if len(new_bytes) != length:
            raise IsoError(
                f"refusing to patch: new {inner_path} is {len(new_bytes)} bytes, "
                f"original is {length}. Writing a different size would overwrite "
                f"real data adjacent to it on the disc."
            )
        located[inner_path] = offset

    _clone_file(source_iso_path, output_iso_path)

    with open(output_iso_path, "r+b") as f:
        for inner_path, new_bytes in replacements.items():
            f.seek(located[inner_path])
            f.write(new_bytes)


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


RES_DAT_ISO_PATH = "/PSP_GAME/INSDIR/RES.DAT"
FIRST_DAT_ISO_PATH = "/PSP_GAME/USRDIR/first.dat"
# UMD_DATA.BIN lives at the ISO root on standard PSP images; some
# repacks place it under SYSDIR, so probe both.
UMD_DATA_ISO_PATHS = ("/UMD_DATA.BIN", "/PSP_GAME/SYSDIR/UMD_DATA.BIN")

# Oreimo Portable ga Tsuzuku Wake ga Nai disc serials
DISC_SERIALS = {
    "NPJH-50568": "Disco 1",
    "NPJH-50569": "Disco 2",
}


def detect_disc(iso_path: str) -> str | None:
    """Returns the UMD serial of the ISO (e.g. 'NPJH-50568' for disc 1,
    'NPJH-50569' for disc 2), or None if it can't be determined."""
    import re

    for inner in UMD_DATA_ISO_PATHS:
        try:
            data = read_file(iso_path, inner)
        except Exception:
            continue
        m = re.search(rb"NPJH-\d{5}", data)
        if m:
            return m.group(0).decode("ascii")
    return None


def read_file(iso_path: str, inner_path: str) -> bytes:
    """Reads one file out of the ISO by its path on disc (e.g.
    FIRST_DAT_ISO_PATH), via pycdlib. Unlike read_res_dat's raw magic
    scan, this works for any file regardless of content."""
    import pycdlib

    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    try:
        buf = io.BytesIO()
        iso.get_file_from_iso_fp(buf, iso_path=inner_path)
        return buf.getvalue()
    finally:
        iso.close()


def rebuild_iso_with_files(source_iso_path: str, replacements: dict[str, bytes], output_iso_path: str):
    """Full rebuild path, used when a replacement file's size differs from
    the original (patch_res_dat_into_iso can't handle that case at all).
    Extracts every file off the original ISO (pycdlib), swaps in each
    entry of `replacements` ({iso_path: new_bytes}, e.g.
    {RES_DAT_ISO_PATH: ..., FIRST_DAT_ISO_PATH: ...}), and repacks with
    real mkisofs using the validated flag set (see module docstring).
    Raises IsoError if mkisofs isn't installed - this is an external
    dependency (cdrtools), unlike the same-size patch path which needs
    nothing beyond the stdlib."""
    mkisofs = _mkisofs_executable()
    if not mkisofs:
        raise IsoError(
            "mkisofs not found on PATH. Rebuilding the ISO (needed for this "
            "compile, because a rebuilt file changed size) requires real "
            "mkisofs from cdrtools - install it (macOS: `brew install "
            "cdrtools`; Windows/Linux: see the project README) and try again."
        )

    import tempfile

    with tempfile.TemporaryDirectory(prefix="oreimo_iso_rebuild_") as tmp:
        staging = Path(tmp) / "staging"
        _extract_iso_tree(source_iso_path, staging)

        for inner_path, new_bytes in replacements.items():
            staged = staging / inner_path.lstrip("/")
            if not staged.is_file():
                raise IsoError(f"could not locate {inner_path} in the extracted ISO tree")
            staged.write_bytes(new_bytes)

        proc = subprocess.run(
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
        # Some cygwin mkisofs builds exit 0 even when they fail (e.g. a
        # staging path they can't resolve) - trust the output file, not
        # the exit code.
        if not Path(output_iso_path).is_file():
            raise IsoError(
                f"mkisofs reported success but no ISO was written to "
                f"{output_iso_path}. stderr:\n{(proc.stderr or '').strip()[-800:]}"
            )
