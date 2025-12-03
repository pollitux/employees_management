"""
Author: Raul Granados
Company: Swipall
Description: Application service for managing employees using SQLAlchemy.
"""
from datetime import date, datetime
from typing import Optional
from sqlalchemy.orm import Session

from employees_management.domain.models import Employee, Municipality, Position
from employees_management.infrastructure.employee_repository_impl import EmployeeRepositoryImpl
from employees_management.infrastructure.position_repository_impl import PositionRepositoryImpl
from employees_management.infrastructure.municipality_repository_impl import MunicipalityRepositoryImpl


class EmployeeService:
    """
    Application service for managing employees.
    """

    BASE_RATES = {
        "PROGRAMMER": 150.0,
        "ANALYST": 140.0,
        "ADMINISTRATOR": 130.0,
        "HR": 120.0,
        "TECHNICIAN": 110.0,
    }

    def __init__(self, session: Session):
        self._session = session
        self._employee_repo = EmployeeRepositoryImpl(session)
        self._position_repo = PositionRepositoryImpl(session)
        self._municipality_repo = MunicipalityRepositoryImpl(session)

    def list_employees(self) -> list[type[Employee]]:
        """
        Returns a list of employees that are currently registered.
        :return:
        """
        return self._employee_repo.list_employees()

    def find_employee(self, nss: int) -> Optional[Employee]:
        """
        find employee with given nss using employee repository.
        :param nss:
        :return:
        """
        return self._employee_repo.find_by_nss(nss)

    def delete_employee(self, employee_id: int):
        """
        delete employee with given employee id using employee repository.
        :param employee_id:
        :return:
        """
        employee = self.find_employee(employee_id)
        if employee is None:
            raise ValueError(f"NSS {employee_id} not found")
        return self._employee_repo.delete(employee.id)

    def update_employee(self, employee: Employee, **updates) -> Employee:
        """
        update employee with given employee id using employee repository.
        :param employee: employee instance
        :param updates: fields to update
        :return:
        """
        # update fields with new values
        for key, value in updates.items():
            if key == "birth_date":
                value = datetime.strptime(value, "%Y-%m-%d").date()
            setattr(employee, key, value)
        return self._employee_repo.update(employee=employee)

    def add_employee(
            self,
            *,
            nss: int,
            first_name: str,
            last_name_f: str,
            last_name_m: str,
            position_id: int,
            birth_date: date,
            municipality_id: int,
            employee_type: str,
            hourly_rate: Optional[float] = None,
            hours_worked: Optional[int] = None,
    ) -> Employee:
        """
        add employee with given nss using employee repository.
        :param nss:
        :param first_name:
        :param last_name_f:
        :param last_name_m:
        :param position_id:
        :param birth_date:
        :param municipality_id:
        :param employee_type:
        :param hourly_rate:
        :param hours_worked:
        :return:
        """

        if self.find_employee(nss):
            raise ValueError(f"NSS {nss} must be unique")

        position = self._position_repo.get(position_id)
        if not position:
            raise ValueError("Invalid position ID")

        municipality = self._municipality_repo.get(municipality_id)
        if not municipality:
            raise ValueError("Invalid municipality ID")

        employee_type = employee_type.upper()

        if employee_type == "BASE":
            hourly_rate = position.base_salary
            hours_worked = 0

        elif employee_type == "HONORARY":
            if hourly_rate is None or hours_worked is None:
                raise ValueError("Honorary employees must provide hourly rate and hours worked")
            if not (1 <= hours_worked <= 40):
                raise ValueError("Hours worked must be between 1 and 40")
        else:
            raise ValueError("employee_type must be 'BASE' or 'HONORARY'")
        employee = Employee(
            nss=nss,
            first_name=first_name,
            last_name_f=last_name_f,
            last_name_m=last_name_m,
            birth_date=birth_date,
            employee_type=employee_type,
            position_id=position_id,
            municipality_id=municipality_id,
            hourly_rate=hourly_rate,
            hours_worked=hours_worked,
        )

        return self._employee_repo.add(employee)
