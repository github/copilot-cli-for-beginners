import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import builtins
import json

import pytest
import books
from books import Book, BookCollection, get_statistics
from exceptions import BookNotFoundError, StorageError, ValidationError


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_add_book_empty_title_raises():
    collection = BookCollection()
    with pytest.raises(ValidationError):
        collection.add_book("", "George Orwell", 1949)


def test_add_book_whitespace_title_raises():
    collection = BookCollection()
    with pytest.raises(ValidationError):
        collection.add_book("   ", "George Orwell", 1949)


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    with pytest.raises(BookNotFoundError):
        collection.mark_as_read("Nonexistent Book")

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.remove_book("The Hobbit")
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    with pytest.raises(BookNotFoundError):
        collection.remove_book("Nonexistent Book")

def test_get_statistics_empty_list():
    stats = get_statistics([])
    assert stats == {"total": 0, "read": 0, "unread": 0, "oldest": None, "newest": None}

def test_get_statistics_mixed_books():
    books_list = [
        Book(title="1984", author="George Orwell", year=1949, read=True),
        Book(title="Dune", author="Frank Herbert", year=1965, read=False),
        Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, read=True),
    ]
    stats = get_statistics(books_list)
    assert stats["total"] == 3
    assert stats["read"] == 2
    assert stats["unread"] == 1
    assert stats["oldest"].title == "The Hobbit"
    assert stats["newest"].title == "Dune"

def test_get_statistics_single_book():
    books_list = [Book(title="Dune", author="Frank Herbert", year=1965)]
    stats = get_statistics(books_list)
    assert stats["total"] == 1
    assert stats["oldest"] is stats["newest"]


def test_load_books_missing_file_starts_empty(tmp_path, monkeypatch):
    """load_books should tolerate a missing data file and start empty."""
    missing_file = tmp_path / "does_not_exist.json"
    monkeypatch.setattr(books, "DATA_FILE", str(missing_file))

    collection = BookCollection()

    assert collection.books == []


def test_load_books_reads_existing_data(tmp_path, monkeypatch):
    """load_books should parse existing valid JSON into Book objects."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        '[{"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": true}]'
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()

    assert len(collection.books) == 1
    book = collection.books[0]
    assert book.title == "Dune"
    assert book.author == "Frank Herbert"
    assert book.year == 1965
    assert book.read is True


def test_save_books_persists_to_disk(tmp_path, monkeypatch):
    """save_books should write the current collection as JSON to DATA_FILE."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    saved_data = json.loads(temp_file.read_text())
    assert saved_data == [
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": False}
    ]


