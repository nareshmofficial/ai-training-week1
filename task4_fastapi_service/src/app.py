"""FastAPI employee service application."""

import json
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status

# Ensure both src and project root are in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent
for directory in (str(SRC_DIR), str(PROJECT_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

try:
    from .models import Employee, EmployeeCreate
except (ImportError, ValueError):
    from models import Employee, EmployeeCreate

app = FastAPI(
    title="Employee Service",
    description="FastAPI service for employee management with Pydantic validation.",
    version="1.0.0",
)

DATA_FILE_PATH: Path = Path(__file__).resolve().parent / "data" / "employees.json"


def load_employees() -> list[dict[str, Any]]:
    """Read employee records from the JSON data file."""
    if not DATA_FILE_PATH.exists():
        return []
    with DATA_FILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def save_employees(employees: list[dict[str, Any]]) -> None:
    """Save employee records to the JSON data file."""
    DATA_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(employees, f, indent=4)


@app.get("/", status_code=status.HTTP_200_OK)
def get_root() -> dict[str, str]:
    """Root endpoint welcoming the user and providing endpoint links."""
    return {
        "message": "Welcome to Employee Service API",
        "docs": "/docs",
        "health": "/health",
        "employees": "/employees",
    }


@app.get("/health", status_code=status.HTTP_200_OK)
def get_health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get(
    "/employees",
    response_model=list[Employee],
    status_code=status.HTTP_200_OK,
)
def get_employees() -> list[dict[str, Any]]:
    """Retrieve all employees from employees.json."""
    return load_employees()


@app.get(
    "/employees/{name}",
    response_model=Employee,
    status_code=status.HTTP_200_OK,
)
def get_employee(name: str) -> dict[str, Any]:
    """Retrieve an employee by name (case-insensitive) or return 404."""
    employees = load_employees()
    for emp in employees:
        if emp.get("name", "").lower() == name.lower():
            return emp

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee '{name}' not found",
    )


@app.post(
    "/employees",
    response_model=Employee,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(payload: EmployeeCreate) -> dict[str, Any]:
    """Create a new employee with Pydantic validation and persist to employees.json."""
    employees = load_employees()
    next_id = max([int(emp.get("id", 0)) for emp in employees], default=0) + 1

    new_employee: dict[str, Any] = {
        "id": next_id,
        "name": payload.name,
        "department": payload.department,
        "salary": payload.salary,
    }

    employees.append(new_employee)
    save_employees(employees)
    return new_employee


if __name__ == "__main__":
    import uvicorn

    print("==================================================")
    print("  Starting Employee Service on http://127.0.0.1:8000")
    print("  Swagger UI: http://127.0.0.1:8000/docs")
    print("==================================================")
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)
