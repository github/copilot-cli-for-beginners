import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test.

    Each test gets an isolated temp data.json file to avoid cross-test pollution.
    """
    temp_file = tmp_path / "data.json"
    # Start with an empty JSON array by default
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


def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None


def test_find_by_title_case_insensitive():
    collection = BookCollection()
    collection.add_book("La Odisea", "Homero", -800)
    # search with different casing
    book = collection.find_book_by_title("la odisea")
    assert book is not None
    assert book.author == "Homero"


def test_find_by_author_multiple():
    collection = BookCollection()
    collection.add_book("Book A", "Author X", 2000)
    collection.add_book("Book B", "Author X", 2005)
    collection.add_book("Other", "Author Y", 2010)
    results = collection.find_by_author("author x")
    assert isinstance(results, list)
    assert len(results) == 2
    titles = sorted([b.title for b in results])
    assert titles == ["Book A", "Book B"]


def test_mark_book_as_read_and_persist(tmp_path, monkeypatch):
    # ensure marking persists to disk by reloading collection
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    col1 = BookCollection()
    col1.add_book("Dune", "Frank Herbert", 1965)
    assert col1.find_book_by_title("Dune").read is False

    result = col1.mark_as_read("Dune")
    assert result is True
    assert col1.find_book_by_title("Dune").read is True

    # Reload collection from disk to ensure persisted
    col2 = BookCollection()
    book = col2.find_book_by_title("Dune")
    assert book is not None
    assert book.read is True


def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False


def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_duplicate_titles_remove_only_first():
    collection = BookCollection()
    collection.add_book("Common Title", "Author One", 1990)
    collection.add_book("Common Title", "Author Two", 2000)

    # Remove by title should remove the first match
    result = collection.remove_book("Common Title")
    assert result is True
    remaining = [b for b in collection.books if b.title == "Common Title"]
    assert len(remaining) == 1
    assert remaining[0].author == "Author Two"


def test_empty_data_file_handled(tmp_path, monkeypatch):
    # Simulate an empty/corrupted file (not valid JSON)
    temp_file = tmp_path / "data.json"
    temp_file.write_text("")  # empty file -> JSONDecodeError on load
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    # Should not raise on initialization; collection should be empty
    collection = BookCollection()
    assert isinstance(collection.books, list)
    assert len(collection.books) == 0


def test_find_nonexistent_returns_none():
    collection = BookCollection()
    assert collection.find_book_by_title("Nope") is None


def test_persistence_after_multiple_operations(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    col = BookCollection()
    col.add_book("A", "X", 2001)
    col.add_book("B", "Y", 2002)
    col.mark_as_read("A")
    col.remove_book("B")

    # Reload and assert state
    col2 = BookCollection()
    a = col2.find_book_by_title("A")
    b = col2.find_book_by_title("B")
    assert a is not None and a.read is True
    assert b is None
