"""
Author: Raul Granados
Company: Swipall
Description: Repository for position crud
"""

from typing import Optional
from sqlalchemy.orm import Session
from employees_management.domain.models import Position
from employees_management.domain.position_repository import IPositionRepository


class PositionRepositoryImpl(IPositionRepository):

    def __init__(self, session: Session):
        self._session = session

    def list_positions(self) -> list[type[Position]]:
        """
        List all positions
        :return:
        """
        return self._session.query(Position).order_by(Position.name).all()

    def get(self, position_id: int) -> Optional[Position]:
        """
        Get position by id
        :param position_id:
        :return:
        """
        return self._session.query(Position).get(position_id)

    def add(self, name: str, base_salary: float) -> Position:
        """
        Add a position
        :param base_salary:
        :param name:
        :return:
        """
        position = Position(name=name, base_salary=base_salary)
        self._session.add(position)
        self._session.commit()
        self._session.refresh(position)
        return position
