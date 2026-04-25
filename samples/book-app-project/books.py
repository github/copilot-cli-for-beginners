import json
import os
import tempfile
from dataclasses import dataclass, asdict
from typing import List, Optional, Iterable

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self, data_file: str = DATA_FILE) -> None:
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists.

        Robustness:
        - Handles non-existent file and corrupted JSON gracefully.
        - Validates each record and attempts to coerce types where reasonable.
        - Skips invalid records but reports a warning with count.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.books = []
            return
        except json.JSONDecodeError:
            print(f"Warning: {self.data_file} is corrupted. Starting with empty collection.")
            self.books = []
            return
        if not isinstance(data, Iterable):
            print(f"Warning: {self.data_file} does not contain a list. Starting with empty collection.")
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
            print(f"Warning: skipped {bad} invalid record(s) in {self.data_file}.")
        self.books = loaded

    def save_books(self) -> None:
        """Save the current book collection to JSON using an atomic write.

        Attempts to write to a temporary file in the same directory and then replace
        the target file to avoid partial writes. Catches and reports IO errors.
        """
        try:
            dirpath = os.path.dirname(os.path.abspath(self.data_file)) or "."
            fd, tmp_path = tempfile.mkstemp(prefix=".tmp_books_", dir=dirpath)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump([asdict(b) for b in self.books], f, indent=2, ensure_ascii=False)
                os.replace(tmp_path, self.data_file)
            finally:
                # If tmp_path still exists, try to remove it
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
        except OSError as e:
            print(f"Error: failed to save books to {self.data_file}: {e}")

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
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
        """Find all books by a given author (case-insensitive exact match)."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def search(self, query: str, fields: Optional[List[str]] = None, case_sensitive: bool = False) -> List[Book]:
        """Search books by query string within the provided fields.

        - Partial substring match (default)
        - Case-insensitive by default
        - fields: list containing any of "title" or "author"; defaults to both
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
