# Oreimo Translator

A desktop GUI (PySide6) for translating the script of *Ore no Imouto ga
Konna ni Kawaii Wake ga Nai Portable* (PSP) — built so anyone can produce
their own fan translation of the game, in any language, without touching
a hex editor.

It is the "productized" form of the reverse-engineering work carried out
in the sibling research project (the parent folder of this repo): the
`GPDA` container format, the `.obj` script bytecode with its `blockLen`
block structure, and the binary ISO-patching approach are all proven
against the real game. This app vendors that same logic into a
self-contained Python package (`src/oreimo_translator/core/`), so it runs
on its own — no need to clone the research project or run any other
tooling first.

## How it works

The game stores its ~19,000 dialogue lines inside `RES.DAT`, a nested
archive format with strings encoded as UTF-16LE inside self-describing
binary blocks. The app automates the full round trip:

```
ISO  →  extract RES.DAT  →  decompress every scene  →  parse blocks
  →  edit strings in memory  →  rebuild blocks + archives
  →  patch a copy of the ISO  →  playable, translated ISO
```

1. **Open ISO** — reads `RES.DAT` directly out of the raw ISO file (no
   mounting, no OS-specific tools) and indexes every translatable line
   across all 300 scenes in a few seconds.
2. **Browse & search** — scenes are listed on the left; the table on the
   right shows character, original text, and translation side by side.
   The search box filters across every scene at once, matching either
   original or translated text.
3. **Translate** — double-click a translation cell and type. Edits are
   held in memory only; the source ISO is never touched until you choose
   to compile.
4. **Export / Import** — send the whole project, a single scene, or every
   scene as separate files to CSV/TSV, so translation can happen in
   Excel, Google Sheets, or handed off to other people, then re-imported.
   Each row carries stable IDs (scene + block position), so re-importing
   safely matches edits back to the right line even after re-opening the
   ISO later.
5. **Compile ISO** — rebuilds only the scenes that were actually edited,
   re-nests every archive level, and binary-patches the result into a
   fresh copy of the ISO (the original file is never modified). Typically
   finishes in well under a second, even for a full 300-scene project.
6. **View, export and import scene images** — the "Images" tab (its own
   full view, with its own scene list) shows every background, event/CG,
   character and cutin/tukkomi texture (`MIG.00.1PSP`/`.gim`, PSP's
   proprietary format) attached to the selected scene, decoded on demand.
   Checkboxes above the scene list filter it down to only scenes that
   actually contain a given image category (e.g. "only scenes with a
   Tukkomi" — reaction-stamp overlays, a likely place for baked-in
   Japanese text). `File > Export images...` writes PNGs (for the
   selected scene, or every scene passing the current filter) plus a
   `manifest.json` that identifies each file by scene/category/label;
   `File > Import images...` reads that folder back, validates each PNG
   (dimensions must match exactly), and marks it as a pending edit
   (highlighted in the tree, same as edited dialogue). Compiling picks
   the fastest safe method automatically: a same-size binary patch when
   possible (no extra tools needed), or a full ISO rebuild (requires
   `mkisofs` from cdrtools — see Requirements) when an image edit grows
   `RES.DAT`, which is routine.

## Getting started

### Download a prebuilt binary (recommended)

Every tagged release (`vX.Y.Z`) triggers an automated build for both
**Windows** and **macOS** via GitHub Actions, published under
[Releases](../../releases). Just download the build for your OS and run
it — no Python installation required. This is the easiest and recommended
way to get the app.

### Run from source

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m oreimo_translator.main
```

Compiling dialogue-only edits needs nothing beyond the above. Compiling
image edits needs real `mkisofs` (from **cdrtools**, not `xorriso` — it
silently produces a disc the PSP won't boot correctly, see
`documentation/FORMAT_NOTES.md` §13/§22) on `PATH`:
- macOS: `brew install cdrtools`
- Linux: `sudo apt install genisoimage` (provides `mkisofs`) or your
  distro's `cdrtools`/`cdrkit` package
- Windows: not yet wired up in this app; a Windows `mkisofs.exe` exists
  in `tool-bin/` from the sibling toolchain project but isn't bundled here yet

## Current scope

| Content | Status |
|---|---|
| `Dialogue` / `Dialogue2` blocks (spoken lines, narration) | Fully editable |
| `Chapter` blocks (scene/chapter titles) | Fully editable |
| `Choice` / `Choice2` / `Question` blocks (player-facing menus) | Preserved byte-for-byte, not yet editable here |
| Scene ordering | Reflects on-disk order, not always in-game chronological order |
| Scene images (background/event/character/cutin/tukkomi) | Viewable, exportable to PNG, importable, and compilable into the ISO |
| Compiling image edits into the ISO | Works — boot-tested in PPSSPP (no hang/crash, reaches the title screen and beyond); a full manual playthrough to a specific edited scene hasn't been done yet, see `documentation/FORMAT_NOTES.md` §22 |
| Character expression-swap overlays (mouth/eye parts) | Shown as separate raw parts, not composited onto the base sprite; also excluded from image reinsertion (no builder yet for their container format) |

The `.obj`/`GPDA`/ISO-patch pipeline underneath has been validated
end-to-end with real playtests (PPSSPP), including special characters,
line-length changes, and multi-scene rebuilds — see the sibling research
project's `documentation/FORMAT_NOTES.md` for the full technical history,
including how a couple of nasty bugs (a silent ISO-rebuild corruption, a
stale block-length header causing crashes on resize) were tracked down
and fixed.

## Contributing

Translation-workflow planning (glossaries, terminology, roadmaps) is
tracked outside this repository by design — this repo is just the tool
and its tests. Issues and pull requests around the GUI itself are welcome.

## Credits

Developed by **[Choviics](https://github.com/Choviics)**.

This tool exists so the community can build and maintain their own
translations of this game — into Spanish, or into any other language —
without having to reverse-engineer the format from scratch. If you use it
to make one, consider sharing it back.
