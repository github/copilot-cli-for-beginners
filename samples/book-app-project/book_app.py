import sys
import datetime
from books import Book, BookCollection
from utils import get_collection_stats


# Global collection instance
collection = BookCollection()


def show_books(books: list[Book]) -> None:
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
    """List all books in the collection."""
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    """Prompt the user for book details and add it to the collection."""
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    author = input("Author: ").strip()
    if not author:
        print("\nError: Author cannot be empty.\n")
        return

    year_str = input("Year: ").strip()
    current_year = datetime.date.today().year

    try:
        if not year_str:
            print("\nError: Year is required.\n")
            return
        year = int(year_str)
        if not (1000 <= year <= current_year):
            print(f"\nError: Year must be between 1000 and {current_year}.\n")
            return
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError:
        print("\nError: Year must be a number.\n")


def handle_remove() -> None:
    """Prompt the user for a title and remove the matching book."""
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    if collection.remove_book(title):
        print(f'\n✓ "{title}" was removed from your collection.\n')
    else:
        print(f'\nNo book with the title "{title}" was found.\n')


def handle_find() -> None:
    """Prompt the user for an author name and display matching books."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("\nError: Author name cannot be empty.\n")
        return

    books = collection.find_by_author(author)
    show_books(books)


def handle_mark_read() -> None:
    """Prompt the user for a title and mark the matching book as read."""
    print("\nMark Book as Read\n")

    title = input("Enter the title of the book: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    if collection.mark_as_read(title):
        print(f'\n✓ "{title}" marked as read.\n')
    else:
        print(f'\nNo book with the title "{title}" was found.\n')


def handle_stats() -> None:
    """Display statistics about the book collection."""
    stats = get_collection_stats(collection.list_books())

    print("\nCollection Statistics:\n")
    print(f"  Total books : {stats.total}")
    print(f"  Read        : {stats.read}")
    print(f"  Unread      : {stats.unread}")

    if stats.oldest:
        print(f"  Oldest      : {stats.oldest.title} ({stats.oldest.year})")
    if stats.newest:
        print(f"  Newest      : {stats.newest.title} ({stats.newest.year})")
    print()


def show_help() -> None:
    """Print available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  mark     - Mark a book as read
  stats    - Show collection statistics
  help     - Show this help message
""")


def main() -> None:
    """Entry point — parse the CLI command and dispatch to the correct handler."""
    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "mark": handle_mark_read,
        "stats": handle_stats,
        "help": show_help,
    }

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    handler = commands.get(command)

    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
