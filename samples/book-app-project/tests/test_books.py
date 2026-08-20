import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import threading
import pytest
from unittest.mock import patch, mock_open
import books
from books import Book, BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temp path for every test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


@pytest.fixture
def collection():
    return BookCollection()


@pytest.fixture
def populated_collection():
    col = BookCollection()
    col.add_book("1984", "George Orwell", 1949)
    col.add_book("Animal Farm", "George Orwell", 1945)
    col.add_book("Dune", "Frank Herbert", 1965)
    return col


# ---------------------------------------------------------------------------
# Book dataclass
# ---------------------------------------------------------------------------

class TestBook:
    def test_defaults_read_false(self):
        book = Book(title="Test", author="Author", year=2000)
        assert book.read is False

    def test_explicit_read_true(self):
        book = Book(title="Test", author="Author", year=2000, read=True)
        assert book.read is True


# ---------------------------------------------------------------------------
# load_books
# ---------------------------------------------------------------------------

class TestLoadBooks:
    def test_loads_empty_file(self, collection):
        assert collection.books == []

    def test_loads_existing_books(self, tmp_path, monkeypatch):
        data = [{"title": "1984", "author": "George Orwell", "year": 1949, "read": False}]
        temp_file = tmp_path / "data.json"
        temp_file.write_text(json.dumps(data))
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        col = BookCollection()
        assert len(col.books) == 1
        assert col.books[0].title == "1984"

    def test_missing_file_starts_empty(self, monkeypatch, tmp_path):
        monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "nonexistent.json"))
        col = BookCollection()
        assert col.books == []

    def test_corrupted_json_starts_empty(self, tmp_path, monkeypatch, capsys):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("this is not json {{{")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        col = BookCollection()
        assert col.books == []
        captured = capsys.readouterr()
        assert "corrupted" in captured.out.lower() or "warning" in captured.out.lower()


# ---------------------------------------------------------------------------
# save_books
# ---------------------------------------------------------------------------

