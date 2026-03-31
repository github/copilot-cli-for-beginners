import sys
from typing import Callable
from books import Book, BookCollection


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
    books = collection.list_books()
    show_books(books)


def handle_list_unread() -> None:
    books = collection.get_unread_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_read() -> None:
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book to mark as read: ").strip()
    if collection.mark_as_read(title):
        print(f"\n'{title}' marked as read.\n")
    else:
        print(f"\nBook '{title}' not found in your collection.\n")


def handle_search() -> None:
    print("\nSearch Books\n")

    query = input("Search by title or author: ").strip()
    books = collection.search(query)

    show_books(books)


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list          - Show all books
  list-unread   - Show only unread books
  add           - Add a new book
  remove        - Remove a book by title
  read          - Mark a book as read
  search        - Search books by title or author
  help          - Show this help message
""")


COMMANDS: dict[str, Callable[[], None]] = {
    "list": handle_list,
    "list-unread": handle_list_unread,
    "add": handle_add,
    "remove": handle_remove,
    "read": handle_read,
    "search": handle_search,
    "help": show_help,
}


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    handler = COMMANDS.get(command)

    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
