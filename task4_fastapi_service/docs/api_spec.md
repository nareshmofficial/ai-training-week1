# Employee Service API Specification

This microservice provides REST endpoints to inspect and manage employee records.

---

## Base URL

`http://localhost:8000`

Interactive Swagger documentation is accessible at `/docs` and ReDoc at `/redoc`.

---

## Endpoints

### 1. Health Check
- **Path**: `GET /health`
- **Response**: `200 OK`
  ```json
  {"status": "ok"}
  ```

### 2. List Employees
- **Path**: `GET /employees`
- **Response**: `200 OK`
  ```json
  [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 75000.0},
    {"id": 2, "name": "Bob", "department": "Marketing", "salary": 45000.0}
  ]
  ```

### 3. Get Employee By Name
- **Path**: `GET /employees/{name}`
- **Parameters**: `name` (case-insensitive string)
- **Response**:
  - `200 OK`: Employee object
  - `404 Not Found`:
    ```json
    {"detail": "Employee 'Ravi' not found"}
    ```

### 4. Create Employee
- **Path**: `POST /employees`
- **Request Body**:
  ```json
  {
    "name": "Grace",
    "department": "Security",
    "salary": 95000.0
  }
  ```
- **Validation**:
  - `name`: Must not be empty or whitespace only (`min_length=1`).
  - `salary`: Must be strictly greater than 0 (`gt=0`).
- **Response**:
  - `201 Created`: Returns newly created employee with auto-assigned `id`.
  - `422 Unprocessable Entity`: If `salary <= 0` or `name` is empty.
