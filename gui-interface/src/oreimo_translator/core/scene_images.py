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
import io
import struct
from dataclasses import dataclass, field
from types import SimpleNamespace

from PIL import Image

from . import gpda
from .vendor_gim.gim import gim2png, png2gim

GIM_MAGICS = (b"MIG.", b".GIM")  # little-endian ("MIG.") and big-endian (".GIM") GIM headers

FORMAT_RGBA8888 = 3
FORMAT_P8 = 5
PALETTE_FORMATS = {4, 5}  # P4, P8 - both re-encoded as P8, the only indexed depth the vendored encoder supports
FORMAT_NAMES = {
    0: "RGBA5650", 1: "RGBA5551", 2: "RGBA4444", 3: "RGBA8888", 4: "P4", 5: "P8",
    6: "PA88", 7: "PAxx8888", 8: "DXT1", 9: "DXT3", 10: "DXT5",
}

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


def peek_format(gim_bytes: bytes) -> int:
    """Reads just the numeric GIM pixel-format code (see FORMAT_NAMES)
    from raw MIG.00.1PSP bytes, without decoding any pixels - walks the
    root->picture->image block chain to the image block's format field.
    Used at compile time to match a replacement's encoding to the
    original's (see encode_to_gim). Returns FORMAT_RGBA8888 if no image
    block is found (shouldn't happen for real files, but keeps this a
    safe default rather than raising)."""
    pos = 16  # past the fixed GIM/MIG magic+version+platform header
    for _ in range(3):
        if pos + 16 > len(gim_bytes):
            break
        (block_type,) = struct.unpack_from("<H", gim_bytes, pos)
        content_start = pos + 16
        if block_type == 4:  # image block
            (fmt,) = struct.unpack_from("<H", gim_bytes, content_start + 4)
            return fmt
        pos = content_start
    return FORMAT_RGBA8888


def _build_rgba_palette_image(im: Image.Image, max_colors: int = 256) -> Image.Image | None:
    """Quantizes an RGBA image into an indexed 'P'-mode image carrying a
    full RGBA palette (independent alpha per color - not PIL's usual
    single-transparent-index model). Exact/lossless: every distinct
    (R,G,B,A) combination gets its own palette slot, no color averaging.
    Returns None if the image needs more than max_colors combinations
    (this game's real P8 textures top out at 256 - confirmed one uses a
    genuine alpha *gradient* built entirely from per-color alpha, not
    just a single transparent color, see FORMAT_NOTES.md §23)."""
    w, h = im.size
    palette: list[tuple[int, int, int, int]] = []
    index_of: dict[tuple[int, int, int, int], int] = {}
    indices = bytearray(w * h)
    for i, color in enumerate(im.getdata()):
        idx = index_of.get(color)
        if idx is None:
            if len(palette) >= max_colors:
                return None
            idx = len(palette)
            index_of[color] = idx
            palette.append(color)
        indices[i] = idx

    palette.extend([(0, 0, 0, 0)] * (max_colors - len(palette)))
    flat_rgba = bytes(component for color in palette for component in color)

    im_p = Image.frombytes("P", (w, h), bytes(indices))
    im_p.putpalette(flat_rgba, rawmode="RGBA")
    return im_p


def _quantize_to_palette(im: Image.Image, max_colors: int = 256) -> Image.Image | None:
    """Reduces an image to at most max_colors distinct (R,G,B,A) values so
    it can be stored in the palette format its original used.

    Only Pillow's Fast Octree quantizer handles RGBA - median cut refuses
    outright - and it keeps per-pixel alpha rather than collapsing it to a
    single transparent index, which this game's textures need (§23: at
    least one uses a genuine alpha gradient built from per-color alpha).

    Returns a 'P'-mode image with a full RGBA palette, or None if the
    quantizer couldn't produce one."""
    try:
        reduced = im.quantize(colors=max_colors, method=Image.Quantize.FASTOCTREE)
    except Exception:
        return None
    # Round-trip through the exact builder: after quantizing there are at
    # most max_colors distinct values, so it now succeeds, and the palette
    # is built the same way as in the lossless path.
    return _build_rgba_palette_image(reduced.convert("RGBA"), max_colors)


def encode_to_gim(png_bytes: bytes, target_format: int = FORMAT_RGBA8888) -> tuple[bytes, list[str]]:
    """Encodes PNG bytes to a raw MIG.00.1PSP GIM texture, tiled, matching
    target_format when possible.

    Re-encoding a palette-format (P4/P8) original as RGBA8888 quadruples
    its decoded size (1 byte/pixel -> 4) - this is exactly what caused a
    real in-game crash (see documentation/FORMAT_NOTES.md §22/§23): the
    game budgets texture memory assuming each scene's original formats,
    and a scene whose Background/Cutin got silently blown up to 4x their
    size ran out of room the moment the next texture (Tukkomi) tried to
    load. So when target_format is P4/P8, this tries to encode as an
    8-bit palette instead - the only indexed depth the vendored encoder
    supports (P4 originals still get P8 output; a 256-color palette is
    strictly more capacity than a 16-color one, and 8bpp is 1/4 of
    RGBA8888 either way).

    Palette encoding is exact/lossless for images with <=256 distinct
    (R,G,B,A) combinations - including transparency and alpha gradients,
    since GIM's palette format carries independent alpha per color (see
    _build_rgba_palette_image). Only falls back to RGBA8888, with a
    warning, when the content genuinely needs more than 256 combinations
    - since that can't be represented in a palette without visible
    quality loss the caller hasn't asked for. Returns (gim_bytes,
    warnings) - warnings is non-empty exactly when a palette target had
    to fall back to RGBA8888, so the caller can surface "this may exceed
    the game's texture memory budget" to the user instead of finding out
    from a crash.

    The RGBA8888 path itself was verified byte-for-byte identical to
    Sony's own official GimConv 1.20h tool's output for real translated
    content from this game before being trusted - see §22/§23."""
    warnings: list[str] = []

    if target_format in PALETTE_FORMATS:
        im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        paletted = _build_rgba_palette_image(im)
        if paletted is None:
            # Too many colours to store exactly. Reducing them costs some
            # fidelity; keeping them costs the format, which quadruples
            # the texture's memory and is what actually broke the game in
            # §23 - the texture doesn't load, so the edit appears not to
            # have been applied at all. Fidelity is the cheaper thing to
            # spend, so quantize and keep the format.
            original_colors = len(im.getcolors(maxcolors=1 << 24) or ())
            paletted = _quantize_to_palette(im)
            if paletted is not None:
                warnings.append(
                    f"had {original_colors:,} distinct color+transparency "
                    f"combinations but the original texture here is a 256-color "
                    f"palette format, so it was reduced to 256 to keep that "
                    f"format (small colour shift; encoding it at full colour "
                    f"instead would quadruple its texture memory and the game "
                    f"would fail to load it)"
                )
        if paletted is None:
            warnings.append(
                "could not be stored in the original texture's 256-color "
                "palette format - using RGBA8888 instead (uses more texture "
                "memory than the original and the game may fail to load it; "
                "verify in-game)"
            )
        else:
            buf = io.BytesIO()
            paletted.save(buf, format="PNG")
            return png2gim(buf.getvalue(), _ENCODE_ARGS), warnings

    return png2gim(png_bytes, _ENCODE_ARGS), warnings