def test_add_book_reflected_after_reload(tmp_path, monkeypatch):
    """Books added should be persisted and visible to a freshly loaded collection."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    reloaded = BookCollection()
    assert reloaded.find_book_by_title("Dune") is not None


def test_mark_as_read_persists_after_reload(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")

    reloaded = BookCollection()
    assert reloaded.find_book_by_title("Dune").read is True


def test_remove_book_persists_after_reload(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.remove_book("Dune")

    reloaded = BookCollection()
    assert reloaded.find_book_by_title("Dune") is None


def test_find_book_by_title_case_insensitive():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    assert collection.find_book_by_title("DUNE") is not None
    assert collection.find_book_by_title("dune") is not None


def test_find_book_by_title_not_found_returns_none():
    collection = BookCollection()
    assert collection.find_book_by_title("Nonexistent") is None


def test_list_books_returns_live_reference():
    """list_books currently returns the internal list, not a copy."""
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    result = collection.list_books()
    assert result is collection.books


@pytest.mark.parametrize(
    "author_query,expected_titles",
    [
        ("Frank Herbert", ["Dune"]),
        ("frank herbert", ["Dune"]),
        ("Nonexistent Author", []),
    ],
)
def test_find_by_author(author_query, expected_titles):
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    results = collection.find_by_author(author_query)
    assert [b.title for b in results] == expected_titles


@pytest.mark.parametrize(
    "start,end,expected_titles",
    [
        (1960, 1970, ["Dune"]),
        (1965, 1965, ["Dune"]),
        (1970, 1980, []),
        (1970, 1960, []),  # start > end yields no matches
    ],
)
def test_list_by_year(start, end, expected_titles):
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    results = collection.list_by_year(start, end)
    assert [b.title for b in results] == expected_titles


def test_get_statistics_tied_years_returns_first_match():
    """min()/max() return the first element on ties, current behavior."""
    books_list = [
        Book(title="Book A", author="Author A", year=2000),
        Book(title="Book B", author="Author B", year=2000),
    ]
    stats = get_statistics(books_list)
    assert stats["oldest"].title == "Book A"
    assert stats["newest"].title == "Book A"


def test_load_books_corrupted_json_raises_storage_error(tmp_path, monkeypatch):
    temp_file = tmp_path / "corrupted.json"
    temp_file.write_text("{not valid json")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    with pytest.raises(StorageError):
        BookCollection()


class TestAddBook:
    """Tests for BookCollection.add_book."""

    def test_add_multiple_books_increases_count(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

        assert len(collection.books) == 3
        assert [b.title for b in collection.books] == ["Dune", "1984", "The Hobbit"]

    def test_add_book_new_book_defaults_to_unread(self):
        collection = BookCollection()
        book = collection.add_book("Dune", "Frank Herbert", 1965)

        assert book.read is False

    def test_add_book_allows_duplicate_titles(self):
        """Current behavior: no uniqueness check on title."""
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune", "Frank Herbert", 1965)

        assert len(collection.books) == 2

    @pytest.mark.parametrize("year", [-500, 0, 9999])
    def test_add_book_does_not_validate_year_range(self, year):
        """Current behavior: any integer year is accepted, including
        negative years and far-future years."""
        collection = BookCollection()
        book = collection.add_book("Some Book", "Some Author", year)

        assert book.year == year

    def test_add_book_none_title_raises_validation_error(self):
        collection = BookCollection()
        with pytest.raises(ValidationError):
            collection.add_book(None, "George Orwell", 1949)


class TestRemoveBook:
    """Tests for BookCollection.remove_book."""

    def test_remove_book_case_insensitive(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)

        collection.remove_book("dune")

        assert collection.find_book_by_title("Dune") is None

    def test_remove_book_only_removes_matching_book(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)

        collection.remove_book("Dune")

        remaining_titles = [b.title for b in collection.books]
        assert remaining_titles == ["1984"]

    def test_remove_book_from_empty_collection_raises(self):
        collection = BookCollection()
        with pytest.raises(BookNotFoundError):
            collection.remove_book("Dune")

    def test_remove_book_twice_raises_second_time(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.remove_book("Dune")

        with pytest.raises(BookNotFoundError):
            collection.remove_book("Dune")


class TestFindBookByTitle:
    """Tests for BookCollection.find_book_by_title."""

    def test_find_book_by_title_empty_collection_returns_none(self):
        collection = BookCollection()
        assert collection.find_book_by_title("Dune") is None

    def test_find_book_by_title_returns_correct_book_among_many(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

        found = collection.find_book_by_title("1984")

        assert found is not None
        assert found.author == "George Orwell"


class TestFindByAuthor:
    """Tests for BookCollection.find_by_author."""

    def test_find_by_author_empty_collection_returns_empty_list(self):
        collection = BookCollection()
        assert collection.find_by_author("Frank Herbert") == []

    def test_find_by_author_multiple_matches(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)
        collection.add_book("1984", "George Orwell", 1949)

        results = collection.find_by_author("Frank Herbert")

        assert [b.title for b in results] == ["Dune", "Dune Messiah"]


class TestMarkAsRead:
    """Tests for BookCollection.mark_as_read."""

    def test_mark_as_read_empty_collection_raises(self):
        collection = BookCollection()
        with pytest.raises(BookNotFoundError):
            collection.mark_as_read("Dune")

    def test_mark_as_read_case_insensitive(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)

        collection.mark_as_read("DUNE")

        assert collection.find_book_by_title("Dune").read is True

    def test_mark_as_read_already_read_book_stays_read(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.mark_as_read("Dune")

        collection.mark_as_read("Dune")

        assert collection.find_book_by_title("Dune").read is True

    def test_mark_as_read_only_affects_matching_book(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)

        collection.mark_as_read("Dune")

        assert collection.find_book_by_title("Dune").read is True
        assert collection.find_book_by_title("1984").read is False


class TestEmptyDataEdgeCases:
    """Edge cases exercising an empty BookCollection."""

    def test_list_books_empty_collection_returns_empty_list(self):
        collection = BookCollection()
        assert collection.list_books() == []

    def test_list_by_year_empty_collection_returns_empty_list(self):
        collection = BookCollection()
        assert collection.list_by_year(1900, 2100) == []

    def test_get_statistics_empty_collection(self):
        collection = BookCollection()
        stats = get_statistics(collection.list_books())

        assert stats == {
            "total": 0,
            "read": 0,
            "unread": 0,
            "oldest": None,
            "newest": None,
        }


class TestDuplicateBooks:
    """Adding books with the same title and author."""

    def test_add_exact_duplicate_title_and_author_is_allowed(self):
        """Current behavior: add_book has no uniqueness check, so an
        identical (title, author) pair can be added more than once,
        resulting in two distinct Book entries."""
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune", "Frank Herbert", 1965)

        matching = [b for b in collection.books if b.title == "Dune"]
        assert len(matching) == 2
        assert matching[0] == matching[1]

    def test_duplicate_titles_different_years_both_persist(self):
        """Two editions of the same title/author with different years
        are both kept as separate entries."""
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune", "Frank Herbert", 1990)

        matching = [b for b in collection.books if b.title == "Dune"]
        assert [b.year for b in matching] == [1965, 1990]

    def test_find_book_by_title_returns_first_duplicate(self):
        """find_book_by_title returns only the first match when
        duplicates exist; there's no way to disambiguate by position."""
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune", "Frank Herbert", 1990)

        found = collection.find_book_by_title("Dune")

        assert found.year == 1965


