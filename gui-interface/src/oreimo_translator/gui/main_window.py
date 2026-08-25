from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QAction, QColor, QImage, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QListWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QFileDialog, QMessageBox, QApplication, QAbstractItemView,
    QTabWidget, QTreeWidget, QTreeWidgetItem, QScrollArea, QCheckBox,
)

from ..core import Project
from ..core import scene_images
from ..core import image_io
from ..core import es_bridge
from ..core import text_wrap

APP_VERSION = "0.1.0"
AUTHOR_NAME = "Choviics"
AUTHOR_GITHUB = "https://github.com/Choviics"

EDITED_BACKGROUND = QColor(255, 244, 140)
EDITED_FOREGROUND = QColor(20, 20, 20)
# A line that would be drawn past the edge of the textbox. Compiling
# inserts break markers to fix it, but flagging it here lets the
# translator see it while writing rather than discovering it in-game.
OVERFLOW_BACKGROUND = QColor(255, 138, 128)
OVERFLOW_FOREGROUND = QColor(20, 20, 20)
OVERFLOW_TOOLTIP = (
    "Esta linea se sale de la caja de texto. Al compilar se parte "
    "automaticamente; coloca un \uff3f a mano si prefieres elegir "
    "donde cae el salto."
)


def _mark_edited(item: QTableWidgetItem, edited: bool,
                 width_status: str = text_wrap.FITS):
    """Highlights an edited translation cell with a readable yellow (dark
    text on a light yellow background, set explicitly so it stays legible
    regardless of the OS light/dark theme - the previous version only set
    a yellow background and inherited the theme's text color, which was
    unreadable in dark mode). Clears back to the theme default (rather
    than hardcoding white) when not edited."""
    # "I changed this" and "this is too wide" are separate facts, so
    # they get separate channels: the background keeps meaning edited,
    # and width speaks through the tooltip and - only when it actually
    # needs the writer - a background of its own. Letting width win
    # outright is what made an edited long line stop looking edited.
    if width_status == text_wrap.NEEDS_HELP:
        # Rare, and nothing downstream will fix it: worth overriding the
        # edited colour for.
        item.setBackground(OVERFLOW_BACKGROUND)
        item.setForeground(OVERFLOW_FOREGROUND)
        item.setToolTip(OVERFLOW_TOOLTIP)
        return
    if edited:
        item.setBackground(EDITED_BACKGROUND)
        item.setForeground(EDITED_FOREGROUND)
    elif width_status == text_wrap.WILL_WRAP:
        item.setBackground(WILL_WRAP_BACKGROUND)
        item.setForeground(WILL_WRAP_FOREGROUND)
    else:
        item.setData(Qt.BackgroundRole, None)
        item.setData(Qt.ForegroundRole, None)
    item.setToolTip(WILL_WRAP_TOOLTIP if width_status == text_wrap.WILL_WRAP else "")

COL_SCENE = 0
COL_CHARACTER = 1
COL_ORIGINAL = 2
COL_TRANSLATION = 3

IMAGE_ROLE = Qt.UserRole + 1  # holds a SceneImage on leaf items in the image tree

ALL_IMAGE_CATEGORIES = [label for _, label in scene_images.SCENE_CATEGORIES] + \
    [label for _, label in scene_images.NESTED_CATEGORIES]


