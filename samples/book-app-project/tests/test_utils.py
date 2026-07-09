import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from io import StringIO
from unittest.mock import patch
from utils import print_menu, get_book_details, print_books, get_book_statistics
from books import Book


def test_print_menu(capsys):
    """Test that menu prints correctly."""
    print_menu()
    captured = capsys.readouterr()
    assert "📚 Book Collection App" in captured.out
    assert "1. Add a book" in captured.out
    assert "2. List books" in captured.out
    assert "3. Mark book as read" in captured.out
    assert "4. Remove a book" in captured.out
    assert "5. Exit" in captured.out


def test_get_user_choice_valid(monkeypatch):
    """Test menu choice validation with valid input."""
    from utils import get_user_choice
    
    monkeypatch.setattr('builtins.input', lambda _: "3")
    choice = get_user_choice()
    assert choice == "3"


def test_get_user_choice_retries_on_invalid(monkeypatch):
    """Test menu choice validation retries on invalid input."""
    from utils import get_user_choice
    
    inputs = iter(["", "abc", "10", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    choice = get_user_choice()
    assert choice == "2"


def test_get_book_details_valid(monkeypatch):
    """Test book details input with valid data."""
    inputs = iter(["The Hobbit", "J.R.R. Tolkien", "1937"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    title, author, year = get_book_details()
    assert title == "The Hobbit"
    assert author == "J.R.R. Tolkien"
    assert year == 1937


def test_get_book_details_year_default(monkeypatch):
    """Test book details with empty year (defaults to 0)."""
    inputs = iter(["1984", "George Orwell", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    title, author, year = get_book_details()
    assert title == "1984"
    assert author == "George Orwell"
    assert year == 0


def test_get_book_details_retries_empty_title(monkeypatch):
    """Test book details retries on empty title."""
    inputs = iter(["", "  ", "Valid Title", "Valid Author", "2020"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    title, author, year = get_book_details()
    assert title == "Valid Title"


def test_get_book_details_retries_long_title(monkeypatch):
    """Test book details retries on title exceeding 100 chars."""
    long_title = "A" * 101
    inputs = iter([long_title, "Valid Title", "Valid Author", "2020"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    title, author, year = get_book_details()
    assert title == "Valid Title"


def test_get_book_details_future_year_confirmed(monkeypatch):
    """Test book details accepts future year when confirmed."""
    inputs = iter(["Book", "Author", "2150", "y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    title, author, year = get_book_details()
    assert year == 2150


def test_get_book_details_future_year_rejected(monkeypatch):
    """Test book details retries after rejecting future year."""
    inputs = iter(["Book", "Author", "2150", "n", "2020"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    title, author, year = get_book_details()
    assert year == 2020


def test_print_books_empty(capsys):
    """Test printing empty book list."""
    print_books([])
    captured = capsys.readouterr()
    assert "No books in your collection" in captured.out


def test_print_books_list(capsys):
    """Test printing books with correct formatting."""
    books = [
        Book(title="1984", author="George Orwell", year=1949, read=True),
        Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, read=False),
    ]
    print_books(books)
    captured = capsys.readouterr()
    
    assert "Your Books:" in captured.out
    assert "1984" in captured.out
    assert "George Orwell" in captured.out
    assert "✅ Read" in captured.out
    assert "📖 Unread" in captured.out


def test_get_book_statistics_empty():
    """Test statistics for empty collection."""
    stats = get_book_statistics([])
    
    assert stats["total_count"] == 0
    assert stats["read_count"] == 0
    assert stats["unread_count"] == 0
    assert stats["oldest_book"] is None
    assert stats["newest_book"] is None


def test_get_book_statistics_single_book():
    """Test statistics for single book."""
    books = [Book(title="1984", author="Orwell", year=1949, read=True)]
    stats = get_book_statistics(books)
    
    assert stats["total_count"] == 1
    assert stats["read_count"] == 1
    assert stats["unread_count"] == 0
    assert stats["oldest_book"].title == "1984"
    assert stats["newest_book"].title == "1984"


def test_get_book_statistics_multiple_books():
    """Test statistics for multiple books."""
    books = [
        Book(title="The Hobbit", author="Tolkien", year=1937, read=True),
        Book(title="1984", author="Orwell", year=1949, read=True),
        Book(title="Dune", author="Herbert", year=1965, read=False),
    ]
    stats = get_book_statistics(books)
    
    assert stats["total_count"] == 3
    assert stats["read_count"] == 2
    assert stats["unread_count"] == 1
    assert stats["oldest_book"].title == "The Hobbit"
    assert stats["newest_book"].title == "Dune"