class TestSaveBooks:
    def test_save_persists_to_disk(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        col = BookCollection()
        col.add_book("Dune", "Frank Herbert", 1965)

        saved = json.loads(temp_file.read_text())
        assert len(saved) == 1
        assert saved[0]["title"] == "Dune"

    def test_save_and_reload_roundtrip(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        col1 = BookCollection()
        col1.add_book("Dune", "Frank Herbert", 1965)
        col1.mark_as_read("Dune")

        col2 = BookCollection()
        assert len(col2.books) == 1
        assert col2.books[0].read is True


# ---------------------------------------------------------------------------
# add_book
# ---------------------------------------------------------------------------

class TestAddBook:
    def test_add_book(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        assert len(collection.books) == 1

    def test_add_book_returns_book(self, collection):
        result = collection.add_book("1984", "George Orwell", 1949)
        assert isinstance(result, Book)
        assert result.title == "1984"
        assert result.author == "George Orwell"
        assert result.year == 1949

    def test_add_book_read_defaults_false(self, collection):
        book = collection.add_book("1984", "George Orwell", 1949)
        assert book.read is False

    def test_add_multiple_books(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert len(collection.books) == 2

    def test_add_duplicate_title(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "George Orwell", 1949)
        assert len(collection.books) == 2

    @pytest.mark.parametrize("title,author,year", [
        ("1984", "George Orwell", 1949),
        ("Dune", "Frank Herbert", 1965),
        ("The Hobbit", "J.R.R. Tolkien", 1937),
    ])
    def test_add_various_books(self, collection, title, author, year):
        book = collection.add_book(title, author, year)
        assert book.title == title
        assert book.author == author
        assert book.year == year


# ---------------------------------------------------------------------------
# list_books
# ---------------------------------------------------------------------------

class TestListBooks:
    def test_list_empty(self, collection):
        assert collection.list_books() == []

    def test_list_returns_all(self, populated_collection):
        result = populated_collection.list_books()
        assert len(result) == 3

    def test_list_returns_book_objects(self, populated_collection):
        result = populated_collection.list_books()
        assert all(isinstance(b, Book) for b in result)

    def test_list_is_same_reference(self, populated_collection):
        assert populated_collection.list_books() is populated_collection.books


# ---------------------------------------------------------------------------
# find_book_by_title
# ---------------------------------------------------------------------------

class TestFindBookByTitle:
    def test_find_existing_book(self, populated_collection):
        book = populated_collection.find_book_by_title("1984")
        assert book is not None
        assert book.title == "1984"

    def test_find_nonexistent_returns_none(self, populated_collection):
        assert populated_collection.find_book_by_title("Unknown Book") is None

    def test_find_case_insensitive(self, populated_collection):
        assert populated_collection.find_book_by_title("dune") is not None
        assert populated_collection.find_book_by_title("DUNE") is not None
        assert populated_collection.find_book_by_title("DuNe") is not None

    def test_find_empty_collection(self, collection):
        assert collection.find_book_by_title("1984") is None

    @pytest.mark.parametrize("title", ["1984", "Dune", "Animal Farm"])
    def test_find_each_added_book(self, populated_collection, title):
        assert populated_collection.find_book_by_title(title) is not None


# ---------------------------------------------------------------------------
# mark_as_read
# ---------------------------------------------------------------------------

class TestMarkAsRead:
    def test_mark_existing_book(self, populated_collection):
        result = populated_collection.mark_as_read("Dune")
        assert result is True
        assert populated_collection.find_book_by_title("Dune").read is True

    def test_mark_nonexistent_returns_false(self, collection):
        assert collection.mark_as_read("Nonexistent Book") is False

    def test_mark_case_insensitive(self, populated_collection):
        result = populated_collection.mark_as_read("dune")
        assert result is True

    def test_mark_already_read(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        result = populated_collection.mark_as_read("Dune")
        assert result is True
        assert populated_collection.find_book_by_title("Dune").read is True

    def test_mark_does_not_affect_other_books(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        assert populated_collection.find_book_by_title("1984").read is False


# ---------------------------------------------------------------------------
# remove_book
# ---------------------------------------------------------------------------

class TestRemoveBook:
    def test_remove_existing_book(self, populated_collection):
        result = populated_collection.remove_book("Dune")
        assert result is True
        assert populated_collection.find_book_by_title("Dune") is None

    def test_remove_nonexistent_returns_false(self, collection):
        assert collection.remove_book("Ghost Book") is False

    def test_remove_decrements_count(self, populated_collection):
        before = len(populated_collection.books)
        populated_collection.remove_book("Dune")
        assert len(populated_collection.books) == before - 1

    def test_remove_case_insensitive(self, populated_collection):
        result = populated_collection.remove_book("DUNE")
        assert result is True

    def test_remove_does_not_affect_other_books(self, populated_collection):
        populated_collection.remove_book("Dune")
        assert populated_collection.find_book_by_title("1984") is not None

    def test_remove_from_empty_collection(self, collection):
        assert collection.remove_book("1984") is False


# ---------------------------------------------------------------------------
# find_by_author
# ---------------------------------------------------------------------------

class TestFindByAuthor:
    def test_find_author_with_multiple_books(self, populated_collection):
        result = populated_collection.find_by_author("George Orwell")
        assert len(result) == 2
        assert all(b.author == "George Orwell" for b in result)

    def test_find_author_with_one_book(self, populated_collection):
        result = populated_collection.find_by_author("Frank Herbert")
        assert len(result) == 1
        assert result[0].title == "Dune"

    def test_find_unknown_author_returns_empty(self, populated_collection):
        assert populated_collection.find_by_author("Unknown Author") == []

    def test_find_author_case_insensitive(self, populated_collection):
        assert len(populated_collection.find_by_author("george orwell")) == 2
        assert len(populated_collection.find_by_author("GEORGE ORWELL")) == 2

    def test_find_author_empty_collection(self, collection):
        assert collection.find_by_author("George Orwell") == []

    def test_find_author_returns_book_objects(self, populated_collection):
        result = populated_collection.find_by_author("George Orwell")
        assert all(isinstance(b, Book) for b in result)

    @pytest.mark.parametrize(
        "author,title",
        [
            ("Jean-Paul Sartre", "Nausea"),
            ("Joanne Kathleen Rowling", "Harry Potter and the Philosopher's Stone"),
            ("Gabriel García Márquez", "One Hundred Years of Solitude"),
        ],
    )
    def test_find_author_with_special_name_patterns(self, collection, author, title):
        collection.add_book(title, author, 1967)
        result = collection.find_by_author(author)
        assert len(result) == 1
        assert result[0].title == title
        assert result[0].author == author

    @pytest.mark.parametrize(
        "author,title,query",
        [
            ("Jean-Paul Sartre", "Nausea", "jean-paul sartre"),
            ("Joanne Kathleen Rowling", "Harry Potter and the Philosopher's Stone", "JOANNE KATHLEEN ROWLING"),
            ("Gabriel García Márquez", "One Hundred Years of Solitude", "gabriel garcía márquez"),
        ],
    )
    def test_find_author_special_name_patterns_case_insensitive(self, collection, author, title, query):
        collection.add_book(title, author, 1967)
        result = collection.find_by_author(query)
        assert len(result) == 1
        assert result[0].author == author

    def test_find_author_empty_string_matches_books_with_empty_author(self, collection):
        collection.add_book("Untitled Notes", "", 2020)
        collection.add_book("Dune", "Frank Herbert", 1965)
        result = collection.find_by_author("")
        assert len(result) == 1
        assert result[0].title == "Untitled Notes"
        assert result[0].author == ""

    def test_find_author_empty_string_returns_empty_when_no_empty_author(self, populated_collection):
        assert populated_collection.find_by_author("") == []


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_add_find_read_remove_workflow(self, collection):
        collection.add_book("Neuromancer", "William Gibson", 1984)
        book = collection.find_book_by_title("Neuromancer")
        assert book is not None and book.read is False

        collection.mark_as_read("Neuromancer")
        assert collection.find_book_by_title("Neuromancer").read is True

        collection.remove_book("Neuromancer")
        assert collection.find_book_by_title("Neuromancer") is None
        assert collection.list_books() == []

    def test_find_by_author_after_remove(self, populated_collection):
        populated_collection.remove_book("Animal Farm")
        result = populated_collection.find_by_author("George Orwell")
        assert len(result) == 1
        assert result[0].title == "1984"

    def test_persistence_across_instances(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        col1 = BookCollection()
        col1.add_book("Foundation", "Isaac Asimov", 1951)
        col1.mark_as_read("Foundation")

        col2 = BookCollection()
        book = col2.find_book_by_title("Foundation")
        assert book is not None
        assert book.read is True


# ---------------------------------------------------------------------------
# Duplicate books
# ---------------------------------------------------------------------------

class TestDuplicateBooks:
    def test_add_exact_duplicate_allows_both(self, collection):
        """BookCollection does not enforce uniqueness — both entries are stored."""
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "George Orwell", 1949)
        assert len(collection.books) == 2

    def test_add_same_title_different_author(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "Another Author", 2020)
        assert len(collection.books) == 2

    def test_add_same_title_different_year(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "George Orwell", 2003)
        assert len(collection.books) == 2

    def test_find_by_title_returns_first_duplicate(self, collection):
        """find_book_by_title returns the first match when duplicates exist."""
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "George Orwell", 2003)
        found = collection.find_book_by_title("1984")
        assert found.year == 1949

    def test_remove_duplicate_removes_only_first(self, collection):
        """remove_book removes the first match, leaving the second duplicate."""
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "George Orwell", 2003)
        collection.remove_book("1984")
        assert len(collection.books) == 1
        assert collection.books[0].year == 2003

    def test_mark_as_read_marks_first_duplicate(self, collection):
        """mark_as_read only affects the first matching book."""
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("1984", "George Orwell", 2003)
        collection.mark_as_read("1984")
        assert collection.books[0].read is True
        assert collection.books[1].read is False

    def test_duplicate_books_persist_to_disk(self, tmp_path, monkeypatch):
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        col = BookCollection()
        col.add_book("1984", "George Orwell", 1949)
        col.add_book("1984", "George Orwell", 1949)

        saved = json.loads(temp_file.read_text())
        assert len(saved) == 2


# ---------------------------------------------------------------------------
# Partial title match behaviour
# ---------------------------------------------------------------------------

class TestPartialTitleMatch:
    def test_find_by_partial_title_returns_none(self, populated_collection):
        """find_book_by_title requires an exact (case-insensitive) match."""
        assert populated_collection.find_book_by_title("19") is None
        assert populated_collection.find_book_by_title("Du") is None

    def test_remove_by_partial_title_returns_false(self, populated_collection):
        """remove_book does not remove on a partial match."""
        result = populated_collection.remove_book("19")
        assert result is False
        assert len(populated_collection.books) == 3

    def test_mark_as_read_partial_title_returns_false(self, populated_collection):
        result = populated_collection.mark_as_read("Du")
        assert result is False

    def test_substring_of_existing_title_not_found(self, populated_collection):
        assert populated_collection.find_book_by_title("Animal") is None

    def test_full_title_with_extra_space_not_found(self, populated_collection):
        """Trailing space after strip is removed; extra interior space is not."""
        assert populated_collection.find_book_by_title("1984 ") is None

    def test_exact_match_still_works_after_partial_miss(self, populated_collection):
        assert populated_collection.find_book_by_title("Dune") is not None


# ---------------------------------------------------------------------------
# Finding books when collection is empty
# ---------------------------------------------------------------------------

class TestEmptyCollectionLookups:
    def test_find_book_by_title_empty(self, collection):
        assert collection.find_book_by_title("Anything") is None

    def test_find_by_author_empty(self, collection):
        assert collection.find_by_author("George Orwell") == []

    def test_list_books_empty(self, collection):
        assert collection.list_books() == []

    def test_mark_as_read_empty(self, collection):
        assert collection.mark_as_read("Ghost") is False

    def test_remove_book_empty(self, collection):
        assert collection.remove_book("Ghost") is False

    def test_empty_after_removing_all(self, collection):
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.remove_book("Dune")
        assert collection.list_books() == []
        assert collection.find_book_by_title("Dune") is None
        assert collection.find_by_author("Frank Herbert") == []


# ---------------------------------------------------------------------------
# File permission errors during save
# ---------------------------------------------------------------------------

class TestFilePermissionErrors:
    def test_add_book_propagates_permission_error(self, collection):
        """save_books has no error handling — PermissionError bubbles up."""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                collection.add_book("Dune", "Frank Herbert", 1965)

    def test_mark_as_read_propagates_permission_error(self, collection):
        collection.books.append(Book("Dune", "Frank Herbert", 1965))
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                collection.mark_as_read("Dune")

    def test_remove_book_propagates_permission_error(self, collection):
        collection.books.append(Book("Dune", "Frank Herbert", 1965))
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                collection.remove_book("Dune")

    def test_in_memory_state_unchanged_after_permission_error(self, collection):
        """If save fails, the in-memory list still reflects the attempted mutation."""
        with pytest.raises(PermissionError):
            with patch("builtins.open", side_effect=PermissionError):
                collection.add_book("Dune", "Frank Herbert", 1965)
        # book was appended before save was attempted
        assert collection.find_book_by_title("Dune") is not None

    def test_load_books_readonly_file_raises(self, tmp_path, monkeypatch):
        """A truly unreadable file raises PermissionError on load."""
        temp_file = tmp_path / "data.json"
        temp_file.write_text("[]")
        monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

        with patch("builtins.open", side_effect=PermissionError("no read")):
            with pytest.raises(PermissionError):
                BookCollection()


# ---------------------------------------------------------------------------
# Concurrent access
# ---------------------------------------------------------------------------

class TestConcurrentAccess:
    def test_concurrent_adds_all_stored(self, collection):
        """All books added from multiple threads should appear in the collection."""
        errors = []

        def add(n):
            try:
                collection.add_book(f"Book {n}", f"Author {n}", 2000 + n)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=add, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Threads raised: {errors}"
        assert len(collection.books) == 10

    def test_concurrent_reads_are_safe(self, populated_collection):
        """Simultaneous reads should not raise and should return consistent results."""
        results = []
        errors = []

        def read():
            try:
                results.append(len(populated_collection.list_books()))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=read) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert all(r == 3 for r in results)

    def test_concurrent_mark_as_read(self, collection):
        """Marking the same book as read from multiple threads should not corrupt state."""
        collection.add_book("Dune", "Frank Herbert", 1965)
        errors = []

        def mark():
            try:
                collection.mark_as_read("Dune")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=mark) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert collection.find_book_by_title("Dune").read is True

    def test_concurrent_add_and_read(self, collection):
        """Mixed read/write threads should not raise exceptions."""
        errors = []

        def add(n):
            try:
                collection.add_book(f"Book {n}", "Author", 2000)
            except Exception as e:
                errors.append(e)

        def read():
            try:
                collection.list_books()
            except Exception as e:
                errors.append(e)

        threads = (
            [threading.Thread(target=add, args=(i,)) for i in range(5)]
            + [threading.Thread(target=read) for _ in range(5)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
