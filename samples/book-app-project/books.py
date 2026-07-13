import json
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from typing import Iterator, List, Optional, TextIO, TypedDict

from exceptions import BookNotFoundError, StorageError, ValidationError

DATA_FILE = "data.json"


@contextmanager
def _data_file(mode: str) -> Iterator[TextIO]:
    """Open `DATA_FILE`, translating I/O failures into `StorageError`.

    Centralizes file-handle management for `load_books`/`save_books` so
    neither method needs its own duplicate `open()`/`close()`/error
    handling. `FileNotFoundError` is deliberately left unconverted so
    callers (e.g. `load_books`) can treat "file missing" as a distinct,
    recoverable case rather than a storage failure.

    Args:
        mode (str): The file mode to open `DATA_FILE` with, e.g. "r"
            or "w".

    Yields:
        TextIO: The open file handle.

    Raises:
        FileNotFoundError: If `mode` is a read mode and the file does
            not exist.
        StorageError: If the file cannot be opened, read, or written
            for any other reason (e.g. permissions, disk full).

    Example:
        >>> with _data_file("r") as f:
        ...     data = json.load(f)
    """
    try:
        f = open(DATA_FILE, mode)
    except FileNotFoundError:
        raise
    except OSError as e:
        raise StorageError(f"Could not open {DATA_FILE}: {e}") from e

    try:
        yield f
    except OSError as e:
        raise StorageError(f"Could not access {DATA_FILE}: {e}") from e
    finally:
        f.close()


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookStats(TypedDict):
    total: int
    read: int
    unread: int
    oldest: Optional[Book]
    newest: Optional[Book]


def get_statistics(books: List[Book]) -> BookStats:
    """Compute summary statistics for a list of books.

    Args:
        books (List[Book]): The books to summarize. May be empty.

    Returns:
        BookStats: A dict with the following keys:
            - total (int): Total number of books.
            - read (int): Number of books marked as read.
            - unread (int): Number of books not marked as read.
            - oldest (Optional[Book]): The book with the smallest
              `year`, or `None` if `books` is empty.
            - newest (Optional[Book]): The book with the largest
              `year`, or `None` if `books` is empty.

    Raises:
        None.

    Example:
        >>> books = [
        ...     Book(title="Dune", author="Frank Herbert", year=1965, read=True),
        ...     Book(title="1984", author="George Orwell", year=1949),
        ... ]
        >>> stats = get_statistics(books)
        >>> stats["total"]
        2
        >>> stats["oldest"].title
        '1984'
    """
    if not books:
        return {"total": 0, "read": 0, "unread": 0, "oldest": None, "newest": None}

    read_count = sum(1 for book in books if book.read)

    return {
        "total": len(books),
        "read": read_count,
        "unread": len(books) - read_count,
        "oldest": min(books, key=lambda b: b.year),
        "newest": max(books, key=lambda b: b.year),
    }


class BookCollection:
    """An in-memory collection of `Book` objects backed by a JSON file.

    On construction, the collection is loaded from `DATA_FILE`. Every
    mutating method (`add_book`, `mark_as_read`, `remove_book`) persists
    the updated collection back to `DATA_FILE` before returning.
    """

    def __init__(self):
        """Create a `BookCollection` and load its books from `DATA_FILE`.

        Args:
            None.

        Returns:
            None.

        Raises:
            StorageError: If `DATA_FILE` exists but cannot be read or
                parsed. See `load_books`.

        Example:
            >>> collection = BookCollection()
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists.

        Args:
            None.

        Returns:
            None. Populates `self.books` as a side effect.

        Raises:
            StorageError: If the data file exists but cannot be parsed
                or read (e.g. corrupted JSON or a permission error).

        Example:
            >>> collection = BookCollection()
            >>> collection.load_books()
        """
        try:
            with _data_file("r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError as e:
            raise StorageError(f"{DATA_FILE} is corrupted and could not be read.") from e

    def save_books(self):
        """Save the current book collection to JSON.

        Args:
            None.

        Returns:
            None.

        Raises:
            StorageError: If the data file cannot be written (e.g. disk
                full or a permission error).

        Example:
            >>> collection = BookCollection()
            >>> collection.save_books()
        """
        with _data_file("w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and persist it.

        Args:
            title (str): The book's title. Must be non-empty after
                stripping whitespace.
            author (str): The book's author.
            year (int): The book's publication year.

        Returns:
            Book: The newly created `Book` instance that was added.

        Raises:
            ValidationError: If `title` is empty or whitespace-only.
            StorageError: If the updated collection cannot be saved.

        Example:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> book.title
            'Dune'
        """
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty.")

        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books currently in the collection.

        Args:
            None.

        Returns:
            List[Book]: The list of books, in insertion order. This is
                a live reference to `self.books`, not a copy.

        Raises:
            None.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> len(collection.list_books())
            1
        """
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title, ignoring case.

        Args:
            title (str): The title to search for. Matching is
                case-insensitive but otherwise exact.

        Returns:
            Optional[Book]: The matching `Book`, or `None` if no book
                with that title exists.

        Raises:
            None.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.find_book_by_title("dune").author
            'Frank Herbert'
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> None:
        """Mark a book as read and persist the change.

        Args:
            title (str): The title of the book to mark as read
                (case-insensitive).

        Returns:
            None.

        Raises:
            BookNotFoundError: If no book with the given title exists.
            StorageError: If the updated collection cannot be saved.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.mark_as_read("Dune")
            >>> collection.find_book_by_title("Dune").read
            True
        """
        book = self.find_book_by_title(title)
        if book is None:
            raise BookNotFoundError(f"No book titled '{title}' was found.")

        book.read = True
        self.save_books()

    def remove_book(self, title: str) -> None:
        """Remove a book by title and persist the change.

        Args:
            title (str): The title of the book to remove
                (case-insensitive).

        Returns:
            None.

        Raises:
            BookNotFoundError: If no book with the given title exists.
            StorageError: If the updated collection cannot be saved.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.remove_book("Dune")
            >>> collection.find_book_by_title("Dune") is None
            True
        """
        book = self.find_book_by_title(title)
        if book is None:
            raise BookNotFoundError(f"No book titled '{title}' was found.")

        self.books.remove(book)
        self.save_books()

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author, ignoring case.

        Args:
            author (str): The author name to search for. Matching is
                case-insensitive but otherwise exact.

        Returns:
            List[Book]: All matching books, in insertion order. Empty
                if no books match.

        Raises:
            None.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> [b.title for b in collection.find_by_author("frank herbert")]
            ['Dune']
        """
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books published within a year range, inclusive.

        Args:
            start (int): The earliest publication year to include.
            end (int): The latest publication year to include.

        Returns:
            List[Book]: All books with `start <= book.year <= end`, in
                insertion order. Empty if no books match. If `start`
                is greater than `end`, no books will match.

        Raises:
            None.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> [b.title for b in collection.list_by_year(1960, 1970)]
            ['Dune']
        """
        return [b for b in self.books if start <= b.year <= end]
