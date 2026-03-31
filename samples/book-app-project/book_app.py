import sys
from typing import List
from books import BookCollection, Book


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


def handle_list() -> None:
    """Display all books in the collection."""
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    while True:
        title = input("Title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please try again.")

    while True:
        author = input("Author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please try again.")

    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        if year < 0 or year > 2100:
            print("\nError: Year should be between 0 and 2100.")
            return
        collection.add_book(title, author, year)
        print("\nBook added successfully.")
    except ValueError as e:
        print(f"\nError: {e}")


def handle_remove() -> None:
    """Prompt user to remove a book by title from the collection."""
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nBook title cannot be empty.")
        return

    book = collection.find_book_by_title(title)
    if not book:
        print(f"\nBook '{title}' not found.")
        return

    confirm = input(f"Remove '{book.title}' by {book.author}? (y/n): ").strip().lower()
    if confirm == 'y':
        collection.remove_book(title)
        print(f"\nBook '{title}' removed successfully.")
    else:
        print("\nRemoval cancelled.")


def handle_find() -> None:
    """Prompt user to find books by author name."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("\nAuthor name cannot be empty.")
        return
    books = collection.find_by_author(author)

    show_books(books)


def show_help() -> None:
    """Display help message with available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
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
    elif command == "help":
        show_help()
    else:
        print("\nUnknown command.")
        show_help()


if __name__ == "__main__":
    main()
