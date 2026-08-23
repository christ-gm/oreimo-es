import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .gui.main_window import MainWindow
from .resources import app_icon_path


def _claim_windows_taskbar_identity():
    """Without an explicit AppUserModelID, Windows groups the app under
    whatever process launched it and shows THAT icon in the taskbar -
    python.exe's, when running from source. Matches the spec's
    bundle_identifier so both builds present the same identity."""
    if sys.platform != "win32":
        return
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "com.choviics.oreimotranslator"
    )


def _should_set_window_icon() -> bool:
    """A frozen macOS build already has the right icon - the .app
    bundle's .icns, inset and corner-rounded to match the platform.
    setWindowIcon would override the Dock tile with whatever it's handed,
    which here is the raw full-bleed square PNG, so it actively makes the
    icon worse. Confirmed by running two builds side by side, identical
    except that one had the runtime PNG deleted: only that one showed the
    rounded icon in the Dock.

    Everywhere else there's no bundle icon to defer to - Windows and
    Linux, and macOS run from source - so the PNG is the only icon
    available and setting it is what puts one on screen at all."""
    return not (sys.platform == "darwin" and getattr(sys, "frozen", False))


def main():
    _claim_windows_taskbar_identity()
    app = QApplication(sys.argv)

    # Covers the window and taskbar/alt-tab icon on Windows and Linux,
    # and the Dock icon when running from source on macOS.
    icon_path = app_icon_path()
    if icon_path is not None and _should_set_window_icon():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
