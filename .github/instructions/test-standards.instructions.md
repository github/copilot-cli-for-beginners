---
applyTo: "**/test_*.py"
---

# Test Standards Instructions

Apply these conventions to all pytest test files in this project.

## File and Class Structure

- One test file per source module: `test_books.py` tests `books.py`, `test_utils.py` tests `utils.py`
- Group related tests into classes named `Test<Feature>` (e.g. `TestAddBook`, `TestBookValidation`)
- Separate class groups with a comment banner:

```python
# ---------------------------------------------------------------------------
# Adding books
# ---------------------------------------------------------------------------
class TestAddBook:
    ...
```

## Naming

- Test methods: `test_<what>_<condition>_<expected>` — be descriptive
  ```python
  # ✅ correct
  def test_add_book_empty_title_raises(self, collection):

  # ❌ too vague
  def test_add_book(self):
  ```
- Fixture names: short nouns describing what they return (`collection`, `populated_collection`, `bad_title`)

## Fixtures

- Define shared setup in fixtures, never repeat it inline across tests
- Use `autouse=True` only for global setup that every test needs (e.g. redirecting `DATA_FILE` to a temp path)
- Use `tmp_path` and `monkeypatch` (pytest builtins) for file I/O — never touch the real `data.json`:

```python
@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
```

- Give fixtures a one-line docstring describing what they return

## Assertions

- One logical assertion per test when possible
- Prefer `assert x == y` over `assertEqual`; use `is` for boolean and `None` checks:

```python
assert book.read is False
assert book.rating is None
```

- Use `pytest.raises` for exception tests — always in a `with` block:

```python
with pytest.raises(ValueError):
    collection.add_book("", "Author", 2000)
```

## Parametrize

- Use `@pytest.mark.parametrize` for testing multiple equivalent inputs — do not copy-paste test bodies:

```python
@pytest.mark.parametrize("bad_title", ["", "   ", 123, None])
def test_invalid_title_raises(self, bad_title):
    with pytest.raises((ValueError, TypeError)):
        Book(title=bad_title, author="Author", year=2000)
```

## What to Test

Every feature should have at minimum:
- **Happy path**: valid input produces the expected result
- **Edge cases**: boundary values, empty collections, `None` inputs
- **Error cases**: invalid input raises the correct exception

## Running Tests

```bash
python -m pytest tests/
python -m pytest tests/ -v   # verbose
```
