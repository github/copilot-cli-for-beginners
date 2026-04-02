import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"

logger = logging.getLogger(__name__)


@dataclass
class Book:
    """Represents a single book in the collection.

    Attributes:
        title: Book title (non-empty string).
        author: Book author (non-empty string).
        year: Publication year (1000–2100, or 0 for unknown).
        read: Whether the book has been read.
        rating: Optional rating from 1 to 5.
        review: Optional review text.
    """

    title: str
    author: str
    year: int
    read: bool = False
    rating: Optional[int] = None
    review: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate and normalise book fields after initialisation.

        Raises:
            ValueError: If title or author is empty, year is out of range,
                rating is not between 1 and 5, or review is not a string.
        """
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title must be a non-empty string")
        if not isinstance(self.author, str) or not self.author.strip():
            raise ValueError("Author must be a non-empty string")
        if not isinstance(self.year, int) or (self.year != 0 and (self.year < 1000 or self.year > 2100)):
            raise ValueError("Year must be 0 (unknown) or an integer between 1000 and 2100")
        if self.rating is not None and (not isinstance(self.rating, int) or self.rating < 1 or self.rating > 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if self.review is not None and not isinstance(self.review, str):
            raise ValueError("Review must be a string")

        # Normalize whitespace
        self.title = self.title.strip()
        self.author = self.author.strip()
        if self.review:
            self.review = self.review.strip()


class BookCollection:
    """Manages a collection of books backed by a JSON file.

    Books are loaded from data.json on initialisation and saved back
    after every mutating operation.
    """

    def __init__(self) -> None:
        """Initialise an empty collection and load books from disk."""
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file into memory.

        If the file does not exist, the collection starts empty. If the
        file is corrupted, a warning is logged and the collection starts
        empty. Invalid individual records are skipped with a warning.
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.books = []
            return
        except json.JSONDecodeError:
            logger.warning("data.json is corrupted. Starting with empty collection.")
            self.books = []
            return

        loaded = []
        for record in data:
            try:
                loaded.append(Book(**record))
            except (KeyError, ValueError, TypeError) as exc:
                logger.warning("Skipping invalid book record %r: %s", record, exc)
        self.books = loaded

    def save_books(self) -> None:
        """Save the current book collection to JSON.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
        except (IOError, OSError) as exc:
            logger.error("Failed to save books: %s", exc)
            raise

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection.
        
        Args:
            title: Book title (non-empty string).
            author: Book author (non-empty string).
            year: Publication year (1000–2100).
            
        Returns:
            The created Book object
            
        Raises:
            ValueError: If book data is invalid
        """
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books in the collection.
        
        Returns:
            List of all Book objects
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title (case-insensitive).
        
        Args:
            title: The book title to search for
            
        Returns:
            Book object if found, None otherwise
        """
        return next(
            (b for b in self.books if b.title.lower() == title.lower()),
            None
        )

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read.
        
        Args:
            title: The title of the book to mark as read
            
        Returns:
            True if book was found and updated, False otherwise
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title.

        Args:
            title: The title of the book to remove

        Returns:
            True if book was found and removed, False otherwise
        """
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def set_rating(self, title: str, rating: int, review: Optional[str] = None) -> bool:
        """Set or update a book's rating and optional review.

        Args:
            title: The title of the book to rate.
            rating: Rating value (1–5).
            review: Optional review text.

        Returns:
            True if book was found and rated, False otherwise.

        Raises:
            ValueError: If rating is not between 1 and 5.
            ValueError: If review is not a string.
        """
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        if review is not None and not isinstance(review, str):
            raise ValueError("Review must be a string")

        book = self.find_book_by_title(title)
        if book:
            book.rating = rating
            book.review = review.strip() if review else None
            self.save_books()
            return True
        return False

    def get_rating(self, title: str) -> Optional[int]:
        """Get a book's rating.

        Args:
            title: The title of the book

        Returns:
            The rating (1-5) or None if not rated
        """
        book = self.find_book_by_title(title)
        return book.rating if book else None

    def get_review(self, title: str) -> Optional[str]:
        """Get a book's review.

        Args:
            title: The title of the book

        Returns:
            The review text or None if no review exists
        """
        book = self.find_book_by_title(title)
        return book.review if book else None

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books whose author field contains the given string (case-insensitive).
        
        Args:
            author: The author name to search for
            
        Returns:
            List of books by the specified author
        """
        return [b for b in self.books if author.lower() in b.author.lower()]

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books published between start and end year (inclusive).

        Args:
            start: The start year of the range
            end: The end year of the range

        Returns:
            List of books whose publication year falls within [start, end]

        Raises:
            ValueError: If start or end are not valid years, or start > end
        """
        if not isinstance(start, int) or start < 1000 or start > 2100:
            raise ValueError("start must be an integer between 1000 and 2100")
        if not isinstance(end, int) or end < 1000 or end > 2100:
            raise ValueError("end must be an integer between 1000 and 2100")
        if start > end:
            raise ValueError("start year must not be greater than end year")
        return [b for b in self.books if start <= b.year <= end]
