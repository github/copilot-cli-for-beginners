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
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        if not title.strip():
            raise ValueError("Book title cannot be empty.")

        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def list_unread_books(self) -> List[Book]:
        """Return unread books in their existing collection order."""
        return [book for book in self.books if not book.read]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        if not isinstance(title, str):
            return None

        normalized_title = title.strip().casefold()
        for book in self.books:
            if book.title.strip().casefold() == normalized_title:
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
        if not isinstance(title, str):
            print("Book title must be a string.")
            return False

        normalized_title = title.strip()
        if not normalized_title:
            print("Book title cannot be empty.")
            return False

        book = self.find_book_by_title(normalized_title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True

        print(f'Book not found: "{normalized_title}"')
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
