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
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self) -> None:
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists.

        Each entry is parsed independently: a single malformed or
        wrong-typed entry is skipped (with a warning) rather than
        discarding the entire collection, and duplicate titles are
        skipped to preserve the uniqueness invariant enforced by
        add_book(). Records that violate business rules but are
        otherwise well-formed (e.g. a blank author or a year of 0)
        are still loaded -- those are data quality issues to surface
        elsewhere, not reasons to hide the record.
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
        """Validate and construct a Book from one raw JSON record.

        Returns None (and prints a warning) if the record isn't shaped
        like a book at all (not an object, missing/extra fields, or
        fields of the wrong type). This only checks structural
        correctness, not business rules, so records with blank fields
        or out-of-range values still load successfully.
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
        """Save the current book collection to JSON atomically."""
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

        Raises:
            ValueError: If title/author are blank, year is not a positive
                integer, or a book with the same title already exists.
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
        """Return a copy of all books in the collection."""
        return list(self.books)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Return all books written by the given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """List all books published within a year range (inclusive)."""
        return [b for b in self.books if start <= b.year <= end]
