"""
Author: Raul Granados
Company: Swipall
Description: About dialog for the Employees Management System.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt


class AboutDialog(QDialog):
    """
    Simple informational dialog describing the project, author, and purpose.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("About")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()

        # Main Title
        title = QLabel("<h2>Employees Management System</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Project Description
        description = QLabel(
            """
            <b>Final Project – Technologies of Programming</b><br><br>

            This application was developed as an educational project to demonstrate:<br>
            • SOLID principles<br>
            • Clean Architecture<br>
            • PyQt6 desktop interfaces<br>
            • SQLAlchemy ORM<br>
            • CSV import/export<br>
            • Pandas analytics and reporting<br>
            • Data visualization using Matplotlib<br><br>

            The system includes modules for managing employees, positions, and municipalities,
            as well as salary calculations, advanced filtering, and analytic tools.
            """
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        # Author Info
        author_label = QLabel(
            """
            <b>Author:</b> Raul Granados<br>
            <b>Company:</b> Swipall<br>
            <b>Email:</b> raul@swipall.io<br><br>
            """
        )
        author_label.setWordWrap(True)
        layout.addWidget(author_label)

        # Repo URL (clickable)
        repo_label = QLabel(
            """
            <b>Repository:</b><br>
            <a href="https://github.com/pollitux/employees_management">GitHub Project Link</a><br><br>

            This repository contains the full source code, database scripts,
            and documentation for the academic delivery.
            """
        )
        repo_label.setOpenExternalLinks(True)
        repo_label.setWordWrap(True)
        layout.addWidget(repo_label)

        # Close button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)