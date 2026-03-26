def print_menu() -> None:
    """Display the interactive menu options.

    Used for the interactive menu mode (alternative to CLI arguments).
    """
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Prompt the user to select a menu option (1-5) with validation.

    Used for the interactive menu mode (alternative to CLI arguments).

    Returns:
        A string representing the user's valid choice ('1' through '5').
    """
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            print("Input cannot be empty. Please enter a number between 1 and 5.")
            continue
        if not choice.isdigit() or not 1 <= int(choice) <= 5:
            print(f"Invalid choice: '{choice}'. Please enter a number between 1 and 5.")
            continue
        return choice


def get_book_details() -> tuple[str, str, int]:
    """Interactively prompt the user for book details with input validation.

    Asks for title, author, and publication year in sequence. Each field is
    validated before proceeding: title and author must be non-empty strings,
    and year must be a non-negative integer. The user is re-prompted until
    valid input is provided for each field.

    Returns:
        tuple[str, str, int]: A tuple of (title, author, year) where:
            - title: The book's title (non-empty string).
            - author: The book's author (non-empty string).
            - year: The publication year (non-negative integer).

    Example:
        >>> title, author, year = get_book_details()
        Enter book title: The Hobbit
        Enter author: J.R.R. Tolkien
        Enter publication year: 1937
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a title.")

    while True:
        author = input("Enter author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please enter an author.")

    while True:
        year_input = input("Enter publication year: ").strip()
        if not year_input:
            print("Year cannot be empty. Please enter a year.")
            continue
        try:
            year = int(year_input)
            if year < 0:
                print("Year cannot be negative. Please enter a valid year.")
                continue
            break
        except ValueError:
            print(f"Invalid year: '{year_input}'. Please enter a number.")

    return title, author, year


def print_books(books: list) -> None:
    """Display a list of books in a formatted output with read status."""
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
