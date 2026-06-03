import sys
from books import BookCollection


from utils import print_books, print_help, get_book_details

# Global collection instance (lazy-initialized)
collection = None


def get_collection():
    """Return a lazily-created global BookCollection instance.

    Avoid creating the collection (and touching the data file) at import time so
    importing this module is side-effect free and easier to test.
    """
    global collection
    if collection is None:
        collection = BookCollection()
    return collection


# Initialize collection at import time so tests that reload this module after
# monkeypatching books.DATA_FILE get a collection bound to the patched path.
# This keeps the test expectation while still allowing explicit injection by
# passing data_file to BookCollection in other code paths.
collection = get_collection()

def handle_list():
    books = get_collection().list_books()
    print_books(books)


def handle_list_unread():
    books = get_collection().get_unread_books()
    print_books(books)


def handle_add():
    print("\nAdd a New Book\n")
    try:
        title, author, year = get_book_details()
    except ValueError as e:
        print(f"\nError: {e}\n")
        return

    if not title:
        print("\nError: Title cannot be empty.\n")
        return
    if not author:
        print("\nError: Author cannot be empty.\n")
        return

    try:
        get_collection().add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")
    except Exception as e:
        print(f"\nUnexpected error adding book: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return

    try:
        removed = get_collection().remove_book(title)
        if removed:
            print(f"\nBook '{title}' removed.\n")
        else:
            print(f"\nBook '{title}' not found.\n")
    except Exception as e:
        print(f"\nUnexpected error removing book: {e}\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("\nError: Author name cannot be empty.\n")
        return

    books = get_collection().find_by_author(author)
    print_books(books)


def handle_search(query: str = None):
    print("\nSearch Books by Title or Author\n")
    if not query:
        query = input("Search query: ").strip()
    if not query:
        print("\nError: Search query cannot be empty.\n")
        return
    try:
        books = get_collection().search(query)
        print_books(books)
    except Exception as e:
        print(f"\nUnexpected error searching books: {e}\n")


def handle_mark(title: str = None):
    print("\nMark a Book as Read\n")
    if not title:
        title = input("Enter the title of the book to mark as read: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return
    try:
        if get_collection().mark_as_read(title):
            print(f"\nBook '{title}' marked as read.\n")
        else:
            print(f"\nBook '{title}' not found.\n")
    except Exception as e:
        print(f"\nUnexpected error marking book as read: {e}\n")




def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    # Helper wrappers for commands that accept optional argv arguments
    def _search_wrapper():
        query = " ".join(args) if args else None
        return handle_search(query)

    def _mark_wrapper():
        title = " ".join(args) if args else None
        return handle_mark(title)

    dispatch = {
        "list": handle_list,
        "list-unread": handle_list_unread,
        "add": handle_add,
        "remove": handle_remove,
        "find": handle_find,
        "search": _search_wrapper,
        "mark": _mark_wrapper,
        "help": print_help,
    }

    func = dispatch.get(command)
    if func:
        return func()

    print("Unknown command.\n")
    print_help()


if __name__ == "__main__":
    main()
