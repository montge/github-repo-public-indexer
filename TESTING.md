# Testing Guide

## Overview

This project maintains high test coverage to ensure reliability and catch regressions early.

**Coverage Requirements:**
- **Overall:** ≥ 95%
- **Individual modules:** ≥ 80%
- **Critical modules:** ≥ 90% (github_client, metadata_collector, json_generator)

## Quick Start

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests with coverage
pytest

# Run only unit tests
pytest tests/unit -m unit

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/unit/test_json_generator.py

# Run a specific test
pytest tests/unit/test_json_generator.py::TestJSONGenerator::test_init_default_version
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures and configuration
├── fixtures/             # Test data files
│   └── sample_*.json
├── unit/                 # Unit tests (fast, isolated)
│   ├── test_github_client.py
│   ├── test_metadata_collector.py
│   └── test_json_generator.py
├── integration/          # Integration tests (multiple components)
│   └── test_end_to_end.py
└── functional/           # Functional tests (CLI, full workflows)
    └── test_cli.py
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov=collect_repos

# Run specific test categories
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m functional    # Only functional tests

# Run tests in parallel (faster)
pytest -n auto          # Requires pytest-xdist
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src --cov=collect_repos --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux

# Generate XML report (for CI/CD)
pytest --cov=src --cov=collect_repos --cov-report=xml

# Show missing lines in terminal
pytest --cov=src --cov=collect_repos --cov-report=term-missing
```

### Strict Mode

Enforce coverage requirements:

```bash
# Fail if overall coverage < 95%
pytest --cov=src --cov=collect_repos --cov-fail-under=95

# This is the default in pytest.ini
```

## Writing Tests

### Test Naming Convention

- **Test files:** `test_<module_name>.py`
- **Test classes:** `Test<ClassName>`
- **Test functions:** `test_<functionality>_<expected_behavior>`

Example:
```python
def test_rate_limit_handling_waits_until_reset():
    """Test that rate limit handling waits until reset time."""
    pass
```

### Using Fixtures

Common fixtures are defined in `tests/conftest.py`:

```python
def test_generate_output_creates_file(tmp_path, sample_repo_data):
    """Test that generate_output creates a JSON file."""
    output_file = tmp_path / "output.json"
    generator = JSONGenerator()

    generator.generate_output(
        org_name="test-org",
        repositories=[sample_repo_data],
        output_file=str(output_file),
        backup_previous=False
    )

    assert output_file.exists()
```

**Available Fixtures:**
- `sample_repo_data` - Sample repository metadata
- `sample_metadata` - Sample JSON metadata section
- `mock_github_repo` - Mock GitHub repository object
- `mock_github_client` - Mock GitHub client
- `temp_json_file` - Temporary JSON file with sample data
- `fixtures_dir` - Path to fixtures directory
- `tmp_path` - Pytest built-in temporary directory

### Mocking External Dependencies

Always mock external dependencies (GitHub API, file system):

```python
@patch('src.github_client.Github')
def test_init_without_base_url(mock_github_class):
    """Test initialization without custom base URL."""
    mock_client = MagicMock()
    mock_github_class.return_value = mock_client

    # Setup mock behavior
    mock_user = MagicMock()
    mock_user.login = "test-user"
    mock_client.get_user.return_value = mock_user

    # Test
    client = GitHubClient(token="test_token")

    # Verify
    mock_github_class.assert_called_once_with("test_token")
```

### Parametrized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("include_forks,include_archived,expected_count", [
    (True, True, 10),
    (True, False, 8),
    (False, True, 7),
    (False, False, 5),
])
def test_get_all_repositories_with_filters(
    include_forks, include_archived, expected_count
):
    """Test repository filtering with different options."""
    # Test implementation
    pass
```

### Test Organization

Group related tests in classes:

```python
@pytest.mark.unit
class TestJSONGenerator:
    """Test cases for JSONGenerator class."""

    def test_init_default_version(self):
        """Test JSONGenerator initialization with default version."""
        generator = JSONGenerator()
        assert generator.tool_version == "0.1.0"

    def test_init_custom_version(self):
        """Test JSONGenerator initialization with custom version."""
        generator = JSONGenerator(tool_version="0.2.0")
        assert generator.tool_version == "0.2.0"
```

## Code Quality

### Linting

```bash
# Check code formatting (black)
black --check src tests collect_repos.py

# Auto-format code
black src tests collect_repos.py

# Run flake8
flake8 src tests collect_repos.py
```

### Type Checking

```bash
# Run mypy
mypy src collect_repos.py
```

## Continuous Integration

Tests run automatically on:
- Every push to `main` or `develop`
- Every pull request
- Weekly on Mondays at 9 AM UTC
- Manual workflow dispatch

See `.github/workflows/ci.yml` for details.

### CI Jobs

1. **Lint and Type Check** - Black, flake8, mypy
2. **Test Matrix** - Python 3.8, 3.9, 3.10, 3.11, 3.12
3. **Coverage Check** - Enforces 95% overall coverage
4. **Security Scan** - Safety and Bandit
5. **Build Validation** - Package build and validation

## Debugging Tests

### Run with verbose output

```bash
pytest -v -s  # -s shows print statements
```

### Run specific test with debugging

```bash
pytest tests/unit/test_json_generator.py::TestJSONGenerator::test_init_default_version -vv
```

### Use pytest's debugging

```python
def test_something():
    result = some_function()
    # Add breakpoint
    import pdb; pdb.set_trace()
    assert result == expected
```

Or use pytest's built-in debugger:

```bash
pytest --pdb  # Drop into debugger on failure
pytest --trace  # Drop into debugger at start of each test
```

## Test Coverage Best Practices

1. **Test edge cases** - Empty inputs, null values, boundary conditions
2. **Test error handling** - Exceptions, network errors, invalid data
3. **Mock external dependencies** - Never hit real APIs or file system
4. **Keep tests fast** - Unit tests should run in < 1 second
5. **One assertion per test** - Makes failures easier to diagnose
6. **Use descriptive names** - Test name should describe what's being tested
7. **Test behavior, not implementation** - Focus on inputs/outputs

## Common Issues

### ImportError in tests

Make sure pytest can find the source:

```bash
# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

Or install in development mode:

```bash
pip install -e .
```

### Coverage not reaching 95%

1. Check coverage report: `pytest --cov-report=html`
2. Open `htmlcov/index.html` in browser
3. Find uncovered lines (red)
4. Add tests for those lines

### Tests passing locally but failing in CI

- Check Python version differences
- Verify all dependencies are in requirements-dev.txt
- Check for environment-specific behavior
- Review CI logs carefully

## Contributing Tests

When adding new features:

1. Write tests first (TDD)
2. Ensure coverage stays ≥ 95%
3. Run full test suite: `pytest`
4. Run linters: `black`, `flake8`, `mypy`
5. Check coverage: `pytest --cov-report=term-missing`

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
