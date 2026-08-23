# App icon

Drop the master icon here as **`icon.png`** — square, **1024×1024**, PNG
with transparency. Then generate the per-platform formats:

```bash
python3 scripts/make_icons.py              # art already has its own shape
python3 scripts/make_icons.py --round-corners   # full-bleed square art
```

That writes `icon.ico` (embedded in the Windows `.exe`) and `icon.icns`
(embedded in the macOS `.app`). Commit all three: the release workflow
builds on Windows and macOS runners, and `.icns` generation needs macOS's
`iconutil`, so they can't be produced during CI.

Use `--round-corners` when the source art is a full-bleed square. macOS
does **not** round app icons automatically the way iOS does, so a square
would sit in the Dock as a hard tile among rounded neighbours; the flag
applies Apple's standard inset and corner radius to the `.icns` only. Skip
it when the art already has its own silhouette, or the mask will clip it.

Keep meaningful detail large — the same file is rendered down to 16×16 in
the Windows taskbar.

Until `icon.png` exists the app and both builds work fine, just without an
icon: `resources.app_icon_path()` returns `None` and the spec omits the
icon arguments rather than pointing PyInstaller at a missing file.
