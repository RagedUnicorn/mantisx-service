# Testing Documentation

This document describes the testing setup and framework for the MantisX Service project.

## Test Framework

The project uses **pytest** as the primary testing framework with the following additional packages:

- `pytest` - Core testing framework
- `pytest-cov` - Code coverage reporting
- `pytest-mock` - Enhanced mocking capabilities

## Test Structure

```
tests/
├── __init__.py
├── test_main.py          # Tests for main.py functions
├── test_models.py        # Tests for model classes
├── test_network.py       # Tests for network utilities
└── test_utils.py         # Tests for utility functions
```

## Running Tests

### From Command Line

1. **Run all tests:**

   ```bash
   python -m pytest tests/ -v
   ```

2. **Run with coverage:**

   ```bash
   python -m pytest tests/ --cov=. --cov-report=term-missing --cov-report=html -v
   ```

3. **Run specific test file:**

   ```bash
   python -m pytest tests/test_main.py -v
   ```

4. **Run using the test runner script:**
   ```bash
   python run_tests.py --type all --verbose
   ```

### From VS Code

#### Using Tasks (Ctrl+Shift+P → "Tasks: Run Task")

- **Run Tests** - Basic test execution
- **Run Tests with Coverage** - Tests with coverage report
- **Run Specific Test File** - Run tests for currently open file

#### Using Debug Configurations (F5 or Run and Debug panel)

- **Debug Tests** - Debug all tests
- **Debug Current Test File** - Debug tests in currently open file
- **Debug Tests with Coverage** - Debug tests with coverage reporting

## Test Configuration

Test configuration is defined in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=.",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-fail-under=50"
]
testpaths = ["tests"]
```

## Coverage Reports

- **Terminal**: Shows missing lines directly in terminal output
- **HTML**: Generated in `htmlcov/` directory, open `htmlcov/index.html` in browser
- **Target**: Currently set to 50% minimum coverage

## Writing New Tests

### Test File Naming

- Test files should be named `test_*.py`
- Test classes should be named `Test*`
- Test functions should be named `test_*`

### Example Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from your_module import function_to_test

class TestYourModule:
    """Test cases for your module"""

    def test_function_behavior(self):
        """Test normal function behavior"""
        result = function_to_test("input")
        assert result == "expected_output"

    @patch('your_module.external_dependency')
    def test_function_with_mock(self, mock_dependency):
        """Test function with mocked dependencies"""
        mock_dependency.return_value = "mocked_value"
        result = function_to_test("input")
        mock_dependency.assert_called_once_with("input")
        assert result == "expected_output"

    def test_function_edge_case(self):
        """Test edge cases and error conditions"""
        with pytest.raises(ValueError):
            function_to_test(None)
```

### Current Test Coverage Areas

1. **Main Functions** (`test_main.py`)

   - Argument parsing
   - Session data handling
   - File operations

2. **Models** (`test_models.py`)

   - Enum values and behavior
   - Data class functionality

3. **Utilities** (`test_utils.py`)

   - Session filtering logic
   - Helper functions

4. **Network** (`test_network.py`)
   - Network utility functions
   - Authentication mocking

## Adding More Tests

To expand test coverage, consider adding tests for:

1. **Integration Tests** - Test complete workflows
2. **Error Handling** - Test exception scenarios
3. **Edge Cases** - Test boundary conditions
4. **Performance Tests** - Test with large datasets
5. **API Response Parsing** - Test model parsing with real data

## Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.unit
def test_simple_function():
    """Unit test marker"""
    pass

@pytest.mark.integration
def test_full_workflow():
    """Integration test marker"""
    pass

@pytest.mark.slow
def test_time_consuming_operation():
    """Slow test marker"""
    pass
```

Run specific marker categories:

```bash
python -m pytest -m unit        # Run only unit tests
python -m pytest -m integration # Run only integration tests
python -m pytest -m "not slow"  # Skip slow tests
```
