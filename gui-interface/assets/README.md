# App icon

Drop the master icon here as **`icon.png`** — square, **1024×1024**, PNG.
A full-bleed square is fine; the rounding is handled for you. Then
generate the per-platform formats:

```bash
python3 scripts/make_icons.py
```

That writes `icon.ico` (embedded in the Windows `.exe`) and `icon.icns`
(embedded in the macOS `.app`). Commit all three: the release workflow
builds on Windows and macOS runners, and `.icns` generation needs macOS's
`iconutil`, so they can't be produced during CI.

macOS does **not** round app icons automatically the way iOS does, so a
square would sit in the Dock as a hard tile among rounded neighbours. The
script therefore applies Apple's standard inset and corner radius to the
`.icns` by default — the `.ico` stays full-bleed, which is the Windows
convention. Pass `--no-round-corners` only if the artwork already carries
its own silhouette, which the mask would otherwise clip.

Keep meaningful detail large — the same file is rendered down to 16×16 in
the Windows taskbar.

Until `icon.png` exists the app and both builds work fine, just without an
icon: `resources.app_icon_path()` returns `None` and the spec omits the
icon arguments rather than pointing PyInstaller at a missing file.
