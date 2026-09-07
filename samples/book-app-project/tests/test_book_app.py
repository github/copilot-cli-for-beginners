import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import book_app
from books import Book


def test_handle_list_uses_shared_book_display(monkeypatch):
    books = [Book("1984", "George Orwell", 1949, read=True)]
    collection = Mock()
    collection.list_books.return_value = books
    display = Mock()
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr(book_app, "print_books", display)

    book_app.handle_list()

    display.assert_called_once_with(books)


def test_handle_find_uses_shared_book_display(monkeypatch):
    books = [Book("Dune", "Frank Herbert", 1965)]
    collection = Mock()
    collection.find_by_author.return_value = books
    display = Mock()
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr(book_app, "print_books", display)
    monkeypatch.setattr("builtins.input", lambda _: "Frank Herbert")

    book_app.handle_find()

    collection.find_by_author.assert_called_once_with("Frank Herbert")
    display.assert_called_once_with(books)


def test_handle_unread_uses_shared_book_display(monkeypatch):
    books = [Book("Dune", "Frank Herbert", 1965)]
    collection = Mock()
    collection.list_unread_books.return_value = books
    display = Mock()
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr(book_app, "print_books", display)

    book_app.handle_unread()

    collection.list_unread_books.assert_called_once_with()
    display.assert_called_once_with(books)


def test_handle_unread_reports_when_no_books_are_unread(monkeypatch, capsys):
    collection = Mock()
    collection.list_unread_books.return_value = []
    display = Mock()
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr(book_app, "print_books", display)

    book_app.handle_unread()

    assert capsys.readouterr().out.strip() == "No unread books in your collection."
    display.assert_not_called()


def test_main_routes_unread_command(monkeypatch):
    handler = Mock()
    monkeypatch.setattr(book_app, "handle_unread", handler)
    monkeypatch.setattr(book_app.sys, "argv", ["book_app.py", "unread"])

    book_app.main()

    handler.assert_called_once_with()


def test_show_help_includes_unread_command(capsys):
    book_app.show_help()

    assert "unread   - Show unread books" in capsys.readouterr().out
