import sys
from PyQt6.QtWidgets import QApplication

from employees_management.application.employee_export_service import EmployeeExportService
from employees_management.application.employee_import_service import EmployeeImportService
from employees_management.application.municipality_service import MunicipalityService
from employees_management.application.position_service import PositionService
from employees_management.application.pandas_service import PandasService

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

    import_service = EmployeeImportService(
        employee_service,
        position_service,
        municipality_service
    )

    pandas_service = PandasService()

    export_service = EmployeeExportService(pandas_service)

    window = MainWindow(
        employee_service=employee_service,
        position_service=position_service,
        municipality_service=municipality_service,
        import_service=import_service,
        pandas_service=pandas_service,
        export_service=export_service,
    )

    window.resize(800, 600)
    window.show()

    exit_code = app.exec()
    session.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
