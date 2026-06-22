import json
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False
    # Each review is a dict: {"rating": int, "text": str}
    reviews: List[Dict] = field(default_factory=list)


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists.

        Backwards-compatible: older entries without `reviews` will work because
        Book has a default for that field.
        """
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
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

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
        """Find all books by a given author.

        Supports case-insensitive partial (substring) matches. Leading/trailing
        whitespace in the query is ignored. If the query is empty, returns an
        empty list.
        """
        author_q = (author or "").strip().lower()
        if not author_q:
            return []
        return [b for b in self.books if author_q in (b.author or "").lower()]

    def search(self, query: str) -> List[Book]:
        """Search books by title OR author using case-insensitive substring matching."""
        q = query.lower()
        return [b for b in self.books if q in b.title.lower() or q in b.author.lower()]

    def add_review(self, title: str, rating: int, text: str = "") -> bool:
        """Add a review (rating 1-5 and optional text) to the book identified by title.

        Raises ValueError for invalid rating. Returns True on success, False if book not found.
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")

        book = self.find_book_by_title(title)
        if not book:
            return False

        review = {"rating": int(rating), "text": text}
        book.reviews.append(review)
        self.save_books()
        return True

    def get_reviews(self, title: str) -> List[Dict]:
        book = self.find_book_by_title(title)
        if not book:
            return []
        return book.reviews

    def average_rating(self, title: str) -> Optional[float]:
        book = self.find_book_by_title(title)
        if not book or not book.reviews:
            return None
        total = sum(r.get("rating", 0) for r in book.reviews)
        count = len(book.reviews)
        return total / count

    def give_improvements(self) -> List[str]:
        """Return the word 'improvements' three times in a row as a list.

        This method provides a simple, deterministic response matching the
        request to "give improvements 3 times in a row".
        """
        suggestion = "improvements"
        return [suggestion, suggestion, suggestion]
