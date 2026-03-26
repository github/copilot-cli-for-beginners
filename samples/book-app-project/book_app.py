from __future__ import annotations

import sys
from books import BookCollection
from utils import get_book_details, print_books


# Global collection instance (initialized in main)
collection: BookCollection | None = None


def handle_list() -> None:
    print_books(collection.list_books())


def handle_add() -> None:
    print("\nAdd a New Book\n")
    title, author, year = get_book_details()

    try:
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except (ValueError, OSError) as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    try:
        if collection.remove_book(title):
            print("\nBook removed.\n")
        else:
            print("\nBook not found.\n")
    except OSError as e:
        print(f"\nError: Could not save changes: {e}\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("\nError: Author name cannot be empty.\n")
        return

    print_books(collection.find_by_author(author))


def handle_mark_read() -> None:
    print("\nMark a Book as Read\n")

    title = input("Enter the title: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    try:
        if collection.mark_as_read(title):
            print("\nBook marked as read.\n")
        else:
            print("\nBook not found.\n")
    except OSError as e:
        print(f"\nError: Could not save changes: {e}\n")


def handle_find_title() -> None:
    print("\nFind a Book by Title\n")

    title = input("Enter the title: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    book = collection.find_by_title(title)
    if book:
        print_books([book])
    else:
        print("\nBook not found.\n")


def handle_search_year() -> None:
    print("\nSearch Books by Year Range\n")

    start_str = input("Start year: ").strip()
    end_str = input("End year: ").strip()

    try:
        start = int(start_str)
        end = int(end_str)
        print_books(collection.list_by_year(start, end))
    except ValueError as e:
        print(f"\nError: {e}\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list         - Show all books
  add          - Add a new book
  remove       - Remove a book by title
  find         - Find books by author
  find-title   - Find a book by title
  mark-read    - Mark a book as read
  search-year  - Search books by year range
  help         - Show this help message
""")


def main() -> None:
    global collection
    collection = BookCollection()

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "find-title": handle_find_title,
        "mark-read": handle_mark_read,
        "search-year": handle_search_year,
        "help": show_help,
    }

    handler = commands.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
