# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

# The per-platform icon files are generated from assets/icon.png by
# scripts/make_icons.py and committed. Each is wired in only if it's
# actually present, so a checkout without the artwork still builds
# (PyInstaller hard-errors on an icon path that doesn't exist).
ASSETS = Path(SPECPATH) / 'assets'
ICON_PNG = ASSETS / 'icon.png'    # loaded at runtime for the window icon
ICON_ICO = ASSETS / 'icon.ico'    # embedded in the Windows executable
ICON_ICNS = ASSETS / 'icon.icns'  # embedded in the macOS .app bundle

# Nothing external is bundled any more. Compiling an ISO used to shell out
# to cdrtools' mkisofs whenever RES.DAT changed size, so Windows builds
# carried a cygwin mkisofs.exe (and its DLL) to spare users an install that
# has no one-step version on that platform. core/iso_grow.py now resizes
# files inside the ISO directly, so there is no external program left to
# ship - on any platform.

a = Analysis(
    ['app_entry.py'],
    pathex=['src'],
    binaries=MKISOFS_BUNDLES,
    datas=[(str(ICON_PNG), 'assets')] if ICON_PNG.exists() else [],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Oreimo Translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_ICO) if ICON_ICO.exists() else None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Oreimo Translator',
)
app = BUNDLE(
    coll,
    name='Oreimo Translator.app',
    icon=str(ICON_ICNS) if ICON_ICNS.exists() else None,
    bundle_identifier='com.choviics.oreimotranslator',
)
