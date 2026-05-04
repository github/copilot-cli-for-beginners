from datetime import datetime
from typing import Optional, Tuple

VALID_MENU_CHOICES = {"1", "2", "3", "4", "5", "6"}
MIN_YEAR = 1
MAX_YEAR = datetime.now().year + 1
MAX_FIELD_LENGTH = 200


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. List books")
    print("2. Add a book")
    print("3. Remove a book")
    print("4. Find books by author")
    print("5. Help")
    print("6. Exit")


def _prompt(message: str) -> Optional[str]:
    """Prompt the user, returning None if input is aborted (EOF/Ctrl+C)."""
    try:
        return input(message)
    except (EOFError, KeyboardInterrupt):
        print()  # newline after ^C / ^D
        return None


def _prompt_non_empty(message: str, field_name: str) -> Optional[str]:
    """Re-prompt until a non-empty, valid value is provided, or input is aborted."""
    while True:
        value = _prompt(message)
        if value is None:
            return None
        value = value.strip()
        if not value:
            print(f"{field_name} cannot be empty or whitespace. Please try again.")
            continue
        if len(value) > MAX_FIELD_LENGTH:
            print(f"{field_name} is too long (max {MAX_FIELD_LENGTH} characters). Please try again.")
            continue
        return value


def get_user_choice() -> Optional[str]:
    """Prompt for a menu choice. Re-prompts on invalid input."""
    while True:
        choice = _prompt("Choose an option (1-6): ")
        if choice is None:
            return None
        choice = choice.strip()
        if not choice:
            print("Choice cannot be empty. Please enter a number between 1 and 6.")
            continue
        if not choice.isdigit():
            print(f"Invalid choice: '{choice}' is not a number. Please enter a number between 1 and 6.")
            continue
        if choice not in VALID_MENU_CHOICES:
            print(f"Invalid choice: {choice} is out of range. Please enter a number between 1 and 6.")
            continue
        return choice


def get_book_details() -> Optional[Tuple[str, str, int]]:
    """Interactively collect details for a new book from standard input.

    Prompts the user, in order, for the book's title, author, and publication
    year. Each field is validated and the user is re-prompted until a valid
    value is entered or input is aborted (Ctrl+C / Ctrl+D / EOF).

    Validation rules:
        - Title and author: stripped of surrounding whitespace; must be
          non-empty after stripping and no longer than ``MAX_FIELD_LENGTH``
          characters.
        - Year: must parse as an integer and fall within the inclusive range
          ``MIN_YEAR`` to ``MAX_YEAR`` (current year + 1, to allow upcoming
          releases).

    Parameters:
        None. All input is read interactively from stdin via ``input()``.

    Returns:
        Optional[Tuple[str, str, int]]:
            - On success: a 3-tuple ``(title, author, year)`` where ``title``
              and ``author`` are stripped, non-empty strings and ``year`` is an
              ``int`` within the valid range.
            - ``None`` if the user aborts input at any prompt (EOFError or
              KeyboardInterrupt). No partial data is returned.

    Side effects:
        Writes prompts and validation error messages to standard output.

    Example:
        >>> details = get_book_details()
        >>> if details is not None:
        ...     title, author, year = details
    """
    title = _prompt_non_empty("Enter book title: ", "Title")
    if title is None:
        return None

    author = _prompt_non_empty("Enter author: ", "Author")
    if author is None:
        return None

    while True:
        year_input = _prompt(f"Enter publication year ({MIN_YEAR}-{MAX_YEAR}): ")
        if year_input is None:
            return None
        year_input = year_input.strip()
        if not year_input:
            print("Year cannot be empty. Please try again.")
            continue
        try:
            year = int(year_input)
        except ValueError:
            print(f"Invalid year: '{year_input}' is not a number. Please try again.")
            continue
        if not (MIN_YEAR <= year <= MAX_YEAR):
            print(f"Year must be between {MIN_YEAR} and {MAX_YEAR}. Please try again.")
            continue
        break

    return title, author, year



