# Testing Standards for this FastAPI Project

## Overview
This document outlines the testing standards for the FastAPI project, emphasizing the use of pytest as the testing framework. All tests must adhere to these guidelines to ensure consistency, maintainability, and high code quality.

## Directory Structure
- All tests must be placed in the `tests/` directory.
- Separate `unit/` and `integration/` subdirectories under `tests/` for clear organization.
- Use `conftest.py` in the root `tests/` directory for shared fixtures (e.g., `app`, `client`, `db_session`, `auth_token`).
- Additional `conftest.py` files can be added in subdirectories if needed for scoped fixtures.

## Naming Conventions
- **Test files**: `test_<module>.py` (e.g., `app/main.py` → `tests/unit/test_main.py` or `tests/integration/test_main.py`).
- **Test functions**: `def test_<target>_<expected_behavior>()` (e.g., `test_create_task_returns_201`).
- **Test classes**: `class Test<Module>()` if grouping related tests (e.g., `class TestTaskEndpoints`).
- **Fixture names**: Use descriptive, lowercase names (e.g., `authenticated_client`, `sample_task_data`).
- **Mark names**: Use `@pytest.mark.<category>` for categorization (e.g., `@pytest.mark.integration`, `@pytest.mark.slow`).

## Pytest Framework Usage
- Use `pytest` as the primary testing framework.
- Leverage pytest's built-in features: fixtures, parametrization, marks, and plugins.
- Run tests with `uv run pytest` to respect the project's dependency management.
- Use `pytest-asyncio` for testing async functions (already configured).

## Unit Testing Guidelines
- Test individual functions, classes, or methods in isolation.
- Mock external dependencies using `pytest-mock` or `unittest.mock`.
- Use `pytest.raises` for testing exceptions.
- Focus on logic, edge cases, and error handling.
- Example:
  ```python
  def test_calculate_completion_rate_with_no_tasks():
      # Arrange
      tasks = []
      
      # Act & Assert
      with pytest.raises(ZeroDivisionError):
          calculate_completion_rate(tasks)
  ```

## Integration Testing Guidelines
- Test end-to-end functionality, including API endpoints.
- Use `httpx.AsyncClient` for making HTTP requests to the FastAPI app.
- Mark integration tests with `@pytest.mark.integration`.
- Test status codes, response JSON, headers, and database state changes.
- Example:
  ```python
  @pytest.mark.asyncio
  @pytest.mark.integration
  async def test_get_productivity_report_returns_200(authenticated_client):
      response = await authenticated_client.get("/productivity/report")
      assert response.status_code == 200
      data = response.json()
      assert "total_tasks" in data
      assert "completion_rate" in data
  ```

## API Testing Requirements
- Cover all CRUD operations for each endpoint.
- Test happy paths, validation errors, authentication failures, and edge cases.
- Validate responses against Pydantic models from `app/models.py`.
- Ensure async endpoints are properly awaited.
- Test rate limiting, authentication, and authorization.

## Fixtures and Test Data
- Define reusable fixtures in `tests/conftest.py`:
  - `app`: FastAPI application instance
  - `client`: `httpx.AsyncClient` for integration tests
  - `db_session`: Database session for tests requiring data persistence
  - `auth_token`: Valid authentication token
  - `authenticated_client`: Client with authentication headers
- Use factories or builders for complex test data (e.g., `TaskFactory`).
- Ensure fixtures are async-compatible where needed.

## Advanced Pytest Features
- **Parametrization**: Use `@pytest.mark.parametrize` for testing multiple inputs.
  ```python
  @pytest.mark.parametrize("input_value,expected", [
      (0, 0),
      (5, 25),
      (10, 100),
  ])
  def test_square_function(input_value, expected):
      assert square(input_value) == expected
  ```
- **Mocking**: Use `mocker` fixture for patching functions or objects.
- **Marks**: Use marks for test categorization and selective running (e.g., `pytest -m integration`).
- **Fixtures**: Leverage fixture scoping (`function`, `class`, `module`, `session`).

## Coverage and Quality
- Run coverage with `uv run pytest --cov=app --cov-report=html tests/`.
- Aim for 85%+ coverage on new or modified code.
- Use `pytest-cov` for coverage reporting.
- Ensure tests are fast; mark slow tests with `@pytest.mark.slow`.

## Running Tests
- All tests: `uv run pytest`
- Unit tests only: `uv run pytest tests/unit/`
- Integration tests only: `uv run pytest -m integration`
- With coverage: `uv run pytest --cov=app tests/`
- Specific test: `uv run pytest tests/unit/test_main.py::test_specific_function`

## Agent Behavior Rules
- When generating tests, strictly follow these naming conventions and directory structure.
- Always place test files under `tests/` and respect the unit/integration separation.
- Include comprehensive test cases: happy path, validation, error conditions, and type checking.
- Use appropriate fixtures and marks.
- Ensure tests are async when testing async code.
- Validate API responses against Pydantic models.

## Best Practices
- Write descriptive test names that explain what is being tested.
- Keep tests independent and isolated.
- Use assertions that provide clear failure messages.
- Avoid testing implementation details; focus on behavior.
- Regularly run the full test suite to catch regressions.

## Summary
Follow pytest conventions, maintain clear separation between unit and integration tests, use fixtures effectively, and ensure comprehensive coverage of API endpoints with proper validation against Pydantic models. All tests must be placed in the `tests/` directory and adhere to the specified naming conventions.
