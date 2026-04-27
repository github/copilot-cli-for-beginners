import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import Book, BookCollection, BookDataError


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book() -> None:
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid() -> None:
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book() -> None:
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid() -> None:
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_add_book_rejects_empty_title() -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match="Title cannot be empty."):
        collection.add_book("", "Frank Herbert", 1965)


def test_add_book_rejects_empty_author() -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match="Author cannot be empty."):
        collection.add_book("Dune", "   ", 1965)


def test_add_book_rejects_negative_year() -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match="Year cannot be negative."):
        collection.add_book("Dune", "Frank Herbert", -1)


@pytest.mark.parametrize("year", [True, "1965", 1965.5])
def test_add_book_rejects_non_integer_year(year: object) -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match="Year must be an integer."):
        collection.add_book("Dune", "Frank Herbert", year)  # type: ignore[arg-type]


def test_add_book_rejects_duplicate_title_case_insensitively() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    with pytest.raises(ValueError, match="A book with this title already exists."):
        collection.add_book("  dune  ", "Someone Else", 2024)

    assert [book.title for book in collection.list_books()] == ["Dune"]


def test_add_book_rejects_duplicate_title_and_author() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    with pytest.raises(ValueError, match="A book with this title already exists."):
        collection.add_book("Dune", "Frank Herbert", 1965)

    assert [book.title for book in collection.list_books()] == ["Dune"]


def test_add_book_strips_title_and_author() -> None:
    collection = BookCollection()

    book = collection.add_book("  Dune  ", "  Frank Herbert  ", 1965)

    assert book.title == "Dune"
    assert book.author == "Frank Herbert"


def test_add_book_rolls_back_when_save_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    collection = BookCollection()

    def fail_save(_books: object = None) -> None:
        raise BookDataError("Disk full.")

    monkeypatch.setattr(collection, "save_books", fail_save)

    with pytest.raises(BookDataError, match="Disk full."):
        collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.list_books() == []


def test_save_books_rejects_empty_title() -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match="Title cannot be empty."):
        collection.save_books([Book(title="   ", author="Frank Herbert", year=1965)])

    assert collection.list_books() == []


def test_save_books_validation_does_not_overwrite_existing_file() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    data_file = Path(books.DATA_FILE)

    original_file_contents = data_file.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="Title cannot be empty."):
        collection.save_books([Book(title="", author="Someone", year=2024)])

    assert data_file.read_text(encoding="utf-8") == original_file_contents
    assert [book.title for book in collection.list_books()] == ["Dune"]


def test_mark_as_read_rolls_back_when_save_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    def fail_save(_books: object = None) -> None:
        raise BookDataError("Disk full.")

    monkeypatch.setattr(collection, "save_books", fail_save)

    with pytest.raises(BookDataError, match="Disk full."):
        collection.mark_as_read("Dune")

    book = collection.find_book_by_title("Dune")
    assert book is not None
    assert book.read is False


def test_remove_book_rolls_back_when_save_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    def fail_save(_books: object = None) -> None:
        raise BookDataError("Disk full.")

    monkeypatch.setattr(collection, "save_books", fail_save)

    with pytest.raises(BookDataError, match="Disk full."):
        collection.remove_book("Dune")

    assert collection.find_book_by_title("Dune") is not None


def test_list_by_year_returns_books_inclusive() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)
    collection.add_book("The Martian", "Andy Weir", 2011)

    books_in_range = collection.list_by_year(1965, 1984)

    assert [book.title for book in books_in_range] == ["Dune", "Neuromancer"]


def test_get_unread_books_returns_empty_list_when_collection_is_empty() -> None:
    collection = BookCollection()

    assert collection.get_unread_books() == []


def test_get_unread_books_returns_only_unread_books_in_order() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)
    collection.add_book("The Martian", "Andy Weir", 2011)
    collection.mark_as_read("Neuromancer")

    unread_books = collection.get_unread_books()

    assert [book.title for book in unread_books] == ["Dune", "The Martian"]


def test_get_unread_books_returns_empty_list_when_all_books_are_read() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Neuromancer", "William Gibson", 1984)
    collection.mark_as_read("Dune")
    collection.mark_as_read("Neuromancer")

    assert collection.get_unread_books() == []


