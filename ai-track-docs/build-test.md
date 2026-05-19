# Build and Test

## Prerequisites

| Tool | Requirement | Status |
|------|-------------|--------|
| **Python** | 3.10 or higher | Required |
| **pip** | Package manager | Included with Python 3.10+ |
| **pytest** | Test framework | Listed in `pyproject.toml` |

Verify: `python --version` should show `Python 3.10.x` or higher.

## Build Commands

### Python (Primary Sample)

Navigate to the project:
```bash
cd samples/book-app-project
```

Install the project with dev dependencies:
```bash
pip install -e .
```

This installs the `book-app` package in editable mode and includes `pytest`.

## Test Commands

### Run the Local Validation Script
```bash
cd samples/book-app-project
python run_tests.py
```

This wraps the standard pytest command in a single cross-platform script for local validation.

### Run All Tests
```bash
cd samples/book-app-project
pytest tests/ -v
```

### Run Tests with Coverage Report
```bash
cd samples/book-app-project
pytest tests/ --cov=. --cov-report=term-missing
```

### Run a Specific Test File
```bash
cd samples/book-app-project
pytest tests/test_utils.py -v
```

### Run a Single Test
```bash
cd samples/book-app-project
pytest tests/test_utils.py::test_get_book_details_valid_year -v
```

## Local Development

1. **Clone and navigate:**
   ```bash
   git clone https://github.com/<your-username>/copilot-cli-for-beginners-mnf.git
   cd copilot-cli-for-beginners-mnf/samples/book-app-project
   ```

2. **Install in editable mode:**
   ```bash
   pip install -e .
   ```

3. **Run the app:**
   ```bash
   python book_app.py
   ```

4. **Run tests after changes:**
   ```bash
   pytest tests/ -v
   ```

## Verification (Exercise 2 Baseline)

After making changes, verify locally:
```bash
cd samples/book-app-project
python run_tests.py
```

Expected output: All tests pass (green checkmarks).

## Baseline Tests Added

- `test_utils.py` — Unit tests for utility functions
  - `test_get_book_details_valid_year()` — Verifies year parsing works correctly
  - `test_get_book_details_invalid_year()` — Verifies invalid years default to 0

## Walk Ex2 Coverage Baseline

Command used:

```bash
cd samples/book-app-project
python -m pytest tests --cov=. --cov-report=term
```

Latest observed summary:

- Tests: 22 passed
- TOTAL coverage: 79%
