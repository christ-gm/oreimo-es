"""
RES.DAT's seek index ("seekmap") - a plain-text table, gzip-compressed and
stored inside first.dat, listing the ABSOLUTE byte offset (and size) of
every single entry in RES.DAT's whole nested tree, ~7,700 lines for this
game.

WHY THIS MATTERS: the game seeks into RES.DAT using these recorded
offsets, not by walking the GPDA headers. Rebuilding RES.DAT with any
entry whose size changes shifts every later offset - and a stale seekmap
then points the game at the middle of unrelated data, which hangs it
(confirmed in-game: an image edit produced a build that froze forever on
the scene load, and diffing the seekmap against the rebuilt RES.DAT
showed 2,249 of 3,579 leaf entries pointing at non-gzip garbage; see
documentation/FORMAT_NOTES.md §24).

This is also exactly why dialogue-only edits never hit the problem: GPDA's
0x800 alignment padding absorbs text-sized changes, so no offset moves and
the original seekmap stays valid. Image edits routinely change sizes
enough to shift things.

Layout inside first.dat:
    first.dat (GPDA) -> "seekmap" (GPDA) -> "res.map.gz" (gzip'd text)

Text format (CRLF line endings, cp932/Shift-JIS, note the trailing space
before each newline), one line per entry, indented with tabs by depth:

    resource.dat 0 <size> <hash> 0 <entry_count>
    \t<name> <abs_offset> <size> <hash> 0 <entry_count>     <- nested GPDA
    \t\t<name> <abs_offset> <size> <hash>                   <- leaf file

The 4th field is a hash the reference implementation never decoded - it
copies each one through from the previous seekmap in traversal order,
which is safe because the tree's shape and ordering never change, only
offsets and sizes. This port does the same.

Ported from the sibling toolchain's CppPorts/ModSeekMap.cs
(zapan/FastAsyncOreimoTranslateTool). Validated by regenerating the
original seekmap from the untouched RES.DAT and getting a byte-for-byte
identical result (all 358,454 bytes).
"""
import gzip
import io
import struct

from . import gpda

SEEKMAP_ENTRY = "seekmap"
SEEKMAP_FILE = "res.map.gz"
ENCODING = "cp932"


def extract_text(first_dat: bytes) -> bytes:
    """Returns the decompressed seekmap text from a first.dat blob."""
    entries = gpda.parse_gpda(first_dat)
    sm = next(e for e in entries if e.name == SEEKMAP_ENTRY)
    blob = first_dat[sm.data_offset:sm.data_offset + sm.data_size]
    inner = gpda.parse_gpda(blob)[0]
    return gzip.decompress(blob[inner.data_offset:inner.data_offset + inner.data_size])


def regenerate(res_dat: bytes, old_seekmap_text: bytes) -> bytes:
    """Walks the rebuilt RES.DAT and emits a fresh seekmap with correct
    offsets/sizes, reusing each line's opaque 4th-field hash from
    old_seekmap_text (consumed in the same traversal order - see module
    docstring)."""
    old_lines = old_seekmap_text.decode(ENCODING, errors="replace").split("\r\n")
    line_iter = iter(old_lines)
    out = io.StringIO()

    def copy_hash():
        for line in line_iter:
            if line.strip():
                out.write(line.split()[3])
                return
        raise ValueError("old seekmap ran out of lines - tree shape changed unexpectedly")

    def walk(current_offset: int, nesting: int):
        _magic, archive_size, _unknown, entry_count = struct.unpack_from(
            "<4sIII", res_dat, current_offset
        )
        out.write(f"{archive_size} ")
        copy_hash()
        out.write(f" 0 {entry_count} \r\n")

        entries = []
        off = current_offset + 0x10
        for _ in range(entry_count):
            e_off, _reserved, e_size, _name_off = struct.unpack_from("<IIII", res_dat, off)
            off += 16
            entries.append((e_off, e_size))

        names = []
        for _ in range(entry_count):
            (name_len,) = struct.unpack_from("<I", res_dat, off)
            off += 4
            names.append(res_dat[off:off + name_len].decode(ENCODING, errors="replace"))
            off += name_len

        for (e_off, e_size), name in zip(entries, names):
            total_offset = current_offset + e_off
            out.write("\t" * nesting)
            if res_dat[total_offset:total_offset + 4] == b"GPDA":
                out.write(f"{name} {total_offset} ")
                walk(total_offset, nesting + 1)
                continue
            out.write(f"{name} {total_offset} {e_size} ")
            copy_hash()
            out.write(" \r\n")

    out.write("resource.dat 0 ")
    walk(0, 1)
    return out.getvalue().encode(ENCODING, errors="replace")


def rebuild_first_dat(first_dat: bytes, new_seekmap_text: bytes) -> bytes:
    """Returns a new first.dat with its seekmap replaced by
    new_seekmap_text (re-gzipped), every other entry passed through
    byte-for-byte."""
    new_gz = gzip.compress(new_seekmap_text, compresslevel=9, mtime=0)

    entries = gpda.parse_gpda(first_dat)
    sm = next(e for e in entries if e.name == SEEKMAP_ENTRY)
    sm_blob = first_dat[sm.data_offset:sm.data_offset + sm.data_size]

    new_sm_entries = [
        (x.name, new_gz if x.name == SEEKMAP_FILE
         else sm_blob[x.data_offset:x.data_offset + x.data_size])
        for x in gpda.parse_gpda(sm_blob)
    ]
    new_sm_blob = gpda.build_gpda(new_sm_entries)

    new_entries = [
        (e.name, new_sm_blob if e.name == SEEKMAP_ENTRY
         else first_dat[e.data_offset:e.data_offset + e.data_size])
        for e in entries
    ]
    return gpda.build_gpda(new_entries)


def update_for(res_dat: bytes, first_dat: bytes) -> bytes:
    """Convenience: regenerate the seekmap for res_dat and return the
    updated first.dat."""
    return rebuild_first_dat(first_dat, regenerate(res_dat, extract_text(first_dat)))
