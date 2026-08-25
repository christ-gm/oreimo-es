<!--
This file is injected verbatim into the body of every GitHub Release by
.github/workflows/release.yml (both the automatic release on push to
main, and manual vX.Y.Z tag releases). It describes what the app can do
as of the current state of main - keep it updated in the same PR that
adds or changes a user-facing feature, since that PR's merge into main
is what publishes the next release.

Keep it short. It is the first thing most people read about the tool, not
a manual - the README is the manual, and this should point at it rather
than repeat it. Write it for someone downloading the app: no file paths,
no internal FORMAT_NOTES.md section references.
-->

**Oreimo Translator** opens the game's disc image, shows you every line of
dialogue and every image inside it, lets you change them, and writes a
disc you can play.

Download it and it works. There is nothing else to install, on Windows,
macOS or Linux.

### What you can do

- **Translate the dialogue.** All ~19,000 lines of either disc, indexed in
  seconds, searchable across every scene at once. Accents and special
  characters work.
- **Let it handle the tricky parts.** Long lines are broken to fit the
  textbox automatically, character names are reattached for you, and
  edited images keep the format the game expects.
- **Work with other people.** Export to CSV or TSV for a spreadsheet or
  another translator, then import the results back where they belong.
- **Replace the images.** View, export and reimport the backgrounds,
  event CGs and cutins — useful for the text that is baked into the
  artwork rather than stored as script.
- **Build a playable disc.** Your original ISO is never modified, and most
  builds finish in seconds.

### Good to know

- **The Spanish translation is not bundled.** The app can load it in one
  step, but the translation files live in the repository — download them
  from there first.
- **Menu titles and choice buttons are images**, not text, so translating
  the script doesn't change them.
- **There is no save file.** Closing the window discards your edits, so
  export or compile before you do.

### Full documentation

Everything above in detail — how each feature works, the export and import
formats, what is and isn't supported, and how to translate the game into a
language other than Spanish — is in the
**[GUI documentation](https://github.com/christ-gm/oreimo-es/blob/main/gui-interface/README.md)**.

### Credits

Developed by **[Choviics](https://github.com/Choviics)** and
**[christ-gm](https://github.com/christ-gm)**.

Questions? Write to us on **[Facebook](FACEBOOK_LINK_HERE)**.
