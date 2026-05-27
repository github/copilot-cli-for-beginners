import sys
from books import BookCollection
from typing import List, Any


# Global collection instance
collection = BookCollection()


def show_books(books: List[Any]) -> None:
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


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_search() -> None:
    """Search books by title or author.

    Usage: book_app.py search <query> [title|author]
    If query is omitted, user is prompted.
    """
    # prefer CLI args when provided
    if len(sys.argv) >= 3:
        query = sys.argv[2]
    else:
        query = input("Query: ").strip()

    field = 'title'
    if len(sys.argv) >= 4:
        field = sys.argv[3].lower()
    books = collection.search_books(query, field)
    show_books(books)


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author (exact match)
  search   - Search books by title or author (partial, case-insensitive). Usage: search <query> [title|author]
  help     - Show this help message
""")


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    COMMANDS = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "search": handle_search,
        "help": show_help,
    }

    handler = COMMANDS.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
