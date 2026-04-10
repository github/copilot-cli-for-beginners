import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch
from utils import get_book_details


def make_inputs(*values):
    """Helper: returns a side_effect list for patching input() with multiple calls."""
    return list(values)


# ---------------------------------------------------------------------------
# TestGetBookDetails
# ---------------------------------------------------------------------------

class TestGetBookDetails:
    """Tests for utils.get_book_details()."""

    # --- Happy path ---

    def test_valid_input_returns_correct_tuple(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "1965")):
            title, author, year = get_book_details()
        assert title == "Dune"
        assert author == "Frank Herbert"
        assert year == 1965

    def test_returns_tuple_of_three(self):
        with patch("builtins.input", side_effect=make_inputs("1984", "George Orwell", "1949")):
            result = get_book_details()
        assert len(result) == 3

    def test_year_is_int(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "1965")):
            _, _, year = get_book_details()
        assert isinstance(year, int)

    def test_title_and_author_are_strings(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "1965")):
            title, author, _ = get_book_details()
        assert isinstance(title, str)
        assert isinstance(author, str)

    # --- Whitespace stripping ---

    def test_strips_leading_trailing_whitespace_from_title(self):
        with patch("builtins.input", side_effect=make_inputs("  Dune  ", "Frank Herbert", "1965")):
            title, _, _ = get_book_details()
        assert title == "Dune"

    def test_strips_whitespace_from_author(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "  Frank Herbert  ", "1965")):
            _, author, _ = get_book_details()
        assert author == "Frank Herbert"

    def test_strips_whitespace_from_year(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "  1965  ")):
            _, _, year = get_book_details()
        assert year == 1965

    # --- Empty strings ---

    def test_empty_title_returns_empty_string(self):
        with patch("builtins.input", side_effect=make_inputs("", "Frank Herbert", "1965")):
            title, _, _ = get_book_details()
        assert title == ""

    def test_empty_author_returns_empty_string(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "", "1965")):
            _, author, _ = get_book_details()
        assert author == ""

    def test_empty_year_defaults_to_zero(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "")):
            _, _, year = get_book_details()
        assert year == 0

    def test_whitespace_only_title_returns_empty_string(self):
        with patch("builtins.input", side_effect=make_inputs("   ", "Frank Herbert", "1965")):
            title, _, _ = get_book_details()
        assert title == ""

    def test_whitespace_only_author_returns_empty_string(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "   ", "1965")):
            _, author, _ = get_book_details()
        assert author == ""

    # --- Invalid year formats ---

    def test_non_numeric_year_defaults_to_zero(self, capsys):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "abc")):
            _, _, year = get_book_details()
        assert year == 0

    def test_non_numeric_year_prints_warning(self, capsys):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "abc")):
            get_book_details()
        assert "Invalid year" in capsys.readouterr().out

    def test_float_year_defaults_to_zero(self, capsys):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "19.65")):
            _, _, year = get_book_details()
        assert year == 0

    def test_letter_mixed_with_digits_defaults_to_zero(self, capsys):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "19ab")):
            _, _, year = get_book_details()
        assert year == 0

    def test_negative_year_is_accepted(self):
        # Current behaviour: negative years pass through (known gap)
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "-100")):
            _, _, year = get_book_details()
        assert year == -100

    def test_zero_year_is_accepted(self):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", "0")):
            _, _, year = get_book_details()
        assert year == 0

    @pytest.mark.parametrize("bad_year", ["abc", "19.5", "19ab", "--", "year", "①②③"])
    def test_various_invalid_year_formats_default_to_zero(self, bad_year):
        with patch("builtins.input", side_effect=make_inputs("Dune", "Frank Herbert", bad_year)):
            _, _, year = get_book_details()
        assert year == 0

    # --- Very long titles ---

    def test_very_long_title_is_accepted(self):
        long_title = "A" * 1000
        with patch("builtins.input", side_effect=make_inputs(long_title, "Author", "2000")):
            title, _, _ = get_book_details()
        assert title == long_title

    def test_very_long_author_is_accepted(self):
        long_author = "B" * 1000
        with patch("builtins.input", side_effect=make_inputs("Title", long_author, "2000")):
            _, author, _ = get_book_details()
        assert author == long_author

    # --- Special characters in author names ---

    @pytest.mark.parametrize("author", [
        "J.R.R. Tolkien",           # dots
        "García Márquez",           # accented characters
        "Μary Shelley",             # Greek character
        "O'Brien",                  # apostrophe
        "Smith-Jones",              # hyphen
        "山田 太郎",                 # Japanese characters
        "李白",                      # Chinese characters
        "Ångström, A.",             # Nordic characters
        "Author (Ed.)",             # parentheses
        "First & Second",           # ampersand
    ])
    def test_special_characters_in_author(self, author):
        with patch("builtins.input", side_effect=make_inputs("Title", author, "2000")):
            _, result_author, _ = get_book_details()
        assert result_author == author

    @pytest.mark.parametrize("title", [
        "It's a Wonderful Life",    # apostrophe
        "Harry Potter & the ...",   # ampersand
        "Book: A Subtitle",         # colon
        "Title (2nd Edition)",      # parentheses
        "日本語タイトル",             # Japanese
        "Ñoño",                     # Spanish special characters
    ])
    def test_special_characters_in_title(self, title):
        with patch("builtins.input", side_effect=make_inputs(title, "Author", "2000")):
            result_title, _, _ = get_book_details()
        assert result_title == title
