"""Pydantic data models for employee schema validation."""

from pydantic import BaseModel, Field, field_validator


class EmployeeCreate(BaseModel):
    """Payload model for creating a new employee."""

    name: str = Field(
        ...,
        min_length=1,
        description="Employee name (must not be empty)",
        examples=["Alice"],
    )
    department: str = Field(
        default="General",
        description="Department name",
        examples=["Engineering"],
    )
    salary: float = Field(
        ...,
        gt=0,
        description="Salary must be strictly greater than 0",
        examples=[75000.0],
    )

    @field_validator("name")
    @classmethod
    def validate_name_not_empty_or_whitespace(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Employee name cannot be empty or whitespace only")
        return trimmed


class Employee(EmployeeCreate):
    """Model representing an employee entity with an assigned ID."""

    id: int = Field(
        ...,
        description="Unique employee ID",
        examples=[1],
    )


if __name__ == "__main__":
    print("--- models.py Pydantic Schema Demo ---")
    valid_emp = Employee(id=1, name="Alice", department="Engineering", salary=75000.0)
    print("Valid Employee Model:", valid_emp.model_dump())

    try:
        EmployeeCreate(name="", salary=-5)
    except Exception:
        print("Validation test (empty name & salary -5): Caught expected error -> 422")
    print("--------------------------------------")
