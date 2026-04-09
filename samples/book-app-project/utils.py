def print_menu() -> None:
    """Display the main menu with available options."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """
    Prompt user for a menu choice and validate input.
    
    Continues prompting until valid input (1-5) is received. Rejects empty strings
    and non-numeric entries.
    
    Returns:
        str: A valid choice from 1-5.
    """
    while True:
        choice = input("Choose an option (1-5): ").strip()
        
        if not choice:
            print("Error: Input cannot be empty. Please enter a number 1-5.")
            continue
        
        if not choice.isdigit():
            print("Error: Please enter a numeric value (1-5).")
            continue
        
        if choice not in ("1", "2", "3", "4", "5"):
            print("Error: Please choose a valid option (1-5).")
            continue
        
        return choice


def get_book_details() -> tuple[str, str, int]:
    """
    Collect book information from user input.
    
    Prompts the user for book title, author, and publication year. Validates that
    the title is not empty (raises ValueError if it is). Handles year parsing with
    a default value of 0 if parsing fails.
    
    Returns:
        tuple[str, str, int]: A tuple containing (title, author, year).
    
    Raises:
        ValueError: If the title is empty after stripping whitespace.
    
    Examples:
        >>> title, author, year = get_book_details()
        # User enters: "1984", "George Orwell", "1949"
        >>> (title, author, year)
        ('1984', 'George Orwell', 1949)
    """
    title = input("Enter book title: ").strip()
    
    if not title:
        raise ValueError("Book title cannot be empty.")
    
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input) if year_input else 0
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books: list) -> None:
    """
    Display a formatted list of books with read status.
    
    Args:
        books (list): List of Book objects to display. If empty, a message is shown.
    
    Examples:
        >>> books = [Book("1984", "George Orwell", 1949, read=True)]
        >>> print_books(books)
        Your Books:
        1. 1984 by George Orwell (1949) - ✅ Read
    """
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
