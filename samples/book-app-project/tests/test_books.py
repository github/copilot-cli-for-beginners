import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import Book, BookCollection, get_statistics


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False

def test_get_statistics_empty_list():
    stats = get_statistics([])
    assert stats == {"total": 0, "read": 0, "unread": 0, "oldest": None, "newest": None}

def test_get_statistics_mixed_books():
    books_list = [
        Book(title="1984", author="George Orwell", year=1949, read=True),
        Book(title="Dune", author="Frank Herbert", year=1965, read=False),
        Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, read=True),
    ]
    stats = get_statistics(books_list)
    assert stats["total"] == 3
    assert stats["read"] == 2
    assert stats["unread"] == 1
    assert stats["oldest"].title == "The Hobbit"
    assert stats["newest"].title == "Dune"

def test_get_statistics_single_book():
    books_list = [Book(title="Dune", author="Frank Herbert", year=1965)]
    stats = get_statistics(books_list)
    assert stats["total"] == 1
    assert stats["oldest"] is stats["newest"]
