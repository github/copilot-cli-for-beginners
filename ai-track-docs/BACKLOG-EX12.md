# Backlog Items

## 1. Move test-only dependency out of runtime dependencies

- Code link: `samples/book-app-project/pyproject.toml`
- Problem: `pytest` is still declared in the main dependency list even though it is only needed for validation.
- Acceptance criteria:
  - Test tooling is separated from runtime dependencies.
  - The local validation flow still works for contributors.
  - Dependency notes are updated to reflect the new layout.

## 2. Add structured logs to remove and find flows

- Code link: `samples/book-app-project/book_app.py`
- Problem: only the add flow emits structured logs today, so operator visibility is inconsistent.
- Acceptance criteria:
  - `handle_remove()` emits `op`, `status`, and `elapsed_ms`.
  - `handle_find()` emits `op`, `status`, and `elapsed_ms`.
  - Tests verify at least one success and one failure-style log path.

## 3. Add a safe data file configuration override

- Code link: `samples/book-app-project/books.py`
- Problem: the data file path is fixed to `data.json`, which makes local experimentation less flexible.
- Acceptance criteria:
  - The app can load a data file path from a safe environment variable or CLI option.
  - The default behavior stays unchanged when no override is provided.
  - Tests cover the override path.

## 4. Add coverage guidance to the local test script

- Code link: `samples/book-app-project/run_tests.py`
- Problem: the local script provides a pass/fail signal but no optional path for collecting coverage evidence.
- Acceptance criteria:
  - The script supports a simple coverage mode.
  - Documentation explains when to use the normal mode versus coverage mode.
  - The script exits non-zero when the underlying test command fails.

## 5. Consolidate CLI input validation rules

- Code link: `samples/book-app-project/book_app.py`
- Problem: the CLI layer and collection layer both enforce parts of the add-book validation flow.
- Acceptance criteria:
  - Validation rules are defined in one clear owning layer or helper.
  - User-facing error messages remain beginner-friendly.
  - Existing tests continue to pass and one new regression test is added.