import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import book_app
import books


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


@pytest.fixture
def set_input(monkeypatch: pytest.MonkeyPatch):
    """Provide a helper for mocking sequential input responses."""

    def _set_input(responses: list[str]) -> None:
        remaining_responses = responses.copy()
        monkeypatch.setattr("builtins.input", lambda _: remaining_responses.pop(0))

    return _set_input


class TestHandleAdd:
    """Tests for handle_add."""

    @pytest.mark.parametrize(
        ("responses", "expected_book"),
        [
            (["  Dune  ", "  Frank Herbert  ", "1965"], ("Dune", "Frank Herbert", 1965)),
            (["Neuromancer", "William Gibson", "0"], ("Neuromancer", "William Gibson", 0)),
            (
                ["Snow Crash", "Neal Stephenson", str(date.today().year)],
                ("Snow Crash", "Neal Stephenson", date.today().year),
            ),
        ],
    )
    def test_normalizes_text_and_allows_valid_years(
        self,
        responses: list[str],
        expected_book: tuple[str, str, int],
        set_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        set_input(responses)

        result = book_app.handle_add(collection)

        captured = capsys.readouterr()
        saved_book = collection.list_books()[0]
        assert result == 0
        assert "Book added successfully." in captured.out
        assert (saved_book.title, saved_book.author, saved_book.year) == expected_book

    @pytest.mark.parametrize(
        ("responses", "expected_message"),
        [
            (["", "Frank Herbert", "1965"], "Error: Title cannot be empty."),
            (["Dune", "", "1965"], "Error: Author cannot be empty."),
            (["Dune", "Frank Herbert", ""], "Error: Year cannot be empty. Please enter a publication year."),
            (["Dune", "Frank Herbert", "invalid"], "Error: Year must be a whole number."),
            (["Dune", "Frank Herbert", "-1"], "Error: Year cannot be negative."),
            (
                ["Dune", "Frank Herbert", str(date.today().year + 1)],
                f"Error: Year cannot be in the future. Please enter a year up to {date.today().year}.",
            ),
        ],
    )
    def test_invalid_input(
        self,
        responses: list[str],
        expected_message: str,
        set_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        set_input(responses)

        result = book_app.handle_add(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert expected_message in captured.out


class TestHandleList:
    """Tests for handle_list."""

    def test_shows_empty_state(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()

        result = book_app.handle_list(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "No books found." in captured.out

    def test_displays_books_with_shared_format(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")

        result = book_app.handle_list(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "Your Book Collection:" in captured.out
        assert "1. [ ] Dune by Frank Herbert (1965)" in captured.out
        assert "2. [✓] 1984 by George Orwell (1949)" in captured.out


class TestHandleListUnread:
    """Tests for handle_list_unread."""

    def test_shows_only_unread_books(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")

        result = book_app.handle_list_unread(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "Your Book Collection:" in captured.out
        assert "1. [ ] Dune by Frank Herbert (1965)" in captured.out
        assert "1984 by George Orwell (1949)" not in captured.out

    def test_shows_empty_state_when_no_unread_books(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.mark_as_read("Dune")

        result = book_app.handle_list_unread(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "No books found." in captured.out


class TestHandleRemove:
    """Tests for handle_remove."""

    @pytest.mark.parametrize("title", ["", "   "])
    def test_missing_title(
        self,
        title: str,
        set_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        set_input([title])

        result = book_app.handle_remove(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert "Error: Title cannot be empty." in captured.out

    def test_book_not_found(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        monkeypatch.setattr("builtins.input", lambda _: "Missing Book")

        result = book_app.handle_remove(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert 'Error: Book "Missing Book" was not found in the collection.' in captured.out

    def test_partial_title_shows_suggestion(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)
        monkeypatch.setattr("builtins.input", lambda _: "Dune")

        result = book_app.handle_remove(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert (
            'Error: No exact match found for "Dune". Try one of these full titles: '
            '"Dune Messiah".'
        ) in captured.out


class TestHandleMarkRead:
    """Tests for handle_mark_read."""

    @pytest.mark.parametrize("title", ["", "   "])
    def test_missing_title(
        self,
        title: str,
        set_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        set_input([title])

        result = book_app.handle_mark_read(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert "Error: Title cannot be empty." in captured.out

    def test_book_not_found(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        monkeypatch.setattr("builtins.input", lambda _: "Missing Book")

        result = book_app.handle_mark_read(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert "Error: Book not found." in captured.out

    def test_success(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        monkeypatch.setattr("builtins.input", lambda _: "Dune")

        result = book_app.handle_mark_read(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "Book marked as read." in captured.out
        assert collection.find_book_by_title("Dune").read is True


class TestHandleFind:
    """Tests for handle_find."""

    @pytest.mark.parametrize("author", ["", "   "])
    def test_missing_author(
        self,
        author: str,
        set_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        set_input([author])

        result = book_app.handle_find(collection)

        captured = capsys.readouterr()
        assert result == 1
        assert "Error: Author cannot be empty." in captured.out

    def test_displays_matching_books_with_shared_format(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Children of Dune", "Frank Herbert", 1976)
        monkeypatch.setattr("builtins.input", lambda _: "Frank Herbert")

        result = book_app.handle_find(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "Your Book Collection:" in captured.out
        assert "1. [ ] Dune by Frank Herbert (1965)" in captured.out
        assert "2. [ ] Children of Dune by Frank Herbert (1976)" in captured.out

    def test_allows_whitespace_around_author_name(
        self,
        set_input,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        set_input(["  Frank Herbert  "])

        result = book_app.handle_find(collection)

        captured = capsys.readouterr()
        assert result == 0
        assert "1. [ ] Dune by Frank Herbert (1965)" in captured.out


class TestCreateCollectionCommand:
    """Tests for create_collection_command."""

    def test_returns_handler_result(self) -> None:
        expected_collection = books.BookCollection()

        def handler(collection: books.BookCollection) -> int:
            assert collection is expected_collection
            return 7

        command = book_app.create_collection_command(handler)

        original_collection = book_app.BookCollection
        book_app.BookCollection = lambda: expected_collection
        try:
            result = command()
        finally:
            book_app.BookCollection = original_collection

        assert result == 7

    @pytest.mark.parametrize(
        ("exception_type", "message"),
        [
            (OSError, "cannot open data"),
            (ValueError, "invalid book data"),
        ],
    )
    def test_handles_collection_initialization_errors(
        self,
        exception_type: type[Exception],
        message: str,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        def raise_error() -> None:
            raise exception_type(message)

        monkeypatch.setattr(book_app, "BookCollection", raise_error)
        command = book_app.create_collection_command(lambda _: 0)

        result = command()

        captured = capsys.readouterr()
        assert result == 1
        assert f"Error: {message}" in captured.out


class TestMain:
    """Tests for main."""

    def test_no_args_shows_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        result = book_app.main([])

        captured = capsys.readouterr()
        assert result == 0
        assert "Book Collection Helper" in captured.out

    def test_command_lookup_is_case_insensitive(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        calls: list[str] = []

        def fake_help() -> int:
            calls.append("help")
            return 0

        monkeypatch.setitem(book_app.COMMAND_HANDLERS, "help", fake_help)

        result = book_app.main(["HeLp"])

        assert result == 0
        assert calls == ["help"]

    def test_list_unread_command_dispatches_handler(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        calls: list[str] = []

        def fake_handler() -> int:
            calls.append("list-unread")
            return 0

        monkeypatch.setitem(book_app.COMMAND_HANDLERS, "list-unread", fake_handler)

        result = book_app.main(["list-unread"])

        assert result == 0
        assert calls == ["list-unread"]

    def test_help_command_does_not_initialize_collection(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        def raise_os_error() -> None:
            raise OSError("should not be called")

        monkeypatch.setattr(book_app, "BookCollection", raise_os_error)

        result = book_app.main(["help"])

        captured = capsys.readouterr()
        assert result == 0
        assert "Book Collection Helper" in captured.out
        assert "should not be called" not in captured.out

    def test_unknown_command(self, capsys: pytest.CaptureFixture[str]) -> None:
        result = book_app.main(["unknown"])

        captured = capsys.readouterr()
        assert result == 1
        assert "Unknown command." in captured.out

    def test_collection_init_failure(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        def raise_os_error() -> None:
            raise OSError("cannot read data file")

        monkeypatch.setattr(book_app, "BookCollection", raise_os_error)

        result = book_app.main(["list"])

        captured = capsys.readouterr()
        assert result == 1
        assert "Error: cannot read data file" in captured.out
