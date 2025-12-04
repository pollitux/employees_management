# Employees Management System

### Final Project – Technologies of Programming

### Python + PyQt6 + SQLAlchemy + Clean Architecture + SOLID

This project was developed as the final assignment for the course "Technologies of Programming".  
Its main purpose is educational, allowing students to learn and apply:

- SOLID principles
- Clean Architecture
- PEP 8 and Clean Code conventions
- Repository patterns with SQLAlchemy
- Desktop development with PyQt6
- Separation of responsibilities and modular design
- Data import tools and reporting functionalities

The system provides a complete desktop application for managing employees, positions, and municipalities, including
charts, CSV import, salary calculations, and advanced filtering tools.

---

## Educational Goals

This project demonstrates how to build professional, maintainable, and modular software, following patterns used in real
industry applications.

### SOLID Principles

- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

References:  
https://en.wikipedia.org/wiki/SOLID  
https://contabo.com/blog/es/que-son-los-principios-solid-en-programacion/

---

## Clean Architecture

The project is structured in 4 independent layers:

1. Domain – Entities and repository contracts
2. Application – Services containing business logic
3. Infrastructure – SQLAlchemy ORM, database engine, repository implementations
4. GUI – PyQt6 user interface and charts

This guarantees:

- Low coupling
- High testability
- Framework-independent logic
- Scalability for future features

---

## PEP 8 and Clean Code

Official guide: https://peps.python.org/pep-0008/

Applied conventions include meaningful naming, consistent spacing, small methods, and English-based comments and
docstrings.

---

## Project Structure

```
employees_management/
│
├── application/
│   ├── employee_service.py
│   ├── employee_import_service.py
│   ├── municipality_service.py
│   └── position_service.py
│
├── config/
│   └── settings.py
│
├── domain/
│   ├── models.py
│   ├── employee_repository.py
│   ├── municipality_repository.py
│   └── position_repository.py
│
├── gui/
│   ├── chart_window.py
│   ├── main_window.py
│   ├── municipality_window.py
│   ├── position_window.py
│   ├── window_employee.py
│   ├── window_salary.py
│   └── dialogs/
│
├── icons/
│
├── infrastructure/
│   ├── db.py
│   ├── employee_repository_impl.py
│   ├── municipality_repository_impl.py
│   └── position_repository_impl.py
│
├── translations/
│   ├── es.py
│   └── __init__.py
│
├── employees.db
├── main.py
├── README.md
└── requirements.txt
```

---

## Architecture Overview

### Domain Layer

Contains the core entities and repository interfaces without dependencies on frameworks.

### Application Layer

Encapsulates use cases and business logic. It depends only on domain interfaces.

### Infrastructure Layer

Implements database communication, SQLAlchemy configurations, and repository implementations.

### GUI Layer

Contains PyQt6 windows, dialogs, toolbar menus, CSV import utilities, and Matplotlib charts.

---

## Database Configuration

SQLite (default):
DATABASE_URL = "sqlite:///employees.db"

MySQL (optional):
DATABASE_URL = "mysql+pymysql://user:password@localhost/employees_db"

Tables are automatically created when running the application.

---

## Features

### Employees Module

- Full CRUD operations
- Validation for required fields
- Two employee types: BASE and HONORARY
- Birthdate and municipality selection
- Automatic salary calculation

### Municipalities Module

- Full CRUD
- Integrated with employee registration

### Positions Module

- Full CRUD

### Reports and Charts

- Employees by Position
- Employees by Municipality
- Bar charts rendered using Matplotlib with labels

### Filtering Tools

- Filter by Position
- Filter by Municipality
- Filter by Employee Type (ALL, BASE, HONORARY)
- Text search by name or NSS

### CSV Import

Under Utils → Import CSV, the system supports loading large datasets into the database using bulk insert.

Expected CSV structure:

nss,first_name,last_name_f,last_name_m,position,municipality,birth_date,employee_type,hourly_rate,hours_worked

### Salary Calculator

Includes a dedicated window for computing employee salary based on:

#### Base Employee:

salary = hourly_rate * 40 + (1 percentage per year of service)

#### Honorary Employee:

salary = hourly_rate * hours_worked + (0.2 percentage per extra hour)

---

## Installation

```shell
python -m venv .venv
source .venv/bin/activate   # macOS / Linux  
.venv\Scripts\activate      # Windows  
pip install -r requirements.txt
```

---

## Run the application

```shell
python main.py
```

---

## Code Quality Standards

- Clean Architecture
- SOLID
- Repository pattern
- Database abstraction
- PEP 8 compliance
- English documentation

---

## Academic Purpose

This project is intended as a learning tool for understanding advanced programming practices, architecture patterns, and
GUI development. It serves as a reference implementation for students and is not intended for production use.

