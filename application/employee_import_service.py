from employees_management.domain.models import Employee
from datetime import datetime


class EmployeeImportService:
    """

    """

    def __init__(self, employee_service, position_service, municipality_service):
        self._employee_service = employee_service
        self._position_service = position_service
        self._municipality_service = municipality_service

    def import_csv(self, file_path: str) -> dict:
        """

        :param file_path:
        :return:
        """
        import csv

        employees_to_insert = []
        failed = 0
        errors = []

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    position = self._position_service.find_by_name(row["position"])
                    if not position:
                        position = self._position_service.create_position(row["position"], row["hourly_rate"])

                    municipality = self._municipality_service.find_by_name(row["municipality"])
                    if not municipality:
                        municipality = self._municipality_service.create_municipality(row["municipality"])

                    employee = Employee(
                        nss=int(row["nss"]),
                        first_name=row["first_name"],
                        last_name_f=row["last_name_f"],
                        last_name_m=row["last_name_m"],
                        position_id=position.id,
                        birth_date=datetime.strptime(row["birth_date"], "%Y-%m-%d").date(),
                        municipality_id=municipality.id,
                        employee_type=row["employee_type"].upper(),
                        hourly_rate=float(row["hourly_rate"]),
                        hours_worked=int(row["hours_worked"]),
                    )

                    employees_to_insert.append(employee)

                except Exception as exc:
                    print(f"Failed to import row: {exc}")
                    failed += 1
                    errors.append(str(exc))

        if employees_to_insert:
            self._employee_service.bulk_insert(employees_to_insert)

        return {
            "inserted": len(employees_to_insert),
            "failed": failed,
            "errors": errors
        }
