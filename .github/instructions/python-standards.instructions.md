---
applyTo: "**/*.py"
---

# Python Standards

These rules apply automatically whenever Copilot works on a Python file in
this project. They never load for other file types, so a conversation about a
Dockerfile or some JSON stays clutter-free.

## Style

- Follow PEP 8 style conventions.
- Add type hints to every function signature.
- Prefer f-strings over `%` formatting or `str.format()`.

## Error Handling

- Catch specific exceptions; never use a bare `except:`.
- Validate inputs at function boundaries and fail with a clear message.

## Testing

- Cover the happy path and edge cases (empty input, missing data).
