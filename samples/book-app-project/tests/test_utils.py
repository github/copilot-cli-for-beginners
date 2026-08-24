import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from books import Book
from utils import get_statistics, get_book_details, print_books


def test_get_statistics_empty_list():
    stats = get_statistics([])
    assert stats == {
        "total": 0,
        "read": 0,
        "unread": 0,
        "oldest": None,
        "newest": None,
    }


def test_get_statistics_mixed_read_unread():
    books = [
        Book("1984", "George Orwell", 1949, read=True),
        Book("Dune", "Frank Herbert", 1965, read=False),
        Book("The Hobbit", "J.R.R. Tolkien", 1937, read=True),
    ]
    stats = get_statistics(books)
    assert stats["total"] == 3
    assert stats["read"] == 2
    assert stats["unread"] == 1
    assert stats["oldest"].title == "The Hobbit"
    assert stats["newest"].title == "Dune"


def test_get_statistics_single_book():
    books = [Book("Dune", "Frank Herbert", 1965)]
    stats = get_statistics(books)
    assert stats["oldest"] is stats["newest"] is books[0]


def test_get_book_details_valid_input(monkeypatch):
    inputs = iter(["1984", "George Orwell", "1949"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    title, author, year = get_book_details()
    assert title == "1984"
    assert author == "George Orwell"
    assert year == 1949


def test_get_book_details_reprompts_on_invalid_year(monkeypatch):
    inputs = iter(["1984", "George Orwell", "not-a-year", "1949"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    _, _, year = get_book_details()
    assert year == 1949


def test_get_book_details_reprompts_on_out_of_range_year(monkeypatch):
    inputs = iter(["1984", "George Orwell", "0", "-5", "3000", "1949"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    _, _, year = get_book_details()
    assert year == 1949


def test_get_book_details_reprompts_on_empty_title_and_author(monkeypatch):
    inputs = iter(["", "1984", "", "George Orwell", "1949"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    title, author, year = get_book_details()
    assert title == "1984"
    assert author == "George Orwell"
    assert year == 1949


def test_print_books_empty_list(capsys):
    print_books([])
    captured = capsys.readouterr()
    assert "No books in your collection." in captured.out


def test_print_books_shows_read_and_unread_status(capsys):
    books = [
        Book("1984", "George Orwell", 1949, read=True),
        Book("Dune", "Frank Herbert", 1965, read=False),
    ]
    print_books(books)
    captured = capsys.readouterr()
    assert "1984 by George Orwell (1949) - ✅ Read" in captured.out
    assert "Dune by Frank Herbert (1965) - 📖 Unread" in captured.out
