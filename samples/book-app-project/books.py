"""Utilities for Book and BookCollection used in samples/book-app-project.

Provides a small API for managing a persistent collection of books stored as JSON.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
import tempfile
import os
import logging
from datetime import datetime

__all__ = ["Book", "BookCollection"]

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

DATA_FILE = Path(__file__).parent / "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        return cls(
            title=str(data["title"]),
            author=str(data["author"]),
            year=int(data["year"]),
            read=bool(data.get("read", False)),
        )

    def __repr__(self) -> str:  # helpful for REPL and tests
        return f"Book(title={self.title!r}, author={self.author!r}, year={self.year}, read={self.read})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title.lower(), self.author.lower(), self.year) == (
            other.title.lower(), other.author.lower(), other.year
        )

    def __lt__(self, other: "Book") -> bool:
        return (self.title.lower(), self.author.lower(), self.year) < (
            other.title.lower(), other.author.lower(), other.year
        )


def _validate_year(year: int) -> int:
    now_year = datetime.utcnow().year
    y = int(year)
    if y < 0 or y > now_year + 1:
        raise ValueError(f"year {y} is not reasonable")
    return y


class BookCollection:
    """A simple collection of Book objects with JSON persistence.

    Data file defaults to samples/book-app-project/data.json (next to this file),
    but a custom path may be passed to the constructor (useful for tests).
    """

    def __init__(self, data_file: Optional[Path] = None):
        self.data_file: Path = Path(data_file) if data_file else DATA_FILE
        self.books: List[Book] = []
        self.load_books()

    def __enter__(self) -> "BookCollection":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        # On normal exit persist changes; never suppress exceptions.
        try:
            self.save_books()
        except Exception:
            LOG.exception("Failed to save books on __exit__")
        return False

    def load_books(self) -> None:
        """Load books from the JSON file if it exists.

        If the file is corrupt, it is moved to a timestamped backup so the user can inspect it.
        """
        if not self.data_file.exists():
            self.books = []
            return
        try:
            with self.data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = [Book.from_dict(b) for b in data]
        except json.JSONDecodeError:
            # Back up corrupted file for inspection and start with empty collection
            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            corrupt_name = self.data_file.with_suffix(f".corrupt.{ts}.json")
            try:
                self.data_file.replace(corrupt_name)
                LOG.warning("Moved corrupted %s to %s", self.data_file, corrupt_name)
            except Exception:
                LOG.exception("Failed to back up corrupted data file %s", self.data_file)
            self.books = []

    def save_books(self) -> None:
        """Atomically save the current book collection to JSON.

        Ensures parent directory exists and writes via a temp file then os.replace.
        """
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = [b.to_dict() for b in self.books]
        # Write to a temp file first, then atomically replace to avoid corruption.
        tmp_fd, tmp_path = tempfile.mkstemp(dir=str(self.data_file.parent))
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
            os.replace(tmp_path, str(self.data_file))
        except Exception:
            # Attempt to clean up temp file on failure
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a book if not already present (title+author considered unique).

        Raises ValueError if the book already exists or year is invalid.
        """
        title_clean = title.strip()
        author_clean = author.strip()
        y = _validate_year(year)
        if self.find_book_by_title_and_author(title_clean, author_clean):
            raise ValueError("Book already exists")
        book = Book(title=title_clean, author=author_clean, year=y)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self, sort_by: Optional[str] = None) -> List[Book]:
        """Return list of books; optionally sort by 'title', 'author', or 'year'."""
        if sort_by in ("title", "author", "year"):
            return sorted(self.books, key=lambda b: getattr(b, sort_by))
        return list(self.books)

    def search_title(self, query: str) -> List[Book]:
        """Return books whose title contains the query (case-insensitive)."""
        q = query.strip().lower()
        return [b for b in self.books if q in b.title.lower()]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find first exact-title match (case-insensitive)."""
        t = title.strip().lower()
        matches = [book for book in self.books if book.title.lower() == t]
        if not matches:
            return None
        if len(matches) > 1:
            LOG.warning("Multiple books found with title %s; returning first. Consider using title+author.", title)
        return matches[0]

    def find_book_by_title_and_author(self, title: str, author: str) -> Optional[Book]:
        t = title.strip().lower()
        a = author.strip().lower()
        for book in self.books:
            if book.title.lower() == t and book.author.lower() == a:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book and not book.read:
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
        """Find all books where the provided string is contained in the author name (case-insensitive)."""
        a = author.strip().lower()
        return [b for b in self.books if a in b.author.lower()]

    def update_book(self, title: str, **fields) -> bool:
        """Update fields on a book identified by title. Allowed fields: title, author, year, read.

        Returns True if the book was found and updated; False otherwise.
        """
        book = self.find_book_by_title(title)
        if not book:
            return False
        allowed = {"title", "author", "year", "read"}
        changed = False
        for k, v in fields.items():
            if k in allowed:
                if k == "year":
                    v = _validate_year(v)
                setattr(book, k, v)
                changed = True
        if changed:
            self.save_books()
        return changed

    def clear_books(self) -> None:
        """Remove all books from the collection and persist the empty state."""
        self.books = []
        self.save_books()

    def count(self) -> int:
        """Return number of books in the collection."""
        return len(self.books)

    def export_json(self, path: Path) -> None:
        """Export the collection to the given path as JSON."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=2, ensure_ascii=False, sort_keys=True)