def test_get_unread_books_returns_copy() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    unread_books = collection.get_unread_books()
    unread_books.clear()

    assert len(collection.get_unread_books()) == 1


def test_list_by_year_rejects_reversed_range() -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match="Start year cannot be greater than end year."):
        collection.list_by_year(2000, 1990)


def test_load_books_raises_for_invalid_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(BookDataError, match="not valid JSON"):
        BookCollection()


def test_load_books_returns_empty_collection_when_file_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "missing.json"))

    collection = BookCollection()

    assert collection.list_books() == []


def test_load_books_raises_when_root_is_not_a_list(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text('{"title": "Dune"}', encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(BookDataError, match="expected a list of books"):
        BookCollection()


def test_load_books_raises_for_invalid_book_shape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text('[{"title": "", "author": "Frank Herbert", "year": 1965}]', encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(BookDataError, match="title must be a non-empty string"):
        BookCollection()


def test_load_books_raises_for_unexpected_field(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": false, "genre": "Sci-Fi"}]',
        encoding="utf-8",
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(BookDataError, match="unexpected genre"):
        BookCollection()


def test_load_books_raises_for_invalid_read_flag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": "yes"}]',
        encoding="utf-8",
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(BookDataError, match="read must be true or false"):
        BookCollection()


def test_load_books_raises_for_duplicate_titles(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        '[{"title": "Dune", "author": "Frank Herbert", "year": 1965}, {"title": "dune", "author": "Brian Herbert", "year": 1999}]',
        encoding="utf-8",
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(BookDataError, match="duplicate title 'dune'"):
        BookCollection()


def test_list_books_returns_copy() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    listed_books = collection.list_books()
    listed_books.clear()

    assert len(collection.list_books()) == 1


def test_find_book_by_title_strips_input() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    book = collection.find_book_by_title("  dune  ")

    assert book is not None
    assert book.title == "Dune"


def test_find_by_author_strips_input() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    books_by_author = collection.find_by_author("  frank herbert  ")

    assert [book.title for book in books_by_author] == ["Dune"]


class TestFindBookIndexByTitle:
    """Tests for BookCollection._find_book_index_by_title."""

    def test_returns_matching_index_for_trimmed_case_insensitive_title(self) -> None:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Neuromancer", "William Gibson", 1984)

        assert collection._find_book_index_by_title("  neuromancer  ") == 1

    def test_returns_none_when_title_is_not_present(self) -> None:
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)

        assert collection._find_book_index_by_title("The Hobbit") is None


class TestTitleValidation:
    """Tests for title validation shared by title-based methods."""

    @pytest.mark.parametrize(
        ("method_name", "raw_title", "message"),
        [
            ("_find_book_index_by_title", "   ", "Title cannot be empty."),
            ("find_book_by_title", "   ", "Title cannot be empty."),
            ("mark_as_read", "   ", "Title cannot be empty."),
            ("remove_book", "   ", "Title cannot be empty."),
            ("_find_book_index_by_title", None, "Title must be a string."),
            ("find_book_by_title", None, "Title must be a string."),
            ("mark_as_read", None, "Title must be a string."),
            ("remove_book", None, "Title must be a string."),
        ],
    )
    def test_rejects_invalid_title_input(
        self, method_name: str, raw_title: object, message: str
    ) -> None:
        collection = BookCollection()
        method = getattr(collection, method_name)

        with pytest.raises(ValueError, match=message):
            method(raw_title)  # type: ignore[misc]


@pytest.mark.parametrize(
    ("start", "end", "message"),
    [
        (True, 2000, "Start year must be an integer."),
        (1990, False, "End year must be an integer."),
        ("1990", 2000, "Start year must be an integer."),
        (1990, 2000.5, "End year must be an integer."),
    ],
)
def test_list_by_year_rejects_non_integer_bounds(start: object, end: object, message: str) -> None:
    collection = BookCollection()

    with pytest.raises(ValueError, match=message):
        collection.list_by_year(start, end)  # type: ignore[arg-type]


def test_list_by_year_returns_empty_list_when_no_books_match() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.list_by_year(2000, 2010) == []


class TestNormalizeText:
    """Tests for BookCollection._normalize_text."""

    def test_returns_trimmed_text(self) -> None:
        assert BookCollection._normalize_text("  Dune  ", "Title") == "Dune"

    @pytest.mark.parametrize(
        ("value", "field_name", "message"),
        [
            (None, "Title", "Title must be a string."),
            (123, "Author", "Author must be a string."),
            ("   ", "Title", "Title cannot be empty."),
        ],
    )
    def test_rejects_invalid_values(self, value: object, field_name: str, message: str) -> None:
        with pytest.raises(ValueError, match=message):
            BookCollection._normalize_text(value, field_name)  # type: ignore[arg-type]


class TestBookFromDict:
    """Tests for BookCollection._book_from_dict."""

    def test_creates_book_and_trims_text_fields(self) -> None:
        book = BookCollection._book_from_dict(
            {"title": "  Dune  ", "author": "  Frank Herbert  ", "year": 1965, "read": True}
        )

        assert book == Book(title="Dune", author="Frank Herbert", year=1965, read=True)

    def test_defaults_read_to_false_when_field_is_missing(self) -> None:
        book = BookCollection._book_from_dict({"title": "Dune", "author": "Frank Herbert", "year": 1965})

        assert book.read is False

    @pytest.mark.parametrize(
        ("raw_book", "message"),
        [
            ("not a dict", "each item must be an object"),
            ({"title": "Dune", "year": 1965}, "missing author"),
            (
                {"title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "Sci-Fi"},
                "unexpected genre",
            ),
            (
                {"title": "Dune", "author": "Frank Herbert", "year": True},
                "year must be an integer",
            ),
            (
                {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": "yes"},
                "read must be true or false",
            ),
        ],
    )
    def test_rejects_invalid_raw_book(self, raw_book: object, message: str) -> None:
        with pytest.raises(BookDataError, match=message):
            BookCollection._book_from_dict(raw_book)


class TestFindDuplicateTitle:
    """Tests for BookCollection._find_duplicate_title."""

    def test_returns_none_when_titles_are_unique(self) -> None:
        books_to_check = [
            Book(title="Dune", author="Frank Herbert", year=1965),
            Book(title="Neuromancer", author="William Gibson", year=1984),
        ]

        assert BookCollection._find_duplicate_title(books_to_check) is None

    def test_returns_later_duplicate_title_using_case_insensitive_match(self) -> None:
        books_to_check = [
            Book(title="Dune", author="Frank Herbert", year=1965),
            Book(title="  dune sequel  ", author="Brian Herbert", year=1999),
            Book(title="DUNE", author="Another Author", year=2001),
        ]

        assert BookCollection._find_duplicate_title(books_to_check) == "DUNE"


def test_load_books_trims_loaded_values_and_preserves_read_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        '[{"title": "  Dune  ", "author": "  Frank Herbert  ", "year": 1965, "read": true}]',
        encoding="utf-8",
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()

    assert collection.list_books() == [Book(title="Dune", author="Frank Herbert", year=1965, read=True)]


def test_load_books_raises_for_os_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_open(*args: object, **kwargs: object) -> None:
        raise OSError(13, "Permission denied")

    monkeypatch.setattr("builtins.open", fail_open)

    with pytest.raises(BookDataError, match="Permission denied"):
        BookCollection()


def test_save_books_with_explicit_list_writes_file_without_replacing_collection() -> None:
    collection = BookCollection()
    books_to_save = [Book(title="Dune", author="Frank Herbert", year=1965, read=True)]

    collection.save_books(books_to_save)

    assert collection.list_books() == []
    reloaded_collection = BookCollection()
    assert reloaded_collection.list_books() == books_to_save


def test_save_books_raises_for_os_error(monkeypatch: pytest.MonkeyPatch) -> None:
    collection = BookCollection()

    def fail_open(*args: object, **kwargs: object) -> None:
        raise OSError(28, "No space left on device")

    monkeypatch.setattr("builtins.open", fail_open)

    with pytest.raises(BookDataError, match="No space left on device"):
        collection.save_books([])


def test_mark_as_read_is_case_insensitive_and_skips_save_for_books_already_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.mark_as_read("Dune") is True

    def fail_save(_books: object = None) -> None:
        raise AssertionError("save_books should not be called for an already-read book")

    monkeypatch.setattr(collection, "save_books", fail_save)

    assert collection.mark_as_read("  dune  ") is True


def test_remove_book_is_case_insensitive_and_trims_input() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    removed = collection.remove_book("  dune  ")

    assert removed is True
    assert collection.list_books() == []


def test_remove_book_does_not_match_partial_titles() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)

    removed = collection.remove_book("Dun")

    assert removed is False
    assert [book.title for book in collection.list_books()] == ["Dune", "Dune Messiah"]


def test_find_by_author_returns_all_case_insensitive_matches_in_order() -> None:
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Children of Dune", "FRANK HERBERT", 1976)
    collection.add_book("Neuromancer", "William Gibson", 1984)

    books_by_author = collection.find_by_author(" frank herbert ")

    assert [book.title for book in books_by_author] == ["Dune", "Children of Dune"]


class TestFindByAuthorEdgeCases:
    """Tests for find_by_author edge cases."""

    @pytest.mark.parametrize(
        ("author_name", "query"),
        [
            ("Jean-Paul Sartre", "jean-paul sartre"),
            ("Mary Anne Evans", "MARY ANNE EVANS"),
            ("Gabriel Garcia Marquez", " gabriel garcia marquez "),
        ],
    )
    def test_matches_complex_author_names(self, author_name: str, query: str) -> None:
        collection = BookCollection()
        collection.add_book("Matching Book", author_name, 1950)
        collection.add_book("Other Book", "Someone Else", 2000)

        books_by_author = collection.find_by_author(query)

        assert [book.title for book in books_by_author] == ["Matching Book"]

    def test_matches_author_name_with_accented_characters(self) -> None:
        collection = BookCollection()
        collection.add_book("Shadow Book", "JOSÉ ÁLVAREZ", 1996)
        collection.add_book("Control Book", "Jose Alvarez", 1995)

        books_by_author = collection.find_by_author("josé álvarez")

        assert [book.title for book in books_by_author] == ["Shadow Book"]

    def test_rejects_empty_author_name(self) -> None:
        collection = BookCollection()

        with pytest.raises(ValueError, match="Author cannot be empty."):
            collection.find_by_author("")


class TestEmptyDataBehavior:
    """Tests for book operations when the collection is empty."""

    def test_list_books_returns_empty_list(self) -> None:
        collection = BookCollection()

        assert collection.list_books() == []

    def test_find_book_by_title_returns_none(self) -> None:
        collection = BookCollection()

        assert collection.find_book_by_title("Dune") is None

    def test_find_by_author_returns_empty_list(self) -> None:
        collection = BookCollection()

        assert collection.find_by_author("Frank Herbert") == []

    def test_mark_as_read_returns_false(self) -> None:
        collection = BookCollection()

        assert collection.mark_as_read("Dune") is False

    def test_remove_book_returns_false(self) -> None:
        collection = BookCollection()

        assert collection.remove_book("Dune") is False


def test_book_collection_lifecycle_supports_add_find_read_and_remove() -> None:
    collection = BookCollection()

    added_book = collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    found_by_title = collection.find_book_by_title("the hobbit")
    found_by_author = collection.find_by_author("j.r.r. tolkien")
    marked_as_read = collection.mark_as_read("The Hobbit")
    removed = collection.remove_book("The Hobbit")

    assert added_book == Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, read=False)
    assert found_by_title == added_book
    assert found_by_author == [added_book]
    assert marked_as_read is True
    assert removed is True
    assert collection.list_books() == []


def test_multiple_collection_instances_can_observe_saved_changes() -> None:
    writer = BookCollection()
    reader = BookCollection()

    writer.add_book("Dune", "Frank Herbert", 1965)
    reader.load_books()

    assert reader.find_book_by_title("Dune") == Book(title="Dune", author="Frank Herbert", year=1965, read=False)
