import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


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


def test_add_review_and_average():
    collection = BookCollection()
    collection.add_book("Sapiens", "Yuval", 2011)
    # Add two reviews
    collection.add_review("Sapiens", 5, "Great read")
    collection.add_review("Sapiens", 3, "It was okay")

    reviews = collection.get_reviews("Sapiens")
    assert len(reviews) == 2

    avg = collection.average_rating("Sapiens")
    assert avg == pytest.approx(4.0)


def test_get_unread_books_returns_only_unread():
    collection = BookCollection()
    collection.add_book("Book A", "Author A", 2000)
    collection.add_book("Book B", "Author B", 2001)
    collection.add_book("Book C", "Author C", 2002)

    # Mark one book as read
    collection.mark_as_read("Book B")

    unread = collection.get_unread_books()
    titles = {b.title for b in unread}

    assert titles == {"Book A", "Book C"}
    assert all(not b.read for b in unread)


def test_get_unread_books_empty_when_all_read():
    collection = BookCollection()
    collection.add_book("Only Book", "Author", 1999)
    collection.mark_as_read("Only Book")

    unread = collection.get_unread_books()
    assert unread == []
