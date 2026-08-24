import json
import os
import tempfile
from dataclasses import dataclass, asdict
from typing import List, Optional

# Resolve relative to this module's directory so the app works regardless
# of the current working directory it's launched from.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


@dataclass
class Book:
    """A single book in the collection.

    Attributes:
        title (str): The book's title. Used as the unique identifier
            within a `BookCollection` (matched case-insensitively).
        author (str): The book's author.
        year (int): The book's publication year.
        read (bool): Whether the book has been read. Defaults to
            ``False`` for newly added books.

    Example:
        >>> book = Book(title="Dune", author="Frank Herbert", year=1965)
        >>> book.read
        False
    """

    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """An in-memory collection of `Book` objects backed by a JSON file.

    On construction, books are loaded from `DATA_FILE`. Any mutating
    method (`add_book`, `remove_book`, `mark_as_read`) persists the
    updated collection back to disk automatically.

    Example:
        >>> collection = BookCollection()
        >>> collection.add_book("Dune", "Frank Herbert", 1965)
        Book(title='Dune', author='Frank Herbert', year=1965, read=False)
    """

    def __init__(self) -> None:
        """Create a collection and load existing books from `DATA_FILE`.

        Does not raise: any problem reading or parsing `DATA_FILE` is
        handled internally by `load_books()`, which falls back to an
        empty collection and prints a warning instead of raising.
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists.

        Reads and parses `DATA_FILE`, populating `self.books`. Each
        entry is parsed independently: a single malformed or
        wrong-typed entry is skipped (with a warning) rather than
        discarding the entire collection, and duplicate titles are
        skipped to preserve the uniqueness invariant enforced by
        `add_book()`. Records that violate business rules but are
        otherwise well-formed (e.g. a blank author or a year of 0)
        are still loaded -- those are data quality issues to surface
        elsewhere, not reasons to hide the record.

        Args:
            None.

        Returns:
            None. Populates `self.books` as a side effect.

        Raises:
            Does not raise. If `DATA_FILE` is missing, corrupted,
            unreadable, or not a JSON list, a warning is printed and
            `self.books` is set to an empty list.

        Example:
            >>> collection = BookCollection()  # calls load_books() internally
            >>> collection.load_books()  # can also be called to reload
        """
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.books = []
            return
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []
            return
        except OSError as e:
            print(
                f"Warning: could not read data.json ({e}). "
                "Starting with empty collection."
            )
            self.books = []
            return

        if not isinstance(data, list):
            print(
                "Warning: data.json does not contain a list of books. "
                "Starting with empty collection."
            )
            self.books = []
            return

        books: List[Book] = []
        seen_titles: set[str] = set()
        for index, record in enumerate(data):
            book = self._parse_book_record(record, index)
            if book is None:
                continue

            key = book.title.lower()
            if key in seen_titles:
                print(
                    f"Warning: skipping duplicate book '{book.title}' "
                    f"at entry {index}."
                )
                continue

            seen_titles.add(key)
            books.append(book)

        self.books = books

    @staticmethod
    def _parse_book_record(record: object, index: int) -> Optional[Book]:
        """Validate and construct a `Book` from one raw JSON record.

        This only checks structural correctness (right shape, right
        types), not business rules, so records with blank fields or
        out-of-range values (e.g. an empty author or year of 0) still
        load successfully. Use `add_book()`'s validation if you need
        to enforce those business rules.

        Args:
            record (object): The raw, already-JSON-decoded value for
                one entry (expected to be a `dict` with `title`,
                `author`, `year`, and optionally `read` keys).
            index (int): The entry's position in the source list, used
                only for warning messages.

        Returns:
            Optional[Book]: The parsed `Book` if `record` is shaped
            like a book, otherwise `None`.

        Raises:
            Does not raise. Invalid records print a warning to stdout
            and return `None` instead.

        Example:
            >>> BookCollection._parse_book_record(
            ...     {"title": "Dune", "author": "Frank Herbert", "year": 1965},
            ...     index=0,
            ... )
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> BookCollection._parse_book_record({"title": "No Author"}, index=1)
            Warning: skipping entry 1 (malformed fields: ...)
        """
        if not isinstance(record, dict):
            print(f"Warning: skipping entry {index} (expected a JSON object).")
            return None

        try:
            book = Book(**record)
        except TypeError as e:
            print(f"Warning: skipping entry {index} (malformed fields: {e}).")
            return None

        if not isinstance(book.title, str) or not isinstance(book.author, str):
            print(f"Warning: skipping entry {index} (title/author must be text).")
            return None
        if not isinstance(book.year, int) or isinstance(book.year, bool):
            print(f"Warning: skipping entry {index} (year must be a whole number).")
            return None
        if not isinstance(book.read, bool):
            print(f"Warning: skipping entry {index} (read must be true/false).")
            return None

        return book

    def save_books(self) -> None:
        """Save the current book collection to JSON atomically.

        Writes to a temporary file in the same directory as
        `DATA_FILE` and then atomically replaces `DATA_FILE` with it
        (via `os.replace`), so a crash or interruption mid-write can't
        leave `DATA_FILE` partially written or corrupted.

        Args:
            None.

        Returns:
            None.

        Raises:
            OSError: If the temporary file can't be created or
                written, or if replacing `DATA_FILE` fails (e.g. due
                to a full disk or insufficient permissions). The
                temporary file is removed before the error propagates.

        Example:
            >>> collection = BookCollection()
            >>> collection.books.append(Book("Dune", "Frank Herbert", 1965))
            >>> collection.save_books()
        """
        directory = os.path.dirname(DATA_FILE) or "."
        fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
            os.replace(temp_path, DATA_FILE)
        except OSError:
            os.remove(temp_path)
            raise

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and persist it.

        Args:
            title (str): The book's title. Leading/trailing whitespace
                is stripped; must be non-empty after stripping.
            author (str): The book's author. Leading/trailing
                whitespace is stripped; must be non-empty after
                stripping.
            year (int): The book's publication year. Must be a
                positive integer (booleans are rejected, since `bool`
                is a subclass of `int` in Python).

        Returns:
            Book: The newly created and persisted `Book`.

        Raises:
            ValueError: If title/author are blank, year is not a
                positive integer, or a book with the same title
                (case-insensitive) already exists.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> collection.add_book("Dune", "Someone Else", 1970)
            Traceback (most recent call last):
                ...
            ValueError: A book titled 'Dune' already exists.
        """
        title = title.strip()
        author = author.strip()

        if not title:
            raise ValueError("Title cannot be empty.")
        if not author:
            raise ValueError("Author cannot be empty.")
        if not isinstance(year, int) or isinstance(year, bool) or year <= 0:
            raise ValueError("Year must be a positive integer.")
        if self.find_book_by_title(title) is not None:
            raise ValueError(f"A book titled '{title}' already exists.")

        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return a copy of all books in the collection.

        A copy (shallow, new list) is returned so callers can't
        accidentally mutate the collection's internal `self.books`
        list by appending/removing from the returned list; the `Book`
        objects themselves are still shared references.

        Args:
            None.

        Returns:
            List[Book]: A new list containing all books, in the same
            order as stored internally (insertion order).

        Raises:
            Does not raise.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> [b.title for b in collection.list_books()]
            ['Dune']
        """
        return list(self.books)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by its exact title, ignoring case.

        Args:
            title (str): The title to search for. Compared
                case-insensitively against each book's `title`.

        Returns:
            Optional[Book]: The matching `Book`, or `None` if no book
            with that title exists.

        Raises:
            Does not raise.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> collection.find_book_by_title("dune").author
            'Frank Herbert'
            >>> collection.find_book_by_title("Missing") is None
            True
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read and persist the change.

        Args:
            title (str): The title of the book to mark as read,
                matched case-insensitively via `find_book_by_title`.

        Returns:
            bool: `True` if a matching book was found and marked as
            read; `False` if no book with that title exists.

        Raises:
            Does not raise directly, but propagates `OSError` from
            `save_books()` if persisting the change fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> collection.mark_as_read("Dune")
            True
            >>> collection.mark_as_read("Nonexistent")
            False
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
            title (str): The title of the book to remove, matched
                case-insensitively via `find_book_by_title`.

        Returns:
            bool: `True` if a matching book was found and removed;
            `False` if no book with that title exists.

        Raises:
            Does not raise directly, but propagates `OSError` from
            `save_books()` if persisting the change fails.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> collection.remove_book("Dune")
            True
            >>> collection.remove_book("Dune")
            False
        """
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Return all books written by the given author.

        Args:
            author (str): The author name to search for. Compared
                case-insensitively against each book's `author`.

        Returns:
            List[Book]: All books whose `author` matches, in
            collection order. Empty if none match.

        Raises:
            Does not raise.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> [b.title for b in collection.find_by_author("frank herbert")]
            ['Dune']
        """
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """List all books published within a year range (inclusive).

        Args:
            start (int): The earliest publication year to include.
            end (int): The latest publication year to include. Callers
                are responsible for ensuring `start <= end`; if
                `start > end`, no books will match.

        Returns:
            List[Book]: All books with `start <= book.year <= end`, in
            collection order. Empty if none match.

        Raises:
            Does not raise.

        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
            >>> [b.title for b in collection.list_by_year(1960, 1970)]
            ['Dune']
        """
        return [b for b in self.books if start <= b.year <= end]
