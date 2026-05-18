def print_menu():
    """Display the main menu options for the book collection app."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Prompt user for menu choice and return stripped input."""
    return input("Choose an option (1-5): ").strip()


def parse_year(year_input: str) -> int:
    """Parse year input, defaulting to 0 if invalid or out of range.

    Args:
        year_input: String representation of a year

    Returns:
        Parsed year as integer, or 0 if parsing fails or out of range

    Note:
        Prints error message to console when parsing fails or year is invalid
    """
    try:
        year = int(year_input)
        if 0 <= year <= 9999:
            return year
        else:
            print("Year out of range. Defaulting to 0.")
            return 0
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        return 0


def get_book_details():
    """Collect book details from user input.

    Prompts user for title, author, and publication year.
    Year input is parsed with error handling.

    Returns:
        Tuple of (title, author, year) where year is int
    """
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    year = parse_year(year_input)

    return title, author, year


def print_books(books):
    """Display a formatted list of books with read status.

    Args:
        books: List of Book objects to display

    Note:
        Shows "No books in your collection." if list is empty
    """
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
