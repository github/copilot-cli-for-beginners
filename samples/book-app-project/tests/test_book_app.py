import os
import sys
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


class TestHandleAdd:
    """Tests for handle_add."""

    @pytest.mark.parametrize(
        ("responses", "expected_message"),
        [
            (["", "Frank Herbert", "1965"], "Error: Title cannot be empty."),
            (["Dune", "", "1965"], "Error: Author cannot be empty."),
            (["Dune", "Frank Herbert", "invalid"], "Error: invalid literal for int()"),
            (["Dune", "Frank Herbert", "-1"], "Error: Year cannot be negative."),
        ],
    )
    def test_invalid_input(
        self,
        responses: list[str],
        expected_message: str,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

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


class TestHandleRemove:
    """Tests for handle_remove."""

    def test_missing_title(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        monkeypatch.setattr("builtins.input", lambda _: "")

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
        assert "Error: Book not found." in captured.out


class TestHandleMarkRead:
    """Tests for handle_mark_read."""

    def test_missing_title(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        monkeypatch.setattr("builtins.input", lambda _: "")

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

    def test_missing_author(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        collection = books.BookCollection()
        monkeypatch.setattr("builtins.input", lambda _: "")

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


class TestMain:
    """Tests for main."""

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
