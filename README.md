# Employees Management System  
### Final Project – Technologies of Programming  
### Python + PyQt6 + SQLAlchemy + Clean Architecture + SOLID

This project was developed as the **final assignment for the course "Technologies of Programming"**.  
Its main purpose is **educational**, aiming to help students understand and apply:

- SOLID principles  
- Clean Architecture  
- Good programming practices  
- PEP 8 style conventions  
- Desktop application development with PyQt6  
- SQLAlchemy ORM and repository patterns  
- Separation of responsibilities and decoupled design  

The result is a fully working **desktop management system** for employees, positions, and municipalities, including statistics shown in charts.

---

## Educational Goals

This project is designed to teach students how to build professional, maintainable and modular software.

### Apply **SOLID principles**

- **S**ingle Responsibility Principle  
- **O**pen/Closed Principle  
- **L**iskov Substitution Principle  
- **I**nterface Segregation Principle  
- **D**ependency Inversion Principle  
 
Official reference:  
https://en.wikipedia.org/wiki/SOLID

 Easy-to-understand explanation:  
https://contabo.com/blog/es/que-son-los-principios-solid-en-programacion/

---

### Follow **Clean Architecture**

This project separates responsibilities into 4 layers:

1. **Domain** – Entities and repository interfaces  
2. **Application** – Use cases / business logic  
3. **Infrastructure** – ORM, database engine, repository implementations  
4. **GUI** – PyQt6 windows, dialogs and charts  

This design ensures:

- High testability  
- Low coupling  
- Clear scalability  
- Independence from frameworks  

---

### Follow **PEP 8 and Clean Code practices**

 PEP 8 official style guide:  
https://peps.python.org/pep-0008/

Applied aspects:

- snake_case for functions and variables  
- PascalCase for classes  
- Clear, simple English comments  
- Line length and spacing guidelines  
- Organized imports  
- Small, readable functions  

---

## Project Structure

```
employees_management/
│
├── application/
│   ├── employee_service.py
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
│   └── window_salary.py
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

### **Domain Layer**
- Pure Python entities  
- Repository interfaces  
- No external dependencies  

### **Application Layer**
- Contains the business logic  
- Services depend on **interfaces**, not implementations  
- Applies the **Dependency Inversion Principle**  

### **Infrastructure Layer**
- Implements repositories using SQLAlchemy  
- Contains database configuration and ORM logic  

### **GUI Layer (PyQt6)**
- CRUD windows for employees, positions, municipalities  
- Salary management window  
- Chart window using Matplotlib  

---

## Database Configuration

### SQLite (default)
```
DATABASE_URL = "sqlite:///employees.db"
```

### MySQL (optional)
```
DATABASE_URL = "mysql+pymysql://user:password@localhost/employees_db"
```

Tables are automatically created on first run.

---

## Features

### Employees Module
- Create, edit and delete employees  
- Assign position and municipality  
- Validate data before saving  
- Salary window included  

### Municipalities Module
- Full CRUD  
- Integrated with employee creation  

### Positions Module
- Full CRUD  
- Used inside employee forms  

### Statistics & Charts
- Bar chart of employees per position  
- Labels displayed above bars  
- Built using embedded Matplotlib  

---

## Installation

```
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## Run the application

```
python main.py
```

---

## Code Quality

The project strictly follows:

- PEP 8  
- English-based documentation  
- Single Responsibility per class  
- SOLID principle compliance  
- Clean and modular folder structure  

This ensures code is readable, maintainable, and aligned with industry expectations.

---

## Academic Purpose

This repository is meant to serve as:

- A **learning tool** for applying advanced programming principles  
- A **reference implementation** for future students  
- A **demonstration project** for software engineering portfolios  
- An example of how to structure real-world desktop applications  

It is not intended for production use, but rather for **educational analysis and classroom presentations**.

---