import sys
from books import BookCollection, get_statistics
from exceptions import BookAppError
from utils import get_book_details, parse_year, print_books, print_stats


try:
    # Global collection instance
    collection = BookCollection()
except BookAppError as e:
    print(f"\nFailed to load book collection: {e}\n")
    sys.exit(1)


def handle_list() -> None:
    books = collection.list_books()
    print_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title, author, year = get_book_details()

    try:
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()

    try:
        collection.remove_book(title)
        print("\nBook removed successfully.\n")
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    print_books(books)


def handle_read() -> None:
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book to mark as read: ").strip()

    try:
        collection.mark_as_read(title)
        print("\nBook marked as read.\n")
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_by_year() -> None:
    print("\nList Books by Year Range\n")

    start_str = input("Start year: ").strip()
    end_str = input("End year: ").strip()

    try:
        start = parse_year(start_str) if start_str else 0
        end = parse_year(end_str) if end_str else 0
        books = collection.list_by_year(start, end)
        print_books(books)
    except BookAppError as e:
        print(f"\nError: {e}\n")


def handle_stats() -> None:
    print("\nBook Collection Statistics\n")

    stats = get_statistics(collection.list_books())
    print_stats(stats)


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  read     - Mark a book as read
  byyear   - List books published within a year range
  stats    - Show collection statistics
  help     - Show this help message
""")


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "read": handle_read,
        "byyear": handle_by_year,
        "stats": handle_stats,
        "help": show_help,
    }

    handler = commands.get(command)
    if handler is None:
        print("Unknown command.\n")
        show_help()
        return

    handler()


if __name__ == "__main__":
    main()
