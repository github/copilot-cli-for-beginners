import json
import os
import tempfile
from dataclasses import dataclass, asdict
from typing import List, Optional, Iterable

DATA_FILE = "data.json"


@dataclass
class Book:
    """Represents a single book in the collection.

    Attributes:
        title (str): Book title.
        author (str): Author name.
        year (int): Publication year.
        read (bool): Whether the book has been read.

    Example:
        >>> Book(title='Dune', author='Frank Herbert', year=1965)
    """
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self, data_file: str = DATA_FILE) -> None:
        """Initialize the BookCollection.

        Args:
            data_file (str): Path to the JSON data file. Defaults to DATA_FILE.

        Side effects:
            Loads existing books from disk into memory via load_books().

        Example:
            >>> col = BookCollection('test_data.json')
        """
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file into memory.

        Reads the JSON array stored at self.data_file and converts each valid
        record into a Book instance. Invalid records are skipped with a warning.

        Returns:
            None

        Raises:
            StorageError: If an I/O error occurs while reading the file (propagated
                from utils.safe_load_json).

        Example:
            >>> col = BookCollection('books.json')
            >>> col.load_books()
        """
        from utils import safe_load_json, log_warn

        data = safe_load_json(self.data_file, default=[])

        if not isinstance(data, Iterable):
            log_warn(f"{self.data_file} does not contain a list. Starting with empty collection.")
            self.books = []
            return

        loaded: List[Book] = []
        bad = 0
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                bad += 1
                continue
            # Extract fields with defaults and attempt conversions
            title = item.get("title")
            author = item.get("author", "")
            year = item.get("year", 0)
            read = item.get("read", False)

            if not isinstance(title, str) or not title.strip():
                bad += 1
                continue
            try:
                year = int(year)
            except (TypeError, ValueError):
                # fallback to 0 if year cannot be parsed
                year = 0
            read = bool(read)
            loaded.append(Book(title=title.strip(), author=str(author), year=year, read=read))

        if bad:
            from utils import log_warn

            log_warn(f"skipped {bad} invalid record(s) in {self.data_file}.")
        self.books = loaded

    def save_books(self) -> None:
        """Persist the current in-memory books to disk atomically.

        Uses utils.atomic_write_json to perform an atomic replace of the
        underlying data file. Any errors encountered are logged; callers should
        not generally need to catch exceptions here unless they need special
        handling.

        Returns:
            None

        Raises:
            StorageError: If writing to disk fails (propagated from utils.atomic_write_json).

        Example:
            >>> col.save_books()
        """
        from utils import atomic_write_json, log_error

        success = atomic_write_json(self.data_file, [asdict(b) for b in self.books])
        if not success:
            log_error(f"failed to save books to {self.data_file}")

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and persist it.

        Args:
            title (str): Title of the book. Must be non-empty.
            author (str): Author name (may be empty).
            year (int): Publication year. Use 0 if unknown.

        Returns:
            Book: The Book instance that was added.

        Raises:
            ValueError: If title is empty.
            StorageError: If persisting the new book to disk fails.

        Example:
            >>> col.add_book('Dune', 'Frank Herbert', 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
        """
        if not title or not title.strip():
            raise ValueError("title must be a non-empty string")
        book = Book(title=title.strip(), author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books currently in the collection.

        Returns:
            List[Book]: Shallow list of Book instances in insertion order.

        Example:
            >>> col.list_books()
        """
        return self.books

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books published between start and end year (inclusive).

        Args:
            start (int): Lower bound year (inclusive).
            end (int): Upper bound year (inclusive).

        Returns:
            List[Book]: Books whose year is between start and end, preserving insertion order.
        """
        if start > end:
            raise ValueError("start year must be less than or equal to end year")

        results: List[Book] = []
        for b in self.books:
            if start <= b.year <= end:
                results.append(b)
        return results

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by exact title (case-insensitive).

        Args:
            title (str): Title to match.

        Returns:
            Optional[Book]: Matching Book if found, otherwise None.

        Example:
            >>> col.find_book_by_title('Dune')
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark the book with the given title as read and persist the change.

        Args:
            title (str): Title of the book to mark as read.

        Returns:
            bool: True if a book was found and updated, False otherwise.

        Raises:
            StorageError: If saving the updated collection fails.

        Example:
            >>> col.mark_as_read('Dune')
            True
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title and persist the change.

        Args:
            title (str): Title of the book to remove.

        Returns:
            bool: True if a book was removed, False if no matching book was found.

        Raises:
            StorageError: If saving the updated collection fails.

        Example:
            >>> col.remove_book('Dune')
            True
        """
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (case-insensitive exact match).

        Args:
            author (str): Author name to match.

        Returns:
            List[Book]: Matching books (may be empty).

        Example:
            >>> col.find_by_author('Frank Herbert')
        """
        return [b for b in self.books if b.author.lower() == author.lower()]

    def search(self, query: str, fields: Optional[List[str]] = None, case_sensitive: bool = False) -> List[Book]:
        """Search books by query string within the provided fields.

        Behavior:
        - Partial substring match (default)
        - Case-insensitive by default
        - fields: list containing any of "title" or "author"; defaults to both

        Args:
            query (str): The substring to search for. If empty, returns an empty list.
            fields (Optional[List[str]]): Fields to search in; allowed values: "title", "author".
            case_sensitive (bool): Whether the search should be case-sensitive.

        Returns:
            List[Book]: Books that match the query in the requested fields.

        Raises:
            ValueError: If an invalid field name is provided in `fields`.

        Example:
            >>> col.search('dune')
        """
        if not query:
            return []
        if fields is None:
            fields = ["title", "author"]

        # Validate fields
        valid = {"title", "author"}
        for f in fields:
            if f not in valid:
                raise ValueError(f"Invalid search field: {f}")

        results: List[Book] = []
        q = query if case_sensitive else query.lower()

        for b in self.books:
            matches = False
            if "title" in fields:
                lhs = b.title if case_sensitive else b.title.lower()
                if q in lhs:
                    matches = True
            if not matches and "author" in fields:
                lhs = b.author if case_sensitive else b.author.lower()
                if q in lhs:
                    matches = True
            if matches:
                results.append(b)
        return results
