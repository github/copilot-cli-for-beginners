import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


@pytest.fixture
def collection(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> BookCollection:
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    test_collection = BookCollection()
    monkeypatch.setattr(book_app, "collection", test_collection)
    return test_collection


def test_list_unread_command_displays_unread_books_only(
    collection: BookCollection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("1984")
    monkeypatch.setattr(sys, "argv", ["book_app.py", "list", "unread"])

    book_app.main()

    output = capsys.readouterr().out
    assert "Dune by Frank Herbert (1965)" in output
    assert "1984 by George Orwell" not in output


def test_list_unread_command_reports_no_books_when_none_are_unread(
    collection: BookCollection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["book_app.py", "list", "unread"])

    book_app.main()

    assert "No books found." in capsys.readouterr().out


def test_help_includes_list_unread_command(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["book_app.py", "help"])

    book_app.main()

    assert "list unread - Show unread books" in capsys.readouterr().out
