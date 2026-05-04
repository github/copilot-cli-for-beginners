import sys
from books import BookCollection, StorageError
from utils import get_book_details, get_user_choice, print_menu


# Global collection instance. Initialized lazily by main() so that
# `import book_app` (e.g. in tests or `--help`) does not trigger disk I/O.
collection: BookCollection = None  # type: ignore[assignment]


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    if not year_str:
        print("\nError: Year is required.\n")
        return
    try:
        year = int(year_str)
    except ValueError:
        print(f"\nError: Year must be a number, got '{year_str}'.\n")
        return

    try:
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")
    except StorageError as e:
        print(f"\nError: Could not save book. {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nError: Title is required.\n")
        return

    try:
        removed = collection.remove_book(title)
    except StorageError as e:
        print(f"\nError: Could not update storage. {e}\n")
        return

    if removed:
        print(f"\nBook '{title}' removed.\n")
    else:
        print(f"\nNo book with title '{title}' found.\n")


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


def handle_add_interactive():
    """Add a book using strict validated prompts (used by interactive menu)."""
    print("\nAdd a New Book\n")
    details = get_book_details()
    if details is None:
        print("\nAdd cancelled.\n")
        return
    title, author, year = details
    try:
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")
    except StorageError as e:
        print(f"\nError: Could not save book. {e}\n")


def interactive_menu():
    """Run the interactive menu loop. Exits on choice 6 or Ctrl+C / EOF."""
    actions = {
        "1": handle_list,
        "2": handle_add_interactive,
        "3": handle_remove,
        "4": handle_find,
        "5": show_help,
    }
    while True:
        print_menu()
        choice = get_user_choice()
        if choice is None or choice == "6":
            print("\nGoodbye! 👋\n")
            return
        actions[choice]()


def main():
    global collection
    try:
        collection = BookCollection()
    except StorageError as e:
        print(f"Error: Could not load book collection. {e}", file=sys.stderr)
        return 1

    if len(sys.argv) < 2:
        interactive_menu()
        return 0

    command = sys.argv[1].lower()

    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "help": show_help,
        "--help": show_help,
        "-h": show_help,
    }

    handler = commands.get(command)
    if handler is None:
        print(f"Unknown command: {command}\n", file=sys.stderr)
        show_help()
        return 2

    handler()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:  # pragma: no cover - last-resort guard
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
