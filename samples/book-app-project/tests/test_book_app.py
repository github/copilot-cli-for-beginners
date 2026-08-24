import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
import book_app


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file and a fresh collection for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    monkeypatch.setattr(book_app, "collection", books.BookCollection())


def test_handle_mark_read_marks_existing_book(monkeypatch, capsys):
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    book_app.handle_mark_read()

    captured = capsys.readouterr()
    assert "Book marked as read." in captured.out
    book = book_app.collection.find_book_by_title("Dune")
    assert book.read is True


def test_handle_mark_read_reports_missing_book(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "Nonexistent Book")

    book_app.handle_mark_read()

    captured = capsys.readouterr()
    assert "Book not found." in captured.out


def test_handle_stats_empty_collection(capsys):
    book_app.handle_stats()

    captured = capsys.readouterr()
    assert "Total books: 0" in captured.out
    assert "Read: 0" in captured.out
    assert "Unread: 0" in captured.out


def test_handle_stats_mixed_read_unread(monkeypatch, capsys):
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    book_app.collection.add_book("1984", "George Orwell", 1949)
    monkeypatch.setattr("builtins.input", lambda _: "Dune")
    book_app.handle_mark_read()

    book_app.handle_stats()

    captured = capsys.readouterr()
    assert "Total books: 2" in captured.out
    assert "Read: 1" in captured.out
    assert "Unread: 1" in captured.out
