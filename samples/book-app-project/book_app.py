"""CLI for managing a small BookCollection sample app.

Improvements applied:
- argparse for structured CLI and better help
- dependency injection for BookCollection to improve testability
- handlers accept input/print callables to separate I/O from logic
- fuzzy, case-insensitive title matching for find/remove/mark
- improved books_stats using comprehensions and TypedDict
- explicit year parsing/validation and no bare excepts
- logging used for debug information
"""

import argparse
import logging
import sys
from typing import Callable, Dict, List, Optional, TypedDict

from books import Book, BookCollection

# Types for I/O hooks used for easier testing
InputFunc = Callable[[str], str]
PrintFunc = Callable[[str], None]


class Stats(TypedDict, total=False):
    total: int
    read: int
    unread: int
    oldest: Optional[Book]
    newest: Optional[Book]


def show_books(books: List[Book], print_func: PrintFunc = print) -> None:
    """Display books in a user-friendly format using print_func."""
    if not books:
        print_func("No books found.")
        return

    print_func("\nYour Book Collection:\n")
    for index, book in enumerate(books, start=1):
        status = "✓" if getattr(book, "read", False) else " "
        print_func(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")
    print_func("")


def parse_year(year_str: str) -> int:
    """Parse and validate a year string. Raises ValueError on invalid input."""
    if not year_str:
        return 0
    try:
        year = int(year_str)
    except ValueError:
        raise ValueError("Year must be an integer")
    if year < 0 or year > 2100:
        raise ValueError("Year must be between 0 and 2100")
    return year


def _find_book_fuzzy(collection: BookCollection, title: str) -> Optional[Book]:
    """Find a book by title using case-insensitive exact then substring matching.

    Returns the first matching Book or None.
    """
    if not title:
        return None

    title_lower = title.lower()
    books = collection.list_books()

    # Exact (case-insensitive) match
    for b in books:
        if b.title and b.title.lower() == title_lower:
            return b

    # Substring match
    for b in books:
        if b.title and title_lower in b.title.lower():
            return b

    return None


def books_stats(books: List[Book]) -> Stats:
    """Return statistics for a list of Book objects.

    Uses comprehensions and explicit handling of year parsing.
    """
    total = len(books)
    read_count = sum(1 for b in books if getattr(b, "read", False))
    unread_count = total - read_count

    # Collect (year, book) for books with valid, non-zero integer years
    year_book_pairs = []
    for b in books:
        y = getattr(b, "year", None)
        if y in (None, 0):
            continue
        try:
            y_int = int(y)
        except (TypeError, ValueError):
            continue
        if y_int == 0:
            continue
        year_book_pairs.append((y_int, b))

    oldest = min(year_book_pairs, key=lambda t: t[0])[1] if year_book_pairs else None
    newest = max(year_book_pairs, key=lambda t: t[0])[1] if year_book_pairs else None

    return Stats(total=total, read=read_count, unread=unread_count, oldest=oldest, newest=newest)


# Handler functions accept the collection and optional I/O hooks for testability
def handle_list(collection: BookCollection, print_func: PrintFunc = print) -> None:
    show_books(collection.list_books(), print_func=print_func)


def handle_add(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[str] = None,
) -> None:
    print_func("\nAdd a New Book\n")

    # Interactive prompts only if values aren't supplied
    if title is None:
        while True:
            title = input_func("Title: ").strip()
            if title:
                break
            print_func("Title cannot be empty. Please try again.")

    if author is None:
        while True:
            author = input_func("Author: ").strip()
            if author:
                break
            print_func("Author cannot be empty. Please try again.")

    if year is None:
        year = input_func("Year (optional): ").strip()

    try:
        year_int = parse_year(year)
        collection.add_book(title, author, year_int)
        print_func("\nBook added successfully.")
    except ValueError as exc:
        print_func(f"\nError: {exc}")


def handle_remove(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
) -> None:
    print_func("\nRemove a Book\n")

    if title is None:
        title = input_func("Enter the title of the book to remove: ").strip()

    if not title:
        print_func("\nBook title cannot be empty.")
        return

    book = _find_book_fuzzy(collection, title)
    if not book:
        print_func(f"\nBook '{title}' not found.")
        return

    confirm = input_func(f"Remove '{book.title}' by {book.author}? (y/n): ").strip().lower()
    if confirm == "y":
        # Remove by exact title stored in book object to avoid case issues
        collection.remove_book(book.title)
        print_func(f"\nBook '{book.title}' removed successfully.")
    else:
        print_func("\nRemoval cancelled.")


def handle_find(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    author: Optional[str] = None,
) -> None:
    print_func("\nFind Books by Author\n")

    if author is None:
        author = input_func("Author name: ").strip()

    if not author:
        print_func("\nAuthor name cannot be empty.")
        return

    # Prefer collection.find_by_author if present, but fall back to filtering
    try:
        books = collection.find_by_author(author)
    except Exception:
        # Fallback: case-insensitive substring match on author field
        author_lower = author.lower()
        books = [b for b in collection.list_books() if getattr(b, "author", "").lower().find(author_lower) != -1]

    show_books(books, print_func=print_func)


def handle_stats(collection: BookCollection, print_func: PrintFunc = print) -> None:
    books = collection.list_books()
    stats = books_stats(books)

    print_func(f"\nTotal books: {stats.get('total', 0)}")
    print_func(f"Read: {stats.get('read', 0)}")
    print_func(f"Unread: {stats.get('unread', 0)}")

    if stats.get("oldest"):
        b = stats["oldest"]
        print_func(f"Oldest: {b.title} by {b.author} ({b.year})")
    else:
        print_func("Oldest: N/A")

    if stats.get("newest"):
        b = stats["newest"]
        print_func(f"Newest: {b.title} by {b.author} ({b.year})")
    else:
        print_func("Newest: N/A")


def handle_mark(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
) -> None:
    print_func("\nMark a Book as Read\n")

    if title is None:
        title = input_func("Enter the title of the book to mark as read: ").strip()

    if not title:
        print_func("\nBook title cannot be empty.")
        return

    book = _find_book_fuzzy(collection, title)
    if not book:
        print_func(f"\nBook '{title}' not found.")
        return

    # Use stored title to mark the correct book
    success = collection.mark_as_read(book.title)
    if success:
        print_func(f"\nBook '{book.title}' marked as read.")
    else:
        print_func(f"\nFailed to mark '{book.title}' as read.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Book Collection Helper")
    sub = parser.add_subparsers(dest="command", required=False)

    sub.add_parser("list", help="Show all books")

    add_p = sub.add_parser("add", help="Add a new book")
    add_p.add_argument("--title", help="Book title")
    add_p.add_argument("--author", help="Book author")
    add_p.add_argument("--year", help="Publication year")

    rm_p = sub.add_parser("remove", help="Remove a book by title")
    rm_p.add_argument("--title", help="Title (exact or substring)")

    find_p = sub.add_parser("find", help="Find books by author")
    find_p.add_argument("--author", help="Author name (substring)")

    mark_p = sub.add_parser("mark", help="Mark a book as read by title")
    mark_p.add_argument("--title", help="Title (exact or substring)")

    sub.add_parser("stats", help="Show collection statistics")

    return parser


def main(argv: Optional[List[str]] = None, collection: Optional[BookCollection] = None) -> int:
    """Main entry point. Returns exit code (0 success, non-zero failure)."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    # Configure default collection
    if collection is None:
        collection = BookCollection()

    # Dispatch commands
    cmd = args.command
    if not cmd:
        parser.print_help()
        return 0

    if cmd == "list":
        handle_list(collection)
    elif cmd == "add":
        handle_add(collection, title=args.title, author=args.author, year=args.year)
    elif cmd == "remove":
        handle_remove(collection, title=args.title)
    elif cmd == "find":
        handle_find(collection, author=args.author)
    elif cmd == "mark":
        handle_mark(collection, title=args.title)
    elif cmd == "stats":
        handle_stats(collection)
    else:
        logging.error("Unknown command: %s", cmd)
        parser.print_help()
        return 2

    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
