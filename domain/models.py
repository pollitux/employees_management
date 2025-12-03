"""
Author: Raul Granados
Company: Swipall
Description: data models
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DATE
from sqlalchemy.orm import relationship

from employees_management.infrastructure.db import Base


class Municipality(Base):
    __tablename__ = "municipality"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    # Back reference: one municipality -> many employees
    employees = relationship("Employee", back_populates="municipality_rel")

    def __repr__(self):
        return f"<Municipality id={self.id} name={self.name}>"


class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    base_salary = Column(Float, nullable=False)
    # Back reference: one position -> many employees
    employees = relationship("Employee", back_populates="position_rel")

    def __repr__(self):
        return f"<Position id={self.id} name={self.name}>"


class Employee(Base):
    """
    Domain model for Student entity.
    """
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    nss = Column(Integer)
    first_name = Column(String(100), nullable=False)
    last_name_f = Column(String(100), nullable=False)
    last_name_m = Column(String(100), nullable=False)
    birth_date = Column(DATE, nullable=False)
    employee_type = Column(String(150), nullable=False)
    # Foreign key
    position_id = Column(Integer, ForeignKey("position.id"), nullable=False)
    # Relationship object
    position_rel = relationship("Position", back_populates="employees")
    municipality_id = Column(Integer, ForeignKey("municipality.id"), nullable=False)
    # Relationship object
    municipality_rel = relationship("Municipality", back_populates="employees")
    hourly_rate = Column(Float)
    hours_worked = Column(Integer)

    def __repr__(self) -> str:
        return f"<Employee id={self.id} name={self.first_name} {self.last_name_m}>"
