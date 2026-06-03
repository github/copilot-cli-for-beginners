"""books.py — Book collection utilities.

This module provides a lightweight Book dataclass and a BookCollection class
that loads/saves a JSON file and offers basic search and mutation helpers.

Notes:
- Data file defaults to "data.json" in the current working directory.
- Uses logging (not print) for diagnostics.
- Implements a simple advisory lock via a "<datafile>.lock" file to reduce
  race conditions when multiple processes write the same file.
"""

import json
import os
import tempfile
import time
import logging
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, ContextManager, List, Optional

logger = logging.getLogger(__name__)

DATA_FILE = "data.json"


def _parse_bool(value: Any) -> bool:
    """Parse a boolean-like value from various JSON representations.

    Accepts booleans, integers (0/1), and common strings ('true','false','1','0','yes','no').
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        return v in ("true", "1", "yes", "y")
    return False


@contextmanager
def _file_lock(path: str, timeout: float = 5.0, poll: float = 0.05) -> ContextManager[None]:
    """Simple advisory lock using an exclusive lockfile.

    Creates '<path>.lock' atomically and removes it on exit. Retries until timeout.
    This is not a POSIX flock; it's a lightweight cross-process guard suitable for
    simple local use.
    """
    lockfile = f"{path}.lock"
    deadline = time.time() + timeout
    fd = None
    while True:
        try:
            # O_EXCL + O_CREAT ensures atomic creation failure if exists
            fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            # write PID for diagnostics
            try:
                os.write(fd, str(os.getpid()).encode("utf-8"))
            except OSError:
                pass
            break
        except FileExistsError:
            if time.time() > deadline:
                raise TimeoutError(f"Timeout acquiring lock for {path}")
            time.sleep(poll)
    try:
        yield
    finally:
        try:
            if fd is not None:
                os.close(fd)
            if os.path.exists(lockfile):
                os.remove(lockfile)
        except OSError:
            logger.debug("Failed to remove lockfile %s", lockfile, exc_info=True)











@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manage a collection of Book objects persisted to a JSON file.

    Public methods provide simple operations for adding, finding, listing,
    marking read, removing and searching books.
    """

    def __init__(self, data_file: Optional[str] = None) -> None:
        # Use provided data_file or fall back to module-level DATA_FILE. Defaulting
        # to DATA_FILE in the function signature would capture the value at import
        # time and make monkeypatching DATA_FILE in tests ineffective.
        self.data_file = data_file if data_file is not None else DATA_FILE
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file.

        Skips malformed entries but loads valid ones. Uses logging for diagnostics.
        """
        try:
            if not os.path.exists(self.data_file):
                self.books = []
                return

            # Acquire a short lock to avoid reading during a write
            try:
                with _file_lock(self.data_file, timeout=0.5):
                    with open(self.data_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
            except TimeoutError:
                # If lock cannot be acquired quickly, try reading without it
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

            if not isinstance(data, list):
                logger.warning("%s does not contain a list. Starting with empty collection.", self.data_file)
                self.books = []
                return

            books: List[Book] = []
            current_year = datetime.utcnow().year
            for i, entry in enumerate(data):
                try:
                    if not isinstance(entry, dict):
                        raise ValueError("entry is not a JSON object")

                    title = entry.get("title")
                    author = entry.get("author")

                    if not title or not author:
                        logger.warning("Skipping invalid book entry at index %d (missing title/author).", i)
                        continue

                    if "year" not in entry:
                        logger.warning("Skipping book '%s' at index %d: missing 'year'.", title, i)
                        continue

                    try:
                        year = int(entry.get("year"))
                    except (TypeError, ValueError):
                        logger.warning("Skipping book '%s' at index %d: invalid 'year'.", title, i)
                        continue

                    if year < 0 or year > current_year:
                        logger.warning("Skipping book '%s' at index %d: year %s out of range.", title, i, year)
                        continue

                    read = _parse_bool(entry.get("read", False))

                    books.append(Book(title=title, author=author, year=year, read=read))
                except (TypeError, ValueError) as e:
                    logger.warning("Skipping malformed book entry at index %d: %s", i, e)

            self.books = books

        except json.JSONDecodeError:
            logger.warning("%s is corrupted or contains invalid JSON. Starting with empty collection.", self.data_file)
            self.books = []
        except OSError as e:
            logger.error("Error reading %s: %s. Starting with empty collection.", self.data_file, e)
            self.books = []

    def save_books(self) -> None:
        """Atomically save the current book collection to JSON.

        Writes to a temporary file in the same directory and then replaces the
        target file. Uses a simple advisory lock to reduce concurrent writers.
        """
        try:
            dirpath = os.path.dirname(os.path.abspath(self.data_file)) or "."
            # Ensure directory exists
            os.makedirs(dirpath, exist_ok=True)

            with _file_lock(self.data_file):
                fd, tmp_path = tempfile.mkstemp(prefix="tmp-", dir=dirpath, text=True)
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        json.dump([asdict(b) for b in self.books], f, indent=2)
                        f.flush()
                        os.fsync(f.fileno())
                    os.replace(tmp_path, self.data_file)
                finally:
                    if os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except OSError:
                            logger.debug("Failed to remove temp file %s", tmp_path, exc_info=True)
        except TimeoutError as e:
            logger.error("Could not acquire lock to save books: %s", e)
        except OSError as e:
            logger.error("Error saving books to %s: %s", self.data_file, e)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection and persist it.

        Raises ValueError for invalid input or if a book with the same title
        (case-insensitive) already exists.
        """
        title = title.strip() if isinstance(title, str) else ""
        author = author.strip() if isinstance(author, str) else ""

        if not title:
            raise ValueError("Title cannot be empty.")
        if not author:
            raise ValueError("Author cannot be empty.")

        try:
            year = int(year)
        except (TypeError, ValueError):
            raise ValueError("Year must be an integer.")

        current_year = datetime.utcnow().year
        if year < 0 or year > current_year:
            raise ValueError(f"Year must be between 0 and {current_year}.")

        # Prevent exact-title duplicates (case-insensitive)
        if any(b.title.lower() == title.lower() for b in self.books):
            raise ValueError(f"A book with the title '{title}' already exists.")

        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return the list of books in insertion order."""
        return self.books

    def get_unread_books(self) -> List[Book]:
        """Return books that are unread (read == False).

        This convenience method keeps callers from filtering the list themselves
        and documents the intended behavior in the public API.
        """
        return [b for b in self.books if not getattr(b, "read", False)]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by exact title (case-insensitive). Returns None if not found."""
        if title is None:
            return None
        t = title.strip().lower()
        for book in self.books:
            if book.title.lower() == t:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title. Returns True if updated."""
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title. Returns True if removed."""
        book = self.find_book_by_title(title)
        if book:
            try:
                self.books.remove(book)
                self.save_books()
                return True
            except ValueError:
                logger.warning("Failed to remove book '%s' — not found in list.", title)
                return False
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Return books that match the author using case-insensitive substring matching."""
        if not author:
            return []
        a = author.strip().lower()
        return [b for b in self.books if isinstance(b.author, str) and a in b.author.strip().lower()]

    def search(self, query: str) -> List[Book]:
        """Search books by title or author using case-insensitive substring matching."""
        if not query:
            return []
        q = str(query).strip().lower()
        if not q:
            return []
        return [b for b in self.books if q in b.title.lower() or q in b.author.lower()]