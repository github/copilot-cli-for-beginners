from __future__ import annotations

import json
from dataclasses import dataclass, asdict


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
        self.books: list[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except (json.JSONDecodeError, TypeError):
            print(f"Warning: {self.data_file} is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current book collection to JSON.

        Raises:
            OSError: If the file cannot be written.
        """
        with open(self.data_file, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection.

        Raises:
            ValueError: If title or author is empty.
            OSError: If the collection cannot be saved.
        """
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if not author.strip():
            raise ValueError("Author cannot be empty")
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> list[Book]:
        """Return all books in the collection."""
        return self.books

    def find_by_title(self, title: str) -> Book | None:
        """Find a book by its title (case-insensitive)."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title.

        Raises:
            OSError: If the collection cannot be saved.
        """
        book = self.find_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title.

        Raises:
            OSError: If the collection cannot be saved.
        """
        book = self.find_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> list[Book]:
        """Find all books by a given author (case-insensitive)."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(self, start: int, end: int) -> list[Book]:
        """Filter books by publication year range (inclusive).

        Args:
            start: The starting year (inclusive).
            end: The ending year (inclusive).

        Returns:
            A list of books published between start and end years.

        Raises:
            ValueError: If start is greater than end.
        """
        if start > end:
            raise ValueError(f"Start year ({start}) cannot be greater than end year ({end})")
        return [b for b in self.books if start <= b.year <= end]
