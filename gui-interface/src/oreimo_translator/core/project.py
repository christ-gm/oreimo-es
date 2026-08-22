"""
Project: the in-memory model for one opened ISO. Indexes every translatable
dialogue/chapter-title line across all 300 scenes, tracks edits, and can
export/import them as CSV/TSV or compile them back into a playable ISO.
"""
import csv
import gzip
from dataclasses import dataclass
from pathlib import Path

from . import gpda, iso_tools, obj_blocks


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

    def __post_init__(self):
        if self.translation is None:
            self.translation = self.original

    @property
    def speaker(self) -> str | None:
        """The speaking character's name, or None for narration lines.
        Derived from `raw_original` - the game embeds it as a literal
        'Name「...」' prefix in the text itself, there's no separate
        structured speaker field in the format."""
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
        self.script_entries: list[gpda.GPDAEntry] = []
        self.scenes: dict[str, list[DialogueEntry]] = {}

    # ---- loading -----------------------------------------------------

    def load(self, iso_path: str, progress_callback=None):
        self.iso_path = iso_path
        self.res_dat = iso_tools.read_res_dat(iso_path)

        script_off, script_size = gpda.find_path(self.res_dat, ["script"])
        script_blob = self.res_dat[script_off:script_off + script_size]
        self.script_entries = gpda.parse_gpda(script_blob)

        self.scenes = {}
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

    def compile(self, output_iso_path: str):
        changed = {name: entries for name, entries in self.scenes.items() if any(e.is_edited for e in entries)}
        if not changed:
            raise ValueError("no edited lines to compile")

        script_off, script_size = gpda.find_path(self.res_dat, ["script"])
        script_blob = self.res_dat[script_off:script_off + script_size]

        new_script_entries = []
        for e in self.script_entries:
            if e.name in changed:
                scene_blob = script_blob[e.data_offset:e.data_offset + e.data_size]
                new_scene_blob = self._rebuild_scene(scene_blob, changed[e.name])
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

        iso_tools.patch_res_dat_into_iso(self.iso_path, new_res_dat, output_iso_path)
        return {
            "scenes_changed": list(changed.keys()),
            "lines_changed": sum(1 for entries in changed.values() for e in entries if e.is_edited),
            "res_dat_size": len(new_res_dat),
        }

    @staticmethod
    def _rebuild_scene(scene_blob: bytes, entries: list[DialogueEntry]) -> bytes:
        scene_entries = gpda.parse_gpda(scene_blob)
        folder000 = next(x for x in scene_entries if x.name == "000")
        folder000_blob = scene_blob[folder000.data_offset:folder000.data_offset + folder000.data_size]
        inner_entries = gpda.parse_gpda(folder000_blob)
        objgz_entry = next(x for x in inner_entries if "obj.gz" in x.name)
        objgz_bytes = folder000_blob[objgz_entry.data_offset:objgz_entry.data_offset + objgz_entry.data_size]
        obj_bytes = gzip.decompress(objgz_bytes)

        edits = {e.block_offset: e.full_translation for e in entries if e.is_edited}
        new_obj_bytes, _applied = obj_blocks.replace_strings_by_offset(obj_bytes, edits)
        new_objgz_bytes = gzip.compress(new_obj_bytes, compresslevel=9, mtime=0)

        new_000_entries = [
            (x.name, new_objgz_bytes if x is objgz_entry else folder000_blob[x.data_offset:x.data_offset + x.data_size])
            for x in inner_entries
        ]
        new_000_blob = gpda.build_gpda(new_000_entries)

        new_scene_entries = [
            (x.name, new_000_blob if x is folder000 else scene_blob[x.data_offset:x.data_offset + x.data_size])
            for x in scene_entries
        ]
        return gpda.build_gpda(new_scene_entries)
