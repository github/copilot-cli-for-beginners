import sys
from books import BookCollection, BookDataError
from utils import format_books, format_error, format_option_list, prompt_required_text, prompt_year


def exit_with_error(message: str) -> int:
    print(format_error(message), end="")
    return 1


def handle_list(collection: BookCollection) -> int:
    books = collection.list_books()
    print(format_books(books), end="")
    return 0


def handle_list_unread(collection: BookCollection) -> int:
    books = collection.get_unread_books()
    print(format_books(books), end="")
    return 0


def handle_add(collection: BookCollection) -> int:
    print("\nAdd a New Book\n")

    try:
        title = prompt_required_text("Title")
        author = prompt_required_text("Author")
        year = prompt_year()
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
        return 0
    except ValueError as e:
        print(format_error(str(e)), end="")
        return 1


def handle_remove(collection: BookCollection) -> int:
    print("\nRemove a Book\n")

    try:
        title = prompt_required_text("Enter the title of the book to remove", "Title")
    except ValueError as e:
        print(format_error(str(e)), end="")
        return 1

    removed = collection.remove_book(title)
    if removed:
        print("\nBook removed.\n")
    else:
        print("\nNo matching book was found.\n")
    return 0


def handle_find(collection: BookCollection) -> int:
    print("\nFind Books by Author\n")

    try:
        author = prompt_required_text("Author name", "Author")
    except ValueError as e:
        print(format_error(str(e)), end="")
        return 1

    books = collection.find_by_author(author)

    print(format_books(books), end="")
    return 0


def handle_year(collection: BookCollection) -> int:
    print("\nFind Books by Year Range\n")

    try:
        start_year = prompt_year("Start year")
        end_year = prompt_year("End year")
        books = collection.list_by_year(start_year, end_year)
    except ValueError as e:
        print(format_error(str(e)), end="")
        return 1

    print(format_books(books), end="")
    return 0


def handle_read(collection: BookCollection) -> int:
    print("\nMark a Book as Read\n")

    try:
        title = prompt_required_text("Enter the title of the book to mark as read", "Title")
    except ValueError as e:
        print(format_error(str(e)), end="")
        return 1

    marked = collection.mark_as_read(title)
    if marked:
        print("\nBook marked as read.\n")
    else:
        print("\nNo matching book was found.\n")
    return 0


def show_help() -> None:
    print(
        format_option_list(
            "Book Collection Helper",
            (
                "Commands:",
                "  list     - Show all books",
                "  list unread - Show only unread books",
                "  add      - Add a new book",
                "  read     - Mark a book as read",
                "  remove   - Remove a book by title",
                "  find     - Find books by author",
                "  year     - Find books by year range",
                "  help     - Show this help message",
            ),
            trailing_blank_line=True,
        ),
        end="",
    )


def validate_command_args(command: str, args: list[str]) -> None:
    if command == "list":
        if not args:
            return
        if len(args) == 1 and str(args[0]).lower() == "unread":
            return
        raise ValueError("Command 'list' only supports the 'unread' option.")

    if args:
        raise ValueError(f"Command '{command}' does not accept additional arguments.")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    if not args:
        show_help()
        return 0

    command = str(args[0]).lower()

    if command == "help":
        show_help()
        return 0

    handlers = {
        "list": handle_list,
        "add": handle_add,
        "read": handle_read,
        "remove": handle_remove,
        "find": handle_find,
        "year": handle_year,
    }
    handler = handlers.get(command)
    if handler is None:
        print(format_error(f"Unknown command '{command}'."), end="")
        show_help()
        return 1

    try:
        validate_command_args(command, args[1:])
        collection = BookCollection()
        if command == "list" and args[1:]:
            return handle_list_unread(collection)
        return handler(collection)
    except ValueError as e:
        return exit_with_error(str(e))
    except KeyboardInterrupt:
        return exit_with_error("Operation cancelled.")
    except EOFError:
        return exit_with_error("No input received.")
    except BookDataError as e:
        return exit_with_error(str(e))

if __name__ == "__main__":
    raise SystemExit(main())
