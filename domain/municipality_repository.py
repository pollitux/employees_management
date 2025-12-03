from abc import ABC, abstractmethod
from typing import List, Optional
from employees_management.domain.models import Municipality


class IMunicipalityRepository(ABC):
    """

    """

    @abstractmethod
    def list_municipalities(self) -> List[Municipality]:
        """

        :return:
        """
        pass

    @abstractmethod
    def get(self, municipality_id: int) -> Optional[Municipality]:
        """

        :param municipality_id:
        :return:
        """
        pass

    @abstractmethod
    def add(self, name: str) -> Municipality:
        """

        :param name:
        :return:
        """
        pass
