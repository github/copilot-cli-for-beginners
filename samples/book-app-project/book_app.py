import sys
from typing import List
from books import Book, BookCollection


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


def show_books_with_indices(books: List[Book]) -> None:
    """Display books with numbers for user selection."""
    if not books:
        print("No books found.")
        return

    print("\nBooks Available:\n")
    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")
    print()


def handle_list() -> None:
    """List all books in the collection."""
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    """Add a new book with validation."""
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    if not title:
        print("Error: Title cannot be empty.\n")
        return

    author = input("Author: ").strip()
    if not author:
        print("Error: Author cannot be empty.\n")
        return

    year_str = input("Year: ").strip()

    try:
        if year_str:
            year = int(year_str)
            if year < 0:
                print("Error: Year must be a positive number.\n")
                return
        else:
            print("Error: Year cannot be empty.\n")
            return

        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError:
        print("Error: Year must be a valid integer.\n")


def handle_remove() -> None:
    """Remove a book by title."""
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("Error: Title cannot be empty.\n")
        return

    if collection.remove_book(title):
        print(f"\n✓ '{title}' has been removed.\n")
    else:
        print(f"\n✗ Book '{title}' not found.\n")


def handle_find() -> None:
    """Find books by author."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("Error: Author name cannot be empty.\n")
        return

    books = collection.find_by_author(author)
    show_books(books)


def mark_by_title() -> None:
    """Mark a book as read by title."""
    title = input("Enter the title of the book to mark as read: ").strip()
    if not title:
        print("Error: Title cannot be empty.\n")
        return

    if collection.mark_as_read(title):
        print(f"\n✓ '{title}' marked as read.\n")
    else:
        print(f"\n✗ Book '{title}' not found.\n")


def mark_by_index() -> None:
    """Mark a book as read by selecting from list."""
    books = collection.list_books()
    if not books:
        print("\nNo books in your collection.\n")
        return

    show_books_with_indices(books)

    try:
        index_input = input("Enter the book number to mark as read: ").strip()
        if not index_input:
            print("Error: Please enter a valid number.\n")
            return

        index = int(index_input) - 1

        if 0 <= index < len(books):
            book = books[index]
            collection.mark_as_read(book.title)
            print(f"\n✓ '{book.title}' marked as read.\n")
        else:
            print(f"\n✗ Invalid selection. Please enter a number between 1 and {len(books)}.\n")
    except ValueError:
        print("Error: Please enter a valid number.\n")


def handle_mark() -> None:
    """Mark a book as read by title or by selecting from a list."""
    print("\nMark a Book as Read\n")

    print("How would you like to mark a book?")
    print("1. By title")
    print("2. By selecting from list")
    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
        mark_by_title()
    elif choice == "2":
        mark_by_index()
    else:
        print("Error: Invalid choice. Please enter 1 or 2.\n")


def show_help() -> None:
    """Display help message with available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  mark     - Mark a book as read
  help     - Show this help message
""")


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
    elif command == "mark":
        handle_mark()
    elif command == "help":
        show_help()
    else:
        print("Error: Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
