import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Iterator, List, Optional, TextIO

DATA_FILE = Path(__file__).with_name("data.json")


class BookDataError(Exception):
    """Raised when book data cannot be loaded or saved safely."""


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self) -> None:
        """Initialize the collection and load any existing books from disk.

        Parameters:
            None: This constructor does not accept additional arguments.

        Returns:
            None: The collection is initialized in place.

        Raises:
            BookDataError: If the configured JSON file exists but cannot be read
                or contains invalid book data.

        Examples:
            >>> collection = BookCollection()
            >>> isinstance(collection.books, list)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    @staticmethod
    def _normalize_text(value: str, field_name: str) -> str:
        """Validate and normalize a required text field.

        Parameters:
            value (str): The raw text value to validate and trim.
            field_name (str): The user-facing field name used in error messages.

        Returns:
            str: The trimmed text value.

        Raises:
            ValueError: If ``value`` is not a string or is empty after trimming.

        Examples:
            >>> BookCollection._normalize_text("  Dune  ", "Title")
            'Dune'
        """
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")

        return cleaned_value

    @staticmethod
    def _book_from_dict(raw_book: Any) -> Book:
        """Convert a raw dictionary into a validated ``Book`` instance.

        Parameters:
            raw_book (Any): The decoded JSON value representing one book.

        Returns:
            Book: A validated ``Book`` object with trimmed title and author.

        Raises:
            BookDataError: If the value is not a dictionary, does not match the
                expected schema, or contains invalid field values.

        Examples:
            >>> BookCollection._book_from_dict(
            ...     {"title": "Dune", "author": "Frank Herbert", "year": 1965}
            ... )
            Book(title='Dune', author='Frank Herbert', year=1965, read=False)
        """
        if not isinstance(raw_book, dict):
            raise BookDataError("Book data is invalid: each item must be an object.")

        required_fields = {"title", "author", "year"}
        optional_fields = {"read"}
        actual_fields = set(raw_book)
        missing_fields = required_fields - actual_fields
        unexpected_fields = actual_fields - required_fields - optional_fields
        if missing_fields or unexpected_fields:
            problems: list[str] = []
            if missing_fields:
                problems.append(f"missing {', '.join(sorted(missing_fields))}")
            if unexpected_fields:
                problems.append(f"unexpected {', '.join(sorted(unexpected_fields))}")
            raise BookDataError(f"Book data is invalid: {', '.join(problems)}.")

        try:
            book = Book(**raw_book)
        except TypeError as exc:
            raise BookDataError("Book data is invalid: each book must match the Book schema.") from exc

        if not isinstance(book.title, str) or not book.title.strip():
            raise BookDataError("Book data is invalid: title must be a non-empty string.")
        if not isinstance(book.author, str) or not book.author.strip():
            raise BookDataError("Book data is invalid: author must be a non-empty string.")
        if not isinstance(book.year, int) or isinstance(book.year, bool):
            raise BookDataError("Book data is invalid: year must be an integer.")
        if not isinstance(book.read, bool):
            raise BookDataError("Book data is invalid: read must be true or false.")

        return Book(title=book.title.strip(), author=book.author.strip(), year=book.year, read=book.read)

    @staticmethod
    def _find_duplicate_title(books: List[Book]) -> Optional[str]:
        """Return the first duplicate title found in a list of books.

        Parameters:
            books (List[Book]): The books to inspect for case-insensitive title
                collisions.

        Returns:
            Optional[str]: The duplicate title as stored on the later matching
            book, or ``None`` if no duplicates are present.

        Raises:
            None: This helper does not raise exceptions directly.

        Examples:
            >>> books = [
            ...     Book(title="Dune", author="Frank Herbert", year=1965),
            ...     Book(title="dune", author="Brian Herbert", year=1999),
            ... ]
            >>> BookCollection._find_duplicate_title(books)
            'dune'
        """
        seen_titles: set[str] = set()
        for book in books:
            normalized_title = book.title.casefold()
            if normalized_title in seen_titles:
                return book.title
            seen_titles.add(normalized_title)
        return None

    @staticmethod
    @contextmanager
    def _open_data_file_for_read() -> Iterator[TextIO]:
        """Open the data file for reading with consistent error handling."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as data_file:
                yield data_file
        except FileNotFoundError:
            raise
        except OSError as exc:
            raise BookDataError(f"Could not load {DATA_FILE}: {exc.strerror or exc}.") from exc

    @staticmethod
    @contextmanager
    def _open_data_file_for_write() -> Iterator[TextIO]:
        """Open the data file for writing with consistent error handling."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as data_file:
                yield data_file
        except OSError as exc:
            raise BookDataError(f"Could not save books to {DATA_FILE}: {exc.strerror or exc}.") from exc

    def load_books(self) -> None:
        """Load books from the configured JSON file into the collection.

        Parameters:
            None: This method reads from ``DATA_FILE`` and updates ``self.books``.

        Returns:
            None: The collection is updated in place.

        Raises:
            BookDataError: If the file is unreadable, is not valid JSON, does
                not contain a list of valid book objects, or includes duplicate
                titles.

        Examples:
            >>> collection = BookCollection()
            >>> collection.load_books()
        """
        try:
            with self._open_data_file_for_read() as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            self.books = []
            return
        except json.JSONDecodeError as exc:
            raise BookDataError(f"Could not load {DATA_FILE}: the file is not valid JSON.") from exc

        if not isinstance(data, list):
            raise BookDataError(f"Could not load {DATA_FILE}: expected a list of books.")

        loaded_books = [self._book_from_dict(book_data) for book_data in data]
        duplicate_title = self._find_duplicate_title(loaded_books)
        if duplicate_title is not None:
            raise BookDataError(f"Book data is invalid: duplicate title '{duplicate_title}'.")

        self.books = loaded_books

    def save_books(self, books: Optional[List[Book]] = None) -> None:
        """Save books to the configured JSON file.

        Parameters:
            books (Optional[List[Book]]): The books to persist. When omitted,
                the current in-memory ``self.books`` list is written.

        Returns:
            None: The JSON file is written as a side effect.

        Raises:
            ValueError: If a book title is not a non-empty string.
            BookDataError: If the file cannot be written.

        Examples:
            >>> collection = BookCollection()
            >>> collection.save_books()
        """
        books_to_save = self.books if books is None else books
        for book in books_to_save:
            self._normalize_text(book.title, "Title")

        with self._open_data_file_for_write() as data_file:
            json.dump([asdict(book) for book in books_to_save], data_file, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and persist the updated list.

        Parameters:
            title (str): The book title to add.
            author (str): The author's name.
            year (int): The publication year.

        Returns:
            Book: The newly created ``Book`` instance.

        Raises:
            ValueError: If the title or author is empty, the year is not a
                non-negative integer, or a matching title already exists.
            BookDataError: If the updated collection cannot be saved.

        Examples:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> book.title
            'Dune'
        """
        cleaned_title = self._normalize_text(title, "Title")
        cleaned_author = self._normalize_text(author, "Author")
        if not isinstance(year, int) or isinstance(year, bool):
            raise ValueError("Year must be an integer.")
        if year < 0:
            raise ValueError("Year cannot be negative.")
        if self._find_book_index_by_title(cleaned_title) is not None:
            raise ValueError("A book with this title already exists.")

        book = Book(title=cleaned_title, author=cleaned_author, year=year)
        updated_books = [*self.books, book]
        self.save_books(updated_books)
        self.books = updated_books
        return book

    def list_books(self) -> List[Book]:
        """Return a copy of the current book list.

        Parameters:
            None: This method reads the in-memory collection only.

        Returns:
            List[Book]: A shallow copy of the stored books in their current
            order.

        Raises:
            None: This method does not raise exceptions directly.

        Examples:
            >>> collection = BookCollection()
            >>> books = collection.list_books()
            >>> isinstance(books, list)
            True
        """
        return list(self.books)

    def get_unread_books(self) -> List[Book]:
        """Return unread books in their current order.

        Parameters:
            None: This method reads the in-memory collection only.

        Returns:
            List[Book]: A new list containing only books whose ``read`` flag is
            ``False``.

        Raises:
            None: This method does not raise exceptions directly.

        Examples:
            >>> collection = BookCollection()
            >>> collection.get_unread_books()
            []
        """
        return [book for book in self.books if not book.read]

    def _find_book_index_by_title(self, title: str) -> Optional[int]:
        """Find a book index by title using trimmed, case-insensitive matching.

        Parameters:
            title (str): The title to search for.

        Returns:
            Optional[int]: The matching index, or ``None`` when no book matches.

        Raises:
            ValueError: If ``title`` is not a non-empty string.

        Examples:
            >>> collection = BookCollection()
            >>> collection._find_book_index_by_title("Dune") is None
            True
        """
        normalized_title = self._normalize_text(title, "Title").casefold()
        for index, book in enumerate(self.books):
            if book.title.casefold() == normalized_title:
                return index
        return None

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Return a book that matches the given title.

        Parameters:
            title (str): The title to locate.

        Returns:
            Optional[Book]: The matching ``Book`` instance, or ``None`` if the
            title is not present.

        Raises:
            ValueError: If ``title`` is not a non-empty string.

        Examples:
            >>> collection = BookCollection()
            >>> collection.find_book_by_title("Dune") is None
            True
        """
        index = self._find_book_index_by_title(title)
        if index is None:
            return None
        return self.books[index]

    def mark_as_read(self, title: str) -> bool:
        """Mark a matching book as read and persist the change.

        Parameters:
            title (str): The title of the book to update.

        Returns:
            bool: ``True`` if a matching book exists, otherwise ``False``.

        Raises:
            ValueError: If ``title`` is not a non-empty string.
            BookDataError: If the updated collection cannot be saved.

        Examples:
            >>> collection = BookCollection()
            >>> collection.mark_as_read("Dune")
            False
        """
        index = self._find_book_index_by_title(title)
        if index is None:
            return False

        book = self.books[index]
        if book.read:
            return True

        updated_books = list(self.books)
        updated_books[index] = replace(book, read=True)
        self.save_books(updated_books)
        self.books = updated_books
        return True

    def remove_book(self, title: str) -> bool:
        """Remove a matching book from the collection and save the change.

        Parameters:
            title (str): The title of the book to remove.

        Returns:
            bool: ``True`` if a book was removed, otherwise ``False``.

        Raises:
            ValueError: If ``title`` is not a non-empty string.
            BookDataError: If the updated collection cannot be saved.

        Examples:
            >>> collection = BookCollection()
            >>> collection.remove_book("Dune")
            False
        """
        index = self._find_book_index_by_title(title)
        if index is None:
            return False

        updated_books = self.books[:index] + self.books[index + 1 :]
        self.save_books(updated_books)
        self.books = updated_books
        return True

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books that match an author name exactly.

        Parameters:
            author (str): The author name to search for.

        Returns:
            List[Book]: All books whose author matches after trimming and
            case-folding.

        Raises:
            ValueError: If ``author`` is not a non-empty string.

        Examples:
            >>> collection = BookCollection()
            >>> collection.find_by_author("Frank Herbert")
            []
        """
        normalized_author = self._normalize_text(author, "Author").casefold()
        return [book for book in self.books if book.author.casefold() == normalized_author]

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books published between two years, inclusive.

        Parameters:
            start (int): The first year in the range.
            end (int): The last year in the range.

        Returns:
            List[Book]: Books whose publication year falls within the range.

        Raises:
            ValueError: If either bound is not an integer or ``start`` is
                greater than ``end``.

        Examples:
            >>> collection = BookCollection()
            >>> collection.list_by_year(1960, 1970)
            []
        """
        if not isinstance(start, int) or isinstance(start, bool):
            raise ValueError("Start year must be an integer.")
        if not isinstance(end, int) or isinstance(end, bool):
            raise ValueError("End year must be an integer.")
        if start > end:
            raise ValueError("Start year cannot be greater than end year.")

        return [book for book in self.books if start <= book.year <= end]
