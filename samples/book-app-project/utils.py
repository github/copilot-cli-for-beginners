from typing import List, Tuple
from books import Book


def print_menu() -> None:
    """
    Display the main menu for the book collection app.
    
    Shows available options:
    1. Add a book
    2. List books
    3. Mark book as read
    4. Remove a book
    5. Exit
    
    Args:
        None
    
    Returns:
        None
    
    Example:
        >>> print_menu()
        
        📚 Book Collection App
        1. Add a book
        2. List books
        3. Mark book as read
        4. Remove a book
        5. Exit
    """
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """
    Prompt user to select an option from the main menu.
    
    Displays a prompt asking user to choose an option (1-5) with comprehensive validation:
    - Rejects empty input
    - Rejects non-numeric input
    - Rejects numbers outside range 1-5
    - Provides specific error messages for each validation failure
    - Continues prompting until valid input is received
    
    Args:
        None
    
    Returns:
        str: A single character string representing user's choice ("1", "2", "3", "4", or "5")
    
    Example:
        >>> choice = get_user_choice()
        Choose an option (1-5): 3
        >>> print(choice)
        3
    """
    while True:
        choice = input("Choose an option (1-5): ").strip()
        
        if not choice:
            print("Error: Please enter a choice.")
            continue
        
        if not choice.isdigit():
            print("Error: Please enter a number, not text.")
            continue
        
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        
        print("Error: Please enter a number between 1 and 5.")


def get_book_details() -> Tuple[str, str, int]:
    """
    Prompts user to enter book details with comprehensive validation.
    
    Collects title, author, and publication year from user input with the following:
    - Title and author: Case-sensitive, non-empty strings (max 3 retries each)
    - Year: Integer between 1000 and 2100 (unlimited retries until valid)
    
    Validation Rules:
    - Title: Cannot be empty/whitespace-only
    - Author: Cannot be empty/whitespace-only
    - Year: Must be a valid integer in range [1000, 2100]
    
    Args:
        None
    
    Returns:
        Tuple[str, str, int]: A tuple containing:
            - title (str): The book's title
            - author (str): The book's author
            - year (int): The book's publication year
    
    Raises:
        None (retries automatically on invalid input)
    
    Notes:
        - Empty entries for title/author allow 3 retries before restarting
        - Year validation loops until valid input is provided
        - All string inputs are stripped of leading/trailing whitespace
        - Empty line followed by 3 failed attempts restarts the entire process
    
    Example:
        >>> title, author, year = get_book_details()
        >>> # User enters: "1984", "George Orwell", "1949"
        >>> print(title, author, year)
        1984 George Orwell 1949
    """
    max_retries = 3
    
    # Get title with retry limit
    title = ""
    for attempt in range(max_retries):
        title = input("Enter book title: ").strip()
        if title:
            break
        print(f"Error: Title cannot be empty. (Attempt {attempt + 1}/{max_retries})")
    else:
        print("Error: Too many empty entries. Cancelling.")
        return get_book_details()
    
    # Get author with retry limit
    author = ""
    for attempt in range(max_retries):
        author = input("Enter author: ").strip()
        if author:
            break
        print(f"Error: Author cannot be empty. (Attempt {attempt + 1}/{max_retries})")
    else:
        print("Error: Too many empty entries. Cancelling.")
        return get_book_details()

    # Get year with validation loop
    while True:
        year_input = input("Enter publication year: ").strip()
        if not year_input:
            print("Error: Year cannot be empty.")
            continue
        try:
            year = int(year_input)
            if not (1000 <= year <= 2100):
                print("Error: Year must be between 1000 and 2100.")
                continue
            return title, author, year
        except ValueError:
            print("Error: Year must be a valid number.")


def print_books(books: List[Book]) -> None:
    """
    Display a formatted list of books with read/unread status.
    
    Prints all books in the collection in a numbered list format showing:
    - Book index number (starting from 1)
    - Book title
    - Author name
    - Publication year
    - Read status (✅ Read or 📖 Unread)
    
    Args:
        books (List[Book]): A list of Book objects to display
    
    Returns:
        None
    
    Example:
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
