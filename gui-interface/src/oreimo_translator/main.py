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


def main():
    _claim_windows_taskbar_identity()
    app = QApplication(sys.argv)

    # Covers the window and taskbar/alt-tab icon on Windows and Linux.
    # macOS takes the Dock icon from the .app bundle's .icns instead, so
    # this only affects the from-source run there.
    icon_path = app_icon_path()
    if icon_path is not None:
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
