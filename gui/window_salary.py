"""
Author: Raul Granados
Company: Swipall
Description: UI employee salary window.
"""

from __future__ import annotations

from PyQt6 import QtWidgets

from employees_management.translations.es import TEXT

from employees_management.models.employee_db import EmployeeDB
from employees_management.models.base_employee import BaseEmployee
from employees_management.models.honorary_employee import HonoraryEmployee


class SalaryWindow(QtWidgets.QDialog):
    """Dialog to calculate salary for an employee."""

    def __init__(
            self,
            employee_db: EmployeeDB,
            parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.employee_db = employee_db

        self.setWindowTitle(TEXT["SALARY_TITLE"])

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QtWidgets.QFormLayout(self)

        self.nss_input = QtWidgets.QLineEdit()
        layout.addRow("NSS:", self.nss_input)

        self.years_input = QtWidgets.QLineEdit()
        self.years_input.setPlaceholderText("Only for BASE employees")
        layout.addRow("Years of service:", self.years_input)

        self.extra_hours_input = QtWidgets.QLineEdit()
        self.extra_hours_input.setPlaceholderText("Only for HONORARY employees")
        layout.addRow("Extra hours:", self.extra_hours_input)

        self.result_label = QtWidgets.QLabel("")
        layout.addRow(TEXT["BTN_SALARY"], self.result_label)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_calculate)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def _on_calculate(self) -> None:
        try:
            nss = int(self.nss_input.text().strip())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Validation error", "NSS must be an integer")
            return

        employee = self.employee_db.find_employee(nss)
        if employee is None:
            QtWidgets.QMessageBox.information(self, "Not found", "Employee not found")
            return

        if isinstance(employee, BaseEmployee):
            try:
                years = int(self.years_input.text().strip())
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    self, "Validation error", "Years of service must be an integer"
                )
                return
            salary = employee.calculate_salary(years_of_service=years)
        elif isinstance(employee, HonoraryEmployee):
            extra_hours_text = self.extra_hours_input.text().strip()
            extra_hours = int(extra_hours_text) if extra_hours_text else 0
            salary = employee.calculate_salary(extra_hours=extra_hours)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                "Employee type does not support salary calculation",
            )
            return

        self.result_label.setText(f"{salary:.2f}")
