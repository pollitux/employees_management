# Employees Management System  
Final Project – Technologies of Programming  
Python + PyQt6 + SQLAlchemy + Pandas + Matplotlib + Clean Architecture + SOLID

This project was developed as the final assignment for the course "Technologies of Programming".  
Its main purpose is educational, demonstrating how to build a modular, maintainable desktop system applying:

- SOLID principles  
- Clean Architecture  
- PEP 8 conventions  
- Good programming practices  
- PyQt6 for desktop UI  
- SQLAlchemy ORM  
- Pandas for data analysis  
- Matplotlib for multiple chart types  
- CSV import and export functionality  

The final result is a complete employee-management desktop system with data persistence, reporting, analytics, and visualization.

## Educational Goals

This project is designed to help students/professors understand how real software projects are structured.

### SOLID Principles  
Applied across services, repositories, and GUI separation.

Reference:  
https://en.wikipedia.org/wiki/SOLID

Explanation:  
https://contabo.com/blog/es/que-son-los-principios-solid-en-programacion/

## Clean Architecture

The system is divided into four independent layers:

1. Domain  
2. Application  
3. Infrastructure  
4. GUI (PyQt6)

This architecture ensures:

- Low coupling  
- High cohesion  
- Easy testing  
- Independence from frameworks  
- Maintainability and scalability  

## PEP 8 and Clean Code

The project follows:

- snake_case for variables and functions  
- PascalCase for classes  
- Meaningful comments written in simple English  
- Small, readable functions  
- Avoiding duplicated logic  
- Modular design  

PEP 8 reference: https://peps.python.org/pep-0008/

## Project Structure

```
employees_management/
│
├── application/
│   ├── employee_service.py
│   ├── municipality_service.py
│   ├── position_service.py
│   ├── employee_import_service.py
│   └── pandas_service.py
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
│   └── window_filters.py
│
├── infrastructure/
│   ├── db.py
│   ├── employee_repository_impl.py
│   ├── municipality_repository_impl.py
│   └── position_repository_impl.py
│
├── icons/
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

## Database Support

### SQLite (default)
```
DATABASE_URL = "sqlite:///employees.db"
```

### MySQL (required for the assignment)
Using SQLAlchemy:

```
DATABASE_URL = "mysql+pymysql://user:password@localhost/employees_db"
```

## Features

### Employees Module
- Add employees (base or honoraries)
- Edit all editable fields
- Delete employees
- Search by NSS or name
- Filters by:
  - Position
  - Municipality
  - Employee type (Base / Honorary)

### CSV Import  
Bulk CSV import includes:
- Position lookup  
- Municipality lookup  
- Normalization of employee type  
- Validation of inputs  
- Summary of inserted and failed rows  

### Pandas Filters  
Three filters implemented:
1. Age ranges  
2. Municipality  
3. Employee type  

### Charts (Matplotlib)
1. Employees by position  
2. Employees by municipality  
3. Salary summary  
4. Employee type distribution (Pie chart)  
5. Age range distribution (Bar chart)

## Pandas Age Range Categorization

```
df["age_range"] = pd.cut(
    ages,
    bins=bins,
    labels=labels,
    right=True
)
```

This line converts numeric employee ages into labeled categories for better visualization.

## Installation

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the application

```shell
python main.py
```

## Academic Requirements Covered

- CSV/XLSX reading  
- MySQL CRUD  
- Pandas filters  
- Matplotlib graphs  
- Database script included  

This project is intended purely for academic and educational use.
