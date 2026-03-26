import sys
from books import BookCollection
from utils import print_books


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
        year = int(year_str) if year_str else 0
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


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    print_books(books)


def handle_search_year():
    print("\nSearch Books by Year Range\n")

    start_str = input("Start year: ").strip()
    end_str = input("End year: ").strip()

    try:
        start = int(start_str)
        end = int(end_str)
        books = collection.list_by_year(start, end)
        print_books(books)
    except ValueError as e:
        print(f"\nError: {e}\n")


def show_help():
    print("""
Book Collection Helper

Commands:
  list         - Show all books
  add          - Add a new book
  remove       - Remove a book by title
  find         - Find books by author
  search-year  - Search books by year range
  help         - Show this help message
""")


def main():
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
    elif command == "search-year":
        handle_search_year()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
