from datetime import datetime
from typing import Optional, List

from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QLabel, QComboBox
)

from PyQt6.QtWidgets import QToolBar, QMenu
from PyQt6.QtGui import QIcon, QAction
# set size for components
from PyQt6.QtCore import QSize

from employees_management.application.employee_import_service import EmployeeImportService
from employees_management.application.pandas_service import PandasService
from employees_management.domain.models import Employee
from employees_management.application.employee_service import EmployeeService
from employees_management.application.position_service import PositionService
from employees_management.application.municipality_service import MunicipalityService
from employees_management.gui.chart_window import ChartWindow
from employees_management.gui.chart_window_pie import PieChartWindow
from employees_management.gui.municipality_window import MunicipalityWindow
from employees_management.gui.position_window import PositionWindow

from employees_management.gui.window_employee import EmployeeDialog
from employees_management.gui.window_salary import SalaryWindow

from employees_management.translations.es import TEXT


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
            import_service: EmployeeImportService,
            pandas_service: PandasService,
    ) -> None:
        super().__init__()
        self._employee_service = employee_service
        self._position_service = position_service
        self._municipality_service = municipality_service
        self._import_service = import_service
        self._pandas_service = pandas_service

        self.setWindowTitle(TEXT["APP_TITLE"])

        # Current selection
        self._selected_id: Optional[int] = None
        self._employees_cache: List[Employee] = []

        self._setup_toolbar()
        self._setup_ui()
        self._load_employees()

    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel(TEXT["BTN_SEARCH"])
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Type NSS or name...")
        self.search_edit.textChanged.connect(self._apply_filter)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)

        # --- Filters by Position and Municipality ---
        filter_layout = QHBoxLayout()

        self.position_filter = QComboBox()
        self.position_filter.addItem(TEXT.get("FILTER_ALL_POSITIONS", "All Positions"), None)
        for position in self._position_service.list_positions():
            self.position_filter.addItem(position.name, position.id)
        self.position_filter.currentIndexChanged.connect(self._apply_filter)

        self.municipality_filter = QComboBox()
        self.municipality_filter.addItem(TEXT.get("FILTER_ALL_MUNICIPALITIES", "All Municipalities"), None)
        for municipality in self._municipality_service.list_municipalities():
            self.municipality_filter.addItem(municipality.name, municipality.id)
        self.municipality_filter.currentIndexChanged.connect(self._apply_filter)

        filter_layout.addWidget(QLabel(TEXT.get("FILTER_POSITION", "Filter by Position:")))
        filter_layout.addWidget(self.position_filter)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel(TEXT.get("FILTER_MUNICIPALITIES", "Filter by Municipalities:")))
        filter_layout.addWidget(self.municipality_filter)

        self.type_filter = QComboBox()
        self.type_filter.addItem(TEXT.get("FILTER_ALL_TYPES", "All Types"), None)
        self.type_filter.addItem("BASE", "BASE")
        self.type_filter.addItem("HONORARY", "HONORARY")
        self.type_filter.currentIndexChanged.connect(self._apply_filter)

        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel(TEXT.get("FILTER_TYPE", "Filter by Type:")))
        filter_layout.addWidget(self.type_filter)

        # Add filters to main layout
        main_layout.addLayout(filter_layout)

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
        self.btn_add = QPushButton(TEXT.get("BTN_ADD", "Add"))
        self.btn_edit = QPushButton(TEXT.get("BTN_EDIT", "Edit"))
        self.btn_delete = QPushButton(TEXT.get("BTN_DELETE", "Delete"))

        self.btn_positions = QPushButton(TEXT.get("BTN_POSITIONS", "Positions"))
        self.btn_municipalities = QPushButton(TEXT.get("BTN_MUNICIPALITIES", "Municipalities"))

        self.btn_add.clicked.connect(self._add_employee)
        self.btn_edit.clicked.connect(self._edit_employee)
        self.btn_delete.clicked.connect(self._delete_employee)
        self.btn_positions.clicked.connect(self._open_position_window)
        self.btn_municipalities.clicked.connect(self._open_municipality_window)

        self.btn_add.setIcon(QtGui.QIcon("icons/add.png"))
        self.btn_edit.setIcon(QtGui.QIcon("icons/update.png"))
        self.btn_delete.setIcon(QtGui.QIcon("icons/delete.png"))

        for btn in [
            self.btn_add, self.btn_edit, self.btn_delete, self.btn_positions,
            self.btn_municipalities
        ]:
            buttons_layout.addWidget(btn)

        # Layout stacking
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(buttons_layout)

    def _setup_toolbar(self) -> None:
        """Creates the top toolbar with menu actions."""

        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        # Set icon size (default might be too large on macOS)
        toolbar.setIconSize(QSize(20, 20))
        # options: 16x16, 20x20, 24x24, 32x32

        self.addToolBar(toolbar)
        self.addToolBar(toolbar)

        # Reports Menu
        reports_menu = QMenu("Reports", self)

        reports_by_position = QAction("Empleados por puesto", self)
        reports_by_position.triggered.connect(self._open_report_employees_by_position)

        reports_by_municipality = QAction("Empledos por municipio", self)
        reports_by_municipality.triggered.connect(self._open_report_employees_by_municipality)

        report_base_vs_honorary = QAction("Base vs Honorarios", self)
        report_base_vs_honorary.triggered.connect(self._open_report_base_vs_honorary)

        salary_report = QAction("Salary Summary", self)
        salary_report.triggered.connect(self._open_report_salary)

        # Add items to menu
        reports_menu.addAction(reports_by_position)
        reports_menu.addAction(reports_by_municipality)
        reports_menu.addAction(report_base_vs_honorary)
        reports_menu.addSeparator()
        reports_menu.addAction(salary_report)

        # Create toolbar button with menu
        reports_action = QAction(QIcon("icons/report.png"), "Reports", self)
        reports_action.setMenu(reports_menu)
        toolbar.addAction(reports_action)

        # Utils Menu
        utils_menu = QMenu("Utils", self)

        import_csv_action = QAction("Import CSV", self)
        import_csv_action.triggered.connect(self._import_csv)
        utils_menu.addAction(import_csv_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "About", "Employee Manager v1.0"))

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(
            lambda: QMessageBox.information(self, "Settings", "Settings window will be available soon."))

        utils_menu.addAction(about_action)
        utils_menu.addAction(settings_action)

        utils_action = QAction(QIcon("icons/tools.png"), "Utils", self)
        utils_action.setMenu(utils_menu)
        toolbar.addAction(utils_action)

        pandas_menu = QMenu("Analitica Pandas Filters", self)

        pandas_filter_age = QAction("Edad de empleados 25-35", self)
        pandas_filter_age.triggered.connect(self._open_filter_age)

        pandas_filter_position = QAction("Empleados por puesto (DF)", self)
        pandas_filter_position.triggered.connect(self._open_filter_position)

        age_range_report = QAction("Rango de edades (Pandas)", self)
        age_range_report.triggered.connect(self._open_report_age_ranges)

        pandas_menu.addAction(pandas_filter_age)
        pandas_menu.addAction(pandas_filter_position)
        pandas_menu.addAction(age_range_report)

        pandas_action = QAction(QIcon("icons/panda.png"), "Pandas Filters", self)
        pandas_action.setMenu(pandas_menu)
        toolbar.addAction(pandas_action)

    def _load_employees(self) -> None:
        self._employees_cache = self._employee_service.list_employees()
        self._apply_filter()
        self._selected_id = None

    def _fill_table(self, employees: List[Employee]) -> None:
        self.table.setRowCount(0)
        for employee in employees:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(employee.nss)))
            self.table.setItem(row, 1, QTableWidgetItem(employee.first_name))
            self.table.setItem(row, 2, QTableWidgetItem(employee.last_name_f))
            self.table.setItem(row, 3, QTableWidgetItem(employee.last_name_m))
            self.table.setItem(row, 4, QTableWidgetItem(employee.position_rel.name))
            self.table.setItem(row, 5, QTableWidgetItem(employee.birth_date.strftime('%Y-%m-%d')))
            self.table.setItem(row, 6, QTableWidgetItem(employee.municipality_rel.name))

    def _apply_filter(self) -> None:
        query = self.search_edit.text().strip().lower()
        selected_position_id = self.position_filter.currentData()
        selected_municipality_id = self.municipality_filter.currentData()
        selected_type = self.type_filter.currentData()  # NEW

        filtered = []

        for employee in self._employees_cache:
            # Text filter
            matches_text = (
                    query in str(employee.nss).lower()
                    or query in employee.first_name.lower()
                    or query in employee.last_name_f.lower()
                    or query in employee.last_name_m.lower()
                    or query in employee.position_rel.name.lower()
                    or query in employee.municipality_rel.name.lower()
            ) if query else True

            # Position filter
            matches_position = (
                employee.position_id == selected_position_id
                if selected_position_id is not None else True
            )

            # Municipality filter
            matches_municipality = (
                employee.municipality_id == selected_municipality_id
                if selected_municipality_id is not None else True
            )

            # Employee type filter (BASE/HONORARY)
            matches_type = (
                employee.employee_type.upper() == selected_type
                if selected_type is not None else True
            )

            # Add employee if all conditions match
            if matches_text and matches_position and matches_municipality and matches_type:
                filtered.append(employee)

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

    def _open_report_employees_by_position(self):
        data = {}
        for employee in self._employees_cache:
            if not employee.position_rel:
                continue
            name = employee.position_rel.name
            data[name] = data.get(name, 0) + 1

        if not data:
            self._show_info("No data available to display chart.")
            return

        self.chart_window = ChartWindow(
            data, self, **{
                "title": "Empleados por puesto",
                "ax_title": "Empleados por puesto",
                "ax_ylabel": "Numero de empleados",
                "ax_xlabel": "Puestos",
            })
        self.chart_window.show()

    def _open_report_employees_by_municipality(self):
        data = {}
        for employee in self._employees_cache:
            if not employee.municipality_rel:
                continue
            name = employee.municipality_rel.name
            data[name] = data.get(name, 0) + 1

        if not data:
            self._show_info("No data available to display chart.")
            return
        # set data to dialog
        self.chart_window = ChartWindow(
            data, self, **{
                "title": "Empleados por municipio",
                "ax_title": "Empleados por municipio",
                "ax_ylabel": "Numero de empleados",
                "ax_xlabel": "Municipio",
            })
        self.chart_window.show()

    def _open_report_base_vs_honorary(self):
        base = 0
        honorary = 0

        for employee in self._employees_cache:
            if employee.employee_type.upper() == "BASE":
                base += 1
            else:
                honorary += 1

        data = {
            "Base": base,
            "Honorarios": honorary
        }

        if base == 0 and honorary == 0:
            QMessageBox.information(self, "No data", "No employees registered.")
            return

        self.chart_window = PieChartWindow(
            data,
            self,
            title="Porcentaje de empleados BASE vs HONORARIOS"
        )
        self.chart_window.show()

    def _open_report_salary(self):
        self.salary_window = SalaryWindow(self._employee_service)
        self.salary_window.show()

    def _import_csv(self):
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        try:
            result = self._import_service.import_csv(file_path)

            summary = (
                f"Imported: {result['inserted']}\n"
                f"Failed: {result['failed']}"
            )

            QMessageBox.information(self, "CSV Import Summary", summary)
            self._load_employees()

        except Exception as exc:
            QMessageBox.critical(self, "Import error", str(exc))

    def _open_filter_age(self):
        df = self._pandas_service.employees_to_dataframe(self._employees_cache)

        filtered = df[(df["age"] >= 25) & (df["age"] <= 35)]

        if filtered.empty:
            QMessageBox.information(self, "No results", "No employees in this age range.")
            return

        from employees_management.gui.pandas_table_window import PandasTableWindow
        PandasTableWindow(filtered, "Emepleados entre 25–35 años", self).show()

    def _open_filter_position(self):
        from employees_management.gui.pandas_table_window import PandasTableWindow

        df = self._pandas_service.employees_to_dataframe(self._employees_cache)

        grouped = df.groupby("position").size().reset_index(name="count")

        window = PandasTableWindow(grouped, "Empleados por puesto (Pandas)", self)
        window.show()

    def _open_report_age_ranges(self):
        """
        Build age ranges using Pandas and show a bar chart of how many employees fall in each range.
        """
        import pandas as pd
        try:
            df = self._pandas_service.employees_to_dataframe(self._employees_cache)
        except Exception as exc:
            QMessageBox.critical(self, "Pandas error", f"Could not build DataFrame: {exc}")
            return

        if df.empty or "age" not in df.columns:
            QMessageBox.information(self, "No data", "No employee age data available.")
            return

        ages = df["age"].dropna()

        if ages.empty:
            QMessageBox.information(self, "No data", "No valid ages to evaluate.")
            return

        # Define bins for age ranges
        bins = [18, 21, 28, 34, 40, 120]
        labels = [
            "18–21",
            "22–28",
            "29–34",
            "35–40",
            "41+"
        ]

        # Convert numeric ages into categorical ranges using Pandas `cut`.
        # - `ages`: a Series containing the numeric ages of employees.
        # - `bins`: the exact numeric boundaries that define the ranges.
        # - `labels`: the text labels assigned to each range.
        # - `right=True`: means each interval is right-inclusive (e.g., 18–21 includes 21).
        # The result is a new column "age_range" that categorizes every employee
        # into one of the defined age groups.
        df["age_range"] = pd.cut(ages, bins=bins, labels=labels, right=True)

        # Count employees per age range
        range_counts = df["age_range"].value_counts().sort_index()

        data = range_counts.to_dict()

        self.chart_window = ChartWindow(
            data,
            self,
            **{
                "title": "Empleados por rango de edad",
                "ax_title": "Empleados por rango de edad",
                "ax_ylabel": "Numero de empleados",
                "ax_xlabel": "Rango de edades",
            }
        )
        self.chart_window.show()

    def _show_info(self, message: str) -> None:
        QMessageBox.information(self, "Info", message)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Error", message)
