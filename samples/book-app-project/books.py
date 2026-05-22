from contextlib import contextmanager
from datetime import date
import json
import os
from pathlib import Path
import tempfile
from dataclasses import dataclass, asdict
from typing import IO, Iterator, List, Optional

DATA_FILE = "data.json"


def _normalize_required_text(value: str, field_name: str) -> str:
    """Trim and validate a required text value.

    Args:
        value (str): The user-provided text to normalize.
        field_name (str): The field name used in validation error messages.

    Returns:
        str: The trimmed text value.

    Raises:
        ValueError: If the trimmed value is empty.

    Examples:
        >>> _normalize_required_text("  Dune  ", "Title")
        'Dune'
        >>> _normalize_required_text("   ", "Author")
        Traceback (most recent call last):
        ...
        ValueError: Author cannot be empty.
    """
    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} cannot be empty.")
    return normalized_value


def _validate_publication_year(year: int) -> int:
    """Validate that a publication year is realistic for the sample app.

    Args:
        year (int): The publication year to validate.

    Returns:
        int: The validated year when it is within the accepted range.

    Raises:
        ValueError: If ``year`` is negative or later than the current year.

    Examples:
        >>> _validate_publication_year(1965)
        1965
        >>> _validate_publication_year(-1)
        Traceback (most recent call last):
        ...
        ValueError: Year cannot be negative.
    """
    if year < 0:
        raise ValueError("Year cannot be negative.")

    current_year = date.today().year
    if year > current_year:
        raise ValueError(f"Year cannot be in the future. Please enter a year up to {current_year}.")

    return year


@dataclass
class Book:
    """Represent a single book in the collection.

    Attributes:
        title (str): The book title.
        author (str): The author name.
        year (int): The publication year.
        read (bool): Whether the book has been marked as read.

    Examples:
        >>> Book(title="Dune", author="Frank Herbert", year=1965)
        Book(title='Dune', author='Frank Herbert', year=1965, read=False)
    """
    title: str
    author: str
    year: int
    read: bool = False


@dataclass(frozen=True)
class BookOperationResult:
    """Describe the outcome of an operation on a book.

    Attributes:
        success (bool): Whether the operation completed successfully.
        message (str): A user-friendly summary of the result.

    Examples:
        >>> BookOperationResult(success=True, message="Removed the book.")
        BookOperationResult(success=True, message='Removed the book.')
    """

    success: bool
    message: str


