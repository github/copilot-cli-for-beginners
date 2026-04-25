import sys
from books import BookCollection
from utils import display_books, display_info, display_error


# Global collection instance
collection = BookCollection()


def handle_list():
    books = collection.list_books()
    display_books(books)


def handle_add():
    display_info("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        display_info("\nBook added successfully.\n")
    except ValueError as e:
        display_error(f"\nError: {e}\n")


def handle_remove():
    display_info("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    display_info("\nBook removed if it existed.\n")


def handle_find():
    display_info("\nFind Books by Title or Author\n")

    query = input("Search query (title or author): ").strip()
    if not query:
        display_error("No query provided.\n")
        return

    # Ask which fields to search; default searches both title and author
    choice = input("Search in (t)itle, (a)uthor, or (b)oth? [b]: ").strip().lower()
    if choice == "t":
        fields = ["title"]
    elif choice == "a":
        fields = ["author"]
    else:
        fields = ["title", "author"]

    books = collection.search(query, fields=fields, case_sensitive=False)

    display_books(books)


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by title or author
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    # Dispatch table for commands -> handler functions
    commands = {
        "list": handle_list,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
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
