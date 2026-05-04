import json
import logging
import os
import shutil
import time
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"

logger = logging.getLogger(__name__)


class StorageError(RuntimeError):
    """Raised when the book collection cannot be read from or written to disk."""


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists.

        Missing file -> empty collection (first run).
        Corrupted file -> empty collection, with the corrupt file backed up
        to ``<DATA_FILE>.corrupt-<timestamp>`` so no data is lost silently.
        Malformed individual entries are skipped with a warning rather than
        aborting the entire load.
        """
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.books = []
            return
        except json.JSONDecodeError:
            self._backup_corrupt_file()
            logger.warning(
                "%s is corrupted. Starting with empty collection (backup saved).",
                DATA_FILE,
            )
            self.books = []
            return
        except OSError as e:
            raise StorageError(f"Could not read {DATA_FILE}: {e}") from e

        if not isinstance(data, list):
            self._backup_corrupt_file()
            logger.warning(
                "%s does not contain a JSON array. Starting with empty collection.",
                DATA_FILE,
            )
            self.books = []
            return

        books: List[Book] = []
        for index, entry in enumerate(data):
            if not isinstance(entry, dict):
                logger.warning("Skipping non-object entry at index %d in %s", index, DATA_FILE)
                continue
            try:
                books.append(Book(**entry))
            except TypeError as e:
                logger.warning(
                    "Skipping malformed entry at index %d in %s: %s", index, DATA_FILE, e
                )
        self.books = books

    @staticmethod
    def _backup_corrupt_file() -> None:
        """Copy a corrupt data file aside so it can be inspected later."""
        try:
            backup = f"{DATA_FILE}.corrupt-{int(time.time())}"
            shutil.copy2(DATA_FILE, backup)
            logger.warning("Backed up corrupt %s to %s", DATA_FILE, backup)
        except OSError as e:
            logger.warning("Could not back up corrupt %s: %s", DATA_FILE, e)

    def save_books(self):
        """Atomically save the current book collection to JSON.

        Writes to a temporary file in the same directory and then uses
        ``os.replace`` to atomically swap it into place, so a crash mid-write
        cannot truncate or corrupt the existing ``data.json``.

        Raises:
            StorageError: If the file cannot be written or replaced.
        """
        tmp_path = f"{DATA_FILE}.tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, DATA_FILE)
        except OSError as e:
            # Best-effort cleanup of the temp file; ignore if it's already gone.
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise StorageError(f"Could not write {DATA_FILE}: {e}") from e

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a book after validating inputs.

        Raises:
            ValueError: If title/author is empty or year is out of range.
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        if not author or not author.strip():
            raise ValueError("Author cannot be empty.")
        if not isinstance(year, int) or year < 1 or year > 9999:
            raise ValueError(f"Year must be between 1 and 9999, got {year}.")

        book = Book(title=title.strip(), author=author.strip(), year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
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
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
