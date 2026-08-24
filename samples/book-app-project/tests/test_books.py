import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


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


class TestAddBook:
    """Tests for BookCollection.add_book."""

    def test_add_book_persists_to_disk(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        saved = json.loads(open(books.DATA_FILE).read())
        assert any(b["title"] == "Dune" for b in saved)

    def test_add_book_strips_whitespace(self):
        collection = BookCollection()
        collection.add_book("  Dune  ", "  Frank Herbert  ", 1965)
        book = collection.find_book_by_title("Dune")
        assert book is not None
        assert book.title == "Dune"
        assert book.author == "Frank Herbert"

    def test_add_book_duplicate_title_case_insensitive_raises(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        with pytest.raises(ValueError, match="already exists"):
            collection.add_book("dune", "Someone Else", 1970)

    @pytest.mark.parametrize("title,author", [
        ("", "Frank Herbert"),
        ("   ", "Frank Herbert"),
    ])
    def test_add_book_blank_title_raises(self, title, author):
        collection = BookCollection()
        with pytest.raises(ValueError, match="Title cannot be empty"):
            collection.add_book(title, author, 1965)

    @pytest.mark.parametrize("title,author", [
        ("Dune", ""),
        ("Dune", "   "),
    ])
    def test_add_book_blank_author_raises(self, title, author):
        collection = BookCollection()
        with pytest.raises(ValueError, match="Author cannot be empty"):
            collection.add_book(title, author, 1965)

    @pytest.mark.parametrize("year", [0, -1, -1965])
    def test_add_book_non_positive_year_raises(self, year):
        collection = BookCollection()
        with pytest.raises(ValueError, match="Year must be a positive integer"):
            collection.add_book("Dune", "Frank Herbert", year)

    def test_add_book_boolean_year_raises(self):
        collection = BookCollection()
        with pytest.raises(ValueError, match="Year must be a positive integer"):
            collection.add_book("Dune", "Frank Herbert", True)

    def test_add_book_to_empty_collection(self):
        collection = BookCollection()
        assert collection.books == []
        book = collection.add_book("Dune", "Frank Herbert", 1965)
        assert collection.books == [book]


class TestFindBookByTitle:
    """Tests for BookCollection.find_book_by_title."""

    def test_finds_exact_match(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        found = collection.find_book_by_title("Dune")
        assert found is not None
        assert found.author == "Frank Herbert"

    @pytest.mark.parametrize("query", ["dune", "DUNE", "DuNe"])
    def test_finds_match_case_insensitively(self, query):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        found = collection.find_book_by_title(query)
        assert found is not None
        assert found.title == "Dune"

    def test_returns_none_when_not_found(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert collection.find_book_by_title("Nonexistent") is None

    def test_returns_none_on_empty_collection(self):
        collection = BookCollection()
        assert collection.find_book_by_title("Anything") is None

    def test_does_not_partial_match(self):
        collection = BookCollection()
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)
        assert collection.find_book_by_title("Dune") is None


class TestFindByAuthor:
    """Tests for BookCollection.find_by_author."""

    def test_finds_single_book_by_author(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        results = collection.find_by_author("Frank Herbert")
        assert [b.title for b in results] == ["Dune"]

    def test_finds_multiple_books_by_same_author(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)
        collection.add_book("1984", "George Orwell", 1949)
        results = collection.find_by_author("Frank Herbert")
        assert {b.title for b in results} == {"Dune", "Dune Messiah"}

    @pytest.mark.parametrize("query", ["frank herbert", "FRANK HERBERT"])
    def test_matches_case_insensitively(self, query):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        results = collection.find_by_author(query)
        assert len(results) == 1

    def test_returns_empty_list_when_no_match(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert collection.find_by_author("Unknown Author") == []

    def test_returns_empty_list_on_empty_collection(self):
        collection = BookCollection()
        assert collection.find_by_author("Anyone") == []

    def test_does_not_partial_match_author(self):
        collection = BookCollection()
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        assert collection.find_by_author("Tolkien") == []


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False


class TestMarkAsRead:
    """Tests for BookCollection.mark_as_read."""

    def test_only_marks_the_matching_book(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("Dune")
        assert collection.find_book_by_title("Dune").read is True
        assert collection.find_book_by_title("1984").read is False

    @pytest.mark.parametrize("query", ["dune", "DUNE"])
    def test_matches_case_insensitively(self, query):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert collection.mark_as_read(query) is True
        assert collection.find_book_by_title("Dune").read is True

    def test_marking_already_read_book_stays_true(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.mark_as_read("Dune")
        result = collection.mark_as_read("Dune")
        assert result is True
        assert collection.find_book_by_title("Dune").read is True

    def test_returns_false_on_empty_collection(self):
        collection = BookCollection()
        assert collection.mark_as_read("Anything") is False


def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


class TestRemoveBook:
    """Tests for BookCollection.remove_book."""

    def test_removes_only_the_matching_book(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)
        collection.remove_book("Dune")
        remaining = [b.title for b in collection.books]
        assert remaining == ["Dune Messiah"]

    @pytest.mark.parametrize("query", ["dune", "DUNE"])
    def test_matches_case_insensitively(self, query):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert collection.remove_book(query) is True
        assert collection.books == []

    def test_does_not_partial_match(self):
        collection = BookCollection()
        collection.add_book("Dune Messiah", "Frank Herbert", 1969)
        result = collection.remove_book("Dune")
        assert result is False
        assert len(collection.books) == 1

    def test_returns_false_on_empty_collection(self):
        collection = BookCollection()
        assert collection.remove_book("Anything") is False

    def test_remove_persists_change_to_disk(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.remove_book("Dune")
        saved = json.loads(open(books.DATA_FILE).read())
        assert saved == []


class TestEmptyCollectionEdgeCases:
    """Edge cases exercising an empty (or freshly-emptied) collection."""

    def test_new_collection_starts_empty(self):
        collection = BookCollection()
        assert collection.books == []
        assert collection.list_books() == []

    def test_list_books_returns_new_empty_list_each_time(self):
        collection = BookCollection()
        result1 = collection.list_books()
        result2 = collection.list_books()
        assert result1 == result2 == []
        assert result1 is not result2

    def test_list_by_year_on_empty_collection(self):
        collection = BookCollection()
        assert collection.list_by_year(1900, 2100) == []

    def test_find_by_author_on_empty_collection(self):
        collection = BookCollection()
        assert collection.find_by_author("Anyone") == []

    def test_find_book_by_title_on_empty_collection(self):
        collection = BookCollection()
        assert collection.find_book_by_title("Anything") is None

    def test_remove_from_empty_collection(self):
        collection = BookCollection()
        assert collection.remove_book("Anything") is False

    def test_mark_as_read_on_empty_collection(self):
        collection = BookCollection()
        assert collection.mark_as_read("Anything") is False

    def test_collection_becomes_empty_after_removing_last_book(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.remove_book("Dune")
        assert collection.books == []
        assert collection.list_books() == []


def test_list_by_year_within_range():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.list_by_year(1940, 1970)
    titles = [b.title for b in results]
    assert titles == ["1984", "Dune"]

def test_list_by_year_excludes_out_of_range():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.list_by_year(1940, 1970)
    titles = [b.title for b in results]
    assert "The Hobbit" not in titles

def test_list_by_year_boundary_inclusive():
    collection = BookCollection()
    collection.add_book("Start Year Book", "Author A", 1950)
    collection.add_book("End Year Book", "Author B", 1960)
    results = collection.list_by_year(1950, 1960)
    titles = [b.title for b in results]
    assert "Start Year Book" in titles
    assert "End Year Book" in titles

def test_list_by_year_no_matches():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.list_by_year(2000, 2020)
    assert results == []

def test_list_by_year_empty_collection():
    collection = BookCollection()
    results = collection.list_by_year(1900, 2000)
    assert results == []


def test_load_books_skips_malformed_entry_without_losing_valid_ones(tmp_path, capsys):
    """A single malformed record must not wipe out the whole collection."""
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "1984", "author": "George Orwell", "year": 1949},
        {"title": "Missing Year", "author": "Nobody"},
        "not-even-an-object",
    ]))

    collection = BookCollection()

    assert [b.title for b in collection.books] == ["1984"]
    captured = capsys.readouterr()
    assert "skipping entry 1" in captured.out
    assert "skipping entry 2" in captured.out


def test_load_books_skips_wrong_typed_fields(tmp_path, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "1984", "author": "George Orwell", "year": "1949"},
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": "yes"},
        {"title": "Valid Book", "author": "Someone", "year": 2000},
    ]))

    collection = BookCollection()

    assert [b.title for b in collection.books] == ["Valid Book"]
    captured = capsys.readouterr()
    assert "year must be a whole number" in captured.out
    assert "read must be true/false" in captured.out


def test_load_books_skips_duplicate_titles(tmp_path, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        {"title": "dune", "author": "Someone Else", "year": 1970},
    ]))

    collection = BookCollection()

    assert len(collection.books) == 1
    assert collection.books[0].author == "Frank Herbert"
    captured = capsys.readouterr()
    assert "skipping duplicate book" in captured.out


def test_load_books_keeps_business_rule_violations(tmp_path):
    """Structurally valid but business-rule-invalid records still load
    (e.g. blank author, year 0) -- these are data quality issues to
    surface elsewhere, not reasons to hide the record."""
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "Mysterious Book", "author": "", "year": 0, "read": False},
    ]))

    collection = BookCollection()

    assert len(collection.books) == 1
    assert collection.books[0].title == "Mysterious Book"


def test_load_books_handles_non_list_top_level(tmp_path, capsys):
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps({"title": "Not a list"}))

    collection = BookCollection()

    assert collection.books == []
    captured = capsys.readouterr()
    assert "does not contain a list of books" in captured.out
