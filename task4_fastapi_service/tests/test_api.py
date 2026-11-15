"""Unit and integration tests for FastAPI employee service."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app


@pytest.fixture(autouse=True)
def isolated_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Provide an isolated temporary JSON data file for each test."""
    temp_file = tmp_path / "employees.json"
    baseline = [
        {"id": 1, "name": "Alice", "department": "Engineering", "salary": 75000.0},
        {"id": 2, "name": "Bob", "department": "Marketing", "salary": 45000.0},
        {"id": 3, "name": "Charlie", "department": "Engineering", "salary": 82000.0},
        {"id": 4, "name": "Diana", "department": "HR", "salary": 48000.0},
        {"id": 5, "name": "Evan", "department": "Product", "salary": 60000.0},
    ]
    temp_file.write_text(json.dumps(baseline), encoding="utf-8")
    monkeypatch.setattr(app_module, "DATA_FILE_PATH", temp_file)
    return temp_file


@pytest.fixture
def client() -> TestClient:
    """Return FastAPI TestClient instance."""
    return TestClient(app)


def test_root(client: TestClient) -> None:
    """GET / -> 200 with welcome message and docs links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"


def test_health(client: TestClient) -> None:
    """GET /health -> 200 {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_employees_list(client: TestClient) -> None:
    """GET /employees -> 200 with list of records."""
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert data[0]["name"] == "Alice"


def test_get_employee_success(client: TestClient) -> None:
    """GET /employees/{name} -> 200 for existing employee (case-insensitive)."""
    response = client.get("/employees/Alice")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["salary"] == 75000.0

    # Test case-insensitivity
    response_lower = client.get("/employees/alice")
    assert response_lower.status_code == 200
    assert response_lower.json()["id"] == 1


def test_get_employee_not_found(client: TestClient) -> None:
    """GET /employees/Ravi -> 404 when employee does not exist."""
    response = client.get("/employees/Ravi")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_employee_invalid_salary(client: TestClient) -> None:
    """POST /employees with salary <= 0 (e.g. -5) -> 422 Unprocessable Entity."""
    payload = {"name": "Frank", "department": "Finance", "salary": -5}
    response = client.post("/employees", json=payload)
    assert response.status_code == 422

    # Verify zero salary is also rejected
    zero_payload = {"name": "Frank", "department": "Finance", "salary": 0}
    response_zero = client.post("/employees", json=zero_payload)
    assert response_zero.status_code == 422


def test_create_employee_empty_name(client: TestClient) -> None:
    """POST /employees with empty or whitespace-only name -> 422."""
    empty_payload = {"name": "", "department": "Sales", "salary": 55000.0}
    response_empty = client.post("/employees", json=empty_payload)
    assert response_empty.status_code == 422

    whitespace_payload = {"name": "   ", "department": "Sales", "salary": 55000.0}
    response_ws = client.post("/employees", json=whitespace_payload)
    assert response_ws.status_code == 422


def test_create_employee_success(client: TestClient) -> None:
    """POST /employees with valid payload -> 201 Created."""
    payload = {"name": "Grace", "department": "Security", "salary": 95000.0}
    response = client.post("/employees", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] == 6
    assert created["name"] == "Grace"
    assert created["salary"] == 95000.0

    # Verify record was persisted and can be retrieved
    get_res = client.get("/employees/Grace")
    assert get_res.status_code == 200
    assert get_res.json()["department"] == "Security"


def test_load_employees_missing_file(
    client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify load_employees returns empty list when file does not exist."""
    missing_file = tmp_path / "does_not_exist.json"
    monkeypatch.setattr(app_module, "DATA_FILE_PATH", missing_file)
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []
