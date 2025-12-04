"""
Author: Raul Granados
Company: Swipall
Description: Salary calculator window for employees (DB + SQLAlchemy version).
"""

from __future__ import annotations
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QLabel, QFormLayout, QLineEdit, QDialogButtonBox

from employees_management.application.employee_service import EmployeeService
from employees_management.domain.models import Employee


class SalaryWindow(QtWidgets.QDialog):
    """
    Dialog to calculate salary for an employee.
    """

    def __init__(
            self,
            employee_service: EmployeeService,
            parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._employee_service = employee_service

        self.setWindowTitle("Salary Calculator")
        self._build_ui()

    # UI SETUP
    def _build_ui(self) -> None:
        layout = QFormLayout(self)

        # NSS input
        self.nss_input = QLineEdit()
        self.nss_input.textChanged.connect(self._on_search_employee)
        layout.addRow("NSS:", self.nss_input)

        # Employee readonly info
        self.employee_name_label = QLabel("-")
        layout.addRow("Employee:", self.employee_name_label)

        self.employee_type_label = QLabel("-")
        layout.addRow("Type:", self.employee_type_label)

        self.employee_rate_label = QLabel("-")
        layout.addRow("Hourly rate:", self.employee_rate_label)

        # BASE input
        self.years_input = QLineEdit()
        self.years_input.setPlaceholderText("Only for BASE employees")
        layout.addRow("Years of service:", self.years_input)

        # HONORARY input
        self.extra_hours_input = QLineEdit()
        self.extra_hours_input.setPlaceholderText("Only for HONORARY employees")
        layout.addRow("Extra hours:", self.extra_hours_input)

        # Output label
        self.result_label = QLabel("")
        layout.addRow("Calculated salary:", self.result_label)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_calculate)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

        # internal attribute
        self._current_employee: Employee | None = None

    # QUERY EMPLOYEE DATA WHEN NSS CHANGES
    def _on_search_employee(self) -> None:
        text = self.nss_input.text().strip()

        if not text.isdigit():
            self._clear_employee_info()
            return

        nss = int(text)
        employee = self._employee_service.find_employee(nss)

        if not employee:
            self._clear_employee_info()
            return

        self._current_employee = employee

        full_name = f"{employee.first_name} {employee.last_name_f} {employee.last_name_m}"
        self.employee_name_label.setText(full_name)
        self.employee_type_label.setText(employee.employee_type)
        self.employee_rate_label.setText(f"${employee.hourly_rate:.2f}")

        # Enable/disable fields based on employee type
        if employee.employee_type == "BASE":
            self.years_input.setEnabled(True)
            self.extra_hours_input.setEnabled(False)
            self.extra_hours_input.clear()

        elif employee.employee_type == "HONORARY":
            self.years_input.setEnabled(False)
            self.years_input.clear()
            self.extra_hours_input.setEnabled(True)

    def _clear_employee_info(self):
        self._current_employee = None
        self.employee_name_label.setText("-")
        self.employee_type_label.setText("-")
        self.employee_rate_label.setText("-")

    # SALARY CALCULATION
    def _on_calculate(self) -> None:
        if not self._current_employee:
            QMessageBox.warning(self, "Error", "Employee not found.")
            return

        employee = self._current_employee

        # BASE employees
        if employee.employee_type == "BASE":
            years_text = self.years_input.text().strip()
            if not years_text:
                QMessageBox.warning(self, "Validation error", "Years of service is required.")
                return

            try:
                years = int(years_text)
            except ValueError:
                QMessageBox.warning(self, "Validation error", "Years must be an integer.")
                return

            base_salary = employee.hourly_rate * 40
            final_salary = base_salary * (1 + years * 0.01)

        # HONORARY employees
        elif employee.employee_type == "HONORARY":
            extra_text = self.extra_hours_input.text().strip()
            extra_hours = int(extra_text) if extra_text else 0

            base_hours = employee.hours_worked
            base_salary = employee.hourly_rate * base_hours

            final_salary = base_salary * (1 + extra_hours * 0.002)

        else:
            QMessageBox.warning(self, "Error", "Unknown employee type.")
            return

        self.result_label.setText(f"${final_salary:.2f}")
