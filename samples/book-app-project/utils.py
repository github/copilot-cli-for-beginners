from typing import List, Tuple, Dict, Optional, Any
from books import Book


# ============================================================================
# Validation Functions (pure logic, no I/O)
# ============================================================================

def validate_choice(choice: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a menu choice.
    
    Args:
        choice: User input to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not choice:
        return False, "Empty input. Please enter a number between 1 and 5."
    
    if not choice.isdigit():
        return False, "Invalid input. Please enter a number (not letters or symbols)."
    
    if choice not in ["1", "2", "3", "4", "5"]:
        return False, "Invalid choice. Please enter a number between 1 and 5."
    
    return True, None


def validate_title(title: str) -> Tuple[bool, Optional[str]]:
    """Validate a book title."""
    if not title:
        return False, "Title cannot be empty. Please try again."
    
    if len(title) > 100:
        return False, "Title is too long (max 100 characters). Please try again."
    
    return True, None


def validate_author(author: str) -> Tuple[bool, Optional[str]]:
    """Validate an author name."""
    if not author:
        return False, "Author cannot be empty. Please try again."
    
    if len(author) > 100:
        return False, "Author name is too long (max 100 characters). Please try again."
    
    return True, None


def validate_year(year_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Validate a year input.
    
    Returns:
        Tuple of (is_valid, year_value, error_message)
    """
    if not year_str:
        return True, 0, None
    
    try:
        year = int(year_str)
        if year < 0:
            return False, None, "Year cannot be negative. Please try again."
        if year > 2100:
            return True, year, "year_future"
        return True, year, None
    except ValueError:
        return False, None, f"'{year_str}' is not a valid number. Please enter a year or press Enter."


# ============================================================================
# Display Functions (pure output, no logic)
# ============================================================================

def print_menu() -> None:
    """Display the main menu options."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def print_error(message: str) -> None:
    """Print an error message with indicator."""
    print(f"❌ {message}")


def print_warning(message: str) -> None:
    """Print a warning message with indicator."""
    print(f"⚠️  {message}")


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


# ============================================================================
# Input Functions (combine validation and display)
# ============================================================================

def get_user_choice() -> str:
    """
    Get user menu choice with validation.
    
    Returns:
        Valid menu choice as string (1-5)
    """
    while True:
        choice = input("Choose an option (1-5): ").strip()
        is_valid, error_msg = validate_choice(choice)
        
        if is_valid:
            return choice
        
        print_error(error_msg)


def get_book_title() -> str:
    """Get and validate a book title from user."""
    while True:
        title = input("Enter book title: ").strip()
        is_valid, error_msg = validate_title(title)
        
        if is_valid:
            return title
        
        print_error(error_msg)


def get_book_author() -> str:
    """Get and validate an author name from user."""
    while True:
        author = input("Enter author: ").strip()
        is_valid, error_msg = validate_author(author)
        
        if is_valid:
            return author
        
        print_error(error_msg)


def get_book_year() -> int:
    """Get and validate a publication year from user."""
    while True:
        year_input = input("Enter publication year (or press Enter for 0): ").strip()
        is_valid, year, error_msg = validate_year(year_input)
        
        if error_msg == "year_future":
            confirm = input(f"Year {year} seems very far in the future. Continue? (y/n): ").strip().lower()
            if confirm == "y":
                return year
            continue
        
        if is_valid:
            return year
        
        print_error(error_msg)


def get_book_details() -> Tuple[str, str, int]:
    """
    Interactively prompt user for book information with comprehensive validation.
    
    Returns:
        Tuple of (title, author, year)
    """
    title = get_book_title()
    author = get_book_author()
    year = get_book_year()
    
    return title, author, year


# ============================================================================
# Data Processing Functions (pure logic, no I/O)
# ============================================================================

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
