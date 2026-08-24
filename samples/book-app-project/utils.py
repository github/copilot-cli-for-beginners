from datetime import date

from books import Book


def get_statistics(books: list[Book]) -> dict:
    """Compute summary statistics for a list of Book objects.

    Returns a dict with total count, read/unread counts, and the
    oldest and newest books (by publication year), or None for the
    oldest/newest keys if the list is empty.
    """
    total = len(books)
    read = sum(1 for book in books if book.read)
    unread = total - read

    oldest = min(books, key=lambda book: book.year) if books else None
    newest = max(books, key=lambda book: book.year) if books else None

    return {
        "total": total,
        "read": read,
        "unread": unread,
        "oldest": oldest,
        "newest": newest,
    }


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Prompt until the user enters a non-empty, numeric menu choice."""
    prompt = "Choose an option (1-5): "

    while True:
        choice = input(prompt).strip()

        if not choice:
            prompt = "Choice cannot be empty. Choose an option (1-5): "
            continue

        if not choice.isdigit():
            prompt = f"'{choice}' is not a valid number. Choose an option (1-5): "
            continue

        return choice


def get_book_details() -> tuple[str, str, int]:
    """Prompt the user for book title, author, and publication year.

    Interactively reads input from the console and re-prompts until each
    field is valid:
    - Title: re-prompts until a non-empty (non-whitespace) string is entered.
    - Author: re-prompts until a non-empty (non-whitespace) string is entered.
    - Year: delegates to `_get_valid_year()`, which re-prompts until a whole
      number between 1 and the current year (inclusive) is entered.

    Parameters:
        None. All values are collected via `input()` prompts.

    Returns:
        tuple[str, str, int]: A 3-tuple of `(title, author, year)`, where
        `title` and `author` are stripped, non-empty strings and `year` is
        a validated integer publication year.
    """
    title = input("Enter book title: ").strip()
    while not title:
        title = input("Title cannot be empty. Enter book title: ").strip()

    author = input("Enter author: ").strip()
    while not author:
        author = input("Author cannot be empty. Enter author: ").strip()

    year = _get_valid_year()

    return title, author, year


def _get_valid_year() -> int:
    """Prompt until the user enters a valid publication year.

    A valid year is a whole number between 1 and the current year
    (inclusive), which rules out non-numeric input, negative years,
    and years in the future.
    """
    current_year = date.today().year
    prompt = "Enter publication year: "

    while True:
        year_input = input(prompt).strip()
        try:
            year = int(year_input)
        except ValueError:
            prompt = f"'{year_input}' is not a valid whole number. Enter publication year: "
            continue

        if not 1 <= year <= current_year:
            prompt = (
                f"Year must be between 1 and {current_year}. "
                "Enter publication year: "
            )
            continue

        return year


def print_books(books: list[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
