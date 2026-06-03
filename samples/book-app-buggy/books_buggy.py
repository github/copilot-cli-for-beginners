import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


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

    def save_books(self):
        """Save the current book collection to JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
        except OSError as e:
            print(f"Error saving {DATA_FILE}: {e}")

    def add_book(self, title: str, author: str, year: int) -> Book:
        # Validate inputs: year must be int within reasonable bounds
        try:
            year = int(year)
        except (TypeError, ValueError):
            raise ValueError("Year must be an integer")
        from datetime import datetime
        current_year = datetime.utcnow().year
        if year < 0 or year > current_year:
            raise ValueError(f"Year must be between 0 and {current_year}")
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        # Case-insensitive, stripped comparison
        if title is None:
            return None
        t = title.strip().lower()
        for book in self.books:
            if isinstance(book.title, str) and book.title.strip().lower() == t:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        # Mark only matching book as read
        book = self.find_book_by_title(title)
        if book:
            if not book.read:
                book.read = True
                self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title (exact case-insensitive match)."""
        for book in list(self.books):
            if isinstance(book.title, str) and book.title.strip().lower() == title.strip().lower():
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (case-insensitive substring match)."""
        if not author:
            return []
        a = author.strip().lower()
        return [b for b in self.books if isinstance(b.author, str) and a in b.author.strip().lower()]
