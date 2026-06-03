"""Utility helpers for the Book Collection CLI.

Provides simple IO helpers used by the sample CLI. All functions are
annotated for clearer typing and easier testing.
"""

from typing import Sequence, Tuple
from datetime import datetime


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details() -> Tuple[str, str, int]:
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    if not year_input:
        raise ValueError("Year is required.")

    try:
        year = int(year_input)
    except ValueError:
        raise ValueError("Year must be an integer.")

    current_year = datetime.utcnow().year
    if year < 0 or year > current_year:
        raise ValueError(f"Year must be between 0 and {current_year}.")

    return title, author, year


def print_books(books: Sequence['Book']) -> None:
    """Print a numbered list of books.

    The annotation uses a forward reference to a Book-like object. This keeps
    utils decoupled from the books module while still providing useful typing
    information for callers and linters.
    """
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if getattr(book, "read", False) else "📖 Unread"
        title = getattr(book, "title", "<unknown>")
        author = getattr(book, "author", "<unknown>")
        year = getattr(book, "year", "?")
        print(f"{index}. {title} by {author} ({year}) - {status}")


def print_help() -> None:
    """Print the help text for the book collection CLI."""
    print("Book Collection Helper\n")
    print("Commands:")
    print("  list         - Show all books")
    print("  list-unread  - Show only unread books")
    print("  add          - Add a new book")
    print("  remove       - Remove a book by title")
    print("  find         - Find books by author")
    print("  search       - Search books by title or author")
    print("  mark         - Mark a book as read")
    print("  help         - Show this help message")
