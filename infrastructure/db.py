"""
Author: Raul Granados
Company: Swipall
Description: initial db engine a local session
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from employees_management.config.settings import get_database_url

engine = create_engine(
    get_database_url(),
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

Base = declarative_base()
