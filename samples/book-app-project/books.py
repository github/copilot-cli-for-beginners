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
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []
        except TypeError:
            print(
                "Warning: data.json contains records with unexpected fields. "
                "Starting with empty collection."
            )
            self.books = []

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
