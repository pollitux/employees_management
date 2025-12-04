from typing import Optional, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel, QDialog,
    QFormLayout, QDialogButtonBox
)

from employees_management.domain.models import Position
from employees_management.application.position_service import PositionService


class PositionDialog(QDialog):
    """
    Dialog to create or edit a Position.
    Only contains a 'name' field.
    """

    def __init__(self, parent=None, data=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Position")

        self.name_edit = QLineEdit()
        self.base_salary_edit = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Base salary:", self.base_salary_edit)

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
            self.base_salary_edit.setText(data.get("base_salary", ""))

    def get_data(self) -> dict:
        """
        Get data
        :return:
        """
        return {
            "name": self.name_edit.text().strip(),
            "base_salary": self.base_salary_edit.text().strip()
        }


class PositionWindow(QMainWindow):
    """
    Window to manage Position.
    Full CRUD interface.
    """

    def __init__(self, carrier_service: PositionService):
        super().__init__()
        self._service = carrier_service

        self.setWindowTitle("Manage Position")
        self.resize(400, 300)
        self._selected_id: Optional[int] = None

        self._positions_cache: List[Position] = []

        self._setup_ui()
        self._load_positions()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        central.setLayout(layout)

        # ---- Search Bar ----
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search position by name...")
        self.search_edit.textChanged.connect(self._on_search_changed)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)

        # ---- Table ----
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Salario base"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self._on_row_selected)

        # ---- Buttons ----
        buttons_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")

        self.btn_add.clicked.connect(self._add_position)
        self.btn_edit.clicked.connect(self._edit_position)
        self.btn_delete.clicked.connect(self._delete_position)

        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_edit)
        # buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addStretch()

        # ---- Layout order ----
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)

    # Load Data
    def _load_positions(self):
        self._positions_cache = self._service.list_positions()
        self._apply_filter()
        self._selected_id = None

    def _fill_table(self, carriers: List[Position]):
        self.table.setRowCount(0)

        for position in carriers:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(position.id)))
            self.table.setItem(row, 1, QTableWidgetItem(position.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(position.base_salary)))

    # Filtering
    def _on_search_changed(self, text: str):
        self._apply_filter()

    def _apply_filter(self):
        query = self.search_edit.text().strip().lower()

        if not query:
            filtered = self._positions_cache
        else:
            filtered = [
                c for c in self._positions_cache
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
    def _add_position(self):
        dialog = PositionDialog(self)

        if dialog.exec() == PositionDialog.DialogCode.Accepted:
            data = dialog.get_data()

            try:
                self._service.create_position(data["name"], data['base_salary'])
                self._load_positions()
            except Exception as exc:
                self._show_error(str(exc))

    def _edit_position(self):
        if self._selected_id is None:
            self._show_info("Please select a position first.")
            return

        position = self._find_by_id(self._selected_id)
        if not position:
            self._show_error("Position not found.")
            return

        dialog = PositionDialog(self, data={"name": position.name, "base_salary": str(position.base_salary)})

        if dialog.exec() == PositionDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                self._service.update_position(position, **data)
                self._load_positions()
            except Exception as exc:
                self._show_error(str(exc))

    def _delete_position(self):
        if self._selected_id is None:
            self._show_info("Please select a position first.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm delete",
            "This position might be linked to employees.\nDelete anyway?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            position = self._find_by_id(self._selected_id)
            if position:
                try:
                    session = self._service._repository._session
                    session.delete(position)
                    session.commit()
                    self._load_positions()
                except Exception as exc:
                    self._show_error(str(exc))

    # Helpers
    def _find_by_id(self, carrier_id: int) -> Optional[Position]:
        for c in self._positions_cache:
            if c.id == carrier_id:
                return c
        return None

    def _show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

    def _show_info(self, msg):
        QMessageBox.information(self, "Info", msg)
