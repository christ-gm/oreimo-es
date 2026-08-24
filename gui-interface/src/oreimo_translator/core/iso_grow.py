"""
Writes replacement files into an ISO9660 image *without* re-mastering it,
including when a replacement is larger than the file it replaces.

Why this exists
---------------
The obvious way to put a bigger file on a disc is to rebuild the whole
image with mkisofs. That works (see iso_tools.rebuild_iso_with_files) but
drags in cdrtools, a third-party dependency that isn't installable in one
step on every platform, and it re-masters 1.4 GB to accommodate a change
that is usually a few kilobytes. Importing the full Spanish translation of
disc 1 grows RES.DAT by 14,336 bytes - seven sectors - and first.dat not
at all.

The cheaper route is to edit the filesystem in place. A file's location
and size live in exactly two 32-bit fields of its ISO9660 directory
record (extent LBA and data length, each stored twice, little- then
big-endian). Point those at a different run of sectors and the file
*is* somewhere else, as far as any reader is concerned - the PSP included,
which reaches its files through the standard filesystem. Nothing else on
the disc encodes where a file sits: the path tables record directory
locations only, and first.dat's seekmap holds offsets *within* RES.DAT,
not disc addresses (those are regenerated separately, see seekmap.py).

Where the extra sectors come from
---------------------------------
This game's disc is packed with zero gaps between files, but it ends with
/PSP_GAME/INSDIR/DUMMY.DAT: 64,356,352 bytes of pure zeros, the filler
publishers add to pad a UMD to its pressed size. That is 31,424 reclaimable
sectors, and it is verified to be all-zero at runtime before being touched
- a file with any non-zero byte in it is left alone, whatever it is called.

The allocator is deliberately conservative. It will only ever hand out
space from two places it can prove are safe:

  1. the reclaimable filler, once verified all-zero, and
  2. everything past the last sector any file occupies.

It never tries to reuse arbitrary-looking gaps, because a "gap" in a
naive file-only scan is exactly where a directory extent or a path table
would hide, and overwriting one of those corrupts the disc in a way that
is tedious to diagnose. Being unable to find a hole is not a failure mode
here - the image can always be extended at the end.

Strategies, in order of preference
----------------------------------
  1. Same size            -> overwrite the data where it lies.
  2. Free space follows   -> leave the file put, widen its length field.
  3. Evict the neighbours -> if the files immediately behind it can be
                             relocated into free space, move them and then
                             widen. This is the case that matters here:
                             bgm.awb (26,351 sectors) fits inside the
                             filler (31,424), so RES.DAT grows into the
                             room bgm.awb vacates and the image never
                             changes size at all.
  4. Relocate the file    -> move it whole into a free run big enough.
  5. Extend the image     -> always available, always works, costs bytes.

Every strategy ends the same way: patch the directory records, then
correct volume_space_size in every volume descriptor (this disc carries
two, a PVD and the extra descriptor `-iso-level 4` emits; both point at
the same directory tree, so there is only ever one set of records to fix).

Validated by reading every file back out of the result and comparing it
byte for byte against the source - see tools/verify_iso.py.
"""
import os
import shutil
import struct
from dataclasses import dataclass

SECTOR = 2048

# Filler files that may be consumed for space, if and only if their
# contents turn out to be entirely zero.
RECLAIMABLE = ("/PSP_GAME/INSDIR/DUMMY.DAT",)


class IsoGrowError(Exception):
    pass


@dataclass(eq=False)  # identity semantics: entries are tracked in sets/dicts
class Entry:
    """One file or directory, and where its directory record lives."""
    path: str
    extent: int         # starting LBA
    length: int         # size in bytes
    record_offset: int  # byte offset of the record itself, for patching
    is_dir: bool

    @property
    def sectors(self) -> int:
        return (self.length + SECTOR - 1) // SECTOR

    @property
    def end(self) -> int:
        """First LBA past this entry."""
        return self.extent + self.sectors


# ---------------------------------------------------------------------
# reading the filesystem
# ---------------------------------------------------------------------

def _u32_le(buf, off):
    return struct.unpack_from("<I", buf, off)[0]


