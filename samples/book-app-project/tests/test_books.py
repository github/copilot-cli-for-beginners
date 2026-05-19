import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection
import logging


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

def test_add_book_invalid_title():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title cannot be empty."):
        collection.add_book("", "Author", 2023)

def test_add_book_invalid_author():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Author cannot be empty."):
        collection.add_book("Title", "", 2023)

def test_add_book_invalid_year():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year must be between 0 and 9999."):
        collection.add_book("Title", "Author", -1)
    with pytest.raises(ValueError, match="Year must be between 0 and 9999."):
        collection.add_book("Title", "Author", 10000)

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

def test_handle_add_invalid_input(monkeypatch, capsys):
    from book_app import handle_add

    # Test empty title
    monkeypatch.setattr('builtins.input', lambda _: "")
    handle_add()
    captured = capsys.readouterr()
    assert "Error: Title cannot be empty." in captured.out

    # Test empty author
    monkeypatch.setattr('builtins.input', lambda prompt: "Title" if "Title" in prompt else "")
    handle_add()
    captured = capsys.readouterr()
    assert "Error: Author cannot be empty." in captured.out

    # Test invalid year
    monkeypatch.setattr('builtins.input', lambda prompt: "Title" if "Title" in prompt else ("Author" if "Author" in prompt else "-1"))
    handle_add()
    captured = capsys.readouterr()
    assert "Error: Year must be between 0 and 9999." in captured.out

def test_list_books():
    collection = BookCollection()
    collection.add_book("Test Book", "Author", 2023)
    books = collection.list_books()
    assert len(books) == 1
    assert books[0].title == "Test Book"

def test_handle_add_logs_structured_success(monkeypatch, caplog):
    import book_app

    book_app.collection = BookCollection()

    answers = iter(["Structured Logging", "Logger Author", "2024"])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    with caplog.at_level(logging.INFO, logger="book_app"):
        book_app.handle_add()

    assert "op=add_book" in caplog.text
    assert "status=success" in caplog.text
    assert "elapsed_ms=" in caplog.text

def test_show_books_toggle_on(monkeypatch, capsys):
    import book_app
    from books import Book

    monkeypatch.setenv("BOOK_APP_SHOW_YEAR", "1")
    book_app.show_books([Book(title="Dune", author="Frank Herbert", year=1965)])

    captured = capsys.readouterr()
    assert "(1965)" in captured.out

def test_show_books_toggle_off(monkeypatch, capsys):
    import book_app
    from books import Book

    monkeypatch.setenv("BOOK_APP_SHOW_YEAR", "0")
    book_app.show_books([Book(title="Dune", author="Frank Herbert", year=1965)])

    captured = capsys.readouterr()
    assert "(1965)" not in captured.out
