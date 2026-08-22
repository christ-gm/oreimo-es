from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QListWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QFileDialog, QMessageBox, QApplication, QAbstractItemView,
)

EDITED_BACKGROUND = QColor(255, 244, 140)
EDITED_FOREGROUND = QColor(20, 20, 20)


def _mark_edited(item: QTableWidgetItem, edited: bool):
    """Highlights an edited translation cell with a readable yellow (dark
    text on a light yellow background, set explicitly so it stays legible
    regardless of the OS light/dark theme - the previous version only set
    a yellow background and inherited the theme's text color, which was
    unreadable in dark mode). Clears back to the theme default (rather
    than hardcoding white) when not edited."""
    if edited:
        item.setBackground(EDITED_BACKGROUND)
        item.setForeground(EDITED_FOREGROUND)
    else:
        item.setData(Qt.BackgroundRole, None)
        item.setData(Qt.ForegroundRole, None)

from ..core import Project

COL_SCENE = 0
COL_CHARACTER = 1
COL_ORIGINAL = 2
COL_TRANSLATION = 3


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
        file_menu = self.menuBar().addMenu("&Archivo")

        act_open = file_menu.addAction("&Abrir ISO...")
        act_open.triggered.connect(self.open_iso)

        file_menu.addSeparator()

        act_export_all = file_menu.addAction("Exportar &todas las escenas (un archivo por escena)...")
        act_export_all.triggered.connect(self.export_all_scenes)

        act_export_scene = file_menu.addAction("Exportar escena &seleccionada...")
        act_export_scene.triggered.connect(self.export_selected_scene)

        act_export_single = file_menu.addAction("Exportar todo en &un solo archivo...")
        act_export_single.triggered.connect(self.export_table)

        file_menu.addSeparator()

        act_import = file_menu.addAction("&Importar archivo(s)...")
        act_import.triggered.connect(self.import_tables)

        file_menu.addSeparator()

        act_compile = file_menu.addAction("&Compilar ISO...")
        act_compile.triggered.connect(self.compile_iso)

    def _build_central_widget(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Buscar:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar en todos los dialogos (original o traduccion)...")
        self.search_box.textChanged.connect(self._on_search_changed)
        search_row.addWidget(self.search_box)
        root.addLayout(search_row)

        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter, 1)

        self.scene_list = QListWidget()
        self.scene_list.currentTextChanged.connect(self._on_scene_selected)
        splitter.addWidget(self.scene_list)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Escena", "Personaje", "Original", "Traduccion"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(COL_SCENE, 120)
        self.table.setColumnWidth(COL_CHARACTER, 100)
        self.table.setColumnWidth(COL_ORIGINAL, 380)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.itemChanged.connect(self._on_item_changed)
        splitter.addWidget(self.table)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.status_label = QLabel()
        self.statusBar().addWidget(self.status_label)

    # ---- actions -----------------------------------------------------

    def open_iso(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir ISO", "", "Imagenes ISO (*.iso)")
        if not path:
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            project = Project()
            project.load(path)
        except Exception as exc:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Error al abrir el ISO", str(exc))
            return
        QApplication.restoreOverrideCursor()

        self.project = project
        self.setWindowTitle(f"Oreimo Translator - {Path(path).name}")
        self.scene_list.clear()
        self.scene_list.addItems(project.scene_names())
        self.search_box.clear()
        self.table.setRowCount(0)
        self._update_status()

    def export_table(self):
        """Exports every scene into a single combined file."""
        if not self._require_project():
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar todo en un archivo", "traduccion.csv",
            "CSV (*.csv);;TSV (*.tsv)"
        )
        if not path:
            return
        delimiter = "\t" if path.lower().endswith(".tsv") else ","
        try:
            self.project.export_table(path, delimiter=delimiter)
        except Exception as exc:
            QMessageBox.critical(self, "Error al exportar", str(exc))
            return
        QMessageBox.information(self, "Exportado", f"Tabla exportada a:\n{path}")

    def export_selected_scene(self):
        if not self._require_project():
            return
        current = self.scene_list.currentItem()
        if not current:
            QMessageBox.information(self, "Sin escena seleccionada", "Selecciona una escena en la lista primero.")
            return
        scene_name = current.text()
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar escena", f"{scene_name}.csv",
            "CSV (*.csv);;TSV (*.tsv)"
        )
        if not path:
            return
        delimiter = "\t" if path.lower().endswith(".tsv") else ","
        try:
            self.project.export_scene(scene_name, path, delimiter=delimiter)
        except Exception as exc:
            QMessageBox.critical(self, "Error al exportar", str(exc))
            return
        QMessageBox.information(self, "Exportado", f"Escena {scene_name!r} exportada a:\n{path}")

    def export_all_scenes(self):
        """Exports every scene to its own file (named after the scene) in
        a chosen folder - so files can be sent/edited/re-imported
        individually or as any group later."""
        if not self._require_project():
            return
        directory = QFileDialog.getExistingDirectory(self, "Elegir carpeta de destino")
        if not directory:
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            written = self.project.export_all_per_scene(directory)
        except Exception as exc:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Error al exportar", str(exc))
            return
        QApplication.restoreOverrideCursor()

        QMessageBox.information(
            self, "Exportado",
            f"{len(written)} archivos (uno por escena) escritos en:\n{directory}"
        )

    def import_tables(self):
        """Imports one or more previously-exported files at once - each
        file's rows are matched back to their scene by the 'scene' column,
        so any combination of files (one scene, several, or all of them)
        can be selected together and applied in one go."""
        if not self._require_project():
            return
        paths, _ = QFileDialog.getOpenFileNames(self, "Importar archivo(s)", "", "CSV/TSV (*.csv *.tsv)")
        if not paths:
            return

        try:
            results = self.project.import_tables(paths)
        except Exception as exc:
            QMessageBox.critical(self, "Error al importar", str(exc))
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
                preview += f"\n... y {len(all_warnings) - 20} avisos mas"
            QMessageBox.warning(self, "Importado con avisos", preview)
        else:
            QMessageBox.information(
                self, "Importado",
                f"{len(paths)} archivo(s) importados, todas las filas se aplicaron correctamente."
            )

    def compile_iso(self):
        if not self._require_project():
            return
        if self.project.edited_count() == 0:
            QMessageBox.information(self, "Nada que compilar", "No hay lineas editadas todavia.")
            return

        default_name = Path(self.project.iso_path).stem + "_ES.iso"
        path, _ = QFileDialog.getSaveFileName(self, "Compilar ISO", default_name, "Imagenes ISO (*.iso)")
        if not path:
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            report = self.project.compile(path)
        except Exception as exc:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Error al compilar", str(exc))
            return
        QApplication.restoreOverrideCursor()

        QMessageBox.information(
            self, "ISO compilado",
            f"Listo: {path}\n\n"
            f"Escenas modificadas: {len(report['scenes_changed'])}\n"
            f"Lineas cambiadas: {report['lines_changed']}"
        )

    # ---- view updates -----------------------------------------------------

    def _require_project(self) -> bool:
        if self.project is None:
            QMessageBox.information(self, "Sin ISO", "Primero abre un ISO (Archivo > Abrir ISO...).")
            return False
        return True

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
            _mark_edited(translation_item, entry.is_edited)
            self.table.setItem(row, COL_TRANSLATION, translation_item)
        self._populating = False

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._populating or item.column() != COL_TRANSLATION:
            return
        scene_item = self.table.item(item.row(), COL_SCENE)
        entry = scene_item.data(Qt.UserRole)
        entry.translation = item.text()
        _mark_edited(item, entry.is_edited)
        self._update_status()

    def _update_status(self):
        if not self.project:
            self.status_label.setText("Sin ISO abierto.")
            return
        total = sum(len(v) for v in self.project.scenes.values())
        self.status_label.setText(
            f"{len(self.project.scene_names())} escenas | {total} lineas | "
            f"{self.project.edited_count()} editadas"
        )
