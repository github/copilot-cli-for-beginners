---
name: pytest-gen
description: Generate comprehensive pytest tests - use when generating tests, creating test suites, or testing Python code
---

# Pytest Generation Skill

When generating tests, follow this structure.

## Test Organization

- Group tests by function under test
- Use `@pytest.mark.parametrize` for multiple inputs
- Use fixtures for shared setup
- Follow arrange/act/assert pattern

## Coverage Requirements

- Happy path (expected usage)
- Edge cases (empty strings, None, boundary values)
- Error cases (invalid input, file not found, wrong types)
- Integration (functions working together)

## Template

```python
import pytest
from module_under_test import function_to_test


@pytest.fixture
def sample_data():
    """Provide shared test data."""
    return {"key": "value"}


class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self, sample_data):
        result = function_to_test(valid_input)
        assert result == expected_output

    def test_empty_input(self):
        result = function_to_test("")
        assert result == expected_for_empty

    @pytest.mark.parametrize("input_val,expected", [
        ("valid", True),
        ("", False),
        (None, False),
    ])
    def test_various_inputs(self, input_val, expected):
        assert function_to_test(input_val) == expected
```
