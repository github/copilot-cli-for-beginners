import sys
from collections.abc import Callable

from books import BookCollection
from utils import display_books, display_help


def handle_list(collection: BookCollection) -> int:
    books = collection.list_books()
    display_books(books)
    return 0


def handle_add(collection: BookCollection) -> int:
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
        return 0
    except ValueError as e:
        print(f"\nError: {e}\n")
        return 1


def handle_remove(collection: BookCollection) -> int:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return 1

    if collection.remove_book(title):
        print("\nBook removed successfully.\n")
        return 0

    print("\nError: Book not found.\n")
    return 1


def handle_mark_read(collection: BookCollection) -> int:
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book to mark as read: ").strip()
    if not title:
        print("\nError: Title cannot be empty.\n")
        return 1

    if collection.mark_as_read(title):
        print("\nBook marked as read.\n")
        return 0

    print("\nError: Book not found.\n")
    return 1


def handle_find(collection: BookCollection) -> int:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("\nError: Author cannot be empty.\n")
        return 1

    books = collection.find_by_author(author)

    display_books(books)
    return 0


CollectionCommandHandler = Callable[[BookCollection], int]
CommandHandler = Callable[[], int]


def handle_help() -> int:
    display_help()
    return 0


def create_collection_command(handler: CollectionCommandHandler) -> CommandHandler:
    def command() -> int:
        try:
            collection = BookCollection()
        except (OSError, ValueError) as e:
            print(f"Error: {e}")
            return 1

        return handler(collection)

    return command


COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "list": create_collection_command(handle_list),
    "add": create_collection_command(handle_add),
    "mark-read": create_collection_command(handle_mark_read),
    "remove": create_collection_command(handle_remove),
    "find": create_collection_command(handle_find),
    "help": handle_help,
}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if not args:
        return handle_help()

    command = args[0].lower()

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        print("Unknown command.\n")
        display_help()
        return 1

    return handler()


if __name__ == "__main__":
    raise SystemExit(main())
