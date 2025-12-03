import sys
from PyQt6.QtWidgets import QApplication

from employees_management.application.municipality_service import MunicipalityService
from employees_management.application.position_service import PositionService
from employees_management.infrastructure.db import Base, engine, SessionLocal
from employees_management.domain.models import Employee

from application.employee_service import EmployeeService
from gui.main_window import MainWindow


def init_db() -> None:
    """
    Create tables if they do not exist.
    """
    print(">>> Creating tables if not exist...")
    Base.metadata.create_all(bind=engine)


def main() -> None:
    """

    :return:
    """
    init_db()

    app = QApplication(sys.argv)

    # Create one session for the application
    session = SessionLocal()
    # services
    employee_service = EmployeeService(session=session)
    position_service = PositionService(session=session)
    municipality_service = MunicipalityService(session=session)

    window = MainWindow(
        employee_service=employee_service,
        position_service=position_service,
        municipality_service=municipality_service,
    )
    window.resize(800, 400)
    window.show()

    exit_code = app.exec()
    session.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
