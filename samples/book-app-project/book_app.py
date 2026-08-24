import sys
from books import BookCollection
from utils import get_statistics, print_books


# Global collection instance
collection = BookCollection()


def handle_list():
    books = collection.list_books()
    print_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str)
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    removed = collection.remove_book(title)

    if removed:
        print("\nBook removed.\n")
    else:
        print("\nBook not found.\n")


def handle_mark_read():
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book to mark as read: ").strip()
    marked = collection.mark_as_read(title)

    if marked:
        print("\nBook marked as read.\n")
    else:
        print("\nBook not found.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    print_books(books)


def handle_list_by_year():
    print("\nList Books by Year Range\n")

    start_str = input("Start year: ").strip()
    end_str = input("End year: ").strip()

    try:
        start = int(start_str)
        end = int(end_str)
        if start > end:
            print("\nError: Start year cannot be greater than end year.\n")
            return
        books = collection.list_by_year(start, end)
        print_books(books)
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_stats():
    print("\nBook Collection Statistics\n")

    stats = get_statistics(collection.list_books())
    print(f"Total books: {stats['total']}")
    print(f"Read: {stats['read']}")
    print(f"Unread: {stats['unread']}")
    print()


def show_help():
    print("""
Book Collection Helper

Commands:
  list          - Show all books
  add           - Add a new book
  remove        - Remove a book by title
  mark-read     - Mark a book as read
  find          - Find books by author
  list-by-year  - List books published within a year range
  stats         - Show collection statistics (total, read, unread)
  help          - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    try:
        if command == "list":
            handle_list()
        elif command == "add":
            handle_add()
        elif command == "remove":
            handle_remove()
        elif command == "mark-read":
            handle_mark_read()
        elif command == "find":
            handle_find()
        elif command == "list-by-year":
            handle_list_by_year()
        elif command == "stats":
            handle_stats()
        elif command == "help":
            show_help()
        else:
            print("Unknown command.\n")
            show_help()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.\n")


if __name__ == "__main__":
    main()
