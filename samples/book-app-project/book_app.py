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
from utils import format_rating, show_books, PrintFunc

# Types for I/O hooks used for easier testing
InputFunc = Callable[[str], str]


class Stats(TypedDict, total=False):
    total: int
    read: int
    unread: int
    oldest: Optional[Book]
    newest: Optional[Book]


def parse_year(year_str: str) -> int:
    """Parse and validate a year string.

    Args:
        year_str: String representation of a year, or empty string for unknown.

    Returns:
        Parsed integer year, or 0 if year_str is empty.

    Raises:
        ValueError: If year_str is not an integer or falls outside 0–2100.
    """
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

    Args:
        collection: The BookCollection to search.
        title: The title string to search for.

    Returns:
        The first matching Book, or None if not found.
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

    Args:
        books: List of Book objects to analyse.

    Returns:
        A Stats TypedDict with total, read, unread, oldest, and newest entries.
        Books with year 0 (unknown) are excluded from oldest/newest calculations.
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
    """List all books in the collection.

    Args:
        collection: The BookCollection to list.
        print_func: Callable used for output; defaults to built-in print.
    """
    show_books(collection.list_books(), print_func=print_func)


def handle_add(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[str] = None,
) -> None:
    """Prompt the user to add a new book, or use provided values.

    Args:
        collection: The BookCollection to add to.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        title: Book title; prompts interactively if None.
        author: Book author; prompts interactively if None.
        year: Publication year string; prompts interactively if None.
    """
    print_func("\nAdd a New Book\n")

    # Normalise CLI-supplied values before validation
    if title is not None:
        title = title.strip()
    if author is not None:
        author = author.strip()
    if year is not None:
        year = year.strip()

    # Interactive prompts only if values aren't supplied
    if title is None:
        while True:
            title = input_func("Title: ").strip()
            if title:
                break
            print_func("Title cannot be empty. Please try again.")
    elif not title:
        print_func("\nTitle cannot be empty.")
        return

    if author is None:
        while True:
            author = input_func("Author: ").strip()
            if author:
                break
            print_func("Author cannot be empty. Please try again.")
    elif not author:
        print_func("\nAuthor cannot be empty.")
        return

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
    """Prompt the user to remove a book by title.

    Args:
        collection: The BookCollection to remove from.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        title: Book title to remove; prompts interactively if None.
    """
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
    """Find and display books by author name (substring match).

    Args:
        collection: The BookCollection to search.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        author: Author name to search for; prompts interactively if None.
    """
    print_func("\nFind Books by Author\n")

    if author is None:
        author = input_func("Author name: ").strip()

    if not author:
        print_func("\nAuthor name cannot be empty.")
        return

    books = collection.find_by_author(author)

    show_books(books, print_func=print_func)


def handle_stats(collection: BookCollection, print_func: PrintFunc = print) -> None:
    """Display statistics for the book collection.

    Args:
        collection: The BookCollection to summarise.
        print_func: Callable used for output; defaults to built-in print.
    """
    books = collection.list_books()
    stats = books_stats(books)

    print_func(f"\nTotal books: {stats.get('total', 0)}")
    print_func(f"Read: {stats.get('read', 0)}")
    print_func(f"Unread: {stats.get('unread', 0)}")

    oldest = stats.get("oldest")
    if oldest is not None:
        print_func(f"Oldest: {oldest.title} by {oldest.author} ({oldest.year})")
    else:
        print_func("Oldest: N/A")

    newest = stats.get("newest")
    if newest is not None:
        print_func(f"Newest: {newest.title} by {newest.author} ({newest.year})")
    else:
        print_func("Newest: N/A")


def handle_mark(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
) -> None:
    """Mark a book as read by title.

    Args:
        collection: The BookCollection to update.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        title: Book title to mark; prompts interactively if None.
    """
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


def handle_rate(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
    rating: Optional[str] = None,
) -> None:
    """Rate a book 1–5 stars with an optional review.

    Args:
        collection: The BookCollection to update.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        title: Book title to rate; prompts interactively if None.
        rating: Rating string (1–5); prompts interactively if None.
    """
    print_func("\nRate a Book\n")

    if title is None:
        title = input_func("Enter the title of the book to rate: ").strip()

    if not title:
        print_func("\nBook title cannot be empty.")
        return

    book = _find_book_fuzzy(collection, title)
    if not book:
        print_func(f"\nBook '{title}' not found.")
        return

    rating_int: int
    if rating is None:
        while True:
            rating_input = input_func("Enter rating (1-5): ").strip()
            try:
                rating_int = int(rating_input)
                if 1 <= rating_int <= 5:
                    break
                print_func("Rating must be between 1 and 5. Please try again.")
            except ValueError:
                print_func("Invalid input. Please enter a number between 1 and 5.")
    else:
        try:
            rating_int = int(rating)
            if not (1 <= rating_int <= 5):
                print_func("Error: Rating must be between 1 and 5.")
                return
        except ValueError:
            print_func("Invalid rating format.")
            return

    review: Optional[str] = None
    if rating is None:
        review = input_func("Enter a review (optional, press Enter to skip): ").strip()
        review = review if review else None

    try:
        collection.set_rating(book.title, rating_int, review)
        rating_display = format_rating(rating_int)
        print_func(f"\nBook '{book.title}' rated: {rating_display}")
        if review:
            print_func(f"Review: {review}")
    except ValueError as e:
        print_func(f"\nError: {e}")


