"""
Author: Raul Granados
Company: Swipall
Description: Build database URL for SQLAlchemy.
"""

import os


def get_database_url() -> str:
    """
    Build database URL for SQLAlchemy.
    Uses SQLite as fallback if no engine is specified.
    """
    engine = os.getenv("DB_ENGINE", "sqlite").lower()

    if engine == "mysql":
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "rootpass")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        database = os.getenv("DB_NAME", "employees_db")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    # Default to SQLite
    database_path = os.getenv("DB_NAME", "employees.db")
    return f"sqlite:///{database_path}"
