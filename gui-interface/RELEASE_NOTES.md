<!--
This file is injected verbatim into the body of every GitHub Release by
.github/workflows/release.yml (both the automatic release on push to
main, and manual vX.Y.Z tag releases). It describes what the app can do
as of the current state of main - keep it updated in the same PR that
adds or changes a user-facing feature, since that PR's merge into main
is what publishes the next release.

Write it for someone downloading the app, not for someone reading the
code: no file paths, no internal FORMAT_NOTES.md section references.
-->

### What the app does

- **Open an ISO directly** — reads the game's data straight out of the
  raw `.iso` file. No mounting, no UMD tools, no extra setup. All ~19,000
  dialogue lines across every scene of either disc are indexed in a few
  seconds.
- **Browse and search everything at once** — scenes on the left, and a
  table showing character, original Japanese, and your translation side
  by side. The search box filters across every scene simultaneously,
  matching either the original or the translated text.
- **Translate in place** — double-click any translation cell and type.
  Accented and special characters are supported and have been verified
  in-game.
- **Export and import CSV/TSV** — hand the whole project, a single scene,
  or every scene as separate files to Excel, Google Sheets, or other
  translators, then import the results back. Every row carries a stable
  ID, so re-imported edits land on the right line even after closing and
  re-opening the ISO.
- **View, export and import the game's images** — the Images tab decodes
  and previews every background, event/CG, character and cutin/tukkomi
  texture attached to a scene. Checkboxes filter the scene list down to
  just the scenes containing a given kind of image, which makes finding
  baked-in Japanese text practical. Export them as PNGs, edit them in any
  image editor, and import the folder back in.
- **Compile a playable translated ISO** — rebuilds only what you actually
  edited and writes a fresh copy of the ISO; your original file is never
  modified. Dialogue-only builds typically finish in well under a second.
- **Gets the risky details right so the game doesn't break** — edited
  images are re-encoded in their original pixel format instead of being
  silently blown up to a larger one (which overruns the game's texture
  memory and crashes it), and the game's internal table of file offsets
  is regenerated whenever anything shifts (a stale one freezes the game
  on load). Both of these were real failures, found in-game and fixed.
  If an edit still ends up larger than the original, you get a warning at
  compile time instead of discovering it during a playthrough.
- **Breaks long lines for you** — the game does no word wrapping of its
  own: text just runs off the edge of the box unless the script says
  where to break. Write naturally and the app measures every line against
  the real textbox using the game's own font, adding the breaks when you
  compile. Lines are flagged as you type — blue for "this will be split
  for you", red for the rare case that needs your attention — and if you
  want to pick the break point yourself, you can.
- **Builds the disc without re-mastering it** — a translated or
  image-edited file that outgrew its slot used to mean rebuilding the
  whole 1.4 GB image. The app now resizes files inside the ISO itself, so
  compiling takes seconds and the disc it writes is usually byte-for-byte
  the same size as the one you opened. Every file is read back and checked
  against the original afterwards.
- **Stays responsive** — opening an ISO, compiling, and bulk image export
  all run in the background instead of freezing the window.

### Requirements

**Nothing but the download.** Everything the app does — including
compiling a playable ISO with image edits — works on Windows, macOS and
Linux with no installs and no external tools. Earlier versions needed
cdrtools for some compiles; that is no longer the case.

### Known limitations

- `Choice` / `Question` blocks (in-game player menus) are preserved
  intact but not editable here yet.
- Character expression overlays (mouth/eye parts) are shown as separate
  raw parts rather than composited onto the sprite, and are excluded from
  image reinsertion.
- Scene ordering follows the order on the disc, which is not always the
  in-game chronological order.
