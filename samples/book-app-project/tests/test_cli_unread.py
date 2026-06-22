import sys
import os
import json

# Ensure package import path points to the project samples directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books


@pytest.fixture
def prepare_book_app(tmp_path, monkeypatch):
    """Prepare a temporary DATA_FILE and import a fresh book_app module."""
    temp_file = tmp_path / "data.json"
    # start with an empty list by default
    temp_file.write_text("[]")

    # Point the books module at the temporary file before importing book_app
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    # Ensure book_app is imported fresh so it constructs its collection from the temp file
    if "book_app" in sys.modules:
        del sys.modules["book_app"]

    import importlib
    book_app = importlib.import_module("book_app")

    return book_app, temp_file


def test_cli_unread_shows_only_unread(prepare_book_app, capsys, monkeypatch):
    book_app, temp_file = prepare_book_app

    data = [
        {"title": "Book A", "author": "Author A", "year": 2000, "read": False, "reviews": []},
        {"title": "Book B", "author": "Author B", "year": 2001, "read": True, "reviews": []},
        {"title": "Book C", "author": "Author C", "year": 2002, "read": False, "reviews": []},
    ]
    temp_file.write_text(json.dumps(data))

    # Reload collection inside book_app so it picks up the new file contents
    book_app.collection.load_books()

    monkeypatch.setattr(sys, "argv", ["book_app.py", "unread"])
    book_app.main()

    out = capsys.readouterr().out
    assert "Book A" in out
    assert "Book C" in out
    assert "Book B" not in out


def test_cli_list_unread_alias_behaves_same(prepare_book_app, capsys, monkeypatch):
    book_app, temp_file = prepare_book_app

    data = [
        {"title": "Only Read", "author": "Auth", "year": 1990, "read": True, "reviews": []},
        {"title": "Unread One", "author": "Auth", "year": 1991, "read": False, "reviews": []},
    ]
    temp_file.write_text(json.dumps(data))
    book_app.collection.load_books()

    monkeypatch.setattr(sys, "argv", ["book_app.py", "list-unread"])
    book_app.main()

    out = capsys.readouterr().out
    assert "Unread One" in out
    assert "Only Read" not in out


def test_cli_unread_when_no_unread_books_reports_empty(prepare_book_app, capsys, monkeypatch):
    book_app, temp_file = prepare_book_app

    data = [
        {"title": "R1", "author": "A", "year": 2000, "read": True, "reviews": []},
        {"title": "R2", "author": "B", "year": 2001, "read": True, "reviews": []},
    ]
    temp_file.write_text(json.dumps(data))
    book_app.collection.load_books()

    monkeypatch.setattr(sys, "argv", ["book_app.py", "unread"]) 
    book_app.main()

    out = capsys.readouterr().out
    assert "No books found." in out
