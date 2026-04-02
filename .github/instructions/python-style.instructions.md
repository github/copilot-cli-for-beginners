---
applyTo: "**/*.py"
---

# Python Style Instructions

Apply these conventions to all Python code in this project.

## PEP 8

- Use 4 spaces for indentation — never tabs
- Limit lines to 88 characters (Black-compatible)
- Two blank lines between top-level definitions (classes, functions)
- One blank line between methods inside a class
- Use `snake_case` for variables, functions, and module names
- Use `PascalCase` for class names
- Use `UPPER_SNAKE_CASE` for module-level constants
- No trailing whitespace; files must end with a single newline

## Type Hints

All functions and methods must have type hints on every parameter and the return value:

```python
# ✅ correct
def add_book(self, title: str, author: str, year: int) -> Book:

# ❌ wrong — missing hints
def add_book(self, title, author, year):
```

- Use `Optional[X]` (or `X | None` in Python 3.10+) for values that may be `None`
- Use `List[X]`, `Dict[K, V]`, `Tuple[X, ...]` from `typing` for Python < 3.9; use built-in `list[X]` etc. for 3.9+
- Never use bare `Any` unless there is no alternative — add a comment explaining why

## Docstrings

Use Google-style docstrings on all public classes, methods, and functions:

```python
def find_by_author(self, author: str) -> List[Book]:
    """Find all books whose author field contains the given string (case-insensitive).

    Args:
        author: The author name or substring to search for.

    Returns:
        List of matching Book objects; empty list if none found.
    """
```

Rules:
- First line: short imperative sentence ending with a period
- Blank line between the summary and `Args` / `Returns` / `Raises`
- Omit sections that don't apply (e.g. no `Returns` for `-> None`)
- Private methods (prefixed `_`) do not need docstrings unless the logic is non-obvious

## Imports

- Standard library imports first, then third-party, then local — separated by blank lines
- No wildcard imports (`from module import *`)
- Remove unused imports

## Error Handling

- Use `ValueError` for invalid input and validation failures
- Use `IOError` / `OSError` for file system operations
- Always name caught exceptions `exc` (not `e`, `err`, or `error`)
- Never use bare `except:` — always catch a specific type
- In library code, re-raise after logging; never silently swallow exceptions
