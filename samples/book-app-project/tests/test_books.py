import json
import os
import sys
import threading
from dataclasses import asdict
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import books
from books import Book, BookCollection


@pytest.fixture
def temp_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Provide a temporary data file path for each test."""
    temp_file = tmp_path / "data.json"
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    return temp_file


@pytest.fixture
def empty_data_file(temp_data_file: Path) -> Path:
    """Create an empty JSON collection file."""
    temp_data_file.write_text("[]")
    return temp_data_file


@pytest.fixture
def empty_collection(empty_data_file: Path) -> BookCollection:
    """Provide a collection backed by an empty data file."""
    return BookCollection()


@pytest.fixture
def collection_with_books(empty_collection: BookCollection) -> BookCollection:
    """Provide a collection populated with sample books."""
    empty_collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    empty_collection.add_book("Dune", "Frank Herbert", 1965)
    empty_collection.add_book("Neuromancer", "William Gibson", 1984)
    return empty_collection


def make_collection_without_init() -> BookCollection:
    """Create a collection instance without triggering load_books."""
    collection = object.__new__(BookCollection)
    collection.books = []
    return collection


class TestNormalizeRequiredText:
    """Tests for _normalize_required_text."""

    @pytest.mark.parametrize(
        ("value", "field_name", "expected"),
        [
            ("Dune", "Title", "Dune"),
            ("  Frank Herbert  ", "Author", "Frank Herbert"),
            ("\nFoundation\t", "Title", "Foundation"),
        ],
    )
    def test_trims_and_returns_text(
        self,
        value: str,
        field_name: str,
        expected: str,
    ) -> None:
        assert books._normalize_required_text(value, field_name) == expected

    @pytest.mark.parametrize("value", ["", "   ", "\n\t  "])
    def test_rejects_empty_text(self, value: str) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty."):
            books._normalize_required_text(value, "Title")

    def test_raises_attribute_error_for_none(self) -> None:
        with pytest.raises(AttributeError):
            books._normalize_required_text(None, "Title")  # type: ignore[arg-type]


class TestBookDataclass:
    """Tests for Book."""

    def test_defaults_read_to_false(self) -> None:
        assert Book(title="Dune", author="Frank Herbert", year=1965) == Book(
            title="Dune",
            author="Frank Herbert",
            year=1965,
            read=False,
        )

    def test_asdict_includes_all_fields(self) -> None:
        assert asdict(Book(title="Dune", author="Frank Herbert", year=1965, read=True)) == {
            "title": "Dune",
            "author": "Frank Herbert",
            "year": 1965,
            "read": True,
        }


class TestInitAndLoading:
    """Tests for __init__ and load_books."""

    def test_init_loads_existing_books(self, temp_data_file: Path) -> None:
        temp_data_file.write_text(
            '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": true}]'
        )

        collection = BookCollection()

        assert collection.books == [
            Book(title="Dune", author="Frank Herbert", year=1965, read=True)
        ]

    def test_load_books_starts_empty_when_file_is_missing(self, temp_data_file: Path) -> None:
        collection = BookCollection()
        assert collection.books == []

    @pytest.mark.parametrize(
        ("contents", "expected_backup_name"),
        [
            ("{not valid json", "data.corrupted.json"),
            ('{"title": "Dune"}', "data.corrupted.json"),
            ('[{"title": "Dune", "year": 1965}]', "data.corrupted.json"),
            ('["Dune"]', "data.corrupted.json"),
        ],
    )
    def test_load_books_quarantines_invalid_data(
        self,
        temp_data_file: Path,
        capsys: pytest.CaptureFixture[str],
        contents: str,
        expected_backup_name: str,
    ) -> None:
        temp_data_file.write_text(contents)

        collection = BookCollection()

        captured = capsys.readouterr()
        backup_path = temp_data_file.with_name(expected_backup_name)
        assert collection.books == []
        assert temp_data_file.exists() is False
        assert backup_path.read_text() == contents
        assert "Warning: data.json is corrupted or invalid." in captured.out
        assert expected_backup_name in captured.out

    def test_load_books_uses_incremented_quarantine_name_when_backup_exists(
        self,
        temp_data_file: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        temp_data_file.write_text("{not valid json")
        temp_data_file.with_name("data.corrupted.json").write_text("older backup")

        collection = BookCollection()

        captured = capsys.readouterr()
        assert collection.books == []
        assert temp_data_file.with_name("data.corrupted.json").read_text() == "older backup"
        assert temp_data_file.with_name("data.corrupted-1.json").read_text() == "{not valid json"
        assert "data.corrupted-1.json" in captured.out

    def test_load_books_replaces_existing_in_memory_books(self, empty_collection: BookCollection) -> None:
        empty_collection.books = [Book(title="Old", author="Author", year=1900)]
        data_path = Path(books.DATA_FILE)
        data_path.write_text(
            '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": false}]'
        )

        empty_collection.load_books()

        assert empty_collection.books == [
            Book(title="Dune", author="Frank Herbert", year=1965, read=False)
        ]


class TestInternalHelpers:
    """Tests for internal file and data loading helpers."""

    def test_open_data_file_reads_contents(self, temp_data_file: Path) -> None:
        temp_data_file.write_text("hello")
        collection = make_collection_without_init()

        with collection._open_data_file("r") as data_file:
            assert data_file.read() == "hello"

    def test_open_data_file_writes_contents(self, temp_data_file: Path) -> None:
        collection = make_collection_without_init()

        with collection._open_data_file("w") as data_file:
            data_file.write("hello")

        assert temp_data_file.read_text() == "hello"

    def test_quarantine_corrupted_file_moves_data_file(self, temp_data_file: Path) -> None:
        temp_data_file.write_text("broken")
        collection = make_collection_without_init()

        backup_path = collection._quarantine_corrupted_file()

        assert temp_data_file.exists() is False
        assert backup_path.name == "data.corrupted.json"
        assert backup_path.read_text() == "broken"

    def test_quarantine_corrupted_file_skips_existing_backup(self, temp_data_file: Path) -> None:
        temp_data_file.write_text("broken")
        temp_data_file.with_name("data.corrupted.json").write_text("older backup")
        collection = make_collection_without_init()

        backup_path = collection._quarantine_corrupted_file()

        assert backup_path.name == "data.corrupted-1.json"
        assert backup_path.read_text() == "broken"

    def test_load_book_data_returns_book_instances(self, temp_data_file: Path) -> None:
        temp_data_file.write_text(
            '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": true}]'
        )
        collection = make_collection_without_init()

        assert collection._load_book_data() == [
            Book(title="Dune", author="Frank Herbert", year=1965, read=True)
        ]

    @pytest.mark.parametrize(
        ("contents", "expected_message"),
        [
            ('{"title": "Dune"}', "Expected a list of books."),
            ('["Dune"]', "Book entry #1 must be an object."),
            ('[{"title": "Dune", "year": 1965}]', "Book entry #1 has invalid fields."),
            (
                '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": false, "genre": "Sci-Fi"}]',
                "Book entry #1 has invalid fields.",
            ),
            (
                '[{"title": "Dune", "author": "Frank Herbert", "year": 1965}, {"title": "1984"}]',
                "Book entry #2 has invalid fields.",
            ),
        ],
    )
    def test_load_book_data_rejects_invalid_shapes(
        self,
        temp_data_file: Path,
        contents: str,
        expected_message: str,
    ) -> None:
        temp_data_file.write_text(contents)
        collection = make_collection_without_init()

        with pytest.raises(ValueError, match=expected_message):
            collection._load_book_data()


class TestSaveBooks:
    """Tests for save_books."""

    def test_save_books_writes_expected_json(self, empty_collection: BookCollection, temp_data_file: Path) -> None:
        empty_collection.books = [
            Book(title="Dune", author="Frank Herbert", year=1965, read=False),
            Book(title="1984", author="George Orwell", year=1949, read=True),
        ]

        empty_collection.save_books()

        assert temp_data_file.read_text().strip() == (
            "[\n"
            "  {\n"
            '    "title": "Dune",\n'
            '    "author": "Frank Herbert",\n'
            '    "year": 1965,\n'
            '    "read": false\n'
            "  },\n"
            "  {\n"
            '    "title": "1984",\n'
            '    "author": "George Orwell",\n'
            '    "year": 1949,\n'
            '    "read": true\n'
            "  }\n"
            "]"
        )

    def test_save_books_creates_missing_parent_directory(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        data_file = tmp_path / "nested" / "books.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))
        collection = make_collection_without_init()
        collection.books = [Book(title="Dune", author="Frank Herbert", year=1965)]

        collection.save_books()

        assert data_file.exists()
        assert json.loads(data_file.read_text()) == [
            {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": False}
        ]

    def test_save_books_overwrites_previous_contents(
        self,
        empty_collection: BookCollection,
        temp_data_file: Path,
    ) -> None:
        temp_data_file.write_text("stale data")
        empty_collection.books = [Book(title="Dune", author="Frank Herbert", year=1965)]

        empty_collection.save_books()

        assert json.loads(temp_data_file.read_text()) == [
            {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": False}
        ]

    def test_save_books_propagates_permission_error_from_replace(
        self,
        empty_collection: BookCollection,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        empty_collection.books = [Book(title="Dune", author="Frank Herbert", year=1965)]

        def raise_permission_error(source: Path, destination: Path) -> None:
            raise PermissionError("permission denied")

        monkeypatch.setattr(books.os, "replace", raise_permission_error)

        with pytest.raises(PermissionError, match="permission denied"):
            empty_collection.save_books()


class TestAddBook:
    """Tests for add_book."""

    def test_add_book_returns_new_book_and_updates_collection(
        self,
        empty_collection: BookCollection,
    ) -> None:
        book = empty_collection.add_book("1984", "George Orwell", 1949)

        assert book == Book(title="1984", author="George Orwell", year=1949, read=False)
        assert empty_collection.books == [book]

    def test_add_book_strips_surrounding_whitespace(self, empty_collection: BookCollection) -> None:
        book = empty_collection.add_book("  Dune  ", "  Frank Herbert  ", 1965)

        assert asdict(book) == {
            "title": "Dune",
            "author": "Frank Herbert",
            "year": 1965,
            "read": False,
        }

    @pytest.mark.parametrize("title", ["", "   ", "\n\t"])
    def test_add_book_rejects_empty_title(self, empty_collection: BookCollection, title: str) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty."):
            empty_collection.add_book(title, "Frank Herbert", 1965)

    @pytest.mark.parametrize("author", ["", "   ", "\n\t"])
    def test_add_book_rejects_empty_author(self, empty_collection: BookCollection, author: str) -> None:
        with pytest.raises(ValueError, match="Author cannot be empty."):
            empty_collection.add_book("Dune", author, 1965)

    @pytest.mark.parametrize("year", [-1, -1965])
    def test_add_book_rejects_negative_year(self, empty_collection: BookCollection, year: int) -> None:
        with pytest.raises(ValueError, match="Year cannot be negative."):
            empty_collection.add_book("Dune", "Frank Herbert", year)

    def test_add_book_rejects_future_year(self, empty_collection: BookCollection) -> None:
        future_year = date.today().year + 1

        with pytest.raises(
            ValueError,
            match=rf"Year cannot be in the future\. Please enter a year up to {date.today().year}\.",
        ):
            empty_collection.add_book("Dune", "Frank Herbert", future_year)

    def test_add_book_persists_normalized_values(
        self,
        empty_collection: BookCollection,
    ) -> None:
        added_book = empty_collection.add_book("  Dune  ", "  Frank Herbert  ", 1965)
        reloaded_collection = BookCollection()

        assert reloaded_collection.books == [added_book]

    def test_add_book_allows_duplicate_title_and_author(self, empty_collection: BookCollection) -> None:
        first_book = empty_collection.add_book("Dune", "Frank Herbert", 1965)
        second_book = empty_collection.add_book("Dune", "Frank Herbert", 1965)

        assert empty_collection.books == [first_book, second_book]


class TestListBooks:
    """Tests for list_books."""

    def test_returns_internal_list(self, collection_with_books: BookCollection) -> None:
        assert collection_with_books.list_books() is collection_with_books.books

    def test_returns_empty_list_for_empty_collection(self, empty_collection: BookCollection) -> None:
        assert empty_collection.list_books() == []


class TestListByYear:
    """Tests for list_by_year."""

    @pytest.mark.parametrize(
        ("start", "end", "expected_titles"),
        [
            (1937, 1937, ["The Hobbit"]),
            (1937, 1965, ["The Hobbit", "Dune"]),
            (1965, 1984, ["Dune", "Neuromancer"]),
            (-10, 1937, ["The Hobbit"]),
        ],
    )
    def test_returns_books_in_inclusive_range(
        self,
        collection_with_books: BookCollection,
        start: int,
        end: int,
        expected_titles: list[str],
    ) -> None:
        result = collection_with_books.list_by_year(start, end)

        assert [book.title for book in result] == expected_titles

    @pytest.mark.parametrize(("start", "end"), [(1900, 1901), (1985, 1990), (2000, 1990)])
    def test_returns_empty_list_when_no_books_match(
        self,
        collection_with_books: BookCollection,
        start: int,
        end: int,
    ) -> None:
        assert collection_with_books.list_by_year(start, end) == []


class TestFindBookByTitle:
    """Tests for find_book_by_title."""

    def test_matches_title_case_insensitively(self, collection_with_books: BookCollection) -> None:
        result = collection_with_books.find_book_by_title("dUnE")

        assert result == Book(title="Dune", author="Frank Herbert", year=1965, read=False)

    def test_returns_first_match_when_titles_are_duplicated(self, empty_collection: BookCollection) -> None:
        first_book = empty_collection.add_book("Dune", "Frank Herbert", 1965)
        empty_collection.add_book("Dune", "Someone Else", 2021)

        assert empty_collection.find_book_by_title("dune") is first_book

    def test_returns_none_when_title_is_not_found(self, collection_with_books: BookCollection) -> None:
        assert collection_with_books.find_book_by_title("Foundation") is None

    @pytest.mark.parametrize("title", ["Dune", "", "   "])
    def test_returns_none_when_collection_is_empty(
        self,
        empty_collection: BookCollection,
        title: str,
    ) -> None:
        assert empty_collection.find_book_by_title(title) is None


class TestMarkAsRead:
    """Tests for mark_as_read."""

    def test_marks_book_case_insensitively_and_persists(self, empty_collection: BookCollection) -> None:
        empty_collection.add_book("Dune", "Frank Herbert", 1965)

        result = empty_collection.mark_as_read("dUnE")
        reloaded_collection = BookCollection()

        assert result is True
        assert reloaded_collection.find_book_by_title("Dune").read is True

    def test_returns_false_without_saving_when_title_is_not_found(
        self,
        empty_collection: BookCollection,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        save_books_called = False

        def fake_save_books() -> None:
            nonlocal save_books_called
            save_books_called = True

        monkeypatch.setattr(empty_collection, "save_books", fake_save_books)

        result = empty_collection.mark_as_read("Missing Book")

        assert result is False
        assert save_books_called is False

    def test_returns_false_for_empty_collection(self, empty_collection: BookCollection) -> None:
        assert empty_collection.mark_as_read("Dune") is False

    def test_only_marks_first_matching_title(self, empty_collection: BookCollection) -> None:
        first_book = empty_collection.add_book("Dune", "Frank Herbert", 1965)
        second_book = empty_collection.add_book("Dune", "Brian Herbert", 2001)

        assert empty_collection.mark_as_read("Dune") is True
        assert first_book.read is True
        assert second_book.read is False


class TestRemoveBook:
    """Tests for remove_book."""

    def test_removes_book_that_exists_and_persists(self, empty_collection: BookCollection) -> None:
        empty_collection.add_book("Dune", "Frank Herbert", 1965)

        result = empty_collection.remove_book("Dune")
        reloaded_collection = BookCollection()

        assert result.success is True
        assert result.message == 'Removed "Dune" from the collection.'
        assert reloaded_collection.books == []

    def test_matches_title_case_insensitively(self, empty_collection: BookCollection) -> None:
        empty_collection.add_book("Dune", "Frank Herbert", 1965)

        result = empty_collection.remove_book("dUnE")
        reloaded_collection = BookCollection()

        assert result.success is True
        assert result.message == 'Removed "Dune" from the collection.'
        assert reloaded_collection.books == []

    def test_returns_feedback_when_book_does_not_exist(
        self,
        empty_collection: BookCollection,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        save_books_called = False

        def fake_save_books() -> None:
            nonlocal save_books_called
            save_books_called = True

        monkeypatch.setattr(empty_collection, "save_books", fake_save_books)

        result = empty_collection.remove_book("Missing Book")

        assert result.success is False
        assert result.message == 'Book "Missing Book" was not found in the collection.'
        assert save_books_called is False

    def test_rejects_empty_title(self, empty_collection: BookCollection) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty."):
            empty_collection.remove_book("   ")

    def test_returns_feedback_when_collection_is_empty(self, empty_collection: BookCollection) -> None:
        result = empty_collection.remove_book("Dune")

        assert result.success is False
        assert result.message == 'Book "Dune" was not found in the collection.'

    def test_only_removes_first_matching_title(self, empty_collection: BookCollection) -> None:
        first_book = empty_collection.add_book("Dune", "Frank Herbert", 1965)
        second_book = empty_collection.add_book("Dune", "Brian Herbert", 2001)

        result = empty_collection.remove_book("Dune")

        assert result.success is True
        assert empty_collection.books == [second_book]
        assert first_book not in empty_collection.books

    def test_does_not_remove_book_by_partial_title_match(self, empty_collection: BookCollection) -> None:
        empty_collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

        result = empty_collection.remove_book("Hob")

        assert result.success is False
        assert result.message == (
            'No exact match found for "Hob". Try one of these full titles: "The Hobbit".'
        )
        assert [book.title for book in empty_collection.books] == ["The Hobbit"]

    def test_ignores_whitespace_around_title(self, empty_collection: BookCollection) -> None:
        empty_collection.add_book("Dune", "Frank Herbert", 1965)

        result = empty_collection.remove_book("  dune  ")

        assert result.success is True
        assert empty_collection.books == []


class TestFindByAuthor:
    """Tests for find_by_author."""

    def test_matches_author_case_insensitively(self, collection_with_books: BookCollection) -> None:
        result = collection_with_books.find_by_author("frank herbert")

        assert result == [Book(title="Dune", author="Frank Herbert", year=1965, read=False)]

    def test_returns_all_matching_books(self, empty_collection: BookCollection) -> None:
        empty_collection.add_book("Dune", "Frank Herbert", 1965)
        empty_collection.add_book("Children of Dune", "Frank Herbert", 1976)

        assert [book.title for book in empty_collection.find_by_author("Frank Herbert")] == [
            "Dune",
            "Children of Dune",
        ]

    @pytest.mark.parametrize(
        ("stored_author", "searched_author"),
        [
            ("Jean-Paul Sartre", "jean-paul sartre"),
            ("Mary Wollstonecraft Shelley", "mary wollstonecraft shelley"),
            ("Gabriel Garcia Marquez", ""),
            ("Gabriel Garcia Marquez", "   "),
            ("Gabriel Garcia Marquez", "gabriel garcia marquez"),
            ("Gabriel García Márquez", "gabriel garcía márquez"),
        ],
    )
    def test_handles_author_name_edge_cases(
        self,
        empty_collection: BookCollection,
        stored_author: str,
        searched_author: str,
    ) -> None:
        empty_collection.add_book("Sample Book", stored_author, 1965)

        result = empty_collection.find_by_author(searched_author)

        expected = [] if searched_author.strip() == "" else [empty_collection.books[0]]
        assert result == expected

    def test_returns_empty_list_when_author_has_no_matches(
        self,
        collection_with_books: BookCollection,
    ) -> None:
        assert collection_with_books.find_by_author("Isaac Asimov") == []

    @pytest.mark.parametrize("author", ["Frank Herbert", "", "   "])
    def test_returns_empty_list_for_empty_collection(
        self,
        empty_collection: BookCollection,
        author: str,
    ) -> None:
        assert empty_collection.find_by_author(author) == []


class TestConcurrentAccess:
    """Tests for concurrent access patterns."""

    def test_separate_collections_can_overwrite_each_others_changes(
        self,
        temp_data_file: Path,
    ) -> None:
        first_collection = BookCollection()
        second_collection = BookCollection()
        barrier = threading.Barrier(2)

        def add_book_after_sync(
            collection: BookCollection,
            title: str,
            author: str,
            year: int,
        ) -> None:
            barrier.wait()
            collection.add_book(title, author, year)

        first_thread = threading.Thread(
            target=add_book_after_sync,
            args=(first_collection, "Dune", "Frank Herbert", 1965),
        )
        second_thread = threading.Thread(
            target=add_book_after_sync,
            args=(second_collection, "Neuromancer", "William Gibson", 1984),
        )

        first_thread.start()
        second_thread.start()
        first_thread.join()
        second_thread.join()

        saved_books = json.loads(temp_data_file.read_text())
        assert len(saved_books) == 1
        assert saved_books[0]["title"] in {"Dune", "Neuromancer"}
