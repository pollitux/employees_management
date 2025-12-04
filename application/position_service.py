from typing import Optional

from sqlalchemy.orm import Session
from employees_management.domain.models import Position
from employees_management.infrastructure.position_repository_impl import PositionRepositoryImpl


class PositionService:
    """
    Position Service
    """

    def __init__(self, session: Session):
        self._session = session

        self._position_repo = PositionRepositoryImpl(session)

    def list_positions(self) -> list[type[Position]]:
        """

        :return:
        """
        return self._position_repo.list_positions()

    def create_position(self, name: str, base_salary: float) -> Position:
        """

        :param base_salary:
        :param name:
        :return:
        """
        if not name and base_salary > 0:
            raise ValueError("Name is required")
        return self._position_repo.add(name, base_salary)

    def update_position(self, position: Position, **updates) -> Position:
        """

        :param position:
        :return:
        """
        # update fields with new values
        # update fields with new values
        for key, value in updates.items():
            setattr(position, key, value)
        return self._position_repo.update(position)

    def find_by_name(self, name) -> Optional[Position]:
        """

        :param name:
        :return:
        """
        return self._position_repo.find_by_name(name)
