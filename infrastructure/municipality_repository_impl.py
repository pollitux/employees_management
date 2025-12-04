"""
Author: Raul Granados
Company: Swipall
Description: Repository for municipality crud
"""

from typing import Optional
from sqlalchemy.orm import Session
from employees_management.domain.models import Municipality
from employees_management.domain.municipality_repository import IMunicipalityRepository


class MunicipalityRepositoryImpl(IMunicipalityRepository):

    def __init__(self, session: Session):
        self._session = session

    def list_municipalities(self) -> list[type[Municipality]]:
        """
        List all municipalities
        :return:
        """
        return self._session.query(Municipality).order_by(Municipality.name).all()

    def get(self, municipality_id: int) -> Optional[Municipality]:
        """
        Get municipality by id
        :param municipality_id:
        :return:
        """
        return self._session.query(Municipality).get(municipality_id)

    def add(self, name: str) -> Municipality:
        """
        Add a municipality
        :param name:
        :return:
        """
        municipality = Municipality(name=name)
        self._session.add(municipality)
        self._session.commit()
        self._session.refresh(municipality)
        return municipality

    def update(self, municipality: Municipality) -> Municipality:
        """
        update municipality to the database.

        Args:
            municipality (Municipality): The Municipality object to update.

        Returns:
            Municipality: The persisted Employee instance with ID assigned.
        """
        self._session.commit()
        self._session.refresh(municipality)
        return municipality

    def find_by_name(self, name: str) -> Optional[Municipality]:
        """
        Get municipality by name
        :param name:
        :return:
        """
        return self._session.query(Municipality).filter(Municipality.name == name).first()

    def delete(self, municipality: Municipality) -> bool:
        """
        Delete municipality
        :param municipality:
        :return:
        """
        self._session.delete(municipality)
        self._session.commit()
        return True
