# Logging Notes

## Structured Logging Path

- Module: `samples/book-app-project/book_app.py`
- Path: `handle_add()`
- Fields: `op`, `status`, `elapsed_ms`

## Local Verification

Run from the repo root:

```bash
cd samples/book-app-project
python book_app.py add 2>&1
```

Then enter a title, author, and year. The command prints the user-facing message and emits a structured log line such as:

```text
op=add_book status=success elapsed_ms=0.123 year=2024
```

Validation failures emit the same core fields with a failure status, for example:

```text
op=add_book status=validation_error elapsed_ms=0.045 reason=empty_title
```

## Notes

- The log line is emitted through Python's standard `logging` module.
- `elapsed_ms` measures the CLI add flow from input collection through validation and save.