class BookCollection:
    """Manage a collection of books stored in a JSON file."""

    def __init__(self) -> None:
        """Create a collection and load any saved books from disk.

        Returns:
            None: This initializer sets up the in-memory collection.

        Examples:
            >>> collection = BookCollection()
            >>> isinstance(collection.books, list)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    @contextmanager
    def _open_data_file(self, mode: str) -> Iterator[IO[str]]:
        """Open the JSON data file using a shared context manager.

        Args:
            mode (str): The file mode to pass to ``open()``, such as ``"r"`` or
                ``"w"``.

        Yields:
            IO[str]: An open text file handle for the collection data file.

        Examples:
            >>> collection = BookCollection()
            >>> with collection._open_data_file("r") as data_file:
            ...     hasattr(data_file, "read")
            True
        """
        with open(DATA_FILE, mode) as data_file:
            yield data_file

    def _quarantine_corrupted_file(self) -> Path:
        """Rename an unreadable data file to a safe backup path.

        Returns:
            Path: The new path of the quarantined file.

        Raises:
            OSError: If the file cannot be renamed.

        Examples:
            >>> collection = BookCollection()
            >>> backup_path = Path("data.corrupted.json")
            >>> isinstance(backup_path, Path)
            True
        """
        data_path = Path(DATA_FILE)
        backup_path = data_path.with_name(f"{data_path.stem}.corrupted{data_path.suffix}")
        counter = 1

        while backup_path.exists():
            backup_path = data_path.with_name(
                f"{data_path.stem}.corrupted-{counter}{data_path.suffix}"
            )
            counter += 1

        os.replace(data_path, backup_path)
        return backup_path

    def _load_book_data(self) -> List[Book]:
        """Validate and convert raw JSON entries into ``Book`` objects.

        Returns:
            List[Book]: The validated books loaded from the JSON file.

        Raises:
            ValueError: If the JSON structure or any book entry is invalid.

        Examples:
            >>> collection = BookCollection()
            >>> isinstance(collection._load_book_data(), list)
            True
        """
        with self._open_data_file("r") as data_file:
            data = json.load(data_file)

        if not isinstance(data, list):
            raise ValueError("Expected a list of books.")

        loaded_books: List[Book] = []
        for index, book_data in enumerate(data, start=1):
            if not isinstance(book_data, dict):
                raise ValueError(f"Book entry #{index} must be an object.")

            try:
                loaded_books.append(Book(**book_data))
            except TypeError as exc:
                raise ValueError(f"Book entry #{index} has invalid fields.") from exc

        return loaded_books

    def load_books(self) -> None:
        """Load books from the JSON data file into the collection.

        If the file does not exist or contains invalid JSON, the collection
        starts empty.

        Returns:
            None: The loaded books are assigned to ``self.books``.

        Examples:
            >>> collection = BookCollection()
            >>> collection.load_books()
        """
        try:
            self.books = self._load_book_data()
        except FileNotFoundError:
            self.books = []
        except (json.JSONDecodeError, ValueError) as exc:
            self.books = []
            backup_path = self._quarantine_corrupted_file()
            print(
                "Warning: data.json is corrupted or invalid. "
                f"The unreadable file was moved to {backup_path.name}. "
                "Starting with empty collection."
            )

    def save_books(self) -> None:
        """Write the current book collection to the JSON data file.

        Returns:
            None: The method persists the current collection to disk.

        Raises:
            OSError: If the data file cannot be written.
            TypeError: If a book entry cannot be serialized to JSON.

        Examples:
            >>> collection = BookCollection()
            >>> collection.save_books()
        """
        data_path = Path(DATA_FILE)
        data_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=data_path.parent,
            delete=False,
        ) as temp_file:
            json.dump([asdict(b) for b in self.books], temp_file, indent=2)
            temp_file.write("\n")
            temp_file_path = Path(temp_file.name)

        os.replace(temp_file_path, data_path)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and save the updated data.

        Args:
            title (str): The title of the book to add.
            author (str): The author of the book to add.
            year (int): The publication year of the book.

        Returns:
            Book: The newly created ``Book`` instance.

        Raises:
            ValueError: If ``title`` or ``author`` is empty after trimming, or
                if ``year`` is negative.
            OSError: If the updated collection cannot be written to disk.
            TypeError: If the updated collection cannot be serialized to JSON.

        Examples:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> book.title
            'Dune'
        """
        normalized_title = _normalize_required_text(title, "Title")
        normalized_author = _normalize_required_text(author, "Author")

        validated_year = _validate_publication_year(year)

        book = Book(title=normalized_title, author=normalized_author, year=validated_year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books currently stored in the collection.

        Returns:
            List[Book]: The in-memory list of books.

        Examples:
            >>> collection = BookCollection()
            >>> books = collection.list_books()
            >>> isinstance(books, list)
            True
        """
        return self.books

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books published within an inclusive year range.

        Args:
            start (int): The earliest publication year to include.
            end (int): The latest publication year to include.

        Returns:
            List[Book]: Books whose publication year falls between ``start``
            and ``end``, inclusive.

        Examples:
            >>> collection = BookCollection()
            >>> collection.list_by_year(2000, 2020)
            []
        """
        return [book for book in self.books if start <= book.year <= end]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find the first book whose title matches case-insensitively.

        Args:
            title (str): The title to search for.

        Returns:
            Optional[Book]: The matching book if found; otherwise, ``None``.

        Examples:
            >>> collection = BookCollection()
            >>> collection.find_book_by_title("Dune") is None
            True
        """
        normalized_title = title.strip()
        if not normalized_title:
            return None

        normalized_query = normalized_title.casefold()
        for book in self.books:
            if book.title.casefold() == normalized_query:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read when a matching title is found.

        Args:
            title (str): The title of the book to mark as read.

        Returns:
            bool: ``True`` if a matching book was updated; otherwise, ``False``.

        Raises:
            OSError: If the updated collection cannot be written to disk.
            TypeError: If the updated collection cannot be serialized to JSON.

        Examples:
            >>> collection = BookCollection()
            >>> collection.mark_as_read("Dune")
            False
        """
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> BookOperationResult:
        """Remove the first book whose title matches case-insensitively.

        Args:
            title (str): The title of the book to remove.

        Returns:
            BookOperationResult: Describes whether a book was removed and why.

        Raises:
            ValueError: If ``title`` is empty after trimming.
            OSError: If the updated collection cannot be written to disk.
            TypeError: If the updated collection cannot be serialized to JSON.

        Examples:
            >>> collection = BookCollection()
            >>> collection.remove_book("Dune").success
            False
        """
        normalized_title = _normalize_required_text(title, "Title")
        book = self.find_book_by_title(normalized_title)
        if book:
            self.books.remove(book)
            self.save_books()
            return BookOperationResult(
                success=True,
                message=f'Removed "{book.title}" from the collection.',
            )

        partial_matches = [
            candidate.title
            for candidate in self.books
            if normalized_title.casefold() in candidate.title.casefold()
        ]
        if partial_matches:
            suggestions = ", ".join(f'"{title}"' for title in partial_matches)
            return BookOperationResult(
                success=False,
                message=(
                    f'No exact match found for "{normalized_title}". '
                    f"Try one of these full titles: {suggestions}."
                ),
            )

        return BookOperationResult(
            success=False,
            message=f'Book "{normalized_title}" was not found in the collection.',
        )

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books written by a given author.

        Args:
            author (str): The author name to match case-insensitively.

        Returns:
            List[Book]: All books whose author matches the supplied name.

        Examples:
            >>> collection = BookCollection()
            >>> collection.find_by_author("Frank Herbert")
            []
        """
        return [b for b in self.books if b.author.lower() == author.lower()]
