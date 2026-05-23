from collections.abc import Sequence
from datetime import date
from typing import Final, Literal, TypeAlias, cast

from books import Book


MenuChoice: TypeAlias = Literal["1", "2", "3", "4", "5"]
BookDetails: TypeAlias = tuple[str, str, int]

VALID_CHOICES: Final[set[MenuChoice]] = {"1", "2", "3", "4", "5"}
COMMAND_HELP_TEXT: Final[str] = """
Book Collection Helper

Commands:
  list       - Show all books
  list-unread - Show only unread books
  add        - Add a new book
  mark-read  - Mark a book as read
  remove     - Remove a book by title
  find       - Find books by author
  export-csv - Export all books to a CSV file
  help       - Show this help message
"""
MENU_TEXT: Final[str] = """
📚 Book Collection App
1. Add a book
2. List books
3. Mark book as read
4. Remove a book
5. Exit
"""


def format_menu() -> str:
    return MENU_TEXT


def display_menu() -> None:
    print(format_menu())


def print_menu() -> None:
    display_menu()


def format_help() -> str:
    return COMMAND_HELP_TEXT


def display_help() -> None:
    print(format_help())


def print_help() -> None:
    display_help()


def validate_user_choice(choice: str) -> str | None:
    if not choice:
        return "Choice cannot be empty. Please enter a number from 1 to 5."

    if not choice.isdigit():
        return "Invalid choice. Please enter a number from 1 to 5."

    if choice not in VALID_CHOICES:
        return "Choice must be between 1 and 5."

    return None


def get_user_choice() -> MenuChoice:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        error_message = validate_user_choice(choice)
        if error_message is not None:
            print(error_message)
            continue

        return cast(MenuChoice, choice)


def validate_title(title: str) -> str | None:
    if title:
        return None

    return "Title cannot be empty. Please enter a book title."


def current_calendar_year() -> int:
    return date.today().year


def parse_publication_year(year_input: str) -> tuple[int | None, str | None]:
    normalized_year = year_input.strip()
    if not normalized_year:
        return None, "Year cannot be empty. Please enter a publication year."

    try:
        year = int(normalized_year)
    except ValueError:
        return None, "Year must be a whole number."

    if year < 0:
        return None, "Year cannot be negative."

    max_year = current_calendar_year()
    if year > max_year:
        return None, f"Year cannot be in the future. Please enter a year up to {max_year}."

    return year, None


def get_book_details() -> BookDetails:
    """Prompt the user for book details and return them as a tuple.

    Parameters:
        None. The function reads all values interactively from standard input.

    Returns:
        tuple[str, str, int]: A tuple containing:
            - title: The non-empty book title entered by the user.
            - author: The author name entered by the user.
            - year: The publication year as an integer after validation.
    """
    while True:
        title = input("Enter book title: ").strip()
        error_message = validate_title(title)
        if error_message is None:
            break

        print(error_message)

    author = input("Enter author: ").strip()

    while True:
        year_input = input("Enter publication year: ").strip()
        year, error_message = parse_publication_year(year_input)
        if error_message is None and year is not None:
            break

        print(error_message)

    return title, author, year


def format_books(books: Sequence[Book]) -> str:
    """Build the book list display text in a consistent, user-friendly format."""
    if not books:
        return "No books found."

    book_lines = ["Your Book Collection:", ""]

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        book_lines.append(
            f"{index}. [{status}] {book.title} by {book.author} ({book.year})",
        )

    return "\n".join(book_lines)


def display_books(books: Sequence[Book]) -> None:
    print(format_books(books))


def print_books(books: Sequence[Book]) -> None:
    display_books(books)
