import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

import pytest
import books
from books import Book, BookCollection, get_statistics
from exceptions import BookNotFoundError, StorageError, ValidationError


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

def test_add_book_empty_title_raises():
    collection = BookCollection()
    with pytest.raises(ValidationError):
        collection.add_book("", "George Orwell", 1949)


def test_add_book_whitespace_title_raises():
    collection = BookCollection()
    with pytest.raises(ValidationError):
        collection.add_book("   ", "George Orwell", 1949)


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    with pytest.raises(BookNotFoundError):
        collection.mark_as_read("Nonexistent Book")

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.remove_book("The Hobbit")
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    with pytest.raises(BookNotFoundError):
        collection.remove_book("Nonexistent Book")

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


def test_load_books_missing_file_starts_empty(tmp_path, monkeypatch):
    """load_books should tolerate a missing data file and start empty."""
    missing_file = tmp_path / "does_not_exist.json"
    monkeypatch.setattr(books, "DATA_FILE", str(missing_file))

    collection = BookCollection()

    assert collection.books == []


def test_load_books_reads_existing_data(tmp_path, monkeypatch):
    """load_books should parse existing valid JSON into Book objects."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": true}]'
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()

    assert len(collection.books) == 1
    book = collection.books[0]
    assert book.title == "Dune"
    assert book.author == "Frank Herbert"
    assert book.year == 1965
    assert book.read is True


def test_save_books_persists_to_disk(tmp_path, monkeypatch):
    """save_books should write the current collection as JSON to DATA_FILE."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    saved_data = json.loads(temp_file.read_text())
    assert saved_data == [
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": False}
    ]


def test_add_book_reflected_after_reload(tmp_path, monkeypatch):
    """Books added should be persisted and visible to a freshly loaded collection."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    reloaded = BookCollection()
    assert reloaded.find_book_by_title("Dune") is not None


def test_mark_as_read_persists_after_reload(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")

    reloaded = BookCollection()
    assert reloaded.find_book_by_title("Dune").read is True


def test_remove_book_persists_after_reload(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.remove_book("Dune")

    reloaded = BookCollection()
    assert reloaded.find_book_by_title("Dune") is None


def test_find_book_by_title_case_insensitive():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.find_book_by_title("DUNE") is not None
    assert collection.find_book_by_title("dune") is not None


def test_find_book_by_title_not_found_returns_none():
    collection = BookCollection()
    assert collection.find_book_by_title("Nonexistent") is None


def test_list_books_returns_live_reference():
    """list_books currently returns the internal list, not a copy."""
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.list_books()
    assert result is collection.books


@pytest.mark.parametrize(
    "author_query,expected_titles",
    [
        ("Frank Herbert", ["Dune"]),
        ("frank herbert", ["Dune"]),
        ("Nonexistent Author", []),
    ],
)
def test_find_by_author(author_query, expected_titles):
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    results = collection.find_by_author(author_query)
    assert [b.title for b in results] == expected_titles


@pytest.mark.parametrize(
    "start,end,expected_titles",
    [
        (1960, 1970, ["Dune"]),
        (1965, 1965, ["Dune"]),
        (1970, 1980, []),
        (1970, 1960, []),  # start > end yields no matches
    ],
)
def test_list_by_year(start, end, expected_titles):
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    results = collection.list_by_year(start, end)
    assert [b.title for b in results] == expected_titles


def test_get_statistics_tied_years_returns_first_match():
    """min()/max() return the first element on ties, current behavior."""
    books_list = [
        Book(title="Book A", author="Author A", year=2000),
        Book(title="Book B", author="Author B", year=2000),
    ]
    stats = get_statistics(books_list)
    assert stats["oldest"].title == "Book A"
    assert stats["newest"].title == "Book A"


def test_load_books_corrupted_json_raises_storage_error(tmp_path, monkeypatch):
    temp_file = tmp_path / "corrupted.json"
    temp_file.write_text("{not valid json")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(StorageError):
        BookCollection()
