"""
Author: Raul Granados
Company: Swipall
Description: Interface for employee repository
"""

from abc import ABC, abstractmethod
from typing import Optional
from employees_management.domain.models import Employee


class IEmployeeRepository(ABC):
    """
    Interface for Employee repository.
    """

    @abstractmethod
    def list_employees(self) -> list[Employee]:
        """
        Retrieve all employees.
        :return: list of Employee
        """
        pass

    @abstractmethod
    def get(self, employee_id: int) -> Optional[Employee]:
        """
        Retrieve employee by ID.
        :param employee_id: int
        :return: Optional[Employee]
        """
        pass

    @abstractmethod
    def add(self, employee: Employee) -> Employee:
        """
        Add a new employee.
        :param employee: Employee instance
        :return: persisted Employee with ID
        """
        pass

    @abstractmethod
    def delete(self, employee_id: int) -> bool:
        """
        Delete employee by ID.
        :param employee_id: int
        :return: success status
        """
        pass
