"""Script to seed employees.json with initial records."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "src" / "data" / "employees.json"

DEFAULT_EMPLOYEES = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 75000.0},
    {"id": 2, "name": "Bob", "department": "Marketing", "salary": 45000.0},
    {"id": 3, "name": "Charlie", "department": "Engineering", "salary": 82000.0},
    {"id": 4, "name": "Diana", "department": "HR", "salary": 48000.0},
    {"id": 5, "name": "Evan", "department": "Product", "salary": 60000.0},
]


def seed() -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(DEFAULT_EMPLOYEES, f, indent=4)
    print(f"Seeded {len(DEFAULT_EMPLOYEES)} employees to {DATA_FILE}")


if __name__ == "__main__":
    seed()
