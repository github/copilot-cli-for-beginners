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


# --- Validation tests for add_book ---

def test_add_book_empty_title_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title cannot be empty"):
        collection.add_book("", "Author", 2020)


def test_add_book_whitespace_title_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title cannot be empty"):
        collection.add_book("   ", "Author", 2020)


def test_add_book_empty_author_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Author cannot be empty"):
        collection.add_book("Title", "", 2020)


def test_add_book_year_zero_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year must be between"):
        collection.add_book("Title", "Author", 0)


def test_add_book_negative_year_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year must be between"):
        collection.add_book("Title", "Author", -5)


def test_add_book_strips_whitespace():
    collection = BookCollection()
    book = collection.add_book("  1984  ", "  Orwell  ", 1949)
    assert book.title == "1984"
    assert book.author == "Orwell"


def test_add_book_year_too_large_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year must be between"):
        collection.add_book("Title", "Author", 10000)


def test_add_book_whitespace_author_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Author cannot be empty"):
        collection.add_book("Title", "   \t  ", 2020)


def test_add_book_none_title_raises():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title cannot be empty"):
        collection.add_book(None, "Author", 2020)


def test_add_book_valid_boundary_years():
    """Year 1 and 9999 should both be accepted."""
    collection = BookCollection()
    book_min = collection.add_book("Ancient", "Author", 1)
    book_max = collection.add_book("Future", "Author", 9999)
    assert book_min.year == 1
    assert book_max.year == 9999


def test_add_book_persists_to_disk():
    """Validated book is saved and survives a reload."""
    collection = BookCollection()
    collection.add_book("Persisted", "Writer", 2000)
    reloaded = BookCollection()
    assert len(reloaded.books) == 1
    assert reloaded.books[0].title == "Persisted"


def test_add_book_invalid_does_not_persist():
    """A rejected book should not be saved to disk."""
    collection = BookCollection()
    with pytest.raises(ValueError):
        collection.add_book("", "Author", 2020)
    reloaded = BookCollection()
    assert len(reloaded.books) == 0


# --- Display consolidation: print_books removed from utils ---

def test_utils_has_no_print_books():
    """Confirm the duplicate print_books was removed from utils."""
    import utils
    assert not hasattr(utils, "print_books")
