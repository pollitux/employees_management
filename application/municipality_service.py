from sqlalchemy.orm import Session

from employees_management.infrastructure.municipality_repository_impl import MunicipalityRepositoryImpl
from students.domain.models import Municipality


class MunicipalityService:
    """
    Municipality Service
    """

    def __init__(self, session: Session):
        self._session = session

        self._municipality_repo = MunicipalityRepositoryImpl(session)

    def list_municipalities(self) -> list[type[Municipality]]:
        """

        :return:
        """
        return self._municipality_repo.list_municipalities()

    def create_municipality(self, name: str) -> Municipality:
        """

        :param name:
        :return:
        """
        if not name:
            raise ValueError("Name is required")
        return self._municipality_repo.add(name)

    def update(self, municipality: Municipality, **updates) -> Municipality:
        """

        :param municipality:
        :return:
        """
        # update fields with new values
        municipality.name = updates.get("name", municipality.name)
        return self._municipality_repo.update(municipality)

    def find_by_name(self, name: str) -> Municipality:
        """
        Get Municipality by name
        :param name:
        :return:
        """
        return self._municipality_repo.find_by_name(name)

    def delete_municipality(self, municipality: Municipality):
        """
        delete municipality with given municipality id using municipality repository.
        :param municipality:
        :return:
        """
        return self._municipality_repo.delete(municipality)
