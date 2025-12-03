from datetime import datetime
from typing import Optional, List
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QLabel
)

from employees_management.domain.models import Employee
from employees_management.application.employee_service import EmployeeService
from employees_management.application.position_service import PositionService
from employees_management.application.municipality_service import MunicipalityService
from employees_management.gui.municipality_window import MunicipalityWindow
from employees_management.gui.position_window import PositionWindow

from employees_management.gui.window_employee import EmployeeDialog


class MainWindow(QMainWindow):
    """
    Main window for the Employee Management UI.
    Handles UI rendering and interactions.
    Business logic is in EmployeeService.
    """

    def __init__(
            self,
            employee_service: EmployeeService,
            position_service: PositionService,
            municipality_service: MunicipalityService,
    ) -> None:
        super().__init__()
        self._employee_service = employee_service
        self._position_service = position_service
        self._municipality_service = municipality_service

        self.setWindowTitle("Employee Manager")

        # Current selection
        self._selected_id: Optional[int] = None
        self._employees_cache: List[Employee] = []

        self._setup_ui()
        self._load_employees()

    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Type NSS or name...")
        self.search_edit.textChanged.connect(self._apply_filter)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)

        # Table
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "NSS", "First name", "Last name F", "Last name M",
            "Position", "Birth date", "Municipality"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(self._on_row_selected)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")

        self.btn_positions = QPushButton("Manage Positions")
        self.btn_municipalities = QPushButton("Manage Municipalities")

        self.btn_add.clicked.connect(self._add_employee)
        self.btn_edit.clicked.connect(self._edit_employee)
        self.btn_delete.clicked.connect(self._delete_employee)
        self.btn_positions.clicked.connect(self._open_position_window)
        self.btn_municipalities.clicked.connect(self._open_municipality_window)

        for btn in [
            self.btn_add, self.btn_edit, self.btn_delete, self.btn_positions,
            self.btn_municipalities
        ]:
            buttons_layout.addWidget(btn)

        # Layout stacking
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(buttons_layout)

    def _load_employees(self) -> None:
        self._employees_cache = self._employee_service.list_employees()
        self._apply_filter()
        self._selected_id = None

    def _fill_table(self, employees: List[Employee]) -> None:
        self.table.setRowCount(0)
        for emp in employees:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(emp.nss)))
            self.table.setItem(row, 1, QTableWidgetItem(emp.first_name))
            self.table.setItem(row, 2, QTableWidgetItem(emp.last_name_f))
            self.table.setItem(row, 3, QTableWidgetItem(emp.last_name_m))
            self.table.setItem(row, 4, QTableWidgetItem(emp.position_rel.name))
            self.table.setItem(row, 5, QTableWidgetItem(emp.birth_date.strftime('%Y-%m-%d')))
            self.table.setItem(row, 6, QTableWidgetItem(emp.municipality_rel.name))

    def _apply_filter(self) -> None:
        query = self.search_edit.text().strip().lower()
        if not query:
            filtered = self._employees_cache
        else:
            filtered = [
                emp for emp in self._employees_cache
                if query in str(emp.nss).lower()
                   or query in emp.first_name.lower()
                   or query in emp.last_name_f.lower()
                   or query in emp.last_name_m.lower()
                   or query in emp.position_rel.name.lower()
                   or query in emp.municipality_rel.name.lower()
            ]
        self._fill_table(filtered)

    def _on_row_selected(self) -> None:
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self._selected_id = self.table.item(row, 0).text()
        else:
            self._selected_id = None

    # crud operations
    def _add_employee(self) -> None:
        positions = self._position_service.list_positions()
        municipalities = self._municipality_service.list_municipalities()

        dialog = EmployeeDialog(self, positions=positions, municipalities=municipalities)

        if dialog.exec() == EmployeeDialog.DialogCode.Accepted:
            data = dialog.get_data()
            # create employee
            try:
                self._employee_service.add_employee(
                    nss=data["nss"],
                    first_name=data["first_name"],
                    last_name_f=data["last_name_f"],
                    last_name_m=data["last_name_m"],
                    position_id=data["position_id"],
                    birth_date=datetime.strptime(data["birth_date"], "%Y-%m-%d").date(),
                    municipality_id=data["municipality_id"],
                    employee_type=data["employee_type"],
                    hourly_rate=data.get("hourly_rate"),
                    hours_worked=data.get("hours_worked"),
                )
                self._load_employees()
            except Exception as exc:
                self._show_error(str(exc))

    def _edit_employee(self) -> None:
        """Open dialog to edit selected employee."""
        if self._selected_id is None:
            self._show_info("Please select a employee first.")
            return

        employee = self._employee_service.find_employee(self._selected_id)
        if not employee:
            self._show_error("Employee not found.")
            return

        positions = self._position_service.list_positions()
        municipalities = self._municipality_service.list_municipalities()

        dialog = EmployeeDialog(self, positions=positions, municipalities=municipalities, data={
            "nss": employee.nss,
            "first_name": employee.first_name,
            "last_name_m": employee.last_name_m,
            "last_name_f": employee.last_name_f,
            "position_id": employee.position_id,
            "municipality_id": employee.municipality_id,
            "employee_type": employee.employee_type,
            "hourly_rate": str(employee.hourly_rate),
            "hours_worked": str(employee.hours_worked),
            "birth_date": employee.birth_date.strftime("%Y-%m-%d"),
        })

        if dialog.exec() == EmployeeDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                # update employee
                self._employee_service.update_employee(employee, **data)
                self._load_employees()
            except Exception as exc:
                self._show_error(str(exc))

    def _delete_employee(self) -> None:
        if self._selected_id is None:
            self._show_info("Please select an employee first.")
            return
        confirm = QMessageBox.question(
            self,
            "Confirm delete",
            f"Are you sure you want to delete employee with NSS {self._selected_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self._employee_service.delete_employee(self._selected_id)
            self._load_employees()

    def _open_position_window(self):
        self.position_window = PositionWindow(self._position_service)
        self.position_window.show()

    def _open_municipality_window(self):
        self.municipality_window = MunicipalityWindow(self._municipality_service)
        self.municipality_window.show()

    def _show_info(self, message: str) -> None:
        QMessageBox.information(self, "Info", message)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Error", message)
