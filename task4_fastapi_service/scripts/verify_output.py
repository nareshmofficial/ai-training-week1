"""Verification script to test and display the expected output for Task 4."""

import sys
import warnings
from pathlib import Path

# Suppress minor starlette deprecation notice for clean output
warnings.filterwarnings("ignore")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

from src.app import app


def main() -> None:
    client = TestClient(app)

    print("=" * 45)
    print("        TASK 4 - EXPECTED OUTPUT")
    print("=" * 45)

    # 1. GET /health
    res_health = client.get("/health")
    print(f"GET /health -> {res_health.json()}")

    # 2. GET /employees/Ravi
    res_ravi = client.get("/employees/Ravi")
    print(f"GET /employees/Ravi -> {res_ravi.status_code}")

    # 3. POST salary -5
    res_invalid_salary = client.post("/employees", json={"name": "Frank", "salary": -5})
    print(f"POST salary -5 -> {res_invalid_salary.status_code}")

    print("=" * 45)


if __name__ == "__main__":
    main()
