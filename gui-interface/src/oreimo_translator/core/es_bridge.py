"""
Bridge between this GUI and the oreimo-es translation project's
consolidated JSON files (translation/Translation.json for disc 1,
translation/Translation_disc2.json for disc 2).

Those files map scene -> {index: translated_line} (plus a "names" table
mapping original speaker names to their Spanish versions, e.g.
'Maid' -> 'Sirvienta'). Lines are stored WITHOUT the 'Name「...」' speaker
prefix: the dotnet pipeline keeps speakers in its own actor table and
re-attaches them at injection time. This GUI embeds the speaker inline in
each text block instead, so when loading an ES file here we re-attach the
speaker derived from the EN original - using the translated name from the
"names" table when one exists (DialogueEntry.speaker_override).
"""
import json
import re

from .project import split_speaker


def canonical_scene(name: str) -> str:
    """Normalizes a scene identifier so different namings collapse to one
    key: '000scriptAKYO_0000A.obj', '000script_AKYO_0000A.obj' and
    'AKYO_0000A' all become 'AKYO_0000A'."""
    n = name.strip()
    n = re.sub(r"\.obj$", "", n, flags=re.IGNORECASE)
    n = re.sub(r"^000script_?", "", n, flags=re.IGNORECASE)
    return n


def _scene_lines(value) -> list[str]:
    """JSON scenes store either a list of lines or a {"0": ..., "1": ...}
    object; both come back as an ordered list here."""
    if isinstance(value, dict):
        return [value[k] for k in sorted(value.keys(), key=int)]
    return list(value)


def load_es_translation(project, json_path: str) -> dict:
    """Loads an oreimo-es consolidated JSON into the opened project,
    matching scenes by name and lines by position within each scene.

    Scenes whose line counts don't match the ISO's parse are skipped
    (reported, never mis-aligned). Returns a report dict:
      {scenes, matched_scenes, matched_lines, names_applied, skipped}
    where skipped is a list of (scene_name, reason) tuples."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    names = data.get("names", {})
    es_scenes = {
        canonical_scene(k): v for k, v in data.items() if k != "names"
    }

    matched_scenes = 0
    matched_lines = 0
    names_applied = 0
    skipped = []

    for scene_name, entries in project.scenes.items():
        value = es_scenes.get(canonical_scene(scene_name))
        if value is None:
            skipped.append((scene_name, "sin entrada en el JSON"))
            continue

        lines = _scene_lines(value)
        if len(lines) != len(entries):
            skipped.append(
                (scene_name,
                 f"{len(entries)} líneas en el ISO vs {len(lines)} en el JSON")
            )
            continue

        for entry, es in zip(entries, lines):
            speaker = entry.speaker
            if speaker is not None:
                # Our stored line is dialogue-only (or still wrapped in
                # 「」 if the pipeline left brackets); strip any leftover
                # prefix/brackets - join_speaker re-adds them on compile.
                _, dialogue = split_speaker(es)
                if not dialogue:
                    dialogue = es
                entry.translation = dialogue
                es_speaker = names.get(speaker, speaker)
                if es_speaker != speaker:
                    entry.speaker_override = es_speaker
                    names_applied += 1
            else:
                # Narration / chapter titles ('--...' lines): verbatim.
                entry.translation = es
            matched_lines += 1
        matched_scenes += 1

    return {
        "scenes": len(project.scenes),
        "matched_scenes": matched_scenes,
        "matched_lines": matched_lines,
        "names_applied": names_applied,
        "skipped": skipped,
    }