class _Worker(QThread):
    """Runs one no-argument callable on a background thread and reports
    back via signals - used for anything slow enough to freeze the UI if
    run directly on the main thread (ISO load, ISO compile, bulk image
    export). Compiling is much cheaper now that resizing happens inside
    the ISO rather than by re-mastering it, but it still copies a 1.4 GB
    file, which is long enough to freeze the window - including the mouse
    pointer, since Qt couldn't process any events - if run inline."""
    succeeded = Signal(object)
    failed = Signal(str)

    def __init__(self, fn, parent=None):
        super().__init__(parent)
        self._fn = fn

    def run(self):
        try:
            result = self._fn()
        except Exception as exc:
            self.failed.emit(str(exc))
        else:
            self.succeeded.emit(result)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oreimo Translator")
        self.resize(1100, 700)

        self.project: Project | None = None
        self._populating = False  # guards against itemChanged feedback while we fill the table

        self._build_menu()
        self._build_central_widget()
        self._update_status()

    # ---- UI construction -------------------------------------------------

    def _build_menu(self):
        file_menu = self.menuBar().addMenu("&File")

        act_open = file_menu.addAction("&Open ISO...")
        act_open.triggered.connect(self.open_iso)

        file_menu.addSeparator()

        act_export_all = file_menu.addAction("Export &all scenes (one file per scene)...")
        act_export_all.triggered.connect(self.export_all_scenes)

        act_export_scene = file_menu.addAction("Export &selected scene...")
        act_export_scene.triggered.connect(self.export_selected_scene)

        act_export_single = file_menu.addAction("Export everything to a &single file...")
        act_export_single.triggered.connect(self.export_table)

        file_menu.addSeparator()

        act_import = file_menu.addAction("&Import file(s)...")
        act_import.triggered.connect(self.import_tables)

        act_import_es = file_menu.addAction("Import &ES translation (oreimo-es JSON)...")
        act_import_es.triggered.connect(self.import_es_translation)

        file_menu.addSeparator()

        act_export_images_scene = file_menu.addAction("Export &images for selected scene...")
        act_export_images_scene.triggered.connect(self.export_images_selected_scene)

        act_export_images_filtered = file_menu.addAction("Export images for &filtered scenes...")
        act_export_images_filtered.triggered.connect(self.export_images_filtered)

        act_import_images = file_menu.addAction("Import ima&ges...")
        act_import_images.triggered.connect(self.import_images)

        file_menu.addSeparator()

        act_compile = file_menu.addAction("&Compile ISO...")
        act_compile.triggered.connect(self.compile_iso)

        help_menu = self.menuBar().addMenu("&Help")
        act_about = help_menu.addAction("&About Oreimo Translator...")
        act_about.setMenuRole(QAction.MenuRole.NoRole)
        act_about.triggered.connect(self.show_about)

    def _build_central_widget(self):
        # The tab bar is the top-level central widget (full window width,
        # above everything else) rather than being scoped to one pane of a
        # splitter - Dialogue and Images are two fully independent views,
        # each with its own scene list, so switching tabs is an obvious,
        # unambiguous mode switch instead of a tab bar floating next to a
        # shared sidebar.
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self._build_dialogue_tab(), "Dialogue")
        self.tabs.addTab(self._build_images_tab(), "Images")

        self.status_label = QLabel()
        self.statusBar().addWidget(self.status_label)

    def _build_dialogue_tab(self) -> QWidget:
        widget = QWidget()
        root = QVBoxLayout(widget)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search all dialogue (original or translation)...")
        self.search_box.textChanged.connect(self._on_search_changed)
        search_row.addWidget(self.search_box)
        root.addLayout(search_row)

        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter, 1)

        self.scene_list = QListWidget()
        self.scene_list.currentTextChanged.connect(self._on_scene_selected)
        splitter.addWidget(self.scene_list)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Scene", "Character", "Original", "Translation"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(COL_SCENE, 120)
        self.table.setColumnWidth(COL_CHARACTER, 100)
        self.table.setColumnWidth(COL_ORIGINAL, 380)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.itemChanged.connect(self._on_item_changed)
        splitter.addWidget(self.table)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        return widget

    def _build_images_tab(self) -> QWidget:
        """Scene images panel: a scene list on the left - filterable by
        which image categories (Background/Event.CG/Character/Cutin/
        Tukkomi, see core/scene_images.py) a scene actually contains -
        a category/name tree for the selected scene in the middle, and a
        scaled preview on the right. Pixel decoding is on-demand per
        selected image, not eager, since a scene can have 40+ character-
        part textures and each decode costs real time (~100ms for a
        512x512 texture, pure-Python unpacking)."""
        widget = QWidget()
        root = QVBoxLayout(widget)

        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Show scenes with:"))
        self.image_category_checks: dict[str, QCheckBox] = {}
        for label in ALL_IMAGE_CATEGORIES:
            box = QCheckBox(label)
            box.setChecked(True)
            box.stateChanged.connect(self._on_image_filter_changed)
            filter_row.addWidget(box)
            self.image_category_checks[label] = box
        filter_row.addStretch(1)
        root.addLayout(filter_row)

        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter, 1)

        self.image_scene_list = QListWidget()
        self.image_scene_list.currentTextChanged.connect(self._on_image_scene_selected)
        splitter.addWidget(self.image_scene_list)

        self.image_tree = QTreeWidget()
        self.image_tree.setHeaderHidden(True)
        self.image_tree.setMinimumWidth(220)
        self.image_tree.currentItemChanged.connect(self._on_image_selected)
        splitter.addWidget(self.image_tree)

        preview_widget = QWidget()
        preview_column = QVBoxLayout(preview_widget)
        self.image_info_label = QLabel("Select a scene, then an image.")
        preview_column.addWidget(self.image_info_label)
        self.image_scroll = QScrollArea()
        self.image_scroll.setWidgetResizable(True)
        self.image_preview_label = QLabel()
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_scroll.setWidget(self.image_preview_label)
        preview_column.addWidget(self.image_scroll, 1)
        splitter.addWidget(preview_widget)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 0)
        splitter.setStretchFactor(2, 1)
        return widget

    # ---- actions -----------------------------------------------------

    def open_iso(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open ISO", "", "ISO images (*.iso)")
        if not path:
            return

        def load():
            project = Project()
            project.load(path)
            return project

        def on_success(project):
            self.project = project
            title = f"Oreimo Translator - {Path(path).name}"
            if project.disc_serial:
                title += f" [{project.disc_serial}]"
            self.setWindowTitle(title)
            self.scene_list.clear()
            self.scene_list.addItems(project.scene_names())
            self.search_box.clear()
            self.table.setRowCount(0)

            for box in self.image_category_checks.values():
                box.blockSignals(True)
                box.setChecked(True)
                box.blockSignals(False)
            self._refresh_image_scene_list()

            self._update_status()

        def on_error(message):
            QMessageBox.critical(self, "Error opening ISO", message)

        self._run_background(load, on_success, on_error, busy_message=f"Opening {Path(path).name}...")

    def export_table(self):
        """Exports every scene into a single combined file."""
        if not self._require_project():
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export everything to a file", "translation.csv",
            "CSV (*.csv);;TSV (*.tsv)"
        )
        if not path:
            return
        delimiter = "\t" if path.lower().endswith(".tsv") else ","
        try:
            self.project.export_table(path, delimiter=delimiter)
        except Exception as exc:
            QMessageBox.critical(self, "Error exporting", str(exc))
            return
        QMessageBox.information(self, "Exported", f"Table exported to:\n{path}")

    def export_selected_scene(self):
        if not self._require_project():
            return
        current = self.scene_list.currentItem()
        if not current:
            QMessageBox.information(self, "No scene selected", "Select a scene in the list first.")
            return
        scene_name = current.text()
        path, _ = QFileDialog.getSaveFileName(
            self, "Export scene", f"{scene_name}.csv",
            "CSV (*.csv);;TSV (*.tsv)"
        )
        if not path:
            return
        delimiter = "\t" if path.lower().endswith(".tsv") else ","
        try:
            self.project.export_scene(scene_name, path, delimiter=delimiter)
        except Exception as exc:
            QMessageBox.critical(self, "Error exporting", str(exc))
            return
        QMessageBox.information(self, "Exported", f"Scene {scene_name!r} exported to:\n{path}")

    def export_all_scenes(self):
        """Exports every scene to its own file (named after the scene) in
        a chosen folder - so files can be sent/edited/re-imported
        individually or as any group later."""
        if not self._require_project():
            return
        directory = QFileDialog.getExistingDirectory(self, "Choose destination folder")
        if not directory:
            return

        def on_success(written):
            QMessageBox.information(
                self, "Exported",
                f"{len(written)} files (one per scene) written to:\n{directory}"
            )

        def on_error(message):
            QMessageBox.critical(self, "Error exporting", message)

        self._run_background(
            lambda: self.project.export_all_per_scene(directory),
            on_success, on_error, busy_message="Exporting all scenes...",
        )

    def import_tables(self):
        """Imports one or more previously-exported files at once - each
        file's rows are matched back to their scene by the 'scene' column,
        so any combination of files (one scene, several, or all of them)
        can be selected together and applied in one go."""
        if not self._require_project():
            return
        paths, _ = QFileDialog.getOpenFileNames(self, "Import file(s)", "", "CSV/TSV (*.csv *.tsv)")
        if not paths:
            return

        try:
            results = self.project.import_tables(paths)
        except Exception as exc:
            QMessageBox.critical(self, "Error importing", str(exc))
            return

        self._refresh_current_view()
        self._update_status()

        all_warnings = []
        for path, warnings in results.items():
            for w in warnings:
                all_warnings.append(f"{Path(path).name}: {w}")

        if all_warnings:
            preview = "\n".join(all_warnings[:20])
            if len(all_warnings) > 20:
                preview += f"\n... and {len(all_warnings) - 20} more warnings"
            QMessageBox.warning(self, "Imported with warnings", preview)
        else:
            QMessageBox.information(
                self, "Imported",
                f"{len(paths)} file(s) imported, all rows applied successfully."
            )

    def import_es_translation(self):
        """Loads an oreimo-es consolidated translation JSON (Translation.json
        for disc 1, Translation_disc2.json for disc 2) into the opened
        project, applying the existing Spanish translation in one go."""
        if not self._require_project():
            return

        suggested = "Translation_disc2.json" if self.project.disc_serial == "NPJH-50569" else "Translation.json"
        path, _ = QFileDialog.getOpenFileName(
            self, "Importar traducción ES", suggested, "JSON (*.json)"
        )
        if not path:
            return

        def load():
            return es_bridge.load_es_translation(self.project, path)

        def on_success(report):
            self._refresh_current_view()
            self._update_status()

            skipped = report["skipped"]
            summary = (
                f"Escenas: {report['matched_scenes']}/{report['scenes']} cargadas\n"
                f"Líneas aplicadas: {report['matched_lines']}\n"
                f"Nombres traducidos: {report['names_applied']}"
            )
            if report["matched_scenes"] == 0 and report["scenes"] > 0:
                summary += (
                    "\n\nNinguna escena coincidió. ¿Seguro que este JSON es de "
                    f"este disco? ({'Disco 2 -> Translation_disc2.json' if self.project.disc_serial == 'NPJH-50569' else 'Disco 1 -> Translation.json'})"
                )
            elif skipped:
                preview = "\n".join(f"  {n}: {r}" for n, r in skipped[:15])
                if len(skipped) > 15:
                    preview += f"\n  ... y {len(skipped) - 15} más"
                QMessageBox.warning(
                    self, "Traducción ES importada con avisos",
                    f"{summary}\n\nEscenas omitidas:\n{preview}"
                )
            else:
                QMessageBox.information(self, "Traducción ES importada", summary)

        def on_error(message):
            QMessageBox.critical(self, "Error importando traducción ES", message)

        self._run_background(
            load, on_success, on_error, busy_message="Importando traducción ES...",
        )

    def export_images_selected_scene(self):
        if not self._require_project():
            return
        current = self.image_scene_list.currentItem()
        if not current:
            QMessageBox.information(self, "No scene selected", "Select a scene in the Images tab's list first.")
            return
        scene_name = current.text()
        directory = QFileDialog.getExistingDirectory(self, "Choose destination folder")
        if not directory:
            return

        def on_success(manifest):
            QMessageBox.information(
                self, "Exported",
                f"{len(manifest)} image(s) for {scene_name!r} exported to:\n{directory}"
            )

        def on_error(message):
            QMessageBox.critical(self, "Error exporting images", message)

        self._run_background(
            lambda: image_io.export_images(self.project, [scene_name], directory),
            on_success, on_error, busy_message=f"Exporting images for {scene_name}...",
        )

    def export_images_filtered(self):
        """Exports every image for every scene currently shown in the
        Images tab's scene list - i.e. whatever the category checkboxes
        are filtering to right now (or all 300 scenes if every box is
        checked, the default)."""
        if not self._require_project():
            return
        scene_names = [self.image_scene_list.item(i).text() for i in range(self.image_scene_list.count())]
        if not scene_names:
            QMessageBox.information(self, "No scenes to export", "No scenes match the current image filter.")
            return
        directory = QFileDialog.getExistingDirectory(self, "Choose destination folder")
        if not directory:
            return

        def on_success(manifest):
            QMessageBox.information(
                self, "Exported",
                f"{len(manifest)} image(s) across {len(scene_names)} scene(s) exported to:\n{directory}"
            )

        def on_error(message):
            QMessageBox.critical(self, "Error exporting images", message)

        self._run_background(
            lambda: image_io.export_images(self.project, scene_names, directory),
            on_success, on_error,
            busy_message=f"Exporting images for {len(scene_names)} scene(s)...",
        )

    def import_images(self):
        """Imports PNGs back from a folder previously written by one of
        the image export actions above (identified via that folder's
        manifest.json - see core/image_io.py). Validated replacements are
        held in memory as pending edits, same as translated dialogue text,
        until Compile ISO writes them back."""
        if not self._require_project():
            return
        directory = QFileDialog.getExistingDirectory(self, "Choose folder with manifest.json")
        if not directory:
            return

        try:
            imported, warnings = image_io.import_images(directory, self.project)
        except Exception as exc:
            QMessageBox.critical(self, "Error importing images", str(exc))
            return

        self.project.apply_image_imports(imported)
        self._refresh_image_scene_list()
        current = self.image_scene_list.currentItem()
        if current:
            self._fill_image_tree(current.text())
        self._update_status()

        message = f"{len(imported)} image(s) imported and validated."
        if warnings:
            preview = "\n".join(warnings[:20])
            if len(warnings) > 20:
                preview += f"\n... and {len(warnings) - 20} more warnings"
            QMessageBox.warning(self, "Imported with warnings", f"{message}\n\n{preview}")
        else:
            QMessageBox.information(self, "Imported", message)

    def compile_iso(self):
        if not self._require_project():
            return
        if self.project.edited_count() == 0 and self.project.edited_image_count() == 0:
            QMessageBox.information(self, "Nothing to compile", "No lines or images have been edited yet.")
            return

        default_name = Path(self.project.iso_path).stem + "_ES.iso"
        path, _ = QFileDialog.getSaveFileName(self, "Compile ISO", default_name, "ISO images (*.iso)")
        if not path:
            return

        def on_success(report):
            if report.get("res_dat_resized"):
                grew = report.get("iso_grew_by") or 0
                size_note = f"grew by {grew / 1048576:.1f} MB" if grew else "same size as the original"
                method = f"resized in place, disc {size_note}"
            else:
                method = "patched in place (same size)"
            message = (
                f"Done: {path}\n\n"
                f"Scenes changed: {len(report['scenes_changed'])}\n"
                f"Lines changed: {report['lines_changed']}\n"
                f"Images changed: {report['images_changed']}\n"
                f"Method: {method}"
                + (f"\nLines auto-wrapped: {report['lines_wrapped']}"
                   if report.get("lines_wrapped") else "")
            )
            orphans = report.get("orphan_image_edits") or []
            if orphans:
                scenes = sorted({k[0] for k in orphans})
                message += (
                    f"\n\n{len(orphans)} imported image(s) were NOT written: "
                    f"their scenes ({', '.join(scenes[:6])}) are not on this "
                    f"disc. An export from the other disc won't match."
                )

            unsupported = report.get("unsupported_image_edits") or []
            if unsupported:
                names = ", ".join(f"{s}/{c}/{l}" for s, c, l in unsupported[:10])
                if len(unsupported) > 10:
                    names += f", and {len(unsupported) - 10} more"
                message += (
                    f"\n\n{len(unsupported)} Character image edit(s) were NOT applied - "
                    f"reinserting Character images isn't supported yet:\n{names}"
                )

            encoding_warnings = report.get("encoding_warnings") or []
            if orphans and not encoding_warnings:
                QMessageBox.warning(self, "ISO compiled with warnings", message)
                return
            if encoding_warnings:
                preview = "\n".join(encoding_warnings[:20])
                if len(encoding_warnings) > 20:
                    preview += f"\n... and {len(encoding_warnings) - 20} more"
                message += (
                    f"\n\n{len(encoding_warnings)} image encoding warning(s) - these "
                    f"images ended up using more texture memory than the original, "
                    f"which can crash the game (verify in-game before shipping):\n{preview}"
                )
                QMessageBox.warning(self, "ISO compiled with warnings", message)
            else:
                QMessageBox.information(self, "ISO compiled", message)

        def on_error(message):
            QMessageBox.critical(self, "Error compiling", message)

        self._run_background(
            lambda: self.project.compile(path),
            on_success, on_error,
            busy_message="Compiling ISO...",
        )

    def show_about(self):
        QMessageBox.about(
            self, "About Oreimo Translator",
            f"<h3>Oreimo Translator</h3>"
            f"<p>Version {APP_VERSION}</p>"
            f"<p>GUI tool for extracting, translating and reinserting "
            f"dialogue for the Oreimo Spanish localization project.</p>"
            f"<p>Created by {AUTHOR_NAME}<br>"
            f"<a href=\"{AUTHOR_GITHUB}\">{AUTHOR_GITHUB}</a></p>"
        )

    # ---- view updates -----------------------------------------------------

    def _require_project(self) -> bool:
        if self.project is None:
            QMessageBox.information(self, "No ISO open", "Open an ISO first (File > Open ISO...).")
            return False
        return True

    def _set_busy(self, busy: bool, message: str = ""):
        """Disables the menu and the central tabs (so the user can't
        trigger another action, or click around the scene lists, while a
        background worker is reading/mutating the same Project instance
        on another thread) and shows a wait cursor + status message."""
        if busy:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.statusBar().showMessage(message)
        else:
            QApplication.restoreOverrideCursor()
            self.statusBar().clearMessage()
        self.menuBar().setEnabled(not busy)
        self.tabs.setEnabled(not busy)

    def _run_background(self, fn, on_success, on_error, busy_message: str = "Working..."):
        """Runs fn() on a background QThread so the UI stays responsive
        (repaints, moves the cursor, etc.) - see _Worker's docstring for
        why this exists. on_success(result) / on_error(message) run back
        on the main thread once the worker finishes.

        Keeps the worker alive in self._background_workers until Qt's own
        `finished` signal fires (guaranteed to mean the OS thread has
        actually exited) rather than dropping the reference right after
        succeeded/failed - releasing it any earlier risks Python garbage-
        collecting the QThread object while the thread is still finishing
        up, which Qt treats as fatal ("QThread: Destroyed while thread is
        still running", aborts the process). A list, not a single slot,
        so an overlapping second call (shouldn't normally happen - the
        menu is disabled while busy - but is cheap to make safe) can't
        drop an earlier worker's reference either."""
        self._set_busy(True, busy_message)
        if not hasattr(self, "_background_workers"):
            self._background_workers = []
        worker = _Worker(fn, parent=self)

        def _cleanup():
            self._set_busy(False)
            if worker in self._background_workers:
                self._background_workers.remove(worker)
            worker.deleteLater()

        worker.succeeded.connect(on_success)
        worker.failed.connect(on_error)
        worker.finished.connect(_cleanup)
        self._background_workers.append(worker)
        worker.start()

    def _on_scene_selected(self, scene_name: str):
        if not scene_name or not self.project:
            return
        if self.search_box.text().strip():
            return  # search results are showing; scene click will be handled separately if needed
        entries = self.project.entries_for_scene(scene_name)
        self._fill_table(entries, show_scene_column=False)

    def _on_search_changed(self, text: str):
        if not self.project:
            return
        text = text.strip()
        if not text:
            current = self.scene_list.currentItem()
            if current:
                self._on_scene_selected(current.text())
            else:
                self.table.setRowCount(0)
            return
        results = self.project.search(text)
        self._fill_table(results, show_scene_column=True)

    def _refresh_current_view(self):
        if self.search_box.text().strip():
            self._on_search_changed(self.search_box.text())
        else:
            current = self.scene_list.currentItem()
            if current:
                self._on_scene_selected(current.text())

    def _fill_table(self, entries, show_scene_column: bool):
        self._populating = True
        self.table.setRowCount(len(entries))
        self.table.setColumnHidden(COL_SCENE, not show_scene_column)
        for row, entry in enumerate(entries):
            scene_item = QTableWidgetItem(entry.scene)
            scene_item.setFlags(scene_item.flags() & ~Qt.ItemIsEditable)
            scene_item.setData(Qt.UserRole, entry)
            self.table.setItem(row, COL_SCENE, scene_item)

            character_item = QTableWidgetItem(entry.speaker or "")
            character_item.setFlags(character_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, COL_CHARACTER, character_item)

            original_item = QTableWidgetItem(entry.original)
            original_item.setFlags(original_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, COL_ORIGINAL, original_item)

            translation_item = QTableWidgetItem(entry.translation)
            _mark_edited(translation_item, entry.is_edited,
                         text_wrap.status(entry.translation, entry.speaker is not None))
            self.table.setItem(row, COL_TRANSLATION, translation_item)
        self._populating = False

    def _refresh_image_scene_list(self):
        """Repopulates the Images tab's scene list to only the scenes that
        have at least one of the checked categories present (checking
        nothing shows every scene). Uses Project.scene_image_categories(),
        a cheap {scene: {category, ...}} index built once per loaded
        project (no pixel decoding)."""
        if not self.project:
            return
        checked = {label for label, box in self.image_category_checks.items() if box.isChecked()}
        index = self.project.scene_image_categories()

        current = self.image_scene_list.currentItem()
        previous_name = current.text() if current else None

        self.image_scene_list.blockSignals(True)
        self.image_scene_list.clear()
        for name in self.project.scene_names():
            cats = index.get(name, set())
            if not checked or cats & checked:
                self.image_scene_list.addItem(name)
        self.image_scene_list.blockSignals(False)

        # keep the same scene selected across a filter change, when it's
        # still in the filtered list
        matches = self.image_scene_list.findItems(previous_name, Qt.MatchExactly) if previous_name else []
        if matches:
            self.image_scene_list.setCurrentItem(matches[0])
        elif self.image_scene_list.count():
            self.image_scene_list.setCurrentRow(0)
        else:
            self.image_tree.clear()
            self.image_preview_label.clear()
            self.image_info_label.setText("No scenes match the selected filters.")

    def _on_image_filter_changed(self, _state):
        self._refresh_image_scene_list()

    def _on_image_scene_selected(self, scene_name: str):
        if not scene_name or not self.project:
            return
        self._fill_image_tree(scene_name)

    def _fill_image_tree(self, scene_name: str):
        """Populates the Images tab's tree with this scene's image
        categories/labels (cheap - just gzip decompression and GIM-header
        magic checks, no pixel decoding yet, see core/scene_images.py)."""
        self.image_tree.clear()
        self.image_preview_label.clear()
        self.image_info_label.setText("Select a scene, then an image.")
        try:
            grouped = self.project.images_for_scene(scene_name)
        except Exception as exc:
            self.image_info_label.setText(f"Could not read images for this scene: {exc}")
            return

        if not grouped:
            self.image_info_label.setText("This scene has no image data.")
            return

        for category, images in grouped.items():
            edited_count = sum(1 for image in images if image.is_edited)
            header = f"{category} ({len(images)})" if not edited_count else f"{category} ({len(images)}, {edited_count} edited)"
            category_item = QTreeWidgetItem([header])
            self.image_tree.addTopLevelItem(category_item)
            for image in images:
                leaf = QTreeWidgetItem([image.label])
                leaf.setData(0, IMAGE_ROLE, image)
                if image.is_edited:
                    leaf.setBackground(0, EDITED_BACKGROUND)
                    leaf.setForeground(0, EDITED_FOREGROUND)
                category_item.addChild(leaf)
        self.image_tree.expandAll()

    def _on_image_selected(self, current: QTreeWidgetItem | None, _previous):
        if current is None:
            return
        image = current.data(0, IMAGE_ROLE)
        if image is None:
            return  # a category header was clicked, not a leaf

        if image.replacement_png_bytes is not None:
            # a pending import exists for this image - preview THAT instead
            # of the original still on the ISO, so the user can confirm what
            # will actually be written on the next compile.
            pixmap = QPixmap()
            if not pixmap.loadFromData(image.replacement_png_bytes, "PNG"):
                self.image_preview_label.clear()
                self.image_info_label.setText(
                    f"{image.category} / {image.label} - imported replacement is not a readable PNG"
                )
                return
            width, height = pixmap.width(), pixmap.height()
            status = f"{image.category} / {image.label} - {width}x{height} (showing IMPORTED replacement, not yet compiled)"
        else:
            try:
                width, height, rgba = scene_images.decode_to_rgba(image.gim_bytes)
            except Exception as exc:
                self.image_preview_label.clear()
                self.image_info_label.setText(f"{image.category} / {image.label} - failed to decode: {exc}")
                return

            # .copy() forces Qt to own its own buffer immediately - rgba is a
            # plain Python bytes object about to go out of scope, and QImage's
            # constructor doesn't keep a Python reference to it on its own.
            qimage = QImage(rgba, width, height, QImage.Format_RGBA8888).copy()
            pixmap = QPixmap.fromImage(qimage)
            status = f"{image.category} / {image.label} - {width}x{height}"

        max_side = 640
        if width > max_side or height > max_side:
            pixmap = pixmap.scaled(max_side, max_side, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_preview_label.setPixmap(pixmap)
        self.image_info_label.setText(status)

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._populating or item.column() != COL_TRANSLATION:
            return
        scene_item = self.table.item(item.row(), COL_SCENE)
        entry = scene_item.data(Qt.UserRole)
        entry.translation = item.text()
        _mark_edited(item, entry.is_edited,
                     text_wrap.status(entry.translation, entry.speaker is not None))
        self._update_status()

    def _update_status(self):
        if not self.project:
            self.status_label.setText("No ISO open.")
            return
        total = sum(len(v) for v in self.project.scenes.values())
        self.status_label.setText(
            f"{len(self.project.scene_names())} scenes | {total} lines | "
            f"{self.project.edited_count()} lines edited | "
            f"{self.project.edited_image_count()} image(s) edited"
        )
