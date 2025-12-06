from typing import List
from employees_management.domain.models import Employee
from employees_management.application.pandas_service import PandasService


class EmployeeExportService:
    """
    Service responsible for exporting filtered employees to CSV (or Excel).
    This service keeps business logic out of the UI.
    """

    def __init__(self, pandas_service: PandasService):
        self._pandas_service = pandas_service

    def export_to_csv(self, employees: List[Employee], file_path: str) -> None:
        """
        Export given employees to a CSV file.

        Parameters
        ----------
        employees : List[Employee]
            Employees after filtering (UI should pass this list).

        file_path : str
            Where to save the CSV file.

        Raises
        ------
        ValueError : If employees list is empty.
        IOError : If CSV cannot be written.
        """

        if not employees:
            raise ValueError("No employees to export.")

        df = self._pandas_service.employees_to_dataframe(employees)

        try:
            df.to_csv(file_path, index=False)
        except Exception as exc:
            raise IOError(f"Error writing CSV: {exc}")
