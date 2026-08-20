import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch
from utils import get_book_details


def make_inputs(title, author, year):
    """Helper to patch input() with three sequential responses."""
    return patch("builtins.input", side_effect=[title, author, year])


# ---------------------------------------------------------------------------
# Valid input
# ---------------------------------------------------------------------------

class TestGetBookDetailsValidInput:
    def test_returns_tuple_of_three(self):
        with make_inputs("1984", "George Orwell", "1949"):
            result = get_book_details()
        assert len(result) == 3

    def test_valid_book(self):
        with make_inputs("1984", "George Orwell", "1949"):
            title, author, year = get_book_details()
        assert title == "1984"
        assert author == "George Orwell"
        assert year == 1949

    def test_year_returned_as_int(self):
        with make_inputs("Dune", "Frank Herbert", "1965"):
            _, _, year = get_book_details()
        assert isinstance(year, int)

    def test_strips_whitespace_from_title(self):
        with make_inputs("  1984  ", "George Orwell", "1949"):
            title, _, _ = get_book_details()
        assert title == "1984"

    def test_strips_whitespace_from_author(self):
        with make_inputs("Dune", "  Frank Herbert  ", "1965"):
            _, author, _ = get_book_details()
        assert author == "Frank Herbert"

    def test_strips_whitespace_from_year(self):
        with make_inputs("Dune", "Frank Herbert", "  1965  "):
            _, _, year = get_book_details()
        assert year == 1965

    @pytest.mark.parametrize("title,author,year_str,expected_year", [
        ("1984", "George Orwell", "1949", 1949),
        ("Dune", "Frank Herbert", "1965", 1965),
        ("The Hobbit", "J.R.R. Tolkien", "1937", 1937),
        ("Foundation", "Isaac Asimov", "1951", 1951),
    ])
    def test_various_valid_books(self, title, author, year_str, expected_year):
        with make_inputs(title, author, year_str):
            t, a, y = get_book_details()
        assert t == title
        assert a == author
        assert y == expected_year


# ---------------------------------------------------------------------------
# Empty strings
# ---------------------------------------------------------------------------

class TestGetBookDetailsEmptyStrings:
    def test_empty_title_returns_empty_string(self):
        with make_inputs("", "George Orwell", "1949"):
            title, _, _ = get_book_details()
        assert title == ""

    def test_empty_author_returns_empty_string(self):
        with make_inputs("1984", "", "1949"):
            _, author, _ = get_book_details()
        assert author == ""

    def test_whitespace_only_title_stripped_to_empty(self):
        with make_inputs("   ", "George Orwell", "1949"):
            title, _, _ = get_book_details()
        assert title == ""

    def test_whitespace_only_author_stripped_to_empty(self):
        with make_inputs("1984", "   ", "1949"):
            _, author, _ = get_book_details()
        assert author == ""

    def test_empty_year_defaults_to_zero(self, capsys):
        with make_inputs("1984", "George Orwell", ""):
            _, _, year = get_book_details()
        assert year == 0

    def test_all_empty_inputs(self):
        with make_inputs("", "", ""):
            title, author, year = get_book_details()
        assert title == ""
        assert author == ""
        assert year == 0


# ---------------------------------------------------------------------------
# Invalid year formats
# ---------------------------------------------------------------------------

class TestGetBookDetailsInvalidYear:
    def test_non_numeric_year_defaults_to_zero(self, capsys):
        with make_inputs("1984", "George Orwell", "nineteen-forty-nine"):
            _, _, year = get_book_details()
        assert year == 0

    def test_invalid_year_prints_warning(self, capsys):
        with make_inputs("1984", "George Orwell", "abc"):
            get_book_details()
        captured = capsys.readouterr()
        assert "invalid year" in captured.out.lower()

    def test_float_year_string_defaults_to_zero(self, capsys):
        with make_inputs("1984", "George Orwell", "1949.5"):
            _, _, year = get_book_details()
        assert year == 0

    def test_year_with_letters_defaults_to_zero(self, capsys):
        with make_inputs("1984", "George Orwell", "1949abc"):
            _, _, year = get_book_details()
        assert year == 0

    def test_negative_year_is_accepted_as_int(self):
        with make_inputs("Ancient Text", "Unknown", "-500"):
            _, _, year = get_book_details()
        assert year == -500

    def test_zero_year_is_accepted(self):
        with make_inputs("Test", "Author", "0"):
            _, _, year = get_book_details()
        assert year == 0

    def test_very_large_year_is_accepted(self):
        with make_inputs("Future Book", "Author", "9999"):
            _, _, year = get_book_details()
        assert year == 9999

    @pytest.mark.parametrize("bad_year", ["abc", "12.5", "20xx", "--", "year", "①②③"])
    def test_various_invalid_years_default_to_zero(self, bad_year, capsys):
        with make_inputs("Title", "Author", bad_year):
            _, _, year = get_book_details()
        assert year == 0


# ---------------------------------------------------------------------------
# Very long titles
# ---------------------------------------------------------------------------

class TestGetBookDetailsLongTitles:
    def test_long_title_preserved(self):
        long_title = "A" * 500
        with make_inputs(long_title, "Author", "2000"):
            title, _, _ = get_book_details()
        assert title == long_title

    def test_long_title_still_stripped(self):
        long_title = "  " + "B" * 300 + "  "
        with make_inputs(long_title, "Author", "2000"):
            title, _, _ = get_book_details()
        assert title == "B" * 300

    def test_long_author_name_preserved(self):
        long_author = "Gabriel " * 50
        with make_inputs("Title", long_author, "2000"):
            _, author, _ = get_book_details()
        assert author == long_author.strip()

    def test_title_with_spaces_preserved(self):
        spaced = "The " * 100
        with make_inputs(spaced, "Author", "2000"):
            title, _, _ = get_book_details()
        assert title == spaced.strip()


# ---------------------------------------------------------------------------
# Special characters in author names
# ---------------------------------------------------------------------------

class TestGetBookDetailsSpecialCharacters:
    @pytest.mark.parametrize("author", [
        "J.R.R. Tolkien",
        "Ursula K. Le Guin",
        "Gabriel García Márquez",
        "Haruki Murakami (村上春樹)",
        "Nnedi Okofor-Obi",
        "Jean-Paul Sartre",
        "bell hooks",
        "O'Henry",
        "Author & Co-Author",
        "Name <email@example.com>",
        "Author's Name",
        "Ångström, Anders",
    ])
    def test_special_character_authors(self, author):
        with make_inputs("Some Book", author, "2000"):
            _, result_author, _ = get_book_details()
        assert result_author == author

    def test_title_with_punctuation(self):
        title = "It's a Wonderful Life: A Story (2nd Ed.)"
        with make_inputs(title, "Author", "1990"):
            result_title, _, _ = get_book_details()
        assert result_title == title

    def test_title_with_unicode(self):
        title = "café au lait & bœuf — a novel"
        with make_inputs(title, "Author", "2010"):
            result_title, _, _ = get_book_details()
        assert result_title == title

    def test_title_with_newline_stripped(self):
        with make_inputs("Title\n", "Author", "2000"):
            title, _, _ = get_book_details()
        assert title == "Title"

    def test_author_with_emoji(self):
        author = "Author 📚"
        with make_inputs("Book", author, "2021"):
            _, result_author, _ = get_book_details()
        assert result_author == author
