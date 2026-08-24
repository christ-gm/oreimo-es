"""
Project: the in-memory model for one opened ISO. Indexes every translatable
dialogue/chapter-title line across all scenes of the opened disc, tracks
edits, and can export/import them as CSV/TSV or compile them back into a
playable ISO.
"""
import csv
import gzip
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from . import gpda, iso_grow, iso_tools, obj_blocks, scene_images, image_io, seekmap, text_wrap


def split_speaker(text: str) -> tuple[str | None, str]:
    """If text is of the form '<Speaker>「...」' (the game's literal dialogue
    convention - Japanese corner brackets used as quote marks, even in the
    English/Spanish script), returns (speaker, dialogue) with the speaker
    name AND the brackets stripped out of dialogue. Otherwise (narration,
    no speaker prefix) returns (None, text) unchanged. Validated against
    all 19,000 lines of this game's real dialogue: the pattern is
    unambiguous - every line either matches it exactly or contains no
    bracket at all."""
    if text.endswith("」") and "「" in text:
        idx = text.index("「")
        return text[:idx], text[idx + 1:-1]
    return None, text


def join_speaker(speaker: str | None, dialogue: str) -> str:
    """Inverse of split_speaker: reconstructs the full raw string the game
    engine needs (speaker name + brackets + dialogue), or just the
    dialogue unchanged for narration (no speaker)."""
    if speaker is None:
        return dialogue
    return f"{speaker}「{dialogue}」"


@dataclass
class DialogueEntry:
    scene: str
    block_offset: int  # byte offset of the block within its scene's decompressed .obj - unique per scene
    raw_original: str  # exact text as stored in the .obj, e.g. 'Kirino「Yup!」' - may include a speaker prefix
    translation: str | None = None  # dialogue-only, no speaker/brackets; defaults to `original` below
    speaker_override: str | None = None  # replaces the original speaker name (e.g. ES name) when set

    def __post_init__(self):
        if self.translation is None:
            self.translation = self.original

    @property
    def speaker(self) -> str | None:
        """The speaking character's name, or None for narration lines.
        Derived from `raw_original` - the game embeds it as a literal
        'Name「...」' prefix in the text itself, there's no separate
        structured speaker field in the format. An imported translation
        may override it (speaker_override) so compiled output keeps the
        translated name."""
        if self.speaker_override is not None:
            return self.speaker_override
        speaker, _ = split_speaker(self.raw_original)
        return speaker

    @property
    def original(self) -> str:
        """Display/editable form: dialogue text only, with any speaker
        name + brackets stripped (the speaker is shown in its own
        column/field instead)."""
        _, dialogue = split_speaker(self.raw_original)
        return dialogue

    @property
    def is_edited(self) -> bool:
        return self.translation != self.original

    @property
    def full_translation(self) -> str:
        """Reconstructs the exact string that must be written back into
        the .obj block: speaker + brackets + translated dialogue (or just
        the translation, unchanged, for narration lines with no speaker)."""
        return join_speaker(self.speaker, self.translation)


