import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils import get_book_details


def _mock_input(monkeypatch, responses):
    """Patch `builtins.input` to return each item in `responses` in turn.

    Each call to `input(prompt)` inside the code under test pops the next
    value from `responses`, in order.
    """
    responses_iter = iter(responses)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses_iter))


class TestGetBookDetailsValidInput:
    """Happy-path input for get_book_details."""

    def test_valid_title_author_year(self, monkeypatch):
        _mock_input(monkeypatch, ["Dune", "Frank Herbert", "1965"])

        title, author, year = get_book_details()

        assert title == "Dune"
        assert author == "Frank Herbert"
        assert year == 1965

    def test_negative_year_is_accepted(self, monkeypatch):
        """Current behavior: parse_year accepts any valid integer,
        including negative years (e.g. BCE dates)."""
        _mock_input(monkeypatch, ["Ancient Text", "Unknown", "-500"])

        _, _, year = get_book_details()

        assert year == -500


class TestGetBookDetailsEmptyStrings:
    """Empty/whitespace-only input handling for get_book_details."""

    def test_empty_title_reprompts_until_nonempty(self, monkeypatch, capsys):
        _mock_input(monkeypatch, ["", "   ", "Dune", "Frank Herbert", "1965"])

        title, author, year = get_book_details()

        assert title == "Dune"
        captured = capsys.readouterr()
        assert "Title cannot be empty" in captured.out

    def test_empty_author_is_allowed(self, monkeypatch):
        """Author has no validation, so an empty string is accepted."""
        _mock_input(monkeypatch, ["Dune", "", "1965"])

        _, author, _ = get_book_details()

        assert author == ""

    def test_empty_year_defaults_to_zero(self, monkeypatch, capsys):
        _mock_input(monkeypatch, ["Dune", "Frank Herbert", ""])

        _, _, year = get_book_details()

        assert year == 0
        captured = capsys.readouterr()
        assert "Invalid year. Defaulting to 0." in captured.out


class TestGetBookDetailsInvalidYearFormats:
    """Non-numeric / malformed year input handling."""

    @pytest.mark.parametrize(
        "year_input",
        ["abc", "19.65", "twenty", "19-65", "1965a", "one thousand", "1,965"],
    )
    def test_non_numeric_year_defaults_to_zero(self, monkeypatch, year_input):
        _mock_input(monkeypatch, ["Dune", "Frank Herbert", year_input])

        _, _, year = get_book_details()

        assert year == 0

    def test_year_with_surrounding_whitespace_is_parsed_correctly(self, monkeypatch):
        _mock_input(monkeypatch, ["Dune", "Frank Herbert", "  1965  "])

        _, _, year = get_book_details()

        assert year == 1965


class TestGetBookDetailsVeryLongTitles:
    """Very long title input handling."""

    def test_very_long_title_is_accepted_as_is(self, monkeypatch):
        long_title = "A" * 5000

        _mock_input(monkeypatch, [long_title, "Frank Herbert", "1965"])
        title, _, _ = get_book_details()

        assert title == long_title
        assert len(title) == 5000

    def test_title_with_surrounding_whitespace_is_stripped(self, monkeypatch):
        _mock_input(monkeypatch, ["   Dune   ", "Frank Herbert", "1965"])

        title, _, _ = get_book_details()

        assert title == "Dune"


class TestGetBookDetailsSpecialCharactersInAuthor:
    """Special characters, accents, and non-Latin scripts in author names."""

    @pytest.mark.parametrize(
        "author_input",
        [
            "J.R.R. Tolkien",
            "O'Brien",
            "Gabriel Garcia Marquez",
            "Jose Saramago",
            "Emile Zola",
            "李白",
            "Author-With-Hyphens",
            "Multiple   Spaces   Author",
            "Author & Co.",
        ],
    )
    def test_special_characters_in_author_are_preserved(self, monkeypatch, author_input):
        _mock_input(monkeypatch, ["Some Title", author_input, "2000"])

        _, author, _ = get_book_details()

        assert author == author_input
