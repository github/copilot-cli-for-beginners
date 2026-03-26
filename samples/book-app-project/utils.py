from __future__ import annotations

from books import Book, BookValidationError


# --- Display Functions (output only) ---


def print_menu() -> None:
    """Display the interactive menu options.

    Used for the interactive menu mode (alternative to CLI arguments).
    """
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Search by year range")
    print("6. Exit")


def print_books(books: list[Book]) -> None:
    """Display a list of books in a formatted output with read status."""
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")


def show_help() -> None:
    """Display available CLI commands."""
    print("""
Book Collection Helper

Commands:
  list         - Show all books
  add          - Add a new book
  remove       - Remove a book by title
  find         - Find books by author
  find-title   - Find a book by title
  mark-read    - Mark a book as read
  search-year  - Search books by year range
  help         - Show this help message
""")


def print_error(message: str) -> None:
    """Display an error message in a consistent format."""
    print(f"\nError: {message}\n")


def print_success(message: str) -> None:
    """Display a success message in a consistent format."""
    print(f"\n{message}\n")


# --- Validation Functions (pure logic, no I/O) ---


def validate_non_empty(value: str, field_name: str) -> None:
    """Check that a string is non-empty after stripping whitespace.

    Raises:
        BookValidationError: If the value is empty or whitespace-only.
    """
    if not value.strip():
        raise BookValidationError(f"{field_name} cannot be empty")


def validate_year_input(year_str: str) -> int:
    """Parse and validate a year string.

    Returns:
        The parsed year as an integer.

    Raises:
        BookValidationError: If the year string is invalid.
    """
    if not year_str.strip():
        raise BookValidationError("Year cannot be empty")
    try:
        year = int(year_str)
    except ValueError:
        raise BookValidationError(f"Invalid year: '{year_str}'. Please enter a number")
    if year < 0:
        raise BookValidationError("Year cannot be negative")
    return year


def validate_menu_choice(choice: str) -> None:
    """Validate a menu choice is a digit between 1-6.

    Raises:
        BookValidationError: If the choice is invalid.
    """
    if not choice:
        raise BookValidationError("Input cannot be empty. Please enter a number between 1 and 6.")
    if not choice.isdigit() or not 1 <= int(choice) <= 6:
        raise BookValidationError(f"Invalid choice: '{choice}'. Please enter a number between 1 and 6.")


# --- Input Functions (combine validation + display) ---


def get_user_choice() -> str:
    """Prompt the user to select a menu option (1-6) with validation.

    Used for the interactive menu mode (alternative to CLI arguments).

    Returns:
        A string representing the user's valid choice ('1' through '6').
    """
    while True:
        choice = input("Choose an option (1-6): ").strip()
        try:
            validate_menu_choice(choice)
        except BookValidationError as e:
            print(str(e))
            continue
        return choice


def get_book_details() -> tuple[str, str, int]:
    """Interactively prompt the user for book details with input validation.

    Re-prompts until valid input is provided for each field.

    Returns:
        tuple[str, str, int]: A tuple of (title, author, year).
    """
    while True:
        title = input("Enter book title: ").strip()
        try:
            validate_non_empty(title, "Title")
        except BookValidationError as e:
            print(f"{e}. Please enter a title.")
            continue
        break

    while True:
        author = input("Enter author: ").strip()
        try:
            validate_non_empty(author, "Author")
        except BookValidationError as e:
            print(f"{e}. Please enter an author.")
            continue
        break

    while True:
        year_input = input("Enter publication year: ").strip()
        try:
            year = validate_year_input(year_input)
        except BookValidationError as e:
            print(f"{e}. Please enter a valid year.")
            continue
        break

    return title, author, year
