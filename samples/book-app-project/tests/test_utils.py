import pytest

from books import Book
from utils import get_user_choice, print_books


def test_get_book_details_retries_empty_title(monkeypatch, capsys):
    responses = iter(["", "The Hobbit", "J.R.R. Tolkien", "1937"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    from utils import get_book_details

    assert get_book_details() == ("The Hobbit", "J.R.R. Tolkien", 1937)
    assert "Book title cannot be empty." in capsys.readouterr().out


def test_get_user_choice_returns_valid_choice(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")

    assert get_user_choice() == "3"


@pytest.mark.parametrize(
    "invalid_choice, expected_message",
    [
        ("", "Please enter a choice from 1 to 5."),
        ("abc", "Please enter a numeric choice from 1 to 5."),
    ],
)
def test_get_user_choice_retries_invalid_input(
    monkeypatch, capsys, invalid_choice, expected_message
):
    choices = iter([invalid_choice, "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(choices))

    assert get_user_choice() == "2"
    assert expected_message in capsys.readouterr().out


def test_print_books_displays_read_status(capsys):
    books = [Book("1984", "George Orwell", 1949, read=True)]

    print_books(books)

    output = capsys.readouterr().out
    assert "1. 1984 by George Orwell (1949) - Read" in output
    assert "✅" not in output
    assert "📖" not in output


def test_print_books_handles_empty_collection(capsys):
    print_books([])

    assert capsys.readouterr().out == "No books in your collection.\n"
