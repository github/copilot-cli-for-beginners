# Error Handling in the Book App

Good error handling helps the book app reject invalid input, protect saved data, and show useful messages without mixing user-interface code with book-management logic.

## Responsibilities

Keep responsibilities separate:

- `books.py` validates and manages book data.
- `utils.py` validates interactive input.
- `book_app.py` displays user-facing messages.

This makes the collection class easier to test and reuse from another interface.

## Validate Input Consistently

Validate values at public method boundaries, even when a command-line helper already validates them. Callers can also be tests or other Python modules.

Important checks include:

- Titles and authors must be non-empty strings after trimming whitespace.
- Publication years must be integers in the accepted range.
- Boolean values must not be accepted as publication years, because `bool` is a subclass of `int` in Python.
- Search and removal titles should be normalized consistently, for example with `strip()` and `casefold()`.

Do not silently convert invalid input to a placeholder such as `0`. Raise a clear `ValueError` instead:

```python
if not isinstance(year, int) or isinstance(year, bool):
    raise ValueError("Publication year must be an integer.")
```

## Use Clear Error Contracts

Use exceptions when an operation cannot complete normally:

```python
try:
    collection.add_book(title, author, year)
except ValueError as error:
    print(f"Error: {error}")
```

Use return values for expected results, such as whether a matching book exists:

```python
if collection.remove_book(title):
    print("Book removed successfully.")
else:
    print("No matching book was found.")
```

Keep this contract consistent. A recommended approach is:

- `find_book_by_title`: return `Book | None`.
- `add_book`: return the new `Book` or raise `ValueError`.
- `remove_book`: return `True` when removed and `False` when not found.
- Persistence and data-integrity failures: raise a clear exception.

## Keep User-Facing Messages in the CLI

The data layer should report errors through exceptions or return values, not print directly. Otherwise, a library caller cannot choose how to display or log the problem.

```python
def handle_remove():
    title = input("Enter the title of the book to remove: ").strip()

    try:
        removed = collection.remove_book(title)
    except ValueError as error:
        print(f"\nError: {error}\n")
        return

    if removed:
        print("\nBook removed successfully.\n")
    else:
        print("\nNo matching book was found.\n")
```

Only one layer should own the final user-facing result. Avoid printing `Book not found` from `books.py` while `book_app.py` also prints a generic removal message.

## Protect Corrupted Data

Malformed JSON should not silently become an empty collection. If the user later saves a new book, the original corrupted file could be overwritten and recoverable data lost.

A safer flow is:

1. Detect the parsing error.
2. Preserve the original file.
3. Report which configured file is invalid.
4. Let the application decide whether recovery is appropriate.

Include the configured path in diagnostics rather than hard-coding `data.json`:

```python
raise ValueError(
    f"{DATA_FILE} contains invalid JSON and was not changed."
) from error
```

## Validate Loaded Records

Valid JSON is not necessarily valid book data. Before creating `Book` instances, check that:

- The top-level value is a list.
- Each item is an object.
- Required fields are present.
- `title` and `author` are non-empty strings.
- `year` is an integer.
- `read` is a Boolean when present.

Build a temporary list and replace `self.books` only after every record validates. This prevents partially loaded collections.

## Handle Save Failures Safely

Methods such as `add_book()` and `mark_as_read()` should not leave memory changed when saving fails. Build and save the proposed state first, then update `self.books` only after persistence succeeds.

Wrap expected file-system failures with useful context while preserving the original cause:

```python
try:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
except OSError as error:
    raise OSError(f"Could not save books to {DATA_FILE}.") from error
```

Opening a file with `"w"` truncates it before writing. For stronger protection, write to a temporary file and replace the original only after the complete write succeeds.

## Consistent Diagnostics

Error messages should explain what failed and whether data changed:

```text
Error: Book title cannot be empty.
Error: Publication year must be an integer.
Error: data.json contains invalid JSON and was not changed.
Error: Could not save books to data.json.
No matching book was found.
```

Use consistent wording, punctuation, and routing. When wrapping an exception, use `raise ... from error` so debugging can still inspect the original cause.

## Tests to Add

Cover both successful operations and failure paths:

- Empty or whitespace-only titles and authors.
- Non-string titles or authors.
- Invalid, negative, or unrealistic years.
- Case-insensitive and whitespace-tolerant title searches.
- Missing books.
- Corrupted JSON.
- JSON with the wrong top-level type.
- Records with missing fields or incorrect types.
- Permission or other save failures.
- Confirmation that failed saves do not change the in-memory collection.

The main gotcha is that a valid JSON document can still contain invalid application data. Validate syntax and meaning separately.
