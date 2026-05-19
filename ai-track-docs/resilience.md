# Resilience Notes

## Improvement

- Module: `samples/book-app-project/books.py`
- Path: `BookCollection.load_books()`
- Change: read-time `OSError` failures now fall back to an empty collection with a warning instead of crashing startup.

## Failure Scenarios Covered

- `PermissionError` while opening the data file
- Generic `OSError` while opening the data file

## Verification

Run from the repo root:

```bash
python -m pytest samples/book-app-project/tests/test_books.py -q
```

The failure tests confirm the app can still initialize with an empty collection when the data file cannot be read.