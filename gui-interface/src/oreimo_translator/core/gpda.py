"""
Reader/writer for the GPDA archive container format used throughout this
game's data files (first.dat, RES.DAT, and nested blobs inside RES.DAT).

Vendored from the sibling reverse-engineering project (../tools/gpda_parser.py
and gpda_builder.py) — see that project's documentation/FORMAT_NOTES.md §3
for the full format writeup. Kept as a self-contained copy so this app has
no dependency on the sibling project's directory.

Header layout (all little-endian):
  0x00: magic "GPDA" (4 bytes)
  0x04: uint32 total blob size
  0x08: uint32 unknown (observed 0)
  0x0C: uint32 entry_count
  0x10: entry_count * 16-byte entries:
        uint32 data_offset (relative to the start of THIS blob)
        uint32 reserved (observed 0)
        uint32 data_size
        uint32 name_offset (absolute offset within this blob to a
                length-prefixed name)
  name table: for each entry, uint32 name_len + name_len bytes (ASCII)

Entry data blocks are 0x800-byte aligned relative to the blob start; no
trailing padding after the last entry.
"""
import struct

ALIGN = 0x800


class GPDAEntry:
    def __init__(self, data_offset, data_size, name):
        self.data_offset = data_offset
        self.data_size = data_size
        self.name = name

    def __repr__(self):
        return f"<GPDAEntry name={self.name!r} offset=0x{self.data_offset:x} size={self.data_size}>"


def parse_gpda(data: bytes):
    magic = data[0:4]
    if magic != b"GPDA":
        raise ValueError(f"Not a GPDA blob (magic={magic!r})")

    filesize, _unknown, entry_count = struct.unpack_from("<III", data, 4)
    _ = filesize  # not enforced - some nested blobs are read via a size slice

    entries = []
    off = 0x10
    for _ in range(entry_count):
        data_offset, _reserved, data_size, name_offset = struct.unpack_from("<IIII", data, off)
        off += 16
        (name_len,) = struct.unpack_from("<I", data, name_offset)
        name = data[name_offset + 4: name_offset + 4 + name_len].decode("ascii")
        entries.append(GPDAEntry(data_offset, data_size, name))

    return entries


def find_path(data: bytes, parts, base_offset=0, size=None):
    """Resolve a list of path components like ['script', 'AKYO_0010A'] to
    (absolute_offset, size) within `data`, recursing through nested GPDA
    blobs (offsets reset relative to each nested blob's own start)."""
    if size is None:
        size = len(data)
    chunk = data[base_offset:base_offset + size]
    entries = parse_gpda(chunk)
    name = parts[0]
    for e in entries:
        if e.name == name:
            abs_off = base_offset + e.data_offset
            if len(parts) == 1:
                return abs_off, e.data_size
            return find_path(data, parts[1:], abs_off, e.data_size)
    raise KeyError(f"{name!r} not found under offset 0x{base_offset:x}")


def _round_up(n, align=ALIGN):
    return (n + align - 1) // align * align


def build_gpda(entries):
    """entries: list of (name: str, data: bytes). Returns the full GPDA blob,
    replicating the observed 0x800-byte alignment/padding rule."""
    entry_count = len(entries)
    header_size = 16 + entry_count * 16

    name_offsets = []
    name_table = bytearray()
    off = header_size
    for name, _ in entries:
        name_offsets.append(off)
        nb = name.encode("ascii")
        name_table += struct.pack("<I", len(nb)) + nb
        off += 4 + len(nb)

    base_end = header_size + len(name_table)
    first_data_offset = _round_up(base_end)

    data_offsets = []
    data_blob = bytearray()
    cursor = first_data_offset
    for _name, data in entries:
        data_offsets.append(cursor)
        data_blob += data
        cursor += len(data)
        pad_to = _round_up(cursor)
        data_blob += b"\x00" * (pad_to - cursor)
        cursor = pad_to
    _last_name, last_data = entries[-1]
    total_size = data_offsets[-1] + len(last_data)

    entry_table = bytearray()
    for (name, data), data_off, name_off in zip(entries, data_offsets, name_offsets):
        entry_table += struct.pack("<IIII", data_off, 0, len(data), name_off)

    header = b"GPDA" + struct.pack("<III", total_size, 0, entry_count)
    blob = bytearray(header) + entry_table + name_table
    blob += b"\x00" * (first_data_offset - len(blob))
    blob += data_blob[: total_size - first_data_offset]

    assert len(blob) == total_size, f"{len(blob)} != {total_size}"
    return bytes(blob)
