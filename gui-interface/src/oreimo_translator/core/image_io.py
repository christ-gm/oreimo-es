"""
Export/import for scene images: writes decoded GIM textures to PNG files
on disk, one folder per scene and one sub-folder per category, alongside a
manifest.json that's the source of truth for re-identifying each PNG on
import. Folder/file names mirror the manifest for easy manual browsing,
but import never guesses identity by parsing paths - it always looks the
file up through the manifest, keyed by (scene, category, label).

Export layout:
    <output_dir>/manifest.json
    <output_dir>/<scene>/<category_slug>/<safe_label>.png

manifest.json is a flat JSON list of:
    {"scene": ..., "category": ..., "label": ..., "file": "<relative path>",
     "width": ..., "height": ...}

On import, a PNG is only accepted if its pixel dimensions match the
manifest's recorded width/height exactly - the game's renderer assumes a
texture's original dimensions, so a silently resized replacement would be
a likely source of the same kind of crash the dialogue pipeline hit before
block-length handling was fixed (see FORMAT_NOTES.md §17-18).
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from . import scene_images

CATEGORY_SLUGS = {
    "Background": "Background",
    "Event / CG": "Event_CG",
    "Character": "Character",
    "Cutin": "Cutin",
    "Tukkomi": "Tukkomi",
}

MANIFEST_NAME = "manifest.json"


def _safe_filename(label: str) -> str:
    name = label.replace(" ", "_").replace("[", "").replace("]", "")
    return re.sub(r"[^A-Za-z0-9_.\-]", "_", name)


def export_images(project, scene_names: list[str], output_dir: str, progress_callback=None) -> list[dict]:
    """Decodes every image for each scene in scene_names and writes it as
    a PNG under output_dir, plus a manifest.json describing what was
    written. Returns the manifest entries (also saved to disk)."""
    out = Path(output_dir)
    manifest = []
    total = len(scene_names)
    for i, scene_name in enumerate(scene_names):
        grouped = project.images_for_scene(scene_name)
        for category, images in grouped.items():
            slug = CATEGORY_SLUGS.get(category, _safe_filename(category))
            for image in images:
                width, height, rgba = scene_images.decode_to_rgba(image.gim_bytes)
                im = Image.frombytes("RGBA", (width, height), rgba)
                rel_path = f"{scene_name}/{slug}/{_safe_filename(image.label)}.png"
                dest = out / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                im.save(dest)
                manifest.append({
                    "scene": scene_name,
                    "category": category,
                    "label": image.label,
                    "file": rel_path,
                    "width": width,
                    "height": height,
                })
        if progress_callback:
            progress_callback(i + 1, total, scene_name)

    out.mkdir(parents=True, exist_ok=True)
    with open(out / MANIFEST_NAME, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest


@dataclass
class ImportedImage:
    scene: str
    category: str
    label: str
    width: int
    height: int
    png_bytes: bytes   # raw PNG file bytes - re-encoded to GIM lazily, at compile time
    source_path: str


def import_images(input_dir: str, project=None) -> tuple[list[ImportedImage], list[str]]:
    """Reads manifest.json from input_dir and, for every entry whose PNG
    file is present on disk, validates it (readable, dimensions match the
    manifest exactly) and returns it as an ImportedImage ready to hand to
    Project.apply_image_imports(). Entries with no matching file on disk
    are silently skipped (not every exported image needs to be re-
    imported). Returns (imported, warnings) - warnings cover files that
    exist but were rejected (bad PNG, size mismatch)."""
    root = Path(input_dir)
    manifest_path = root / MANIFEST_NAME
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"no {MANIFEST_NAME} found in {input_dir} - pick the folder that was "
            f"used as the destination for an image export"
        )
    with open(manifest_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    imported = []
    warnings = []
    # Scene names differ between the two discs - disc 2 prefixes them with
    # an underscore ('_AKYO_0000A' vs 'AKYO_0000A') and the two discs
    # don't even share the same scenes. An export from one disc therefore
    # matches nothing on the other, and without this check the mismatched
    # edits are accepted here, silently skipped at compile time, and still
    # counted in the "images changed" total - so the app reports having
    # replaced images it never touched.
    known_scenes = set(project.scenes) if project is not None else None
    unknown_scenes: set[str] = set()

    for entry in entries:
        if known_scenes is not None and entry["scene"] not in known_scenes:
            unknown_scenes.add(entry["scene"])
            continue
        png_path = root / entry["file"]
        if not png_path.exists():
            continue
        png_bytes = png_path.read_bytes()
        try:
            with Image.open(png_path) as im:
                width, height = im.width, im.height
        except Exception as exc:
            warnings.append(f"{entry['file']}: could not read PNG ({exc})")
            continue
        if (width, height) != (entry["width"], entry["height"]):
            warnings.append(
                f"{entry['file']}: size {width}x{height} does not match the "
                f"original {entry['width']}x{entry['height']} - skipped (the "
                f"game expects this texture's exact original size)"
            )
            continue
        imported.append(ImportedImage(
            scene=entry["scene"], category=entry["category"], label=entry["label"],
            width=width, height=height, png_bytes=png_bytes, source_path=str(png_path),
        ))

    if unknown_scenes:
        listed = ", ".join(sorted(unknown_scenes)[:8])
        if len(unknown_scenes) > 8:
            listed += f", and {len(unknown_scenes) - 8} more"
        warnings.append(
            f"{len(unknown_scenes)} scene(s) in this folder are not on the "
            f"ISO you have open, so their images were not loaded: {listed}. "
            f"This usually means the folder was exported from the other "
            f"disc - the two discs have different scenes."
        )
    return imported, warnings
