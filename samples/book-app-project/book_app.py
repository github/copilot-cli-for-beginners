import sys
from books import BookCollection, get_statistics
from utils import get_book_details, print_books


# Global collection instance
collection = BookCollection()


def handle_list() -> None:
    books = collection.list_books()
    print_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    title, author, year = get_book_details()

    try:
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

    print_books(books)


def handle_read() -> None:
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book to mark as read: ").strip()
    if collection.mark_as_read(title):
        print("\nBook marked as read.\n")
    else:
        print("\nBook not found.\n")


def handle_by_year() -> None:
    print("\nList Books by Year Range\n")

    start_str = input("Start year: ").strip()
    end_str = input("End year: ").strip()

    try:
        start = int(start_str) if start_str else 0
        end = int(end_str) if end_str else 0
        books = collection.list_by_year(start, end)
        print_books(books)
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_stats() -> None:
    print("\nBook Collection Statistics\n")

    stats = get_statistics(collection.list_books())

    print(f"Total books: {stats['total']}")
    print(f"Read: {stats['read']}")
    print(f"Unread: {stats['unread']}")

    if stats["oldest"]:
        print(f"Oldest: {stats['oldest'].title} ({stats['oldest'].year})")
    if stats["newest"]:
        print(f"Newest: {stats['newest'].title} ({stats['newest'].year})")

    print()


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

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "read":
        handle_read()
    elif command == "byyear":
        handle_by_year()
    elif command == "stats":
        handle_stats()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
