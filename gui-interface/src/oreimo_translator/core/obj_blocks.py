"""
Reader/writer for the game's ".obj" script bytecode format (the decompressed
contents of RES.DAT/script/<scene>/000/000script<scene>.obj.gz).

Vendored + adapted from the sibling reverse-engineering project's
tools/translate_scene.py. See that project's documentation/FORMAT_NOTES.md
§17 for the full writeup of the block structure and the crash it took to
find it: the file is a sequential array of self-describing BLOCKS, each
starting with its own int32 blockLen (total block byte size, used by the
game engine to find "what comes next" via position += blockLen). Any tool
that resizes a string MUST recompute and rewrite the enclosing block's
blockLen, or the game reads garbage past it and crashes.

    offset 0x00: int32 blockCount
    offset 0x04: int32 headerLen        <- length of the header/preamble block
    header block occupies [0, headerLen), passed through unchanged
    then blockCount blocks follow back-to-back, each:
        offset+0x00: int32 blockLen
        offset+0x04: int16 blockType    <- 0x64/0x68=Dialogue, 0x69=Choice,
                                            0x67=Choice2, 0x323=Question,
                                            0x2BC=Chapter
        offset+0x06: type-specific fields, including embedded string(s)
                     (each: int32 char_count, then char_count*2 bytes UTF-16LE)
        ... zero-padded until blockLen is reached

Only Dialogue/Dialogue2 and Chapter blocks are currently readable/writable
here (everything used by translated scenes so far). Choice/Choice2/Question
blocks (player-facing menu choices) are preserved byte-for-byte unchanged
and their embedded strings are not (yet) exposed for translation.
"""
import struct
from dataclasses import dataclass

DIALOGUE = 0x64
DIALOGUE2 = 0x68
CHOICE = 0x69
CHOICE2 = 0x67
QUESTION = 0x0323
CHAPTER = 0x2BC

TEXT_OFFSET_DIALOGUE = 11  # char_count field position, relative to block start
HEADER_LEN_DIALOGUE = 7  # header bytes copied from (block_start + 4) on export

TRANSLATABLE_TYPES = (DIALOGUE, DIALOGUE2, CHAPTER)

# Reference tool uses this as special delete-line syntax we haven't ported.
_MAGIC_MARKERS = ("[DEL]",)


@dataclass
class Block:
    offset: int
    length: int
    block_type: int
    text: str | None  # None if this block type has no (supported) translatable string


def _i32(b, at):
    return struct.unpack_from("<i", b, at)[0]


def _i16(b, at):
    return struct.unpack_from("<h", b, at)[0]


def _read_string(b, at):
    strlen = _i32(b, at)
    at += 4
    return b[at:at + strlen * 2].decode("utf-16-le")


