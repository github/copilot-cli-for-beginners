import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
import book_app
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


def test_get_unread_books_returns_only_unread():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("1984")

    unread = collection.get_unread_books()

    assert len(unread) == 1
    assert unread[0].title == "Dune"


def test_get_unread_books_empty_collection():
    collection = BookCollection()

    unread = collection.get_unread_books()

    assert unread == []


def test_get_unread_books_all_read():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("1984")

    unread = collection.get_unread_books()

    assert unread == []


def test_get_unread_books_none_read():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)

    unread = collection.get_unread_books()

    assert len(unread) == 2


def test_get_unread_books_does_not_modify_collection():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    collection.get_unread_books()

    assert len(collection.books) == 1


# ---------------------------------------------------------------------------
# handle_list_unread output tests
# ---------------------------------------------------------------------------

@pytest.fixture
def patched_collection(tmp_path, monkeypatch):
    """Patch book_app's global collection with a fresh isolated instance."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    fresh = BookCollection()
    monkeypatch.setattr(book_app, "collection", fresh)
    return fresh


def test_handle_list_unread_prints_unread_books(patched_collection, capsys):
    patched_collection.add_book("Dune", "Frank Herbert", 1965)
    patched_collection.add_book("1984", "George Orwell", 1949)
    patched_collection.mark_as_read("1984")

    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "Dune" in output
    assert "1984" not in output


def test_handle_list_unread_shows_no_unread_message_when_all_read(patched_collection, capsys):
    patched_collection.add_book("1984", "George Orwell", 1949)
    patched_collection.mark_as_read("1984")

    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "No unread books found" in output


def test_handle_list_unread_shows_no_unread_message_when_empty(patched_collection, capsys):
    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "No unread books found" in output


def test_handle_list_unread_includes_author_and_year(patched_collection, capsys):
    patched_collection.add_book("Dune", "Frank Herbert", 1965)

    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "Frank Herbert" in output
    assert "1965" in output


# ---------------------------------------------------------------------------
# main() command routing tests
# ---------------------------------------------------------------------------

def test_main_routes_unread_command(patched_collection, monkeypatch, capsys):
    patched_collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "unread"])

    book_app.main()

    output = capsys.readouterr().out
    assert "Dune" in output


def test_main_unread_command_case_insensitive(patched_collection, monkeypatch, capsys):
    patched_collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr(sys, "argv", ["book_app.py", "UNREAD"])

    book_app.main()

    output = capsys.readouterr().out
    assert "Dune" in output


# ---------------------------------------------------------------------------
# show_help includes unread command
# ---------------------------------------------------------------------------

def test_show_help_includes_unread_command(capsys):
    book_app.show_help()

    output = capsys.readouterr().out
    assert "unread" in output
