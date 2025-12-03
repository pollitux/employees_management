from abc import ABC, abstractmethod
from typing import List, Optional
from employees_management.domain.models import Position


class IPositionRepository(ABC):
    """

    """

    @abstractmethod
    def list_positions(self) -> List[Position]:
        """

        :return:
        """
        pass

    @abstractmethod
    def get(self, position_id: int) -> Optional[Position]:
        """

        :param position_id:
        :return:
        """
        pass

    @abstractmethod
    def add(self, name: str, salary_base: float) -> Position:
        """

        :param salary_base:
        :param name:
        :return:
        """
        pass
