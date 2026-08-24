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
   across every scene of the opened disc (either one) in a few seconds.
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
   finishes in well under a second, even for a full-disc project.
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
   `RES.DAT`. Each edited image is re-encoded in its *original* pixel
   format (palette or RGBA8888) rather than always RGBA8888, since that
   mismatch alone can exceed the game's texture memory budget and crash
   it in-game — see `documentation/FORMAT_NOTES.md` §23 for the real
   crash this was found from and fixed. Compiling also regenerates
   `RES.DAT`'s seekmap (a table of absolute file offsets the game seeks
   with, stored inside `first.dat`) whenever anything moves — a stale one
   hangs the game on load, see §24.
7. **Stays responsive during slow operations** — opening an ISO,
   compiling, and bulk image export all run on a background thread
   instead of freezing the window (the whole UI, including the mouse
   cursor, used to lock up during a full ISO rebuild).

## Getting started

### Download a prebuilt binary (recommended)

Every merge into `main` — and every manual `vX.Y.Z` tag — triggers an
automated build for both **Windows** and **macOS** via GitHub Actions,
published under [Releases](../../releases) with a full description of
what the app can do. Just download the build for your OS and run it — no
Python installation required. This is the easiest and recommended way to
get the app.

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
- Windows: nothing to install — the app finds the standalone
  `tool-bin/mkisofs.exe` shipped in this repo automatically (prebuilt
  Windows binaries even bundle it inside)

## Load the Spanish translation (oreimo-es)

This repo ships a complete Spanish translation of both discs. To apply
it with the GUI instead of translating from scratch:

1. Open the **English v1** ISO of the disc you want — the title bar
   shows which disc was detected (`NPJH-50568` = Disc 1, `NPJH-50569`
   = Disc 2).
2. `File > Import ES translation (oreimo-es JSON)...` and pick:
   - `translation/Translation.json` for Disc 1
   - `translation/Translation_disc2.json` for Disc 2

   The file dialog suggests the right one based on the detected disc.
3. Every scene loads pre-translated (speaker names included); edit
   anything you like on top of it, then `File > Compile ISO...`.

Scenes whose line counts don't match the ISO parse are skipped and
reported rather than mis-applied. The compiled ISO needs a full rebuild
when `RES.DAT` changes size (importing a whole translation always does),
which is why the bundled `mkisofs` matters here.

## Current scope

| Content | Status |
|---|---|
| `Dialogue` / `Dialogue2` blocks (spoken lines, narration) | Fully editable |
| `Chapter` blocks (scene/chapter titles) | Fully editable |
| `Choice` / `Choice2` / `Question` blocks (player-facing menus) | Preserved byte-for-byte, not yet editable here |
| Scene ordering | Reflects on-disk order, not always in-game chronological order |
| Scene images (background/event/character/cutin/tukkomi) | Viewable, exportable to PNG, importable, and compilable into the ISO |
| Compiling image edits into the ISO | Works. Two real in-game failures were root-caused and fixed along the way: re-encoding in the wrong pixel format blew past the game's texture memory budget (`FORMAT_NOTES.md` §23), and `RES.DAT`'s seekmap — a table of absolute offsets stored in `first.dat` — went stale whenever anything changed size, hanging the game on load (§24). Both validated by measurement (11,642 palette images round-tripped with 0 mismatches; seekmap regeneration reproduces the original byte-for-byte) plus boot tests |
| Character expression-swap overlays (mouth/eye parts) | Shown as separate raw parts, not composited onto the base sprite; also excluded from image reinsertion (no builder yet for their container format) |
| Re-importing unedited images | `Import images...` re-encodes every PNG present in the folder, not just ones you actually changed — harmless now that format/size are preserved, but still wasted work (not fixed yet, see FORMAT_NOTES.md §23 "Still open") |

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

If your change adds or alters something a user would notice, update
`RELEASE_NOTES.md` in the same PR: that file is injected verbatim into
the body of every GitHub Release, and merging to `main` is what publishes
the next one.

## Credits

Developed by **[Choviics](https://github.com/Choviics)**.

This tool exists so the community can build and maintain their own
translations of this game — into Spanish, or into any other language —
without having to reverse-engineer the format from scratch. If you use it
to make one, consider sharing it back.
