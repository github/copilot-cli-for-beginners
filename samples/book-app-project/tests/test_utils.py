import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from books import Book
import utils


@pytest.fixture
def mock_input(monkeypatch: pytest.MonkeyPatch):
    """Mock interactive input with a predefined sequence of responses."""

    def _mock_input(responses: list[str]) -> None:
        remaining_responses = responses.copy()
        monkeypatch.setattr("builtins.input", lambda _: remaining_responses.pop(0))

    return _mock_input


class TestValidateUserChoice:
    """Tests for validate_user_choice."""

    @pytest.mark.parametrize(
        ("choice", "expected_message"),
        [
            ("", "Choice cannot be empty. Please enter a number from 1 to 5."),
            ("abc", "Invalid choice. Please enter a number from 1 to 5."),
            ("9", "Choice must be between 1 and 5."),
            ("3", None),
        ],
    )
    def test_returns_expected_validation_message(
        self,
        choice: str,
        expected_message: str | None,
    ) -> None:
        assert utils.validate_user_choice(choice) == expected_message


class TestGetUserChoice:
    """Tests for get_user_choice."""

    def test_retries_after_empty_input(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        responses = ["", "2"]
        monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

        result = utils.get_user_choice()

        captured = capsys.readouterr()
        assert result == "2"
        assert "Choice cannot be empty. Please enter a number from 1 to 5." in captured.out

    def test_retries_after_non_numeric_input(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        responses = ["abc", "4"]
        monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

        result = utils.get_user_choice()

        captured = capsys.readouterr()
        assert result == "4"
        assert "Invalid choice. Please enter a number from 1 to 5." in captured.out

    def test_retries_after_out_of_range_number(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        responses = ["9", "5"]
        monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

        result = utils.get_user_choice()

        captured = capsys.readouterr()
        assert result == "5"
        assert "Choice must be between 1 and 5." in captured.out


class TestGetBookDetails:
    """Tests for get_book_details."""

    def test_retries_after_empty_title(
        self,
        mock_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_input(["", "Dune", "Frank Herbert", "1965"])

        result = utils.get_book_details()

        captured = capsys.readouterr()
        assert result == ("Dune", "Frank Herbert", 1965)
        assert "Title cannot be empty. Please enter a book title." in captured.out

    @pytest.mark.parametrize(
        ("year_input", "expected_title", "expected_author"),
        [
            ("invalid", "Dune", "Frank Herbert"),
            ("19.65", "Dune", "Frank Herbert"),
            ("1965a", "Dune", "Frank Herbert"),
            ("", "Dune", "Frank Herbert"),
        ],
    )
    def test_defaults_invalid_year_formats_to_zero(
        self,
        mock_input,
        capsys: pytest.CaptureFixture[str],
        year_input: str,
        expected_title: str,
        expected_author: str,
    ) -> None:
        mock_input([expected_title, expected_author, year_input])

        result = utils.get_book_details()

        captured = capsys.readouterr()
        assert result == (expected_title, expected_author, 0)
        assert "Invalid year. Defaulting to 0." in captured.out

    def test_returns_details_for_valid_input(self, mock_input) -> None:
        mock_input(["The Hobbit", "J.R.R. Tolkien", "1937"])

        result = utils.get_book_details()

        assert result == ("The Hobbit", "J.R.R. Tolkien", 1937)

    def test_trims_surrounding_whitespace_from_inputs(
        self,
        mock_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_input(["  Dune  ", "  Frank Herbert  ", " 1965 "])

        result = utils.get_book_details()

        captured = capsys.readouterr()
        assert result == ("Dune", "Frank Herbert", 1965)
        assert captured.out == ""

    def test_reprompts_when_title_is_only_whitespace(
        self,
        mock_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_input(["   ", "Dune", "Frank Herbert", "1965"])

        result = utils.get_book_details()

        captured = capsys.readouterr()
        assert result == ("Dune", "Frank Herbert", 1965)
        assert "Title cannot be empty. Please enter a book title." in captured.out

    def test_accepts_very_long_title(self, mock_input) -> None:
        long_title = "A" * 500
        mock_input([long_title, "Frank Herbert", "1965"])

        result = utils.get_book_details()

        assert result == (long_title, "Frank Herbert", 1965)

    @pytest.mark.parametrize(
        "author_name",
        [
            "Gabriel Garcia Marquez",
            "Mary Shelley-Wollstonecraft",
            "O'Connor, Flannery",
            "N. K. Jemisin",
        ],
    )
    def test_accepts_special_characters_in_author_names(
        self,
        mock_input,
        author_name: str,
    ) -> None:
        mock_input(["Dune", author_name, "1965"])

        result = utils.get_book_details()

        assert result == ("Dune", author_name, 1965)


class TestParsePublicationYear:
    """Tests for parse_publication_year."""

    @pytest.mark.parametrize(
        ("year_input", "expected_result"),
        [
            ("1965", (1965, None)),
            ("invalid", (0, "Invalid year. Defaulting to 0.")),
        ],
    )
    def test_returns_parsed_year_and_optional_message(
        self,
        year_input: str,
        expected_result: tuple[int, str | None],
    ) -> None:
        assert utils.parse_publication_year(year_input) == expected_result


class TestFormatBooks:
    """Tests for format_books."""

    def test_formats_empty_state(self) -> None:
        assert utils.format_books([]) == "No books found."

    def test_formats_books_with_read_status(self) -> None:
        books = [
            Book(title="Dune", author="Frank Herbert", year=1965, read=False),
            Book(title="1984", author="George Orwell", year=1949, read=True),
        ]

        result = utils.format_books(books)

        assert "Your Book Collection:" in result
        assert "1. [ ] Dune by Frank Herbert (1965)" in result
        assert "2. [✓] 1984 by George Orwell (1949)" in result


class TestPrintBooks:
    """Tests for print_books."""

    def test_prints_empty_state(self, capsys: pytest.CaptureFixture[str]) -> None:
        utils.print_books([])

        captured = capsys.readouterr()
        assert "No books found." in captured.out

    def test_prints_books_with_read_status(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        books = [
            Book(title="Dune", author="Frank Herbert", year=1965, read=False),
            Book(title="1984", author="George Orwell", year=1949, read=True),
        ]

        utils.print_books(books)

        captured = capsys.readouterr()
        assert "Your Book Collection:" in captured.out
        assert "1. [ ] Dune by Frank Herbert (1965)" in captured.out
        assert "2. [✓] 1984 by George Orwell (1949)" in captured.out


class TestPrintHelp:
    """Tests for print_help."""

    def test_prints_command_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        utils.print_help()

        captured = capsys.readouterr()
        assert "Book Collection Helper" in captured.out
        assert "list     - Show all books" in captured.out
        assert "help     - Show this help message" in captured.out


class TestFormatHelp:
    """Tests for format_help."""

    def test_returns_command_help_text(self) -> None:
        result = utils.format_help()

        assert "Book Collection Helper" in result
        assert "list     - Show all books" in result
        assert "help     - Show this help message" in result
