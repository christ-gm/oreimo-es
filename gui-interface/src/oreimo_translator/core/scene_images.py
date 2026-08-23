"""
Scene image extraction: decodes the background, event/CG, character, cutin
and tukkomi GIM textures stored per scene inside RES.DAT/script/<scene>/,
for the "view scene images" GUI panel.

Per scene (see the sibling reverse-engineering project's
documentation/FORMAT_NOTES.md §5), image data lives in two places:

    <scene>/001image_bg          nested GPDA, one gzip'd .gim per background
    <scene>/002image_event       nested GPDA, one gzip'd .gim per event/CG
    <scene>/003image_charactor   nested GPDA, one gzip'd .gim per character
    <scene>/000/002image_cutin   nested GPDA (often empty)
    <scene>/000/003image_tukkomi nested GPDA (often empty)

Most entries decompress straight to a single MIG.00.1PSP (GIM) texture.
Character entries are different: they decompress to a SECOND, GPDA-shaped
container whose entries all have name_offset=0 (no name table - a variant
of the format not seen elsewhere), holding a couple of small ASCII
metadata records (bounding-box strings like "0,0,512,512,"), one
full-canvas base texture, and several smaller alternate mouth/eye-shape
overlay textures (this game's cheap expression-swap trick - matches the
HOHOEMI/WARAI/IKARI/... expression names found in AASTARTPOINT, per
FORMAT_NOTES.md §12). This module surfaces every raw texture it finds as
a separate "part" rather than compositing them onto the base canvas - full
expression compositing is not implemented yet.
"""
import gzip
import struct
from dataclasses import dataclass, field
from types import SimpleNamespace

from . import gpda
from .vendor_gim.gim import gim2png, png2gim

GIM_MAGICS = (b"MIG.", b".GIM")  # little-endian ("MIG.") and big-endian (".GIM") GIM headers

# top-level scene entries, in the order they should be shown
SCENE_CATEGORIES = [
    ("001image_bg", "Background"),
    ("002image_event", "Event / CG"),
    ("003image_charactor", "Character"),
]
# entries nested one level deeper, inside the scene's "000" sub-archive
NESTED_CATEGORIES = [
    ("002image_cutin", "Cutin"),
    ("003image_tukkomi", "Tukkomi"),
]


@dataclass
class SceneImage:
    category: str    # e.g. "Background"
    label: str        # e.g. "BG00A.gim" or "KI_1C.gim [part 2]"
    gim_bytes: bytes  # raw MIG.00.1PSP bytes, ready for decode_to_rgba()
    is_edited: bool = field(default=False, compare=False)  # set by Project.images_for_scene()
    replacement_png_bytes: bytes | None = field(default=None, compare=False)  # set alongside is_edited - the pending imported PNG, if any


def _lenient_entries(data: bytes) -> list[tuple[int, int]]:
    """Reads (data_offset, data_size) pairs from a GPDA-shaped header
    without trusting the name table - the nested character-part archives
    reuse the GPDA header/entry layout but leave every name_offset at 0,
    so gpda.parse_gpda's name lookup would read garbage."""
    if data[0:4] != b"GPDA" or len(data) < 0x10:
        return []
    (entry_count,) = struct.unpack_from("<I", data, 0x0C)
    entries = []
    off = 0x10
    for _ in range(entry_count):
        if off + 16 > len(data):
            break
        data_offset, _reserved, data_size, _name_offset = struct.unpack_from("<IIII", data, off)
        off += 16
        entries.append((data_offset, data_size))
    return entries


def _gim_parts(decompressed: bytes, base_label: str, category: str) -> list[SceneImage]:
    if decompressed[0:4] in GIM_MAGICS:
        return [SceneImage(category, base_label, decompressed)]
    if decompressed[0:4] == b"GPDA":
        parts = []
        for i, (off, size) in enumerate(_lenient_entries(decompressed)):
            if size <= 0 or off + size > len(decompressed):
                continue
            chunk = decompressed[off:off + size]
            if chunk[0:4] in GIM_MAGICS:
                parts.append(SceneImage(category, f"{base_label} [part {i}]", chunk))
        return parts
    return []


def _images_in_container(container_blob: bytes, category: str) -> list[SceneImage]:
    """container_blob is the data of a top-level '00Ximage_xxx' GPDA entry -
    each of its entries is a gzip-compressed blob (usually a single .gim,
    sometimes a nested archive of several parts - see module docstring)."""
    images = []
    for entry in gpda.parse_gpda(container_blob):
        raw_gz = container_blob[entry.data_offset:entry.data_offset + entry.data_size]
        try:
            decompressed = gzip.decompress(raw_gz)
        except OSError:
            continue
        images.extend(_gim_parts(decompressed, entry.name, category))
    return images


def scene_images(script_blob: bytes, scene_entry: gpda.GPDAEntry) -> dict[str, list[SceneImage]]:
    """Returns {category_label: [SceneImage, ...]} for one scene, skipping
    categories with no decodable images. `scene_entry` is the GPDAEntry for
    this scene (from Project.script_entries); `script_blob` is
    Project.script_blob (the parsed top-level 'script' entry's raw bytes)."""
    scene_blob = script_blob[scene_entry.data_offset:scene_entry.data_offset + scene_entry.data_size]
    top = gpda.parse_gpda(scene_blob)

    result: dict[str, list[SceneImage]] = {}

    for entry_name, label in SCENE_CATEGORIES:
        entry = next((x for x in top if x.name == entry_name), None)
        if entry is None:
            continue
        container = scene_blob[entry.data_offset:entry.data_offset + entry.data_size]
        images = _images_in_container(container, label)
        if images:
            result[label] = images

    folder000 = next((x for x in top if x.name == "000"), None)
    if folder000 is not None:
        folder000_blob = scene_blob[folder000.data_offset:folder000.data_offset + folder000.data_size]
        inner = gpda.parse_gpda(folder000_blob)
        for entry_name, label in NESTED_CATEGORIES:
            entry = next((x for x in inner if entry_name in x.name), None)
            if entry is None:
                continue
            container = folder000_blob[entry.data_offset:entry.data_offset + entry.data_size]
            images = _images_in_container(container, label)
            if images:
                result[label] = images

    return result


def decode_to_rgba(gim_bytes: bytes) -> tuple[int, int, bytes]:
    """Decodes raw MIG.00.1PSP bytes to (width, height, rgba8888_bytes)
    suitable for building a QImage(bytes, w, h, QImage.Format_RGBA8888)."""
    with gim2png(gim_bytes, SimpleNamespace(verbose=False)) as im:
        im = im.convert("RGBA")
        return im.width, im.height, im.tobytes()


_ENCODE_ARGS = SimpleNamespace(
    gim_byteorder="little",
    gim_pixel_order=True,  # tiled/swizzled - matches every real GIM found in this game
    gim_saved_date=None,
    gim_originator=None,
    gim_project_name="oreimo_translator",
    gim_user_name="oreimo_translator",
    gim_no_fileinfo=True,
)


def encode_to_gim(png_bytes: bytes) -> bytes:
    """Encodes PNG bytes to a raw MIG.00.1PSP GIM texture (RGBA8888,
    tiled). Round-trip validated (encode then decode_to_rgba back)
    byte-for-byte identical against real background/event/character
    textures from this game before this was trusted for reinsertion - see
    documentation/FORMAT_NOTES.md §22."""
    return png2gim(png_bytes, _ENCODE_ARGS)
