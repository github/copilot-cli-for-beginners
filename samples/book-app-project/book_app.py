import sys
from typing import Callable
from books import BookCollection


# Global collection instance
collection = BookCollection()


def show_books(books: list) -> None:
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
    """Prompt user to add a new book to the collection."""
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
    """Prompt user to remove a book from the collection."""
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find() -> None:
    """Prompt user to search for books by author."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def show_search_results(results: dict[str, list]) -> None:
    """Display search results grouped by title and author matches."""
    title_matches = results["by_title"]
    author_matches = results["by_author"]
    
    has_results = bool(title_matches or author_matches)
    if not has_results:
        print("No books found.")
        return
    
    if title_matches:
        print("\nMatches by Title:\n")
        show_books(title_matches)
    
    if author_matches:
        print("Matches by Author:\n")
        show_books(author_matches)


def handle_search() -> None:
    """Prompt user to search for books by title or author."""
    print("\nSearch Books\n")
    
    query = input("Enter search term (title or author): ").strip()
    if not query:
        print("Search term cannot be empty.\n")
        return
    
    results = collection.search_by_query(query)
    show_search_results(results)


def show_help() -> None:
    """Display help message with available commands."""
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  search   - Search books by title or author
  help     - Show this help message
""")


COMMAND_HANDLERS: dict[str, Callable[[], None]] = {
    "list": handle_list,
    "add": handle_add,
    "remove": handle_remove,
    "find": handle_find,
    "search": handle_search,
    "help": show_help,
}


def main() -> None:
    """Main entry point for the book collection CLI."""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    
    handler = COMMAND_HANDLERS.get(command)
    if handler:
        handler()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
