"""
Line breaking for dialogue, so translated text doesn't run off the box.

The engine wraps nothing by itself. A line is drawn as one continuous run
until it meets the fullwidth underscore U+FF3F ('＿'), the script's
explicit break marker. Type a long line without one and it keeps drawing
past the edge of the textbox - which is what "the letters run off the
screen" looks like.

This project's command-line pipeline already solved that: the
FastAsyncOreimoTranslateTool toolchain has an `insert-linebreaks` step
(`TranslateCLI/LineBreaksInserterCLI.cs`) run as `insert-linebreaks 0 570`,
and the Spanish translation shipped in this repo went through it. What
follows is a faithful port of that code, using the same glyph widths
(see fontmap.py), so this app breaks lines in exactly the same places the
pipeline does instead of inventing a second, subtly different answer.

Measured against the discs, both the shipped English script and the
existing Spanish one leave 0.14% of drawn lines over the limit, and those
are lines carrying ｛size：...｝ control codes that are handled separately
rather than genuine overflows.

Faithful details worth not "improving"
--------------------------------------
- The speaker name is not measured. It's a separate field that the game
  draws in its own box; only the opening bracket '「' is charged, and only
  for speech. (Counting the whole 'Name「' prefix claims 67.7% of the
  game's own lines overflow, which they visibly don't.)
- A line that already contains a marker is left completely alone, even if
  it still looks too long. Whoever put that marker there - the original
  localizers, the pipeline, or the translator - gets the last word.
- Text inside [ ] is pulled out, wrapped on its own, and put back. The
  brackets mark a continuation page, and its contents wrap independently.
- A string that ends up more than three lines long is restructured: the
  first lines stay, the rest move into a [ ] continuation and are
  re-wrapped, because the textbox only shows three lines at a time.
- An unknown glyph is charged the width of '0', which is what the
  toolchain does. Matching it matters more than a cleverer guess.
"""
import re

from .fontmap import ADVANCE, FALLBACK

WRAP_MARKER = "＿"

# The textbox, in pixels: the width the pipeline is invoked with
# (`insert-linebreaks 0 570`).
MAX_LINE_WIDTH = 570

# How many lines the box shows before the rest has to go to a
# continuation page.
LINES_PER_BOX = 3

SPEECH_BRACKET = "「"


def measure(text: str, is_speech: bool = False) -> int:
    """Rendered width of one drawn line, in pixels."""
    width = sum(ADVANCE.get(c, FALLBACK) for c in text)
    if is_speech:
        width += ADVANCE.get(SPEECH_BRACKET, 0)
    return width


def segments(text: str) -> list[str]:
    """The individual drawn lines a string produces."""
    return text.split(WRAP_MARKER)


def overflows(text: str, is_speech: bool = False,
              max_width: int = MAX_LINE_WIDTH) -> bool:
    """True if any line this string produces runs past the box."""
    return any(measure(s, is_speech) > max_width for s in segments(text))


def widest(text: str, is_speech: bool = False) -> int:
    """Width of the longest line this string produces."""
    return max((measure(s, is_speech) for s in segments(text)), default=0)


# Return values of status().
FITS = "fits"          # nothing to do
WILL_WRAP = "will"     # too wide, but compiling will break it up
NEEDS_HELP = "needs"   # too wide and compiling will NOT fix it


def status(text: str, is_speech: bool = False,
           max_width: int = MAX_LINE_WIDTH) -> str:
    """Whether a line fits, will be fixed automatically at compile time,
    or is going to overflow in-game unless the writer intervenes.

    The two failing cases look identical in the text but are completely
    different problems, so they should not look identical on screen. A
    line with no marker in it gets broken up on compile and needs no
    attention at all. A line that already carries a marker is left alone
    on purpose - whoever placed it gets the last word - so if one of its
    segments is still too wide, nothing downstream will save it."""
    if not overflows(text, is_speech, max_width):
        return FITS
    if overflows(wrap(text, is_speech, max_width), is_speech, max_width):
        return NEEDS_HELP
    return WILL_WRAP


def _insert(text: str, is_speech: bool, max_width: int) -> str:
    """Port of LineBreaksInserterCLI.InsertLineBreaks."""
    bracketed = None
    if "[" in text and "]" in text:
        match = re.search(r"\[(.*?)\]", text)
        if match:
            bracketed = match.group(1)
            text = text.replace("[" + bracketed + "]", "")

    if measure(text, is_speech) > max_width and WRAP_MARKER not in text:
        built = ""
        for word in text.split(" "):
            if WRAP_MARKER in built:
                # Only the current line counts towards the limit, so
                # measure from the last marker onwards.
                candidate = built[built.rindex(WRAP_MARKER):] + " " + word
            else:
                candidate = built + " " + word
            if measure(candidate, is_speech) > max_width:
                built += WRAP_MARKER + word
            else:
                built += " " + word
        text = built.strip()

    if bracketed is not None:
        text += "[" + _insert(bracketed, is_speech, max_width) + "]"
    return text


def wrap(text: str, is_speech: bool = False,
         max_width: int = MAX_LINE_WIDTH) -> str:
    """Adds break markers where the text would overflow, and moves
    anything past the third line into a continuation page. Port of
    LineBreaksInserterCLI plus the restructuring step its caller
    (TranslationProjectCli.InsertLineBreaks) applies afterwards."""
    if not text:
        return text

    result = _insert(text, is_speech, max_width)

    # Only reflow into a continuation page when every marker in the
    # result is one we just added. The restructuring step flattens all
    # markers and measures again, which would relocate breaks that a
    # translator - or the pipeline, on an earlier run - deliberately
    # placed. Skipping it here is what takes agreement with the
    # command-line pipeline's own output from 99.85% to 100%.
    if WRAP_MARKER in text:
        return result

    parts = result.split(WRAP_MARKER)
    if len(parts) >= LINES_PER_BOX + 1:
        keep = 2 if len(parts) == LINES_PER_BOX + 1 else 3
        rebuilt = (WRAP_MARKER.join(parts[:keep])
                   + "[" + WRAP_MARKER.join(parts[keep:]) + "]")
        rebuilt = rebuilt.replace(WRAP_MARKER, " ")
        result = _insert(rebuilt, is_speech, max_width)

    return _split_unbreakable(result, is_speech, max_width)


def _split_unbreakable(text: str, is_speech: bool, max_width: int) -> str:
    """Cuts inside a word that is wider than the whole box.

    The upstream algorithm can only break at spaces, so a single token
    with no space in it is emitted on a line of its own and still runs
    off the screen (it also leaves an empty line in front of it, since
    the break goes before the first word). Prose never hits this, which
    is why the pipeline gets away with it, but a long unbroken string
    does - and that is precisely the case that shows up as letters
    marching off the edge.

    Deliberately narrow: it only touches a line that has no space and no
    ｛size：...｝ control code in it, so every line the pipeline handles
    is left exactly as the pipeline left it."""
    lines = []
    for line in text.split(WRAP_MARKER):
        if (measure(line, is_speech) <= max_width
                or " " in line or "｛" in line):
            lines.append(line)
            continue
        current = ""
        for ch in line:
            if current and measure(current + ch, is_speech) > max_width:
                lines.append(current)
                current = ch
            else:
                current += ch
        if current:
            lines.append(current)
    # An empty leading line is the upstream quirk described above; it
    # would render as a blank first row in the box.
    while len(lines) > 1 and not lines[0]:
        lines.pop(0)
    return WRAP_MARKER.join(lines)
