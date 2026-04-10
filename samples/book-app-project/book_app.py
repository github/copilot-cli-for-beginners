import sys
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


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    if not year_str:
        print("\nError: Year cannot be empty.\n")
        return

    try:
        year = int(year_str)
        if year < 1 or year > 2100:
            print("\nError: Year must be between 1 and 2100.\n")
            return
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
    print("\nSearch Books\n")

    query = input("Search query (title or author): ").strip()
    if not query:
        print("\nError: Search query cannot be empty.\n")
        return

    books = collection.search_books(query)
    show_books(books)


def handle_list_unread() -> None:
    books = collection.get_unread_books()
    show_books(books)


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  unread   - Show only unread books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author (exact match)
  search   - Search books by title or author (partial match)
  help     - Show this help message
""")


COMMANDS = {
    "list": handle_list,
    "unread": handle_list_unread,
    "add": handle_add,
    "remove": handle_remove,
    "find": handle_find,
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
        print(f"Unknown command: '{command}'\n")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
