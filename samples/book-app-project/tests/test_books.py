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

def test_add_book_rejects_empty_title():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Book title cannot be empty."):
        collection.add_book("   ", "George Orwell", 1949)

    assert collection.books == []

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


def test_list_unread_books_returns_unread_books_in_collection_order():
    collection = BookCollection()
    first = collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    third = collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")

    unread_books = collection.list_unread_books()

    assert unread_books == [first, third]
    assert unread_books is not collection.books


def test_list_unread_books_does_not_change_collection_state_or_data():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    books_before = list(collection.books)
    data_before = collection.books[0].read

    assert collection.list_unread_books() == []
    assert collection.books == books_before
    assert collection.books[0].read is data_before


def test_list_unread_books_returns_empty_list_when_all_books_are_read():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("1984")

    assert collection.list_unread_books() == []


def test_list_unread_books_returns_empty_list_for_empty_collection():
    collection = BookCollection()

    assert collection.list_unread_books() == []


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


def test_remove_book_matches_case_insensitively_and_ignores_whitespace():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.remove_book("  dUnE  ")

    assert result is True
    assert collection.books == []


def test_remove_book_reports_missing_title(capsys):
    collection = BookCollection()

    result = collection.remove_book("Nonexistent Book")

    assert result is False
    assert 'Book not found: "Nonexistent Book"' in capsys.readouterr().out


@pytest.mark.parametrize(
    ("title", "message"),
    [
        ("   ", "Book title cannot be empty."),
        (None, "Book title must be a string."),
    ],
)
def test_remove_book_rejects_invalid_title(title, message, capsys):
    collection = BookCollection()

    result = collection.remove_book(title)

    assert result is False
    assert message in capsys.readouterr().out
