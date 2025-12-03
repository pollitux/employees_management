"""
Author: Raul Granados
Company: Swipall
Description: Repository for employee CRUD operations using SQLAlchemy.
"""

from typing import Optional, Any
from sqlalchemy.orm import Session
from employees_management.domain.models import Employee
from employees_management.domain.employee_repository import IEmployeeRepository


class EmployeeRepositoryImpl(IEmployeeRepository):
    """
    SQLAlchemy implementation of the IEmployeeRepository interface.
    Provides basic CRUD operations on Employee entities.
    """

    def __init__(self, session: Session):
        self._session = session

    def list_employees(self) -> list[type[Employee]]:
        """
        Retrieve all employees from the database, ordered by last name.

        Returns:
            list[Employee]: List of all Employee instances.
        """
        return self._session.query(Employee).order_by(Employee.last_name_f).all()

    def get(self, employee_id: int) -> Optional[Employee]:
        """
        Retrieve a single employee by ID.

        Args:
            employee_id (int): The ID of the employee to retrieve.

        Returns:
            Optional[Employee]: The employee instance if found, None otherwise.
        """
        return self._session.query(Employee).get(employee_id)

    def find_by_nss(self, nss: int) -> Optional[Employee]:
        """
        Retrieve a single employee by nss using employee repository.

        Args:
            nss (int): The nss of the employee to retrieve.

        Returns:
            Optional[Employee]: The employee instance if found, None otherwise.
        """
        return self._session.query(Employee).filter_by(nss=nss).first()

    def add(self, employee: Employee) -> Employee:
        """
        Add a new employee to the database.

        Args:
            employee (Employee): The Employee object to add.

        Returns:
            Employee: The persisted Employee instance with ID assigned.
        """
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def update(self, employee: Employee) -> Employee:
        """
        update employee to the database.

        Args:
            employee (Employee): The Employee object to update.

        Returns:
            Employee: The persisted Employee instance with ID assigned.
        """
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def delete(self, employee_id: int) -> bool:
        """
        Delete an employee by ID.

        Args:
            employee_id (int): ID of the employee to delete.

        Returns:
            bool: True if deletion was successful, False if employee was not found.
        """
        employee = self.get(employee_id)
        if not employee:
            return False
        self._session.delete(employee)
        self._session.commit()
        return True
