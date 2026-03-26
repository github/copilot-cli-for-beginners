from __future__ import annotations

import json
import logging
import os
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


DATA_FILE = "data.json"


class BookError(Exception):
    """Base exception for book app errors."""


class BookNotFoundError(BookError):
    """Raised when a book is not found."""


class BookValidationError(BookError):
    """Raised when input validation fails."""


class StorageError(BookError):
    """Raised when data cannot be read or written."""


@dataclass
class Book:
    """A single book entry in the collection.

    Represents a book with its metadata and read status. Used as
    the core data model throughout the BookCollection system.

    Attributes:
        title: The title of the book.
        author: The name of the book's author.
        year: The publication year of the book.
        read: Whether the book has been read. Defaults to False.

    Example:
        >>> book = Book(title="1984", author="George Orwell", year=1949)
        >>> book.read
        False
    """

    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self, data_file: str = DATA_FILE) -> None:
        """Initialize a BookCollection backed by a JSON file.

        Creates a new collection and loads any existing books from the
        specified data file. If the file does not exist, the collection
        starts empty.

        Args:
            data_file: Path to the JSON file used for persistence.
                Defaults to "data.json".

        Example:
            >>> collection = BookCollection()
            >>> collection = BookCollection("my_books.json")
        """
        self.data_file = data_file
        self.books: list[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON data file into memory.

        Reads the JSON file and populates ``self.books`` with ``Book``
        instances. Handles missing files (empty collection), corrupted
        JSON, type errors, and I/O failures gracefully.

        Example:
            >>> collection = BookCollection("library.json")
            >>> collection.load_books()
        """
        try:
            data = self._read_json()
            self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except (json.JSONDecodeError, TypeError, OSError):
            logger.warning("Data file is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Persist the current book collection to the JSON data file.

        Serialises every ``Book`` to a dictionary and writes the result
        as formatted JSON, overwriting any previous content.

        Raises:
            StorageError: If the file cannot be written.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.save_books()
        """
        try:
            self._write_json([asdict(b) for b in self.books])
        except OSError as e:
            raise StorageError(f"Could not save to {self.data_file}: {e}") from e

    def _read_json(self) -> list[dict]:
        """Read and parse the JSON data file.

        Returns:
            A list of dictionaries representing book data.

        Raises:
            FileNotFoundError: If the data file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
            OSError: If the file cannot be read.
        """
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, data: list[dict]) -> None:
        """Write data to the JSON file atomically.

        Writes to a temporary file first, then replaces the original
        to avoid data corruption on write failures.

        Args:
            data: A list of dictionaries to serialize as JSON.

        Raises:
            OSError: If the file cannot be written.
        """
        import os
        tmp_fd, tmp_file = tempfile.mkstemp(
            dir=os.path.dirname(self.data_file) or ".",
            suffix=".tmp",
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_file, self.data_file)
        except BaseException:
            os.unlink(tmp_file)
            raise

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and persist the change.

        Creates a ``Book`` instance, appends it to the collection, and
        saves to disk.

        Args:
            title: The book's title. Must not be empty or whitespace-only.
            author: The author's name. Must not be empty or whitespace-only.
            year: The publication year. Must be between 0 and current year + 1.

        Returns:
            The newly created ``Book`` instance.

        Raises:
            BookValidationError: If ``title`` or ``author`` is empty,
                or if ``year`` is negative or later than next year.
            StorageError: If the collection cannot be saved to disk.

        Example:
            >>> collection = BookCollection()
            >>> book = collection.add_book("1984", "George Orwell", 1949)
            >>> book.title
            '1984'
        """
        if not title.strip():
            raise BookValidationError("Title cannot be empty")
        if not author.strip():
            raise BookValidationError("Author cannot be empty")
        if year < 0:
            raise BookValidationError("Year cannot be negative")
        if year > datetime.now().year + 1:
            raise BookValidationError(f"Year cannot be later than {datetime.now().year + 1}")
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> list[Book]:
        """Return all books in the collection.

        Returns:
            A list of all ``Book`` instances. Returns an empty list if
            the collection is empty.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> len(collection.list_books())
            1
        """
        return self.books

    def find_by_title(self, title: str) -> Book | None:
        """Find a book by its title (case-insensitive).

        Args:
            title: The title to search for.

        Returns:
            The matching ``Book``, or ``None`` if not found.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.find_by_title("1984").author
            'George Orwell'
            >>> collection.find_by_title("Unknown") is None
            True
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by its title.

        The search is case-insensitive and leading/trailing whitespace
        in the provided title is stripped before matching.

        Args:
            title: The title of the book (case-insensitive).
                Leading/trailing whitespace is stripped automatically.

        Returns:
            ``True`` if the book was found and marked as read.

        Raises:
            BookValidationError: If ``title`` is empty or whitespace-only.
            BookNotFoundError: If no book with the given title exists.
            StorageError: If the collection cannot be saved.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.mark_as_read("1984")
            True
        """
        stripped = title.strip()
        if not stripped:
            raise BookValidationError("Title cannot be empty")
        book = self.find_by_title(stripped)
        if not book:
            raise BookNotFoundError(f"Book not found: '{stripped}'")
        book.read = True
        self.save_books()
        return True

    def remove_book(self, title: str) -> bool:
        """Remove a book from the collection by its title.

        The search is case-insensitive and leading/trailing whitespace
        in the provided title is stripped before matching.

        Args:
            title: The title of the book to remove (case-insensitive).
                Leading/trailing whitespace is stripped automatically.

        Returns:
            ``True`` if the book was found and removed.

        Raises:
            BookValidationError: If ``title`` is empty or whitespace-only.
            BookNotFoundError: If no book with the given title exists.
            StorageError: If the collection cannot be saved.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.remove_book("1984")
            True
            >>> collection.remove_book("  1984  ")  # whitespace is stripped
            True
        """
        stripped = title.strip()
        if not stripped:
            raise BookValidationError("Title cannot be empty")
        book = self.find_by_title(stripped)
        if not book:
            raise BookNotFoundError(f"Book not found: '{stripped}'")
        self.books.remove(book)
        self.save_books()
        return True

    def find_by_author(self, author: str) -> list[Book]:
        """Find all books by a given author (case-insensitive).

        Supports partial author name matching. The search term will match
        if found anywhere within the author's full name.

        Args:
            author: The author name to search for (supports partial matches).

        Returns:
            A list of matching ``Book`` instances. Returns an empty
            list if no books are found.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.add_book("Animal Farm", "George Orwell", 1945)
            >>> len(collection.find_by_author("george orwell"))
            2
            >>> len(collection.find_by_author("Orwell"))
            2
        """
        if not author.strip():
            return []
        return [b for b in self.books if author.lower() in b.author.lower()]

    def list_by_year(self, start: int, end: int) -> list[Book]:
        """Filter books by publication year range (inclusive).

        Args:
            start: The starting year (inclusive).
            end: The ending year (inclusive). Must be >= ``start``.

        Returns:
            A list of books published between ``start`` and ``end``.

        Raises:
            BookValidationError: If ``start`` is greater than ``end``.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> results = collection.list_by_year(1940, 1960)
            >>> results[0].title
            '1984'
        """
        if start > end:
            raise BookValidationError(f"Start year ({start}) cannot be greater than end year ({end})")
        return [b for b in self.books if start <= b.year <= end]
