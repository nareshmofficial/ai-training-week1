# Employee Service Microservice

A production-ready FastAPI service for employee management featuring strict Pydantic v2 data validation, comprehensive pytest test suites with 80%+ test coverage, automated code formatting with Black and Ruff, and pre-commit Git hooks.

---

## Directory Structure

```
task4_fastapi_service/
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── .pre-commit-config.yaml   # Pre-commit hooks for Black and Ruff
├── pyproject.toml            # Black, Ruff, Pytest & Coverage configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration management
├── docs/
│   └── api_spec.md           # API specification
├── scripts/
│   ├── run_server.py         # Uvicorn launcher
│   └── seed_data.py          # Data seeding utility
├── src/
│   ├── __init__.py
│   ├── app.py                # FastAPI application & endpoints
│   ├── models.py             # Pydantic data models
│   └── data/
│       └── employees.json    # JSON data persistence
└── tests/
    ├── __init__.py
    └── test_api.py           # Pytest test suite
```

---

## Setup and Installation

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Set Up Pre-commit Hooks

```powershell
pre-commit install
pre-commit run --all-files
```

---

## Running the Application

Start the development server with hot-reload:

```powershell
python scripts/run_server.py
```

Or using uvicorn directly:

```powershell
uvicorn src.app:app --reload --port 8000
```

Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Running Tests and Coverage

Execute pytest with coverage analysis:

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

### Expected Test Results:
- `8 passed`
- `Coverage: 100%`

---

## Git Workflow & Branching

This repository follows standard feature branching:
```powershell
# 1. Switch to feature branch
git checkout -b feature/employee-service

# 2. Stage and commit changes in small steps
git add .
git commit -m "feat: implement FastAPI employee service with tests and linting"

# 3. Push and open Pull Request
git push -u origin feature/employee-service
```