class Project:
    def __init__(self):
        self.iso_path: str | None = None
        self.res_dat: bytes | None = None
        self.script_blob: bytes | None = None  # kept for on-demand scene image lookups
        self.script_entries: list[gpda.GPDAEntry] = []
        self.disc_serial: str | None = None  # e.g. 'NPJH-50568' (disc 1) / 'NPJH-50569' (disc 2)
        self.scenes: dict[str, list[DialogueEntry]] = {}
        self._image_category_index: dict[str, set[str]] | None = None
        # (scene, category, label) -> ImportedImage; pending image edits, held
        # in memory until compile() re-encodes and writes them back
        self.image_edits: dict[tuple[str, str, str], image_io.ImportedImage] = {}

    # ---- loading -----------------------------------------------------

    def load(self, iso_path: str, progress_callback=None):
        self.iso_path = iso_path
        self.res_dat = iso_tools.read_res_dat(iso_path)
        self.disc_serial = iso_tools.detect_disc(iso_path)

        script_off, script_size = gpda.find_path(self.res_dat, ["script"])
        script_blob = self.res_dat[script_off:script_off + script_size]
        self.script_blob = script_blob
        self.script_entries = gpda.parse_gpda(script_blob)

        self.scenes = {}
        self._image_category_index = None
        self.image_edits = {}
        total = len(self.script_entries)
        for i, e in enumerate(self.script_entries):
            scene_blob = script_blob[e.data_offset:e.data_offset + e.data_size]
            self.scenes[e.name] = self._index_scene(e.name, scene_blob)
            if progress_callback:
                progress_callback(i + 1, total, e.name)

    @staticmethod
    def _index_scene(scene_name: str, scene_blob: bytes) -> list[DialogueEntry]:
        obj_bytes = Project._extract_obj_bytes(scene_blob)
        entries = []
        for block in obj_blocks.iter_blocks(obj_bytes):
            if block.text is not None:
                entries.append(DialogueEntry(
                    scene=scene_name,
                    block_offset=block.offset,
                    raw_original=block.text,
                ))
        return entries

    @staticmethod
    def _extract_obj_bytes(scene_blob: bytes) -> bytes:
        scene_entries = gpda.parse_gpda(scene_blob)
        folder000 = next(x for x in scene_entries if x.name == "000")
        folder000_blob = scene_blob[folder000.data_offset:folder000.data_offset + folder000.data_size]
        inner_entries = gpda.parse_gpda(folder000_blob)
        objgz_entry = next(x for x in inner_entries if "obj.gz" in x.name)
        objgz_bytes = folder000_blob[objgz_entry.data_offset:objgz_entry.data_offset + objgz_entry.data_size]
        return gzip.decompress(objgz_bytes)

    # ---- queries -------------------------------------------------------

    def scene_names(self) -> list[str]:
        return list(self.scenes.keys())

    def entries_for_scene(self, scene_name: str) -> list[DialogueEntry]:
        return self.scenes.get(scene_name, [])

    def search(self, query: str) -> list[DialogueEntry]:
        query = query.lower()
        results = []
        for entries in self.scenes.values():
            for e in entries:
                if query in e.original.lower() or query in e.translation.lower():
                    results.append(e)
        return results

    def edited_count(self) -> int:
        return sum(1 for entries in self.scenes.values() for e in entries if e.is_edited)

    def images_for_scene(self, scene_name: str) -> dict[str, list[scene_images.SceneImage]]:
        """Decodes and returns every scene image (background/event/
        character/cutin/tukkomi) for scene_name, grouped by category
        label. Returns {} for scenes with no image data or an unknown
        scene name. Each SceneImage's is_edited flag reflects whether a
        validated replacement is pending in self.image_edits."""
        if self.script_blob is None:
            return {}
        entry = next((e for e in self.script_entries if e.name == scene_name), None)
        if entry is None:
            return {}
        grouped = scene_images.scene_images(self.script_blob, entry)
        for category, images in grouped.items():
            for image in images:
                pending = self.image_edits.get((scene_name, category, image.label))
                image.is_edited = pending is not None
                image.replacement_png_bytes = pending.png_bytes if pending else None
        return grouped

    def apply_image_imports(self, imported: list[image_io.ImportedImage]):
        """Stores validated imported images as pending edits, keyed by
        (scene, category, label) - overwrites any earlier pending edit for
        the same image. Nothing is re-encoded or written to disk until
        compile()."""
        for item in imported:
            self.image_edits[(item.scene, item.category, item.label)] = item

    def edited_image_count(self) -> int:
        return len(self.image_edits)

    def scene_image_categories(self) -> dict[str, set[str]]:
        """Returns {scene_name: {category_label, ...}} for every scene -
        which image categories (Background/Event.CG/Character/Cutin/
        Tukkomi) each scene actually has, without decoding any pixels.
        Computed once and cached (~0.5s for the whole 300-scene game)."""
        if self._image_category_index is None:
            self._image_category_index = {
                name: set(self.images_for_scene(name).keys())
                for name in self.scene_names()
            }
        return self._image_category_index

    # ---- editing -------------------------------------------------------

    def set_translation(self, scene_name: str, block_offset: int, new_text: str):
        for e in self.scenes.get(scene_name, []):
            if e.block_offset == block_offset:
                e.translation = new_text
                return
        raise KeyError(f"no entry at scene={scene_name!r} offset={block_offset}")

    # ---- CSV / TSV export & import -------------------------------------

    FIELDNAMES = ["scene", "block_offset", "character", "original", "translation"]

    @staticmethod
    def _write_rows(scene_name: str, entries: list["DialogueEntry"], path: str, delimiter: str):
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=Project.FIELDNAMES, delimiter=delimiter)
            writer.writeheader()
            for e in entries:
                writer.writerow({
                    "scene": scene_name,
                    "block_offset": e.block_offset,
                    "character": e.speaker or "",
                    "original": e.original,
                    "translation": e.translation,
                })

    def export_table(self, path: str, delimiter: str = ","):
        """Exports every scene into a single file."""
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES, delimiter=delimiter)
            writer.writeheader()
            for scene_name, entries in self.scenes.items():
                for e in entries:
                    writer.writerow({
                        "scene": scene_name,
                        "block_offset": e.block_offset,
                        "character": e.speaker or "",
                        "original": e.original,
                        "translation": e.translation,
                    })

    def export_scene(self, scene_name: str, path: str, delimiter: str = ","):
        """Exports a single scene's lines to one file."""
        entries = self.scenes.get(scene_name)
        if entries is None:
            raise KeyError(f"unknown scene {scene_name!r}")
        self._write_rows(scene_name, entries, path, delimiter)

    def export_all_per_scene(self, directory: str, delimiter: str = ",", progress_callback=None) -> list[str]:
        """Exports every scene to its own file inside `directory`, named
        '<scene_name>.csv' (or .tsv) - so the file name always identifies
        which scene it holds, and files can be sent/edited/re-imported
        individually or in any combination. Scenes with zero translatable
        lines are skipped. Returns the list of written file paths."""
        ext = "tsv" if delimiter == "\t" else "csv"
        written = []
        scene_names = list(self.scenes.keys())
        for i, scene_name in enumerate(scene_names):
            entries = self.scenes[scene_name]
            if entries:
                path = str(Path(directory) / f"{scene_name}.{ext}")
                self._write_rows(scene_name, entries, path, delimiter)
                written.append(path)
            if progress_callback:
                progress_callback(i + 1, len(scene_names), scene_name)
        return written

    def import_table(self, path: str, delimiter: str = ",") -> list[str]:
        """Applies translations from a previously exported (and possibly
        edited) file. Returns a list of warning strings for any row that
        couldn't be matched (unknown scene/offset, or the row's 'original'
        no longer matches - meaning the ISO's text changed since export)."""
        warnings = []
        with open(path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row_num, row in enumerate(reader, start=2):
                scene_name = row.get("scene", "")
                try:
                    block_offset = int(row.get("block_offset", ""))
                except (TypeError, ValueError):
                    warnings.append(f"row {row_num}: invalid block_offset {row.get('block_offset')!r}")
                    continue

                entries = self.scenes.get(scene_name)
                if entries is None:
                    warnings.append(f"row {row_num}: unknown scene {scene_name!r}")
                    continue

                match = next((e for e in entries if e.block_offset == block_offset), None)
                if match is None:
                    warnings.append(f"row {row_num}: no entry at scene={scene_name!r} offset={block_offset}")
                    continue

                original_in_file = row.get("original", "")
                if original_in_file != match.original:
                    warnings.append(
                        f"row {row_num}: original text mismatch for scene={scene_name!r} "
                        f"offset={block_offset} (file has {original_in_file!r}, "
                        f"current ISO has {match.original!r}) - skipped"
                    )
                    continue

                match.translation = row.get("translation", match.original)
        return warnings

    def import_tables(self, paths: list[str]) -> dict[str, list[str]]:
        """Imports multiple files (e.g. a group of per-scene exports the
        user selected together). Delimiter is auto-detected per file from
        its extension. Returns {path: [warnings]} for every file."""
        results = {}
        for path in paths:
            delimiter = "\t" if path.lower().endswith(".tsv") else ","
            results[path] = self.import_table(path, delimiter=delimiter)
        return results

    # ---- compiling -------------------------------------------------------

    def compile(self, output_iso_path: str, progress_callback=None):
        self._wrapped_lines = 0
        changed_dialogue = {name: entries for name, entries in self.scenes.items() if any(e.is_edited for e in entries)}
        image_edits_by_scene: dict[str, dict[tuple[str, str, str], image_io.ImportedImage]] = defaultdict(dict)
        for key, item in self.image_edits.items():
            image_edits_by_scene[key[0]][key] = item

        changed_scene_names = set(changed_dialogue) | set(image_edits_by_scene)
        if not changed_scene_names:
            raise ValueError("no edited lines or images to compile")

        script_off, script_size = gpda.find_path(self.res_dat, ["script"])
        script_blob = self.res_dat[script_off:script_off + script_size]

        unsupported_image_edits: list[tuple[str, str, str]] = []
        encoding_warnings: list[str] = []
        new_script_entries = []
        for e in self.script_entries:
            if e.name in changed_scene_names:
                scene_blob = script_blob[e.data_offset:e.data_offset + e.data_size]
                new_scene_blob, unsupported, scene_warnings = self._rebuild_scene(
                    scene_blob,
                    changed_dialogue.get(e.name, []),
                    image_edits_by_scene.get(e.name, {}),
                )
                unsupported_image_edits.extend(unsupported)
                encoding_warnings.extend(f"{e.name}/{w}" for w in scene_warnings)
                new_script_entries.append((e.name, new_scene_blob))
            else:
                new_script_entries.append((e.name, script_blob[e.data_offset:e.data_offset + e.data_size]))
        new_script_blob = gpda.build_gpda(new_script_entries)

        top_entries = gpda.parse_gpda(self.res_dat)
        script_top_entry = next(x for x in top_entries if x.name == "script")
        new_top_entries = []
        for e in top_entries:
            if e is script_top_entry:
                new_top_entries.append((e.name, new_script_blob))
            else:
                new_top_entries.append((e.name, self.res_dat[e.data_offset:e.data_offset + e.data_size]))
        new_res_dat = gpda.build_gpda(new_top_entries)

        # first.dat embeds a seekmap: a table of ABSOLUTE offsets into
        # RES.DAT for every entry in its tree. Any size change in RES.DAT
        # shifts later offsets and makes it stale, which hangs the game on
        # load (confirmed in-game - see core/seekmap.py and
        # documentation/FORMAT_NOTES.md §24). Regenerate it unconditionally:
        # when nothing actually moved (the usual dialogue-only case, where
        # GPDA padding absorbs the change) the result is byte-identical to
        # the original, so first.dat is unchanged and the fast path below
        # still applies.
        original_first_dat = iso_tools.read_file(self.iso_path, iso_tools.FIRST_DAT_ISO_PATH)
        new_first_dat = seekmap.update_for(new_res_dat, original_first_dat)

        replacements = {
            iso_tools.RES_DAT_ISO_PATH: new_res_dat,
            iso_tools.FIRST_DAT_ISO_PATH: new_first_dat,
        }
        # Both files keep their size whenever GPDA's 0x800 padding absorbs
        # the change (the usual dialogue-only case). Image edits, and a
        # whole imported translation, routinely push RES.DAT past that
        # padding - importing all of disc 1's Spanish grows it by 14,336
        # bytes, seven sectors. Either way the write goes through
        # iso_grow, which edits the ISO9660 filesystem in place and needs
        # nothing installed; the old mkisofs rebuild path is gone.
        needs_resize = (
            len(new_res_dat) != len(self.res_dat)
            or len(new_first_dat) != len(original_first_dat)
        )
        iso_report = iso_grow.write_files_into_iso(
            self.iso_path, replacements, output_iso_path,
            progress_callback=progress_callback,
        )
        return {
            "scenes_changed": list(changed_scene_names),
            "lines_changed": sum(1 for entries in changed_dialogue.values() for e in entries if e.is_edited),
            "images_changed": len(self.image_edits) - len(unsupported_image_edits),
            "unsupported_image_edits": unsupported_image_edits,
            "encoding_warnings": encoding_warnings,
            "res_dat_size": len(new_res_dat),
            "res_dat_resized": needs_resize,
            "seekmap_updated": new_first_dat != original_first_dat,
            "files_moved": iso_report["moved"],
            "filler_reclaimed": iso_report["reclaimed"],
            "iso_grew_by": iso_report["image_grew_by"],
            "lines_wrapped": self._wrapped_lines,
        }

    @staticmethod
    def _rebuild_named_image_container(
        container_blob: bytes, edits_by_gim_name: dict[str, image_io.ImportedImage]
    ) -> tuple[bytes, list[str]]:
        """Rebuilds a GPDA container whose entries are each a gzip-
        compressed, individually-named GIM image (the shape used by
        Background/Event/Cutin/Tukkomi - NOT the unnamed multi-part
        Character container, which has no builder yet, see
        _rebuild_scene). edits_by_gim_name: {entry_name: ImportedImage}.

        Re-encodes each edited image in the ORIGINAL entry's own GIM
        format (palette vs RGBA8888) rather than always RGBA8888 - see
        scene_images.encode_to_gim's docstring for why this matters (a
        format change alone, even with the exact same pixels, can exceed
        the game's texture memory budget and crash - confirmed in-game,
        documentation/FORMAT_NOTES.md §22/§23). Also flags any edit whose
        re-encoded size is bigger than the original's, regardless of
        cause, as a warning - a general safety net alongside the
        format-preservation fix. Returns (new_container_blob, warnings)."""
        entries = gpda.parse_gpda(container_blob)
        new_entries = []
        warnings: list[str] = []
        for e in entries:
            old_gz = container_blob[e.data_offset:e.data_offset + e.data_size]
            if e.name in edits_by_gim_name:
                original_gim = gzip.decompress(old_gz)
                target_format = scene_images.peek_format(original_gim)
                new_gim, enc_warnings = scene_images.encode_to_gim(
                    edits_by_gim_name[e.name].png_bytes, target_format
                )
                warnings.extend(f"{e.name}: {w}" for w in enc_warnings)
                if len(new_gim) > len(original_gim):
                    growth = (len(new_gim) - len(original_gim)) / len(original_gim) * 100
                    warnings.append(
                        f"{e.name}: now {growth:.0f}% bigger in texture memory than the "
                        f"original ({len(original_gim):,} -> {len(new_gim):,} bytes) - "
                        f"this may exceed the game's texture memory budget and crash"
                    )
                new_gz = gzip.compress(new_gim, compresslevel=9, mtime=0)
                new_entries.append((e.name, new_gz))
            else:
                new_entries.append((e.name, old_gz))
        return gpda.build_gpda(new_entries), warnings

    @staticmethod
    def _rebuild_scene(
        scene_blob: bytes,
        dialogue_entries: list[DialogueEntry],
        image_edits: dict[tuple[str, str, str], image_io.ImportedImage],
    ) -> tuple[bytes, list[tuple[str, str, str]]]:
        """Rebuilds one scene's GPDA blob applying both kinds of pending
        edits: dialogue text (via obj_blocks, unchanged from before) and
        image replacements (re-encoded via scene_images.encode_to_gim).
        Character-category image edits aren't supported yet - the format
        the game uses to pack a character's expression-swap parts together
        (see scene_images.py's module docstring) has no builder, only a
        reader, so those are reported back as unsupported instead of
        silently dropped or corrupting the container. Returns
        (new_scene_blob, unsupported_image_edit_keys, encoding_warnings)."""
        unsupported: list[tuple[str, str, str]] = []
        encoding_warnings: list[str] = []
        edits_by_category: dict[str, dict[str, image_io.ImportedImage]] = defaultdict(dict)
        for (_scene, category, gim_name), item in image_edits.items():
            edits_by_category[category][gim_name] = item

        scene_entries = gpda.parse_gpda(scene_blob)
        new_top: dict[str, bytes] = {}

        for entry_name, label in scene_images.SCENE_CATEGORIES:
            if label not in edits_by_category:
                continue
            if label == "Character":
                for item in edits_by_category[label].values():
                    unsupported.append((item.scene, item.category, item.label))
                continue
            entry = next((x for x in scene_entries if x.name == entry_name), None)
            if entry is None:
                continue
            container = scene_blob[entry.data_offset:entry.data_offset + entry.data_size]
            new_top[entry_name], warnings = Project._rebuild_named_image_container(container, edits_by_category[label])
            encoding_warnings.extend(f"{label}/{w}" for w in warnings)

        folder000 = next(x for x in scene_entries if x.name == "000")
        folder000_blob = scene_blob[folder000.data_offset:folder000.data_offset + folder000.data_size]
        inner_entries = gpda.parse_gpda(folder000_blob)
        new_inner: dict[str, bytes] = {}

        if dialogue_entries:
            objgz_entry = next(x for x in inner_entries if "obj.gz" in x.name)
            objgz_bytes = folder000_blob[objgz_entry.data_offset:objgz_entry.data_offset + objgz_entry.data_size]
            obj_bytes = gzip.decompress(objgz_bytes)
            # The engine draws a line straight past the edge of the box
            # unless the script tells it where to break, so add the
            # markers here - the same way, and with the same glyph
            # widths, as the command-line pipeline's insert-linebreaks
            # step, so both routes produce the same script. Only the
            # dialogue is measured; the speaker is drawn in its own box.
            edits = {}
            for e in dialogue_entries:
                if not e.is_edited:
                    continue
                wrapped = text_wrap.wrap(e.translation, is_speech=e.speaker is not None)
                if wrapped != e.translation:
                    self._wrapped_lines += 1
                edits[e.block_offset] = join_speaker(e.speaker, wrapped)
            if edits:
                new_obj_bytes, _applied = obj_blocks.replace_strings_by_offset(obj_bytes, edits)
                new_inner[objgz_entry.name] = gzip.compress(new_obj_bytes, compresslevel=9, mtime=0)

        for entry_name, label in scene_images.NESTED_CATEGORIES:
            if label not in edits_by_category:
                continue
            entry = next((x for x in inner_entries if entry_name in x.name), None)
            if entry is None:
                continue
            container = folder000_blob[entry.data_offset:entry.data_offset + entry.data_size]
            new_inner[entry.name], warnings = Project._rebuild_named_image_container(container, edits_by_category[label])
            encoding_warnings.extend(f"{label}/{w}" for w in warnings)

        if new_inner:
            new_000_entries = [
                (x.name, new_inner.get(x.name, folder000_blob[x.data_offset:x.data_offset + x.data_size]))
                for x in inner_entries
            ]
            new_top["000"] = gpda.build_gpda(new_000_entries)

        if not new_top:
            # every requested edit for this scene was unsupported (Character-only)
            return scene_blob, unsupported, encoding_warnings

        new_scene_entries = [
            (x.name, new_top.get(x.name, scene_blob[x.data_offset:x.data_offset + x.data_size]))
            for x in scene_entries
        ]
        return gpda.build_gpda(new_scene_entries), unsupported, encoding_warnings
