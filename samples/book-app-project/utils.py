from typing import List, Tuple, Dict, Optional, Any
from books import Book


def print_menu() -> None:
    """Display the main menu options."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """
    Get user menu choice with validation.
    
    Validates that input is:
    - Not empty
    - Numeric
    - Between 1-5
    
    Returns:
        Valid menu choice as string (1-5)
    """
    while True:
        choice = input("Choose an option (1-5): ").strip()
        
        # Check for empty input
        if not choice:
            print("❌ Empty input. Please enter a number between 1 and 5.")
            continue
        
        # Check for non-numeric input
        if not choice.isdigit():
            print("❌ Invalid input. Please enter a number (not letters or symbols).")
            continue
        
        # Check if choice is in valid range
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        
        print("❌ Invalid choice. Please enter a number between 1 and 5.")


def get_book_details() -> Tuple[str, str, int]:
    """
    Interactively prompt user for book information with comprehensive validation.
    
    This function guides the user through entering book details with input validation
    at each step. If the user enters invalid data, they are shown a specific error
    message and prompted to try again. The function loops until all inputs are valid.
    
    Parameters:
        None - This function takes no parameters. It prompts for user input directly.
    
    Returns:
        Tuple[str, str, int]: A tuple containing three validated elements:
            - title (str): The book title, non-empty and 1-100 characters long
            - author (str): The book author, non-empty and 1-100 characters long
            - year (int): Publication year as an integer (0 if user presses Enter,
                         or any non-negative year <= 2100)
    
    Input Validation Rules:
        Title:
            - Cannot be empty or whitespace-only (after stripping)
            - Must be between 1-100 characters long
            - Examples accepted: "The Great Gatsby", "1984", "A Brief History of Time"
        
        Author:
            - Cannot be empty or whitespace-only (after stripping)
            - Must be between 1-100 characters long
            - Examples accepted: "F. Scott Fitzgerald", "George Orwell", "Stephen Hawking"
        
        Year:
            - Optional - user can press Enter for default value of 0
            - If provided, must be a valid integer
            - Must be non-negative (>= 0)
            - If > 2100, user is prompted to confirm this unusual value
            - Examples accepted: 1925, 1949, 2023, 0
    
    Raises:
        ValueError: Not raised - all validation is handled with user prompts and retries
    
    Examples:
        >>> # User enters valid information
        >>> title, author, year = get_book_details()
        Enter book title: The Hobbit
        Enter author: J.R.R. Tolkien
        Enter publication year (or press Enter for 0): 1937
        >>> title
        'The Hobbit'
        >>> author
        'J.R.R. Tolkien'
        >>> year
        1937
        
        >>> # User enters invalid data (demonstrated)
        >>> title, author, year = get_book_details()
        Enter book title:           # User pressed Enter (empty)
        ❌ Title cannot be empty. Please try again.
        Enter book title: 1984      # Valid
        Enter author: George Orwell # Valid
        Enter publication year (or press Enter for 0): abc  # Invalid
        ❌ 'abc' is not a valid number. Please enter a year or press Enter.
        Enter publication year (or press Enter for 0): 1949   # Valid
        >>> (title, author, year)
        ('1984', 'George Orwell', 1949)
    
    Notes:
        - Input is automatically stripped of leading/trailing whitespace
        - For year field, pressing Enter sets year to 0 (useful for unknown dates)
        - The function uses a loop to ensure all inputs are valid before returning
        - Error messages include specific guidance (e.g., "too long", "non-numeric")
    """
    # Get and validate title
    while True:
        title = input("Enter book title: ").strip()
        
        if not title:
            print("❌ Title cannot be empty. Please try again.")
            continue
        
        if len(title) > 100:
            print("❌ Title is too long (max 100 characters). Please try again.")
            continue
        
        break
    
    # Get and validate author
    while True:
        author = input("Enter author: ").strip()
        
        if not author:
            print("❌ Author cannot be empty. Please try again.")
            continue
        
        if len(author) > 100:
            print("❌ Author name is too long (max 100 characters). Please try again.")
            continue
        
        break
    
    # Get and validate year
    while True:
        year_input = input("Enter publication year (or press Enter for 0): ").strip()
        
        if not year_input:
            year = 0
            break
        
        try:
            year = int(year_input)
            if year < 0:
                print("❌ Year cannot be negative. Please try again.")
                continue
            if year > 2100:
                confirm = input(f"⚠️  Year {year} seems very far in the future. Continue? (y/n): ").strip().lower()
                if confirm == "y":
                    break
                continue
            break
        except ValueError:
            print(f"❌ '{year_input}' is not a valid number. Please enter a year or press Enter.")

    return title, author, year


def print_books(books: List[Book]) -> None:
    """
    Display all books in a formatted table.
    
    Args:
        books: List of Book objects to display
    """
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")


def get_book_statistics(books: List[Book]) -> Dict[str, Any]:
    """
    Calculate statistics about a collection of books.
    
    Args:
        books: List of Book objects to analyze
    
    Returns:
        Dictionary containing:
        - total_count: Total number of books
        - read_count: Number of books marked as read
        - unread_count: Number of unread books
        - oldest_book: Book object with the earliest year (or None if empty)
        - newest_book: Book object with the latest year (or None if empty)
    
    Example:
        >>> stats = get_book_statistics(my_books)
        >>> print(f"Read {stats['read_count']} of {stats['total_count']} books")
    """
    if not books:
        return {
            "total_count": 0,
            "read_count": 0,
            "unread_count": 0,
            "oldest_book": None,
            "newest_book": None,
        }
    
    total = len(books)
    read_count = sum(1 for book in books if book.read)
    unread_count = total - read_count
    
    oldest_book = min(books, key=lambda b: b.year)
    newest_book = max(books, key=lambda b: b.year)
    
    return {
        "total_count": total,
        "read_count": read_count,
        "unread_count": unread_count,
        "oldest_book": oldest_book,
        "newest_book": newest_book,
    }
