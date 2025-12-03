# Employees Management System (Python + PyQt6 + SQLAlchemy + SQLite/MySQL)

This project is a complete employee management desktop application built with:

- **Python 3**
- **PyQt6** for the graphical interface
- **SQLAlchemy ORM**
- **SQLite or MySQL** (configurable)
- **SOLID Principles**
- **Repository Pattern (Interfaces + Implementations)**
- **Clean Architecture Style**
- **Matplotlib for statistical charts**

The system supports **Employees**, **Municipalities**, **Positions**, and **Salary Charts**, each with full CRUD operations.

---

## 📁 Project Structure

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
│   └── (PNG/SVG icons used by the app)
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
├── employees.db        # SQLite database (optional)
├── main.py             # Application entrypoint
├── README.md
└── requirements.txt
```

---

## 🧱 Architecture Overview

This project follows a **clean layered architecture**:

### 1️⃣ Domain Layer
Located in `domain/`

- Contains **entities/models** (Employee, Municipality, Position)
- Defines **repository interfaces**
- Pure Python, no framework dependencies

### 2️⃣ Application Layer
Located in `application/`

- Contains **use cases / business logic**
- Services depend **only on repository interfaces**

### 3️⃣ Infrastructure Layer
Located in `infrastructure/`

- Implements repositories using SQLAlchemy ORM
- Manages DB engine + sessions

### 4️⃣ GUI Layer (PyQt6)
Located in `gui/`

Contains all user interface windows with full CRUD and charts.

---

## 🛢 Database Configuration

### ✔ SQLite (default)

```
DATABASE_URL = "sqlite:///employees.db"
```

### ✔ MySQL (optional)

```
DATABASE_URL = "mysql+pymysql://user:password@localhost/employees_db"
```

Tables auto-create on startup.

---

## 🚀 Features

### Employees
- Full CRUD  
- Assign position/municipality  
- Integrated salary window  

### Municipalities & Positions
- Full CRUD  
- Used by employee module  

### Charts
- Bar chart of employees per position  
- Labels added above bars

---

## 📦 Installation

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## ▶️ Run Application

```
python main.py
```

---

## 📝 License

MIT License.
