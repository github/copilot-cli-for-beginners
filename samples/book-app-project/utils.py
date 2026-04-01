def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            print("Please enter an option.")
        elif not choice.isdigit() or choice not in "12345":
            print("Invalid option. Please enter a number between 1 and 5.")
        else:
            return choice


def get_book_details():
    """Prompt the user to enter details for a new book.

    Validates that title and author are non-empty strings, re-prompting
    until valid input is provided. Publication year is parsed as an integer;
    if the input is invalid or missing, it defaults to 0.

    Parameters:
        None — all input is gathered interactively via stdin.

    Returns:
        tuple: A three-element tuple containing:
            - title (str): The book's title (non-empty).
            - author (str): The book's author (non-empty).
            - year (int): The publication year, or 0 if not provided or invalid.
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please try again.")

    while True:
        author = input("Enter author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please try again.")

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        rating_str = format_rating(getattr(book, "rating", None))
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status} {rating_str}")


def format_rating(rating) -> str:
    """Format a rating (1-5) as stars or text representation.
    
    Args:
        rating: Rating value (1-5) or None
        
    Returns:
        Formatted rating string (e.g., "⭐⭐⭐⭐⭐" or empty string if None)
    """
    if rating is None:
        return ""
    if isinstance(rating, int) and 1 <= rating <= 5:
        return "⭐" * rating
    return ""


def get_rating_input() -> int:
    """Get a valid rating input from user (1-5).
    
    Returns:
        Rating value (1-5)
    """
    while True:
        try:
            rating = int(input("Rating (1-5): ").strip())
            if 1 <= rating <= 5:
                return rating
            print("Rating must be between 1 and 5. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
