import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import book_app
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


class TestReadCommand:
    """Tests for the read command in the CLI."""

    def test_marks_matching_book_as_read(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        monkeypatch.setattr("builtins.input", lambda _: "Dune")

        exit_code = book_app.main(["read"])

        updated_collection = BookCollection()
        updated_book = updated_collection.find_book_by_title("Dune")

        assert exit_code == 0
        assert updated_book is not None
        assert updated_book.read is True
        assert "Book marked as read." in capsys.readouterr().out

    def test_reports_missing_book(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        monkeypatch.setattr("builtins.input", lambda _: "Missing Book")

        exit_code = book_app.main(["read"])

        assert exit_code == 0
        assert "No matching book was found." in capsys.readouterr().out


class TestYearCommand:
    """Tests for the year command in the CLI."""

    def test_lists_books_in_requested_year_range(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Neuromancer", "William Gibson", 1984)
        collection.add_book("The Martian", "Andy Weir", 2011)
        responses = iter(["1965", "1984"])
        monkeypatch.setattr("builtins.input", lambda _: next(responses))

        exit_code = book_app.main(["year"])
        output = capsys.readouterr().out

        assert exit_code == 0
        assert "Your Book Collection:" in output
        assert "Dune by Frank Herbert (1965)" in output
        assert "Neuromancer by William Gibson (1984)" in output
        assert "The Martian by Andy Weir (2011)" not in output

    def test_returns_error_for_reversed_year_range(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        responses = iter(["2000", "1990"])
        monkeypatch.setattr("builtins.input", lambda _: next(responses))

        exit_code = book_app.main(["year"])
        output = capsys.readouterr().out

        assert exit_code == 1
        assert "Error: Start year cannot be greater than end year." in output


def test_list_uses_shared_book_display(capsys: pytest.CaptureFixture[str]) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    exit_code = book_app.main(["list"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Your Book Collection:" in output
    assert "1. [ ] Dune by Frank Herbert (1965)" in output


def test_list_unread_shows_only_unread_books(capsys: pytest.CaptureFixture[str]) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)
    collection.mark_as_read("Neuromancer")

    exit_code = book_app.main(["list", "unread"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Your Book Collection:" in output
    assert "Dune by Frank Herbert (1965)" in output
    assert "Neuromancer by William Gibson (1984)" not in output


def test_list_unread_accepts_case_insensitive_option(capsys: pytest.CaptureFixture[str]) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)
    collection.mark_as_read("Neuromancer")

    exit_code = book_app.main(["list", "UNREAD"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Dune by Frank Herbert (1965)" in output
    assert "Neuromancer by William Gibson (1984)" not in output


def test_list_unread_shows_no_books_found_when_every_book_is_read(
    capsys: pytest.CaptureFixture[str],
) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")

    exit_code = book_app.main(["list", "unread"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert output == "No books found.\n"


def test_main_without_args_shows_help(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = book_app.main([])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Book Collection Helper" in output


def test_show_help_uses_shared_option_renderer(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_format_option_list(title: str, options: tuple[str, ...], *, trailing_blank_line: bool) -> str:
        captured["title"] = title
        captured["options"] = options
        captured["trailing_blank_line"] = trailing_blank_line
        return "rendered help"

    monkeypatch.setattr(book_app, "format_option_list", fake_format_option_list)

    book_app.show_help()

    assert captured == {
        "title": "Book Collection Helper",
        "options": (
            "Commands:",
            "  list     - Show all books",
            "  list unread - Show only unread books",
            "  add      - Add a new book",
            "  read     - Mark a book as read",
            "  remove   - Remove a book by title",
            "  find     - Find books by author",
            "  year     - Find books by year range",
            "  help     - Show this help message",
        ),
        "trailing_blank_line": True,
    }


def test_show_help_prints_formatted_output(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(book_app, "format_option_list", lambda *args, **kwargs: "rendered help")

    book_app.show_help()

    assert capsys.readouterr().out == "rendered help"


def test_help_command_does_not_load_books(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    exit_code = book_app.main(["help"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Book Collection Helper" in output
    assert "not valid JSON" not in output


def test_add_returns_error_exit_code_for_invalid_input(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "   ")

    exit_code = book_app.main(["add"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Title cannot be empty." in output


def test_add_returns_error_exit_code_for_duplicate_title(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    responses = iter(["  dune  ", "Someone Else", "2024"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))

    exit_code = book_app.main(["add"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: A book with this title already exists." in output


def test_unknown_command_does_not_load_books(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    exit_code = book_app.main(["unknown"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Unknown command 'unknown'." in output
    assert "Book Collection Helper" in output
    assert "not valid JSON" not in output


def test_command_rejects_extra_arguments_before_loading_books(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    exit_code = book_app.main(["list", "extra"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Command 'list' only supports the 'unread' option." in output
    assert "not valid JSON" not in output


def test_list_unread_rejects_multiple_arguments_before_loading_books(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    exit_code = book_app.main(["list", "unread", "extra"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Command 'list' only supports the 'unread' option." in output
    assert "not valid JSON" not in output


def test_runtime_book_data_errors_use_shared_error_format(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail_list(_collection: BookCollection) -> int:
        raise books.BookDataError("Disk full.")

    monkeypatch.setattr(book_app, "handle_list", fail_list)

    exit_code = book_app.main(["list"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Disk full." in output


def test_unread_runtime_book_data_errors_use_shared_error_format(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail_list_unread(_collection: BookCollection) -> int:
        raise books.BookDataError("Disk full.")

    monkeypatch.setattr(book_app, "handle_list_unread", fail_list_unread)

    exit_code = book_app.main(["list", "unread"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Disk full." in output


def test_startup_book_data_errors_use_shared_error_format(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    exit_code = book_app.main(["list"])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Error: Could not load" in output
    assert "not valid JSON" in output
