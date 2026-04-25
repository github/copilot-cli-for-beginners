import json
import os
import sys
from typing import Any, Tuple, List


# Simple log helpers to keep messages consistent and testable.
# These can be later redirected to the `logging` module if desired.
def log_info(msg: str) -> None:
    print(f"INFO: {msg}")


def log_warn(msg: str) -> None:
    print(f"WARNING: {msg}")


def log_error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


# --- Display helpers (separate UI from logic) ---
def display_info(msg: str) -> None:
    """User-facing informational message (UI layer)."""
    print(msg)


def display_warning(msg: str) -> None:
    """User-facing warning message (UI layer)."""
    print(msg)


def display_error(msg: str) -> None:
    """User-facing error message (UI layer)."""
    print(msg, file=sys.stderr)


def safe_load_json(path: str, default: Any) -> Any:
    """Safely load JSON from a file.

    - Returns `default` if the file does not exist or content is invalid.
    - Logs a warning for recoverable issues and an error for I/O failures.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log_warn(f"{path} not found; using default value")
        return default
    except json.JSONDecodeError:
        log_warn(f"{path} is corrupted or not valid JSON; using default value")
        return default
    except OSError as e:
        log_error(f"Failed to read {path}: {e}")
        return default


def atomic_write_json(path: str, obj: Any) -> bool:
    """Write JSON to path atomically. Returns True on success, False on failure.

    Creates a temporary file in the same directory and replaces the target file.
    """
    try:
        dirpath = os.path.dirname(os.path.abspath(path)) or "."
        fd, tmp_path = os.openpty() if False else None, None
        # Use tempfile.mkstemp to create temp file safely
        import tempfile

        fd, tmp_path = tempfile.mkstemp(prefix=".tmp_books_", dir=dirpath)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(obj, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, path)
            return True
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
    except OSError as e:
        log_error(f"Failed to write {path}: {e}")
        return False


# --- existing UI helpers ---

def display_menu() -> None:
    display_info("\n📚 Book Collection App")
    display_info("1. Add a book")
    display_info("2. List books")
    display_info("3. Mark book as read")
    display_info("4. Remove a book")
    display_info("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            display_error("Please enter a choice (1-5).")
            continue
        if not choice.isdigit():
            display_error("Please enter a number between 1 and 5.")
            continue
        return choice


def get_book_details() -> Tuple[str, str, int]:
    """
    Prompt the user for book details and return them.

    Repeatedly asks for book title until a non-empty string is provided. Then
    prompts once for author and publication year. If the year cannot be parsed
    as an integer, it defaults to 0 and prints a warning.

    Returns:
        tuple: (title, author, year)
            - title (str): Non-empty book title provided by the user.
            - author (str): Author name (may be empty if user leaves it blank).
            - year (int): Publication year parsed as int, or 0 if parsing failed
              or the user left it blank.
    """
    # Ensure title is not empty
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        display_error("Title cannot be empty. Please enter a title.")

    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        log_warn("Invalid year input; defaulting to 0.")
        year = 0

    return title, author, year


def display_books(books: List[Any]) -> None:
    if not books:
        display_info("No books in your collection.")
        return

    display_info("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if getattr(book, "read", False) else "📖 Unread"
        display_info(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")


# Backwards-compatible aliases for older code that imported the old names
print_menu = display_menu
print_books = display_books
