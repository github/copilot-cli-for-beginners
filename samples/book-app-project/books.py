import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Union

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self, data_file: Optional[Union[str, Path]] = None):
        self.data_file = str(data_file) if data_file is not None else DATA_FILE
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                self.books = []
                return

            self.books = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                try:
                    self.books.append(Book(**item))
                except TypeError:
                    continue
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current book collection to JSON."""
        directory = os.path.dirname(self.data_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        cleaned_title = title.strip()
        cleaned_author = author.strip()
        if not cleaned_title or not cleaned_author:
            raise ValueError("Title and author are required.")

        try:
            year_value = int(year)
        except (TypeError, ValueError) as exc:
            raise ValueError("Year must be an integer.") from exc

        if year_value <= 0:
            raise ValueError("Year must be a positive integer.")

        book = Book(title=cleaned_title, author=cleaned_author, year=year_value)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        normalized_title = title.strip().lower()
        for book in self.books:
            if book.title.strip().lower() == normalized_title:
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
        """Find all books by a given author, including partial matches."""
        normalized_author = author.strip().lower()
        if not normalized_author:
            return []
        return [
            book for book in self.books
            if normalized_author in book.author.strip().lower()
        ]
