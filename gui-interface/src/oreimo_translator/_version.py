"""
The app's version, in one place.

This is the single source of truth: the About dialog reads it, and the
release workflow reads it too. If the version here has no tag yet, that
is what gets published; otherwise the workflow falls back to bumping the
patch number of the latest tag, which is how routine releases work.

Bumping a major or minor version is therefore a code change, reviewed
like any other, rather than something typed into a tag by hand and
silently disagreeing with what the app reports about itself. It used to:
this stayed at 0.1.0 through every release up to v0.1.6.
"""
__version__ = "1.0.0"
