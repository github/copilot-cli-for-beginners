# Extending the Utils Module

## Overview

The `utils.py` module contains user interface helpers for the book collection app. It handles:
- Menu display and user input collection
- Input validation and parsing
- Formatted output display

## Adding New Input Functions

### Pattern: Input Collection + Validation

```python
def get_new_field():
    """Collect and validate a new field from user input."""
    while True:  # Loop until valid input
        value = input("Enter field: ").strip()
        if validate_field(value):  # Add your validation logic
            return value
        print("Invalid input. Please try again.")
```

### Example: Adding Genre Input

```python
def get_book_genre():
    """Collect book genre from user input."""
    genres = ["Fiction", "Non-Fiction", "Biography", "Science Fiction"]
    while True:
        print("Available genres:")
        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre}")

        choice = input("Choose genre (1-4): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(genres):
                return genres[index]
        except ValueError:
            pass
        print("Invalid choice. Please select 1-4.")
```

## Adding New Display Functions

### Pattern: Conditional Formatting

```python
def print_custom_list(items, formatter_func):
    """Display items using a custom formatter function."""
    if not items:
        print("No items to display.")
        return

    print("\nItems:")
    for index, item in enumerate(items, start=1):
        formatted = formatter_func(item)
        print(f"{index}. {formatted}")
```

### Example: Adding Book Summary Display

```python
def print_book_summaries(books):
    """Display books with brief summaries."""
    if not books:
        print("No books in your collection.")
        return

    print("\nBook Summaries:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        summary = f"{book.title[:30]}..." if len(book.title) > 30 else book.title
        print(f"{index}. {summary} by {book.author} - {status}")
```

## Testing New Functions

### Pattern: Mock User Input

```python
def test_new_function(monkeypatch):
    """Test new input function with mocked user input."""
    inputs = iter(["test input", "another value"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = your_new_function()
    assert result == expected_value
```

### Example: Testing Genre Input

```python
def test_get_book_genre(monkeypatch):
    """Test get_book_genre with mocked input."""
    inputs = iter(["1"])  # User selects first genre
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = utils.get_book_genre()
    assert result == "Fiction"
```

## Best Practices

1. **Input Validation**: Always validate user input and provide clear error messages
2. **Consistent Formatting**: Use consistent emojis and formatting in display functions
3. **Modular Functions**: Keep functions focused on single responsibilities
4. **Error Handling**: Use try/except blocks for parsing operations
5. **Testing**: Mock `input()` calls in tests to avoid interactive prompts

## Integration Points

- Functions in `utils.py` are called by `book_app.py` for user interaction
- Display functions receive Book objects from the `books.py` module
- Input functions return validated data to the main application logic</content>
<parameter name="filePath">c:\crawl-walk-run\copilot-cli-for-beginners-mnf\ai-track-docs\extending-utils.md