def _volume_descriptors(f) -> list[int]:
    """LBAs of every volume descriptor that carries a volume_space_size
    worth correcting (types 1 and 2), stopping at the terminator."""
    lbas = []
    lba = 16
    while lba < 64:
        f.seek(lba * SECTOR)
        vd = f.read(SECTOR)
        if len(vd) < 7 or vd[1:6] != b"CD001":
            raise IsoGrowError(f"no ISO9660 volume descriptor at LBA {lba}")
        if vd[0] == 255:
            return lbas
        if vd[0] in (1, 2):
            lbas.append(lba)
        lba += 1
    raise IsoGrowError("volume descriptor set has no terminator")


def _walk(f, dir_lba: int, dir_len: int, path: str, out: list, depth: int = 0):
    f.seek(dir_lba * SECTOR)
    data = f.read(dir_len)
    pos = 0
    while pos < len(data):
        rec_len = data[pos]
        if rec_len == 0:
            # records never straddle a sector; the rest is padding
            nxt = (pos // SECTOR + 1) * SECTOR
            if nxt >= len(data):
                break
            pos = nxt
            continue
        rec = data[pos:pos + rec_len]
        ident_len = rec[32]
        ident = rec[33:33 + ident_len]
        # '.' and '..' are self/parent links, not entries of their own
        if not (ident_len == 1 and ident in (b"\x00", b"\x01")):
            name = ident.decode("ascii", "replace").split(";")[0]
            is_dir = bool(rec[25] & 2)
            entry = Entry(
                path=f"{path}/{name}",
                extent=_u32_le(rec, 2),
                length=_u32_le(rec, 10),
                record_offset=dir_lba * SECTOR + pos,
                is_dir=is_dir,
            )
            out.append(entry)
            if is_dir and depth < 8:
                _walk(f, entry.extent, entry.length, entry.path, out, depth + 1)
        pos += rec_len
    return out


def read_entries(f) -> list[Entry]:
    """Every file and directory on the disc, with the byte offset of the
    directory record describing each."""
    vds = _volume_descriptors(f)
    if not vds:
        raise IsoGrowError("no primary volume descriptor")
    f.seek(vds[0] * SECTOR)
    pvd = f.read(SECTOR)
    root = pvd[156:190]
    return _walk(f, _u32_le(root, 2), _u32_le(root, 10), "", [])


def _volume_sectors(f) -> int:
    f.seek(16 * SECTOR)
    return _u32_le(f.read(SECTOR), 80)


# ---------------------------------------------------------------------
# writing the filesystem
# ---------------------------------------------------------------------

def _patch_record(f, record_offset: int, extent: int, length: int):
    """Rewrites a directory record's extent and data-length fields. Both
    are 'both-endian': the little-endian copy first, then the big-endian
    one, and a reader is entitled to believe either - so both must be
    written or the disc contradicts itself."""
    f.seek(record_offset + 2)
    f.write(struct.pack("<I", extent) + struct.pack(">I", extent))
    f.seek(record_offset + 10)
    f.write(struct.pack("<I", length) + struct.pack(">I", length))


def _patch_volume_size(f, vd_lbas: list[int], sectors: int):
    for lba in vd_lbas:
        f.seek(lba * SECTOR + 80)
        f.write(struct.pack("<I", sectors) + struct.pack(">I", sectors))


def _is_all_zero(f, extent: int, length: int) -> bool:
    f.seek(extent * SECTOR)
    remaining = length
    while remaining > 0:
        chunk = f.read(min(1 << 20, remaining))
        if not chunk:
            return False
        if chunk.count(0) != len(chunk):
            return False
        remaining -= len(chunk)
    return True


def _copy_run(f, src_lba: int, dst_lba: int, length: int):
    """Moves file data to a different run of sectors. Source and target
    never overlap - targets only ever come from free space - so a plain
    forward chunked copy is safe."""
    remaining = length
    src = src_lba * SECTOR
    dst = dst_lba * SECTOR
    while remaining > 0:
        n = min(1 << 22, remaining)
        f.seek(src)
        data = f.read(n)
        if len(data) != n:
            raise IsoGrowError("short read while relocating file data")
        f.seek(dst)
        f.write(data)
        src += n
        dst += n
        remaining -= n


# ---------------------------------------------------------------------
# free space
# ---------------------------------------------------------------------

class FreeSpace:
    """A sorted list of free [start, end) sector runs, plus the ability
    to grow the image when the runs are exhausted."""

    def __init__(self, runs: list[tuple[int, int]], volume_end: int):
        self.runs = sorted(r for r in runs if r[1] > r[0])
        self.volume_end = volume_end  # first LBA past the image

    def _merge(self):
        merged = []
        for start, end in sorted(self.runs):
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        self.runs = merged

    def release(self, start: int, end: int):
        if end > start:
            self.runs.append((start, end))
            self._merge()

    def free_at(self, lba: int) -> int:
        """How many free sectors run consecutively starting exactly at
        `lba`. Zero if that sector is occupied."""
        for start, end in self.runs:
            if start <= lba < end:
                return end - lba
        return 0

    def take(self, start: int, count: int):
        """Removes [start, start+count) from the pool; it must be free."""
        for i, (s, e) in enumerate(self.runs):
            if s <= start and start + count <= e:
                self.runs.pop(i)
                self.release(s, start)
                self.release(start + count, e)
                return
        raise IsoGrowError(f"internal: {count} sectors at {start} were not free")

    def allocate(self, count: int) -> int:
        """Smallest free run that fits, to keep large runs intact. Falls
        back to extending the image past its current end."""
        best = None
        for start, end in self.runs:
            if end - start >= count and (best is None or (end - start) < (best[1] - best[0])):
                best = (start, end)
        if best is not None:
            self.take(best[0], count)
            return best[0]
        start = self.volume_end
        self.volume_end += count
        return start


# ---------------------------------------------------------------------
# the operation
# ---------------------------------------------------------------------

def write_files_into_iso(
    source_iso_path: str,
    replacements: dict[str, bytes],
    output_iso_path: str,
    progress_callback=None,
) -> dict:
    """Writes `replacements` (inner ISO path -> new bytes) into a copy of
    `source_iso_path`, resizing files as needed. The source is never
    modified. Returns a report describing what had to move."""

    def progress(msg):
        if progress_callback:
            progress_callback(msg)

    progress("Copiando la imagen...")
    if os.path.abspath(source_iso_path) == os.path.abspath(output_iso_path):
        raise IsoGrowError("output ISO must be a different file from the source")
    shutil.copyfile(source_iso_path, output_iso_path)

    report = {"grown": [], "moved": [], "reclaimed": [], "image_grew_by": 0}

    with open(output_iso_path, "r+b") as f:
        vd_lbas = _volume_descriptors(f)
        entries = read_entries(f)
        files = [e for e in entries if not e.is_dir]
        by_path = {e.path.upper(): e for e in files}

        for inner in replacements:
            if inner.upper() not in by_path:
                raise IsoGrowError(f"{inner} is not on this disc")

        volume_end = _volume_sectors(f)
        original_volume_end = volume_end

        # Free space, conservatively: verified-zero filler, plus the tail
        # past the last sector any file occupies. Directory extents and
        # path tables live below the first file on this layout and are
        # never considered.
        runs = []
        targets = {by_path[p.upper()] for p in replacements}
        for entry in files:
            if entry.path.upper() in (r.upper() for r in RECLAIMABLE) and entry not in targets:
                progress(f"Comprobando {entry.path}...")
                if _is_all_zero(f, entry.extent, entry.length):
                    runs.append((entry.extent, entry.end))
                    report["reclaimed"].append(entry.path)
        last_used = max((e.end for e in files if e.path not in report["reclaimed"]), default=0)
        if volume_end > last_used:
            runs.append((last_used, volume_end))

        free = FreeSpace(runs, volume_end)
        # A reclaimed filler is no longer a file: drop its record so
        # nothing points at sectors we are about to hand out.
        for entry in files:
            if entry.path in report["reclaimed"]:
                _patch_record(f, entry.record_offset, entry.extent, 0)

        occupied = {}  # start LBA -> entry, for finding eviction victims
        for entry in files:
            if entry.path not in report["reclaimed"]:
                occupied[entry.extent] = entry

        for inner, new_bytes in replacements.items():
            entry = by_path[inner.upper()]
            old_sectors = entry.sectors
            new_sectors = (len(new_bytes) + SECTOR - 1) // SECTOR

            if new_sectors <= old_sectors:
                # Fits where it is. Any sectors it stops using go back to
                # the pool, and the length field shrinks to match.
                progress(f"Escribiendo {entry.path}...")
                f.seek(entry.extent * SECTOR)
                f.write(new_bytes)
                _pad_to_sector(f, len(new_bytes))
                free.release(entry.extent + new_sectors, entry.end)
                _patch_record(f, entry.record_offset, entry.extent, len(new_bytes))
                continue

            need = new_sectors - old_sectors
            placed = False

            # 2. free space already follows it
            if free.free_at(entry.end) >= need:
                free.take(entry.end, need)
                placed = True
                report["grown"].append((entry.path, entry.extent, need))

            # 3. evict whatever is behind it, if that can be rehomed
            if not placed:
                if _evict_following(f, entry, need, free, occupied, report, progress):
                    placed = True
                    report["grown"].append((entry.path, entry.extent, need))

            # 4/5. move the file itself - into a free run, or past the end
            if not placed:
                dest = free.allocate(new_sectors)
                progress(f"Reubicando {entry.path}...")
                free.release(entry.extent, entry.end)
                del occupied[entry.extent]
                report["moved"].append((entry.path, entry.extent, dest))
                entry.extent = dest
                occupied[dest] = entry

            progress(f"Escribiendo {entry.path}...")
            f.seek(entry.extent * SECTOR)
            f.write(new_bytes)
            _pad_to_sector(f, len(new_bytes))
            _patch_record(f, entry.record_offset, entry.extent, len(new_bytes))
            entry.length = len(new_bytes)

        # The image may now be longer than the volume claims.
        new_volume_end = max(free.volume_end, max(e.end for e in occupied.values()))
        if new_volume_end > original_volume_end:
            report["image_grew_by"] = (new_volume_end - original_volume_end) * SECTOR
        _patch_volume_size(f, vd_lbas, new_volume_end)
        f.truncate(new_volume_end * SECTOR)
        f.flush()
        os.fsync(f.fileno())

    return report


def _pad_to_sector(f, length: int):
    """Zero-fills the tail of the last sector a write landed in, so no
    fragment of the previous occupant shows through."""
    rem = length % SECTOR
    if rem:
        f.write(b"\x00" * (SECTOR - rem))


def _evict_following(f, entry: Entry, need: int, free: FreeSpace,
                     occupied: dict, report: dict, progress) -> bool:
    """Tries to clear `need` sectors immediately behind `entry` by moving
    the files sitting there somewhere else. Returns False - having changed
    nothing - if the files can't all be rehomed, or if the region holds
    anything this code can't account for."""
    victims = []
    cursor = entry.end
    freed = 0
    while freed < need:
        run = free.free_at(cursor)
        if run:
            freed += run
            cursor += run
            continue
        victim = occupied.get(cursor)
        if victim is None:
            return False  # unknown occupant - refuse to guess
        victims.append(victim)
        freed += victim.sectors
        cursor += victim.sectors

    # Every victim must fit in free space that isn't the room we're
    # clearing, or the move is pointless. Reserve tentatively, and only
    # commit once they all have a home.
    plan = []
    scratch = FreeSpace([r for r in free.runs if r[1] <= entry.end or r[0] >= cursor],
                        free.volume_end)
    for victim in victims:
        dest = scratch.allocate(victim.sectors)
        if dest >= free.volume_end:
            return False  # would extend the image; strategy 4/5 is simpler
        plan.append((victim, dest))

    for victim, dest in plan:
        progress(f"Moviendo {victim.path}...")
        _copy_run(f, victim.extent, dest, victim.length)
        _patch_record(f, victim.record_offset, dest, victim.length)
        report["moved"].append((victim.path, victim.extent, dest))
        del occupied[victim.extent]
        victim.extent = dest
        occupied[dest] = victim

    free.runs = scratch.runs
    free.release(entry.end, cursor)
    free.take(entry.end, need)
    return True