def _encode_string(s):
    data = s.encode("utf-16-le")
    return struct.pack("<i", len(data) // 2) + data


def _write_block(content: bytes, output: bytearray):
    """length-prefix + pad to a 16-byte boundary, with an extra 16 bytes of
    padding if the natural pad would be <=8 bytes (reference tool's rule,
    transcribed as-is)."""
    new_len = len(content) + 4
    blank = 0
    while (new_len + blank) % 0x10 != 0:
        blank += 1
    if blank <= 0x8:
        blank += 0x10
    new_len += blank
    output += struct.pack("<i", new_len)
    output += content
    output += b"\x00" * blank


def _block_text(obj_bytes, i, btype):
    if btype in (DIALOGUE, DIALOGUE2):
        return _read_string(obj_bytes, i + TEXT_OFFSET_DIALOGUE)
    if btype == CHAPTER:
        return _read_string(obj_bytes, i + 6)
    return None


def _build_block_content(obj_bytes: bytes, i: int, btype: int, new_text: str) -> bytes:
    """Builds the replacement content (everything after the blockLen
    length-prefix) for a Dialogue/Dialogue2/Chapter block at offset i,
    with its string replaced by new_text. Caller is responsible for
    passing this to _write_block to get the final length-prefixed,
    padded block bytes."""
    if btype in (DIALOGUE, DIALOGUE2):
        header = obj_bytes[i + 4:i + 4 + HEADER_LEN_DIALOGUE]
        return header + _encode_string(new_text)
    # CHAPTER
    idx = i + 6
    idx += _i32(obj_bytes, idx) * 2 + 4  # skip past the OLD string
    type_bytes = obj_bytes[i + 4:i + 6]
    trailing = obj_bytes[idx:idx + 6]
    return type_bytes + _encode_string(new_text) + trailing


def iter_blocks(obj_bytes: bytes):
    """Yields a Block for every block after the header, in file order."""
    block_count = _i32(obj_bytes, 0x00)
    i = _i32(obj_bytes, 0x04)
    for _ in range(block_count):
        block_len = _i32(obj_bytes, i)
        btype = _i16(obj_bytes, i + 4)
        yield Block(i, block_len, btype, _block_text(obj_bytes, i, btype))
        i += block_len


def replace_strings_in_obj(obj_bytes: bytes, translations: list[tuple[str, str]]):
    """translations: list of (old_text, new_text) pairs. Each old_text must
    match a Dialogue/Dialogue2/Chapter block's string exactly and must be
    unique within this call (duplicate lines aren't supported). Returns
    (new_obj_bytes, applied_count). Raises ValueError if any old_text isn't
    found (fails loudly rather than silently skipping)."""
    remaining = {}
    for old, new in translations:
        if old in remaining:
            raise ValueError(f"duplicate old_text in translations: {old!r}")
        for marker in _MAGIC_MARKERS:
            if marker in new:
                raise ValueError(f"translated text contains unsupported marker {marker!r}: {new!r}")
        remaining[old] = new

    block_count = _i32(obj_bytes, 0x00)
    header_len = _i32(obj_bytes, 0x04)
    output = bytearray(obj_bytes[0:header_len])

    i = header_len
    applied = 0
    for _ in range(block_count):
        block_len = _i32(obj_bytes, i)
        btype = _i16(obj_bytes, i + 4)
        text = _block_text(obj_bytes, i, btype)

        if text is not None and text in remaining:
            new_text = remaining.pop(text)
            content = _build_block_content(obj_bytes, i, btype, new_text)
            _write_block(content, output)
            applied += 1
        else:
            output += obj_bytes[i:i + block_len]

        i += block_len

    if remaining:
        raise ValueError(
            f"original string(s) not found (already changed, typo, or in an "
            f"unsupported block type like Choice/Question?): {list(remaining.keys())}"
        )

    struct.pack_into("<i", output, 0x00, block_count)
    return bytes(output), applied


def replace_strings_by_offset(obj_bytes: bytes, edits: dict[int, str]):
    """edits: {block_offset: new_full_text}, where block_offset is a
    Block.offset value from iter_blocks() for a Dialogue/Dialogue2/Chapter
    block. Unlike replace_strings_in_obj (which matches by text content),
    this matches by position - so scenes with duplicate original lines
    (the same text appearing in more than one block) are handled
    correctly, since each block is addressed individually regardless of
    what text it currently holds. Returns (new_obj_bytes, applied_count).
    Raises ValueError if any offset doesn't land on a translatable block."""
    remaining = dict(edits)
    block_count = _i32(obj_bytes, 0x00)
    header_len = _i32(obj_bytes, 0x04)
    output = bytearray(obj_bytes[0:header_len])

    i = header_len
    applied = 0
    for _ in range(block_count):
        block_len = _i32(obj_bytes, i)
        btype = _i16(obj_bytes, i + 4)

        if i in remaining and btype in TRANSLATABLE_TYPES:
            new_text = remaining.pop(i)
            content = _build_block_content(obj_bytes, i, btype, new_text)
            _write_block(content, output)
            applied += 1
        else:
            output += obj_bytes[i:i + block_len]

        i += block_len

    if remaining:
        raise ValueError(f"block offset(s) not found / not a translatable block: {list(remaining.keys())}")

    struct.pack_into("<i", output, 0x00, block_count)
    return bytes(output), applied
