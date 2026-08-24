import json
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

def test_list_by_year_within_range():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.list_by_year(1940, 1970)
    titles = [b.title for b in results]
    assert titles == ["1984", "Dune"]

def test_list_by_year_excludes_out_of_range():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.list_by_year(1940, 1970)
    titles = [b.title for b in results]
    assert "The Hobbit" not in titles

def test_list_by_year_boundary_inclusive():
    collection = BookCollection()
    collection.add_book("Start Year Book", "Author A", 1950)
    collection.add_book("End Year Book", "Author B", 1960)
    results = collection.list_by_year(1950, 1960)
    titles = [b.title for b in results]
    assert "Start Year Book" in titles
    assert "End Year Book" in titles

def test_list_by_year_no_matches():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.list_by_year(2000, 2020)
    assert results == []

def test_list_by_year_empty_collection():
    collection = BookCollection()
    results = collection.list_by_year(1900, 2000)
    assert results == []


def test_load_books_skips_malformed_entry_without_losing_valid_ones(tmp_path, capsys):
    """A single malformed record must not wipe out the whole collection."""
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "1984", "author": "George Orwell", "year": 1949},
        {"title": "Missing Year", "author": "Nobody"},
        "not-even-an-object",
    ]))

    collection = BookCollection()

    assert [b.title for b in collection.books] == ["1984"]
    captured = capsys.readouterr()
    assert "skipping entry 1" in captured.out
    assert "skipping entry 2" in captured.out


def test_load_books_skips_wrong_typed_fields(tmp_path, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "1984", "author": "George Orwell", "year": "1949"},
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": "yes"},
        {"title": "Valid Book", "author": "Someone", "year": 2000},
    ]))

    collection = BookCollection()

    assert [b.title for b in collection.books] == ["Valid Book"]
    captured = capsys.readouterr()
    assert "year must be a whole number" in captured.out
    assert "read must be true/false" in captured.out


def test_load_books_skips_duplicate_titles(tmp_path, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        {"title": "dune", "author": "Someone Else", "year": 1970},
    ]))

    collection = BookCollection()

    assert len(collection.books) == 1
    assert collection.books[0].author == "Frank Herbert"
    captured = capsys.readouterr()
    assert "skipping duplicate book" in captured.out


def test_load_books_keeps_business_rule_violations(tmp_path):
    """Structurally valid but business-rule-invalid records still load
    (e.g. blank author, year 0) -- these are data quality issues to
    surface elsewhere, not reasons to hide the record."""
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "Mysterious Book", "author": "", "year": 0, "read": False},
    ]))

    collection = BookCollection()

    assert len(collection.books) == 1
    assert collection.books[0].title == "Mysterious Book"


def test_load_books_handles_non_list_top_level(tmp_path, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps({"title": "Not a list"}))

    collection = BookCollection()

    assert collection.books == []
    captured = capsys.readouterr()
    assert "does not contain a list of books" in captured.out
