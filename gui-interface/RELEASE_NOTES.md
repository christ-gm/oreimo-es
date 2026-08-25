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

**Oreimo Translator** opens the game's disc image, shows you every line
of dialogue and every image in it, lets you change them, and writes a
disc you can play. Download it and it works — there is nothing else to
install, on Windows, macOS or Linux.

### What you can do with it

- **Open an ISO directly.** It reads the game's data straight out of the
  raw `.iso` file — no mounting, no UMD tools, no setup. All ~19,000
  dialogue lines across every scene of either disc are indexed in a few
  seconds.
- **Browse and search everything at once.** Scenes on the left, and a
  table showing character, original text, and your translation side by
  side. The search box filters across every scene simultaneously,
  matching either the original or the translation.
- **Translate in place.** Double-click any translation cell and type.
  Accented and special characters work and have been verified in-game.
- **Long lines are broken for you.** The game wraps nothing by itself —
  text simply runs off the edge of the box unless the script says where
  to break. Write naturally: the app measures every line against the real
  textbox using the game's own font and inserts the breaks when you
  compile. Lines are flagged as you type, and you can place a break
  yourself when you want to choose where it falls.
- **Hand the work to other people.** Export the whole project, one scene,
  or every scene as separate files for Excel, Google Sheets or another
  translator, then import the results back. Every row carries a stable ID,
  so re-imported edits land on the right line even after closing and
  reopening the ISO.
- **View, export and replace the game's images.** The Images tab decodes
  every background, event/CG, character and cutin texture attached to a
  scene. Filters narrow the scene list to just the ones containing a given
  kind of image, which makes finding baked-in Japanese text practical.
  Export them as PNGs, edit them anywhere, and import the folder back.
- **Compile a playable disc.** It rebuilds only what you actually edited
  and writes a fresh copy; your original ISO is never modified. Most
  builds finish in seconds, and the disc usually comes out byte-for-byte
  the same size as the one you opened.

### The parts that quietly go wrong if nobody handles them

Each of these was a real failure, found by playing the game and fixed:

- An edited image is re-encoded in its **original pixel format**, and
  reduced to fit it when necessary. Storing it at full colour instead
  would multiply the texture's memory several times over, and the game
  then fails to load it — so the edit looks like it simply never
  happened.
- The game's internal **table of file offsets** is regenerated whenever
  anything shifts. A stale one freezes the game on load.
- Making a file bigger **doesn't disturb anything else on the disc**.
  Everything is read back and checked against the original after every
  compile.

### Requirements

Nothing but the download. Earlier versions needed `mkisofs` from cdrtools
for some compiles; that requirement is gone.

### Known limitations

- **The Spanish translation is not bundled.** The app can load this
  project's finished Spanish translation for either disc in one step, but
  the translation files themselves live in the source repository — if you
  only downloaded the app, fetch them from there first.
- **Menu titles and choice buttons are images, not text.** Their wording
  is baked into the pixels, so translating the script doesn't touch them;
  they have to be redrawn as images.
- **Character expression overlays** (mouth and eye parts) are shown as
  separate raw parts rather than composited onto the sprite, and cannot be
  reinserted yet.
- `Choice` / `Question` blocks are preserved intact but not editable here.
- Scene ordering follows the order on the disc, which is not always the
  in-game chronological order.

### Translating into a language other than Spanish

Nothing here is specific to Spanish. The script is stored as UTF-16, so
any character encodes, and the game's font already carries complete sets
for Portuguese, French, German, Italian, Catalan, Polish, Turkish,
Russian and Greek — only Vietnamese falls short. Use the CSV export and
import route. Note that Cyrillic and Greek have never actually been put
on screen, so compile one line and look at it before committing to a
whole script.
