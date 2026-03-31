import sys
from typing import List
from books import BookCollection, Book


# Global collection instance
collection = BookCollection()


def show_books(books: List[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list() -> None:
    """Display all books in the collection."""
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    while True:
        title = input("Title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please try again.")

    while True:
        author = input("Author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please try again.")

    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        if year < 0 or year > 2100:
            print("\nError: Year should be between 0 and 2100.")
            return
        collection.add_book(title, author, year)
        print("\nBook added successfully.")
    except ValueError as e:
        print(f"\nError: {e}")


def handle_remove() -> None:
    """Prompt user to remove a book by title from the collection."""
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nBook title cannot be empty.")
        return

    book = collection.find_book_by_title(title)
    if not book:
        print(f"\nBook '{title}' not found.")
        return

    confirm = input(f"Remove '{book.title}' by {book.author}? (y/n): ").strip().lower()
    if confirm == 'y':
        collection.remove_book(title)
        print(f"\nBook '{title}' removed successfully.")
    else:
        print("\nRemoval cancelled.")


def handle_find() -> None:
    """Prompt user to find books by author name."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("\nAuthor name cannot be empty.")
        return
    books = collection.find_by_author(author)

    show_books(books)


def show_help() -> None:
    """Display help message with available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  stats    - Show collection statistics (total, read/unread, oldest/newest)
  help     - Show this help message
""")


def books_stats(books: List[Book]) -> dict:
    """Return statistics for a list of Book objects.

    Returns a dict with keys: total, read, unread, oldest, newest
    Oldest/newest are Book instances or None.
    """
    total = len(books)
    read_count = sum(1 for b in books if getattr(b, "read", False))
    unread_count = total - read_count

    # Collect books with a valid year (non-zero, non-None)
    year_pairs = []  # list of (year, book)
    for b in books:
        y = getattr(b, "year", None)
        try:
            if y is None:
                continue
            y_int = int(y)
        except Exception:
            continue
        if y_int == 0:
            continue
        year_pairs.append((y_int, b))

    oldest = min(year_pairs, key=lambda t: t[0])[1] if year_pairs else None
    newest = max(year_pairs, key=lambda t: t[0])[1] if year_pairs else None

    return {
        "total": total,
        "read": read_count,
        "unread": unread_count,
        "oldest": oldest,
        "newest": newest,
    }


def handle_stats() -> None:
    """Display collection statistics on the command line."""
    books = collection.list_books()
    stats = books_stats(books)

    print(f"\nTotal books: {stats['total']}")
    print(f"Read: {stats['read']}")
    print(f"Unread: {stats['unread']}")

    if stats["oldest"]:
        b = stats["oldest"]
        print(f"Oldest: {b.title} by {b.author} ({b.year})")
    else:
        print("Oldest: N/A")

    if stats["newest"]:
        b = stats["newest"]
        print(f"Newest: {b.title} by {b.author} ({b.year})")
    else:
        print("Newest: N/A")


def main() -> None:
    """Main entry point for the CLI application."""
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
    elif command == "stats":
        handle_stats()
    elif command == "help":
        show_help()
    else:
        print("\nUnknown command.")
        show_help()


if __name__ == "__main__":
    main()
