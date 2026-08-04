import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, List, Optional

DATA_FILE = Path(__file__).with_name("data.json")


class DataFileError(Exception):
    """Raised when the book collection data cannot be loaded or saved safely."""


@dataclass
class Book:
    """
    Represents a single book in the collection.
    
    Attributes:
        title (str): The title of the book
        author (str): The name of the book's author
        year (int): The publication year of the book
        read (bool): Whether the book has been read (default: False)
    
    Example:
        >>> book = Book(title="1984", author="George Orwell", year=1949)
        >>> book.read
        False
        >>> book.read = True
        >>> book.read
        True
    """
    title: str
    author: str
    year: int
    read: bool = False


class JsonBookStorage:
    """Load and save books in a validated JSON file."""

    def __init__(self, data_file: str | Path):
        self.data_file = Path(data_file)

    def load(self) -> List[Book]:
        """Load validated books, treating a missing file as an empty collection."""
        try:
            with self.data_file.open(encoding="utf-8") as file_handle:
                data = json.load(file_handle)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as error:
            raise DataFileError(
                f"Cannot load {self.data_file}: it contains invalid JSON. "
                "Repair the file before continuing."
            ) from error
        except OSError as error:
            raise DataFileError(
                f"Cannot read {self.data_file}: {error.strerror or error}."
            ) from error

        return self._validate_books(data)

    def save(self, books: List[Book]) -> None:
        """Atomically replace the data file with the current collection."""
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.data_file.parent,
                prefix=f".{self.data_file.name}.",
                suffix=".tmp",
                delete=False,
            ) as file_handle:
                temporary_path = Path(file_handle.name)
                json.dump(
                    [asdict(book) for book in books],
                    file_handle,
                    indent=2,
                    ensure_ascii=False,
                )
                file_handle.write("\n")
                file_handle.flush()
                os.fsync(file_handle.fileno())

            os.replace(temporary_path, self.data_file)
        except OSError as error:
            if temporary_path is not None:
                try:
                    temporary_path.unlink()
                except FileNotFoundError:
                    pass
            raise DataFileError(
                f"Cannot save {self.data_file}: {error.strerror or error}."
            ) from error

    @staticmethod
    def _validate_books(data: Any) -> List[Book]:
        if not isinstance(data, list):
            raise DataFileError("Book data must be a JSON array.")

        books = []
        required_fields = {"title", "author", "year", "read"}
        for index, record in enumerate(data, start=1):
            if not isinstance(record, dict) or set(record) != required_fields:
                raise DataFileError(
                    f"Book record {index} must contain title, author, year, and read."
                )
            if (
                not isinstance(record["title"], str)
                or not isinstance(record["author"], str)
                or isinstance(record["year"], bool)
                or not isinstance(record["year"], int)
                or not isinstance(record["read"], bool)
            ):
                raise DataFileError(
                    f"Book record {index} has fields with invalid types."
                )
            books.append(Book(**record))

        return books


class BookCollection:
    def __init__(self, data_file: str | Path | None = None):
        """
        Initialize the book collection and load books from storage.
        
        Loads books from the JSON file specified by DATA_FILE. A missing file starts
        an empty collection; malformed data is reported without modifying the file.
        
        Raises:
            DataFileError: If the data file cannot be read or validated
        
        Example:
            >>> collection = BookCollection()
            >>> len(collection.books)
            0
        """
        self.storage = JsonBookStorage(data_file or DATA_FILE)
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """
        Load books from the JSON file if it exists.
        
        Reads and validates books from the JSON file. A missing file produces an
        empty collection; invalid data raises DataFileError without changing it.
        
        Raises:
            DataFileError: If the data file cannot be read or validated
        
        Example:
            >>> collection = BookCollection()
            >>> collection.load_books()  # Re-loads from file
        """
        self.books = self.storage.load()

    def save_books(self) -> None:
        """
        Save the current book collection to JSON.
        
        Serializes all books to a temporary file before replacing the JSON file, so
        an interrupted write cannot leave a partially written data file.
        
        Raises:
            DataFileError: If the file cannot be written
        
        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.save_books()  # Writes to data.json
        """
        self.storage.save(self.books)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Add a new book to the collection.
        
        Creates a new Book object and adds it to the collection. The book is
        automatically saved to the JSON file after being added.
        
        Parameters:
            title (str): The title of the book
            author (str): The name of the author
            year (int): The publication year
        
        Returns:
            Book: The newly created Book object
        
        Example:
            >>> collection = BookCollection()
            >>> book = collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
            >>> book.title
            'The Hobbit'
            >>> len(collection.books)
            1
        """
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """
        Return all books in the collection.
        
        Returns:
            List[Book]: A list of all Book objects in the collection. Returns an
                       empty list if the collection is empty.
        
        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> books = collection.list_books()
            >>> len(books)
            1
            >>> books[0].title
            '1984'
        """
        return self.books

    def get_unread_books(self) -> List[Book]:
        """
        Return books that have not been read.

        Returns:
            List[Book]: Unread books in collection order, or an empty list if
                        every book has been read or the collection is empty.
        """
        return [book for book in self.books if not book.read]

    def find_by_title(self, title: str) -> Optional[Book]:
        """
        Find a book by its title (case-insensitive).
        
        Searches the collection for a book with a matching title. The search is
        case-insensitive, so "1984", "1984", and "1984" will all match.
        
        Parameters:
            title (str): The title to search for
        
        Returns:
            Optional[Book]: The first matching Book object, or None if not found
        
        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
            >>> book = collection.find_by_title("the great gatsby")
            >>> book.author
            'F. Scott Fitzgerald'
            >>> collection.find_by_title("Unknown") is None
            True
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """
        Mark a book as read by its title.
        
        Finds the book with the specified title and sets its read flag to True.
        The change is automatically saved to the JSON file. If the book is not
        found, the collection is unchanged.
        
        Parameters:
            title (str): The title of the book to mark as read
        
        Returns:
            bool: True if the book was found and marked as read, False otherwise
        
        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("Dune", "Frank Herbert", 1965)
            >>> result = collection.mark_as_read("Dune")
            >>> result
            True
            >>> collection.find_by_title("Dune").read
            True
            >>> collection.mark_as_read("Unknown") 
            False
        """
        book = self.find_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """
        Remove a book from the collection by its title.
        
        Finds the book with the specified title and removes it from the collection.
        The change is automatically saved to the JSON file. If the book is not found,
        the collection is unchanged.
        
        Parameters:
            title (str): The title of the book to remove
        
        Returns:
            bool: True if the book was found and removed, False otherwise
        
        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
            >>> len(collection.books)
            1
            >>> result = collection.remove_book("The Hobbit")
            >>> result
            True
            >>> len(collection.books)
            0
            >>> collection.remove_book("Unknown")
            False
        """
        book = self.find_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """
        Find all books by a given author (case-insensitive).
        
        Searches the collection for all books with a matching author name. The search
        is case-insensitive, so "George Orwell", "george orwell", and "GEORGE ORWELL"
        will all match.
        
        Parameters:
            author (str): The author name to search for
        
        Returns:
            List[Book]: A list of all Book objects by the specified author. Returns
                       an empty list if no books are found.
        
        Example:
            >>> collection = BookCollection()
            >>> collection.add_book("1984", "George Orwell", 1949)
            >>> collection.add_book("Animal Farm", "George Orwell", 1945)
            >>> collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
            >>> books = collection.find_by_author("george orwell")
            >>> len(books)
            2
            >>> books[0].title
            '1984'
            >>> collection.find_by_author("Unknown Author")
            []
        """
        return [b for b in self.books if b.author.lower() == author.lower()]
