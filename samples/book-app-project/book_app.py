import logging
import os
import sys
import time
from books import BookCollection


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("book_app")


# Global collection instance
collection = BookCollection()


def log_operation(op, status, started_at, **fields):
    elapsed_ms = (time.perf_counter() - started_at) * 1000
    parts = [f"op={op}", f"status={status}", f"elapsed_ms={elapsed_ms:.3f}"]
    parts.extend(f"{key}={value}" for key, value in fields.items())
    logger.info(" ".join(parts))


def should_show_year() -> bool:
    return os.getenv("BOOK_APP_SHOW_YEAR", "1").lower() not in {"0", "false", "off", "no"}


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        year_suffix = f" ({book.year})" if should_show_year() else ""
        print(f"{index}. [{status}] {book.title} by {book.author}{year_suffix}")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")
    started_at = time.perf_counter()

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    # Input validation
    if not title:
        log_operation("add_book", "validation_error", started_at, reason="empty_title")
        print("\nError: Title cannot be empty.\n")
        return
    if not author:
        log_operation("add_book", "validation_error", started_at, reason="empty_author")
        print("\nError: Author cannot be empty.\n")
        return
    try:
        year = int(year_str) if year_str else 0
        if year < 0 or year > 9999:
            raise ValueError("Year must be between 0 and 9999.")
        collection.add_book(title, author, year)
        log_operation("add_book", "success", started_at, year=year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        log_operation("add_book", "validation_error", started_at, reason="invalid_year")
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