def handle_year_range(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> None:
    """Find and display books published within a year range (inclusive).

    Args:
        collection: The BookCollection to search.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        start: Start year string; prompts interactively if None.
        end: End year string; prompts interactively if None.
    """
    print_func("\nFind Books by Year Range\n")

    if start is None:
        start = input_func("Start year: ").strip()
    if end is None:
        end = input_func("End year: ").strip()

    try:
        start_int = parse_year(start)
        end_int = parse_year(end)
        if start_int == 0 or end_int == 0:
            print_func("\nStart and end year are required.")
            return
        books = collection.list_by_year(start_int, end_int)
    except ValueError as exc:
        print_func(f"\nError: {exc}")
        return

    show_books(books, print_func=print_func)


def handle_view_review(
    collection: BookCollection,
    input_func: InputFunc = input,
    print_func: PrintFunc = print,
    title: Optional[str] = None,
) -> None:
    """Display the rating and review for a book.

    Args:
        collection: The BookCollection to query.
        input_func: Callable for reading user input; defaults to built-in input.
        print_func: Callable used for output; defaults to built-in print.
        title: Book title to view; prompts interactively if None.
    """
    print_func("\nView Book Review\n")

    if title is None:
        title = input_func("Enter the title of the book: ").strip()

    if not title:
        print_func("\nBook title cannot be empty.")
        return

    book = _find_book_fuzzy(collection, title)
    if not book:
        print_func(f"\nBook '{title}' not found.")
        return

    print_func(f"\n{book.title} by {book.author} ({book.year})")
    print_func("-" * 50)

    rating = getattr(book, "rating", None)
    if rating:
        rating_display = format_rating(rating)
        print_func(f"Rating: {rating_display} ({rating}/5)")
    else:
        print_func("Rating: Not rated")

    review = getattr(book, "review", None)
    if review:
        print_func(f"Review: {review}")
    else:
        print_func("Review: No review yet")


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser.

    Returns:
        Configured ArgumentParser with all subcommands registered.
    """
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

    rate_p = sub.add_parser("rate", help="Rate a book (1-5 stars)")
    rate_p.add_argument("--title", help="Book title (exact or substring)")
    rate_p.add_argument("--rating", help="Rating (1-5)")

    view_p = sub.add_parser("view-review", help="View a book's rating and review")
    view_p.add_argument("--title", help="Book title (exact or substring)")

    year_p = sub.add_parser("year-range", help="Find books published within a year range")
    year_p.add_argument("--start", help="Start year (inclusive)")
    year_p.add_argument("--end", help="End year (inclusive)")

    sub.add_parser("stats", help="Show collection statistics")

    return parser


# Command dispatcher mapping to improve maintainability
HandlerType = Callable[[BookCollection, argparse.Namespace], None]

_COMMAND_MAP: Dict[str, HandlerType] = {
    "list": lambda coll, _: handle_list(coll),
    "add": lambda coll, a: handle_add(coll, title=getattr(a, "title", None), author=getattr(a, "author", None), year=getattr(a, "year", None)),
    "remove": lambda coll, a: handle_remove(coll, title=getattr(a, "title", None)),
    "find": lambda coll, a: handle_find(coll, author=getattr(a, "author", None)),
    "mark": lambda coll, a: handle_mark(coll, title=getattr(a, "title", None)),
    "rate": lambda coll, a: handle_rate(coll, title=getattr(a, "title", None), rating=getattr(a, "rating", None)),
    "view-review": lambda coll, a: handle_view_review(coll, title=getattr(a, "title", None)),
    "year-range": lambda coll, a: handle_year_range(coll, start=getattr(a, "start", None), end=getattr(a, "end", None)),
    "stats": lambda coll, _: handle_stats(coll),
}


def main(argv: Optional[List[str]] = None, collection: Optional[BookCollection] = None) -> int:
    """Main entry point for the Book Collection CLI.

    Args:
        argv: Argument list; defaults to sys.argv[1:] if None.
        collection: BookCollection instance; creates a default one if None.

    Returns:
        Exit code: 0 on success, non-zero on failure.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args: argparse.Namespace = parser.parse_args(argv)

    # Configure default collection
    if collection is None:
        collection = BookCollection()

    # Dispatch commands
    cmd = args.command
    if not cmd:
        parser.print_help()
        return 0

    handler: Optional[HandlerType] = _COMMAND_MAP.get(cmd)
    if handler is None:
        logging.error("Unknown command: %s", cmd)
        parser.print_help()
        return 2

    # Call the handler with (collection, args)
    try:
        handler(collection, args)
    except Exception as exc:  # noqa: BLE001
        logging.error("Unexpected error: %s", exc, exc_info=True)
        print(f"An unexpected error occurred: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
