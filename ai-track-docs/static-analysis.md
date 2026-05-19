# Static Analysis Notes

## Current State

- No dedicated lint or static-analysis tool is configured in the repository for the primary Python sample.
- There is no checked-in configuration for tools such as `ruff`, `flake8`, `pylint`, `mypy`, or `pyright`.
- The current low-friction validation path relies on running the sample test suite.

## Local Checks You Can Run Today

Primary sample validation:

```bash
cd samples/book-app-project
python run_tests.py
```

Focused test file:

```bash
cd samples/book-app-project
python -m pytest tests/test_books.py -q
```

## Why This Is Documented Instead of Tightened

- The Crawl track emphasizes small, reversible changes.
- Adding a brand-new linter would widen scope beyond the chosen module and likely require repo-wide cleanup.
- The safer exercise artifact is a clear note describing the current checks and the gap.

## Next Upgrade Options

- Add `ruff` for Python style and import hygiene.
- Add `mypy` or `pyright` if the sample moves toward stronger type checking.
- Keep any future rollout scoped to `samples/book-app-project/` first.