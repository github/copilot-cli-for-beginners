import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    """
    Represents a single book in the collection.
    
    Attributes:
        title (str): The book's title (case-sensitive, non-empty)
        author (str): The book's author name (case-sensitive, non-empty)
        year (int): The book's publication year (typically 1000-2100)
        read (bool): Whether the book has been read. Defaults to False (unread)
    
    Example:
        >>> book1 = Book("1984", "George Orwell", 1949)
        >>> print(book1.read)
        False
        
        >>> book2 = Book("The Hobbit", "J.R.R. Tolkien", 1937, read=True)
        >>> print(book2.read)
        True
    """
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> bool:
        """
        Save the current book collection to JSON file with error handling.
        
        Attempts to write the collection to data.json. Handles various error conditions:
        - Permission denied (no write access to file)
        - Disk full (no space available)
        - File system errors (I/O issues)
        
        Args:
            None
        
        Returns:
            bool: True if save was successful, False if an error occurred
        
        Example:
            >>> collection = BookCollection()
            >>> success = collection.save_books()
            >>> if success:
            ...     print("Books saved successfully")
        """
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
            return True
        except PermissionError:
            print(f"Error: Permission denied. Cannot write to {DATA_FILE}.")
            return False
        except OSError as e:
            print(f"Error: Unable to save books. {e}")
            return False
        except Exception as e:
            print(f"Error: Unexpected error while saving. {e}")
            return False

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Add a new book to the collection with validation.
        
        Validates input before creating and storing a Book object:
        - Title: Cannot be empty or whitespace-only
        - Author: Cannot be empty or whitespace-only
        - Year: Must be an integer between 1000 and 2100
        
        Args:
            title (str): The book's title
            author (str): The book's author
            year (int): The book's publication year
        
        Returns:
            Book: The newly created Book object that was added to the collection
        
        Raises:
            ValueError: If title is empty, author is empty, or year is out of range
        
        Example:
            >>> collection = BookCollection()
            >>> book = collection.add_book("1984", "George Orwell", 1949)
            >>> len(collection.list_books())
            1
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace-only.")
        
        # Validate author
        if not author or not author.strip():
            raise ValueError("Author cannot be empty or whitespace-only.")
        
        # Validate year
        if not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        if not (1000 <= year <= 2100):
            raise ValueError("Year must be between 1000 and 2100.")
        
        book = Book(title=title.strip(), author=author.strip(), year=year)
        self.books.append(book)
        
        if not self.save_books():
            self.books.pop()  # Remove book if save failed
            raise ValueError("Failed to save book to file.")
        
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title."""
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            return self.save_books()
        return False

    def mark_as_unread(self, title: str) -> bool:
        """Mark a book as unread by title."""
        book = self.find_book_by_title(title)
        if book:
            book.read = False
            return self.save_books()
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            if not self.save_books():
                self.books.append(book)  # Restore book if save failed
                return False
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
