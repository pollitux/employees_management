from typing import Optional, List

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel, QDialog,
    QFormLayout, QDialogButtonBox
)

from employees_management.domain.models import Municipality
from employees_management.application.municipality_service import MunicipalityService


class MunicipalityDialog(QDialog):
    """
    Dialog to create or edit a municipality.
    Only contains a 'name' field.
    """

    def __init__(self, parent=None, data=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Carrier")

        self.name_edit = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

        if data:
            self.name_edit.setText(data.get("name", ""))

    def get_data(self) -> dict:
        return {
            "name": self.name_edit.text().strip()
        }


class MunicipalityWindow(QMainWindow):
    """
    Window to manage municipalities.
    Full CRUD interface.
    """
    closed = pyqtSignal()

    def __init__(self, municipality_service: MunicipalityService):
        super().__init__()
        self._service = municipality_service

        self.setWindowTitle("Manage Municipalities")
        self.resize(400, 300)
        self._selected_id: Optional[int] = None

        self._municipalities_cache: List[Municipality] = []

        self._setup_ui()
        self._load_municipalities()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # ---- Search Bar ----
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search municipality by name...")
        self.search_edit.textChanged.connect(self._on_search_changed)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)

        # ---- Table ----
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Municipality Name"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self._on_row_selected)

        # ---- Buttons ----
        buttons_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")

        self.btn_add.clicked.connect(self._add_municipality)
        self.btn_edit.clicked.connect(self._edit_municipality)
        self.btn_delete.clicked.connect(self._delete_municipality)

        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_edit)
        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addStretch()

        # ---- Layout order ----
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)

    # Load Data
    def _load_municipalities(self):
        self._municipalities_cache = self._service.list_municipalities()
        self._apply_filter()
        self._selected_id = None

    def _fill_table(self, municipalities: List[Municipality]):
        self.table.setRowCount(0)

        for municipality in municipalities:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(municipality.id)))
            self.table.setItem(row, 1, QTableWidgetItem(municipality.name))

    # Filtering
    def _on_search_changed(self, text: str):
        self._apply_filter()

    def _apply_filter(self):
        query = self.search_edit.text().strip().lower()

        if not query:
            filtered = self._municipalities_cache
        else:
            filtered = [
                c for c in self._municipalities_cache
                if query in c.name.lower()
            ]

        self._fill_table(filtered)

    # Selection
    def _on_row_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            self._selected_id = None
            return
        row = rows[0].row()
        self._selected_id = int(self.table.item(row, 0).text())

    # CRUD operations
    def _add_municipality(self):
        dialog = MunicipalityDialog(self)

        if dialog.exec() == MunicipalityDialog.DialogCode.Accepted:
            data = dialog.get_data()

            try:
                self._service.create_municipality(data["name"])
                self._load_municipalities()
            except Exception as exc:
                self._show_error(str(exc))

    def _edit_municipality(self):
        if self._selected_id is None:
            self._show_info("Please select a municipality first.")
            return

        municipality = self._find_by_id(self._selected_id)
        if not municipality:
            self._show_error("Municipality not found.")
            return

        dialog = MunicipalityDialog(self, data={"name": municipality.name})

        if dialog.exec() == MunicipalityDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self._service.update_municipality(municipality, **data)
                self._load_municipalities()
            except Exception as exc:
                self._show_error(str(exc))

    def _delete_municipality(self):
        if self._selected_id is None:
            self._show_info("Please select a municipality first.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm delete",
            "This municipality might be linked to students.\nDelete anyway?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            municipality = self._find_by_id(self._selected_id)
            if municipality:
                try:
                    self._service.delete_municipality(municipality)
                    self._load_municipalities()
                except Exception as exc:
                    self._show_error(str(exc))

    # Helpers
    def _find_by_id(self, municipality_id: int) -> Optional[Municipality]:
        for c in self._municipalities_cache:
            if c.id == municipality_id:
                return c
        return None

    def _show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

    def _show_info(self, msg):
        QMessageBox.information(self, "Info", msg)

    def closeEvent(self, event):
        """
        Override of the Qt closeEvent() method.

        This method is inherited from QMainWindow and uses CamelCase because it
        is defined by the Qt framework (C++ naming convention). The method is
        automatically called by Qt when the window is closed.

        We override this method to emit the custom `closed` signal. The main
        window (MainWindow) listens to this signal to refresh filters and
        reload data whenever the child window (MunicipalityWindow) is closed.

        Parameters
        ----------
        event : QCloseEvent
            The close event generated by Qt when the user closes the window.

        Notes
        -----
        - We must use the exact method name `closeEvent`, not snake_case.
        - If this method were named `close_event`, Qt would not call it.
        """
        # Emit the custom signal used by MainWindow to refresh data
        self.closed.emit()
        # Call the base implementation (required to allow Qt to close the window normally)
        super().closeEvent(event)