class TestRemoveByPartialTitleMatch:
    """remove_book requires an exact (case-insensitive) title match;
    partial/substring matches are NOT supported by this implementation
    (unlike the intentionally buggy sample in book-app-buggy)."""

    def test_partial_title_match_raises_book_not_found(self):
        collection = BookCollection()
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)

        with pytest.raises(BookNotFoundError):
            collection.remove_book("Dune")

    def test_partial_title_does_not_remove_unrelated_book(self):
        collection = BookCollection()
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)

        with pytest.raises(BookNotFoundError):
            collection.remove_book("Messiah")

        # The book must remain untouched since no exact match was found.
        assert collection.find_book_by_title("Dune Messiah") is not None

    def test_exact_title_removes_correctly_even_with_similar_titles_present(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)

        collection.remove_book("Dune")

        remaining_titles = [b.title for b in collection.books]
        assert remaining_titles == ["Dune Messiah"]


class TestFindingInEmptyCollection:
    """Search/lookup operations against a freshly created, empty
    BookCollection. (Complements the broader TestEmptyDataEdgeCases.)"""

    def test_find_book_by_title_returns_none(self):
        collection = BookCollection()
        assert collection.find_book_by_title("Anything") is None

    def test_find_by_author_returns_empty_list(self):
        collection = BookCollection()
        assert collection.find_by_author("Anyone") == []

    def test_list_by_year_returns_empty_list(self):
        collection = BookCollection()
        assert collection.list_by_year(0, 9999) == []

    def test_remove_book_raises_not_found(self):
        collection = BookCollection()
        with pytest.raises(BookNotFoundError):
            collection.remove_book("Anything")

    def test_mark_as_read_raises_not_found(self):
        collection = BookCollection()
        with pytest.raises(BookNotFoundError):
            collection.mark_as_read("Anything")


class TestSavePermissionErrors:
    """File permission errors during save_books should surface as
    StorageError, not an unhandled OSError/PermissionError."""

    def test_save_books_permission_error_raises_storage_error(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        original_open = builtins.open

        def fake_open(file, mode="r", *args, **kwargs):
            if str(file) == str(temp_file) and "w" in mode:
                raise PermissionError("Permission denied")
            return original_open(file, mode, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", fake_open)

        collection = BookCollection()
        with pytest.raises(StorageError):
            collection.save_books()

    def test_add_book_permission_error_on_save_raises_storage_error(self, tmp_path, monkeypatch):
        """add_book calls save_books internally, so a permission error
        during that save should also propagate as StorageError."""
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        collection = BookCollection()

        original_open = builtins.open

        def fake_open(file, mode="r", *args, **kwargs):
            if str(file) == str(temp_file) and "w" in mode:
                raise PermissionError("Permission denied")
            return original_open(file, mode, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", fake_open)

        with pytest.raises(StorageError):
            collection.add_book("Dune", "Frank Herbert", 1965)

    def test_permission_error_does_not_corrupt_in_memory_state(self, tmp_path, monkeypatch):
        """Even though the write fails, the book was already appended to
        self.books in memory before save_books() was called (current
        behavior: no rollback on save failure)."""
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        collection = BookCollection()

        original_open = builtins.open

        def fake_open(file, mode="r", *args, **kwargs):
            if str(file) == str(temp_file) and "w" in mode:
                raise PermissionError("Permission denied")
            return original_open(file, mode, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", fake_open)

        with pytest.raises(StorageError):
            collection.add_book("Dune", "Frank Herbert", 1965)

        assert collection.find_book_by_title("Dune") is not None


class TestConcurrentAccess:
    """Simulated concurrent access to the same DATA_FILE.

    BookCollection has no file locking, so these tests characterize the
    resulting "last write wins" behavior when multiple in-memory
    instances point at the same underlying file, rather than testing
    true multithreading (which would be flaky for a JSON-file-backed
    sample app with no concurrency primitives)."""

    def test_last_writer_wins_when_two_collections_share_a_file(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        collection_a = BookCollection()
        collection_b = BookCollection()

        collection_a.add_book("Dune", "Frank Herbert", 1965)
        collection_b.add_book("1984", "George Orwell", 1949)

        reloaded = BookCollection()
        titles = [b.title for b in reloaded.books]

        # collection_b saved last, so its save overwrote collection_a's
        # change; collection_a's addition is lost from disk.
        assert titles == ["1984"]

    def test_second_instance_does_not_see_first_instances_unsaved_changes(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        collection_a = BookCollection()
        collection_a.add_book("Dune", "Frank Herbert", 1965)

        # collection_b was created before reading collection_a's save,
        # simulating two processes loading the file at the same moment.
        collection_b = BookCollection()

        assert collection_b.find_book_by_title("Dune") is not None  # loaded after a's save
        collection_b.add_book("1984", "George Orwell", 1949)

        reloaded = BookCollection()
        titles = sorted(b.title for b in reloaded.books)
        assert titles == ["1984", "Dune"]
