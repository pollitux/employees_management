"""
Dialog to create or edit an employee.
Author: Raul Granados
Company: Swipall
"""
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QDialogButtonBox, QComboBox, QCalendarWidget
)


class EmployeeDialog(QDialog):
    """
    Dialog to create or edit an employee.
    """

    def __init__(self, parent=None, positions=None, municipalities=None, data=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Employee")

        self.positions = positions or []
        self.municipalities = municipalities or []
        self.data = data or {}

        self.nss_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.last_name_f_edit = QLineEdit()
        self.last_name_m_edit = QLineEdit()
        self.birth_date_edit = QCalendarWidget()
        self.origin_edit = QLineEdit()

        self.position_combo = QComboBox()
        for pos in self.positions:
            self.position_combo.addItem(pos.name, pos.id)

        self.municipality_combo = QComboBox()
        for m in self.municipalities:
            self.municipality_combo.addItem(m.name, m.id)

        self.employee_type_combo = QComboBox()
        self.employee_type_combo.addItems(["BASE", "HONORARY"])

        self.hourly_rate_edit = QLineEdit()
        self.hours_worked_edit = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("NSS:", self.nss_edit)
        form_layout.addRow("First name:", self.first_name_edit)
        form_layout.addRow("Last name (Father):", self.last_name_f_edit)
        form_layout.addRow("Last name (Mother):", self.last_name_m_edit)
        form_layout.addRow("Birth date:", self.birth_date_edit)
        form_layout.addRow("Municipality:", self.municipality_combo)
        form_layout.addRow("Position:", self.position_combo)
        form_layout.addRow("Employee type:", self.employee_type_combo)
        form_layout.addRow("Hourly rate:", self.hourly_rate_edit)
        form_layout.addRow("Hours worked:", self.hours_worked_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

        if self.data:
            self._load_data()

    def _load_data(self) -> None:
        self.nss_edit.setText(str(self.data.get("nss", "")))
        self.first_name_edit.setText(self.data.get("first_name", ""))
        self.last_name_f_edit.setText(self.data.get("last_name_f", ""))
        self.last_name_m_edit.setText(self.data.get("last_name_m", ""))

        birth_date_str = self.data.get("birth_date", "")
        if birth_date_str:
            qdate = QDate.fromString(birth_date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.birth_date_edit.setSelectedDate(qdate)

        # Combo positions
        pos_id = self.data.get("position_id")
        if pos_id:
            index = self.position_combo.findData(pos_id)
            if index >= 0:
                self.position_combo.setCurrentIndex(index)

        mun_id = self.data.get("municipality_id")
        if mun_id:
            index = self.municipality_combo.findData(mun_id)
            if index >= 0:
                self.municipality_combo.setCurrentIndex(index)

        self.employee_type_combo.setCurrentText(self.data.get("employee_type", "BASE"))
        self.hourly_rate_edit.setText(str(self.data.get("hourly_rate", "")))
        self.hours_worked_edit.setText(str(self.data.get("hours_worked", "")))

    def get_data(self) -> dict:
        """
        Return dialog data as dictionary.
        """
        hourly_rate_text = self.hourly_rate_edit.text().strip()
        hours_worked_text = self.hours_worked_edit.text().strip()

        return {
            "nss": int(self.nss_edit.text().strip()),
            "first_name": self.first_name_edit.text().strip(),
            "last_name_f": self.last_name_f_edit.text().strip(),
            "last_name_m": self.last_name_m_edit.text().strip(),
            "position_id": self.position_combo.currentData(),
            "birth_date": self.birth_date_edit.selectedDate().toString("yyyy-MM-dd"),
            "municipality_id": self.municipality_combo.currentData(),
            "employee_type": self.employee_type_combo.currentText().strip(),
            "hourly_rate": float(hourly_rate_text) if hourly_rate_text else None,
            "hours_worked": int(hours_worked_text) if hours_worked_text else None,
        }
