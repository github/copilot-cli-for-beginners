from typing import List, Tuple

from books import Book, BookStats
from exceptions import ValidationError

# ---------------------------------------------------------------------------
# Data processing: pure functions with no I/O, easy to unit test.
# ---------------------------------------------------------------------------


def is_valid_menu_choice(choice: str) -> bool:
    """Return True if `choice` is a digit string within the menu range 1-5."""
    return choice.isdigit() and 1 <= int(choice) <= 5


def parse_year(year_input: str) -> int:
    """Parse a publication year string.

    Raises:
        ValidationError: If `year_input` is not a valid integer.
    """
    try:
        return int(year_input)
    except ValueError as e:
        raise ValidationError(f"'{year_input}' is not a valid year.") from e


def format_book_line(index: int, book: Book) -> str:
    """Build the display line for a single book."""
    status = "✅ Read" if book.read else "📖 Unread"
    return f"{index}. {book.title} by {book.author} ({book.year}) - {status}"


def format_books(books: List[Book]) -> List[str]:
    """Build the display lines for a list of books."""
    if not books:
        return ["No books in your collection."]

    lines = ["\nYour Books:"]
    lines.extend(format_book_line(index, book) for index, book in enumerate(books, start=1))
    return lines


def format_stats(stats: BookStats) -> List[str]:
    """Build the display lines for collection statistics."""
    lines = [
        f"Total books: {stats['total']}",
        f"Read: {stats['read']}",
        f"Unread: {stats['unread']}",
    ]

    if stats["oldest"]:
        lines.append(f"Oldest: {stats['oldest'].title} ({stats['oldest'].year})")
    if stats["newest"]:
        lines.append(f"Newest: {stats['newest'].title} ({stats['newest'].year})")

    return lines


# ---------------------------------------------------------------------------
# Display: printing and interactive input. Delegates parsing/validation to
# the pure functions above.
# ---------------------------------------------------------------------------


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()

        if not choice:
            print("Input cannot be empty. Please enter a number from 1 to 5.")
            continue

        if not is_valid_menu_choice(choice):
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        return choice


def get_book_details() -> Tuple[str, str, int]:
    """Prompt the user for details of a new book.

    Interactively collects a book's title, author, and publication year
    via `input()`. The title is required and the user is re-prompted
    until a non-empty value is entered. The publication year is parsed
    as an integer; if the input is not a valid number, it defaults to 0
    and a warning is printed.

    Parameters:
        None. All values are gathered interactively from stdin.

    Returns:
        tuple[str, str, int]: A 3-tuple containing:
            - title (str): The book's title. Guaranteed non-empty.
            - author (str): The book's author. May be an empty string
              if the user provides no input.
            - year (int): The publication year, or 0 if the entered
              value could not be parsed as an integer.
    """
    title = ""
    while not title:
        title = input("Enter book title: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a book title.")

    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = parse_year(year_input)
    except ValidationError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books: List[Book]) -> None:
    for line in format_books(books):
        print(line)


def print_stats(stats: BookStats) -> None:
    """Print formatted book collection statistics."""
    for line in format_stats(stats):
        print(line)
    print()
