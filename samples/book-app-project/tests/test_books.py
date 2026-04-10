import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temporary path for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


@pytest.fixture
def collection():
    """Empty BookCollection."""
    return BookCollection()


@pytest.fixture
def populated_collection():
    """BookCollection pre-loaded with three books."""
    col = BookCollection()
    col.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    col.add_book("1984", "George Orwell", 1949)
    col.add_book("Dune", "Frank Herbert", 1965)
    return col


# ---------------------------------------------------------------------------
# TestAddBook
# ---------------------------------------------------------------------------

class TestAddBook:
    """Tests for BookCollection.add_book()."""

    def test_adds_book_to_collection(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        assert len(collection.books) == 1

    def test_returned_book_has_correct_fields(self, collection):
        book = collection.add_book("1984", "George Orwell", 1949)
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year == 1949

    def test_new_book_defaults_to_unread(self, collection):
        book = collection.add_book("1984", "George Orwell", 1949)
        assert book.read is False

    def test_add_multiple_books(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert len(collection.books) == 2

    def test_persists_to_file(self, collection, tmp_path, monkeypatch):
        """Adding a book should persist so a new instance can load it."""
        collection.add_book("1984", "George Orwell", 1949)
        new_collection = BookCollection()
        assert len(new_collection.books) == 1
        assert new_collection.books[0].title == "1984"

    @pytest.mark.parametrize("title,author,year", [
        ("The Hobbit", "J.R.R. Tolkien", 1937),
        ("Dune", "Frank Herbert", 1965),
        ("To Kill a Mockingbird", "Harper Lee", 1960),
    ])
    def test_add_various_books(self, collection, title, author, year):
        book = collection.add_book(title, author, year)
        assert book.title == title
        assert book.author == author
        assert book.year == year

    # --- Year validation ---

    @pytest.mark.parametrize("invalid_year", [0, -1, -100, 2101, 9999])
    def test_add_book_invalid_year_raises(self, collection, invalid_year):
        with pytest.raises(ValueError, match="Year must be between 1 and 2100"):
            collection.add_book("Title", "Author", invalid_year)

    def test_add_book_year_boundary_min(self, collection):
        book = collection.add_book("Ancient", "Author", 1)
        assert book.year == 1

    def test_add_book_year_boundary_max(self, collection):
        book = collection.add_book("Future", "Author", 2100)
        assert book.year == 2100

    def test_invalid_year_does_not_persist(self, collection):
        with pytest.raises(ValueError):
            collection.add_book("Title", "Author", 0)
        assert len(collection.books) == 0


# ---------------------------------------------------------------------------
# TestRemoveBook
# ---------------------------------------------------------------------------

class TestRemoveBook:
    """Tests for BookCollection.remove_book()."""

    def test_removes_existing_book(self, populated_collection):
        result = populated_collection.remove_book("The Hobbit")
        assert result is True
        assert populated_collection.find_book_by_title("The Hobbit") is None

    def test_returns_false_for_nonexistent_book(self, collection):
        result = collection.remove_book("Nonexistent Book")
        assert result is False

    def test_removes_only_target_book(self, populated_collection):
        populated_collection.remove_book("1984")
        assert len(populated_collection.books) == 2
        assert populated_collection.find_book_by_title("The Hobbit") is not None
        assert populated_collection.find_book_by_title("Dune") is not None

    def test_remove_from_empty_collection(self, collection):
        result = collection.remove_book("Any Book")
        assert result is False

    def test_remove_is_case_insensitive(self, populated_collection):
        result = populated_collection.remove_book("the hobbit")
        assert result is True
        assert populated_collection.find_book_by_title("The Hobbit") is None

    def test_remove_persists_to_file(self, populated_collection):
        populated_collection.remove_book("1984")
        reloaded = BookCollection()
        assert reloaded.find_book_by_title("1984") is None


# ---------------------------------------------------------------------------
# TestFindBookByTitle
# ---------------------------------------------------------------------------

class TestFindBookByTitle:
    """Tests for BookCollection.find_book_by_title()."""

    def test_finds_existing_book(self, populated_collection):
        book = populated_collection.find_book_by_title("Dune")
        assert book is not None
        assert book.title == "Dune"

    def test_returns_none_for_missing_book(self, collection):
        result = collection.find_book_by_title("Ghost Book")
        assert result is None

    def test_find_is_case_insensitive(self, populated_collection):
        assert populated_collection.find_book_by_title("dune") is not None
        assert populated_collection.find_book_by_title("DUNE") is not None

    def test_find_in_empty_collection(self, collection):
        assert collection.find_book_by_title("1984") is None

    @pytest.mark.parametrize("title", ["The Hobbit", "1984", "Dune"])
    def test_finds_each_book_by_title(self, populated_collection, title):
        book = populated_collection.find_book_by_title(title)
        assert book is not None
        assert book.title == title


# ---------------------------------------------------------------------------
# TestFindByAuthor
# ---------------------------------------------------------------------------

class TestFindByAuthor:
    """Tests for BookCollection.find_by_author()."""

    def test_finds_books_by_exact_author(self, populated_collection):
        results = populated_collection.find_by_author("George Orwell")
        assert len(results) == 1
        assert results[0].title == "1984"

    def test_returns_empty_for_unknown_author(self, collection):
        results = collection.find_by_author("Unknown Author")
        assert results == []

    def test_find_author_is_case_insensitive(self, populated_collection):
        results = populated_collection.find_by_author("george orwell")
        assert len(results) == 1

    def test_find_by_author_empty_collection(self, collection):
        assert collection.find_by_author("Anyone") == []

    def test_find_returns_all_books_by_author(self, collection):
        collection.add_book("Animal Farm", "George Orwell", 1945)
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        results = collection.find_by_author("George Orwell")
        assert len(results) == 2

    # --- Partial match ---

    def test_partial_last_name_returns_match(self, populated_collection):
        results = populated_collection.find_by_author("Orwell")
        assert len(results) == 1
        assert results[0].title == "1984"

    def test_partial_first_name_returns_match(self, populated_collection):
        results = populated_collection.find_by_author("George")
        assert len(results) == 1
        assert results[0].author == "George Orwell"

    def test_partial_name_matches_multiple_authors(self, collection):
        collection.add_book("Book A", "George Orwell", 1945)
        collection.add_book("Book B", "George Bernard Shaw", 1900)
        collection.add_book("Book C", "Frank Herbert", 1965)
        results = collection.find_by_author("George")
        assert len(results) == 2

    def test_partial_name_no_match_returns_empty(self, populated_collection):
        results = populated_collection.find_by_author("Asimov")
        assert results == []

    # --- Case variations ---

    @pytest.mark.parametrize("query", [
        "orwell",
        "ORWELL",
        "Orwell",
        "oRwElL",
    ])
    def test_partial_match_is_case_insensitive(self, populated_collection, query):
        results = populated_collection.find_by_author(query)
        assert len(results) == 1
        assert results[0].title == "1984"

    def test_uppercase_full_name_matches(self, populated_collection):
        results = populated_collection.find_by_author("GEORGE ORWELL")
        assert len(results) == 1

    # --- Edge cases ---

    def test_empty_string_matches_all(self, populated_collection):
        """Empty string is a substring of every author name."""
        results = populated_collection.find_by_author("")
        assert len(results) == len(populated_collection.books)

    def test_single_character_matches_correct_books(self, populated_collection):
        results = populated_collection.find_by_author("J")
        titles = [b.title for b in results]
        assert "The Hobbit" in titles  # J.R.R. Tolkien

    def test_returns_list_type(self, collection):
        assert isinstance(collection.find_by_author("Anyone"), list)


# ---------------------------------------------------------------------------
# TestMarkAsRead
# ---------------------------------------------------------------------------

class TestMarkAsRead:
    """Tests for BookCollection.mark_as_read()."""

    def test_marks_book_as_read(self, populated_collection):
        result = populated_collection.mark_as_read("Dune")
        assert result is True
        book = populated_collection.find_book_by_title("Dune")
        assert book.read is True

    def test_returns_false_for_nonexistent_book(self, collection):
        assert collection.mark_as_read("Ghost Book") is False

    def test_only_target_book_marked_read(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        assert populated_collection.find_book_by_title("The Hobbit").read is False
        assert populated_collection.find_book_by_title("1984").read is False

    def test_mark_as_read_is_case_insensitive(self, populated_collection):
        result = populated_collection.mark_as_read("dune")
        assert result is True
        assert populated_collection.find_book_by_title("Dune").read is True

    def test_mark_already_read_book(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        result = populated_collection.mark_as_read("Dune")
        assert result is True
        assert populated_collection.find_book_by_title("Dune").read is True

    def test_mark_as_read_persists_to_file(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        reloaded = BookCollection()
        assert reloaded.find_book_by_title("Dune").read is True


# ---------------------------------------------------------------------------
# TestSearchBooks
# ---------------------------------------------------------------------------

class TestSearchBooks:
    """Tests for BookCollection.search_books()."""

    def test_search_by_partial_title(self, populated_collection):
        results = populated_collection.search_books("hobbit")
        assert len(results) == 1
        assert results[0].title == "The Hobbit"

    def test_search_by_partial_author(self, populated_collection):
        results = populated_collection.search_books("orwell")
        assert len(results) == 1
        assert results[0].title == "1984"

    def test_search_is_case_insensitive(self, populated_collection):
        assert len(populated_collection.search_books("DUNE")) == 1
        assert len(populated_collection.search_books("frank")) == 1

    def test_search_returns_empty_for_no_match(self, populated_collection):
        assert populated_collection.search_books("nonexistent") == []

    def test_search_empty_collection(self, collection):
        assert collection.search_books("anything") == []

    def test_search_matches_multiple_books(self, collection):
        collection.add_book("Animal Farm", "George Orwell", 1945)
        collection.add_book("1984", "George Orwell", 1949)
        results = collection.search_books("orwell")
        assert len(results) == 2

    @pytest.mark.parametrize("query,expected_count", [
        ("Tolkien", 1),
        ("the", 1),   # "The Hobbit"
        ("19", 1),    # "1984" のみ（year フィールドは検索対象外）
        ("z", 0),
    ])
    def test_search_various_queries(self, populated_collection, query, expected_count):
        results = populated_collection.search_books(query)
        assert len(results) == expected_count


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases: empty collection, corrupted file, persistence."""

    def test_empty_collection_list_books(self, collection):
        assert collection.list_books() == []

    def test_list_books_returns_all(self, populated_collection):
        assert len(populated_collection.list_books()) == 3

    def test_load_missing_file_starts_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "missing.json"))
        col = BookCollection()
        assert col.books == []

    def test_load_corrupted_file_starts_empty(self, tmp_path, monkeypatch, capsys):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{not valid json}")
        monkeypatch.setattr(books, "DATA_FILE", str(bad_file))
        col = BookCollection()
        assert col.books == []
        assert "corrupted" in capsys.readouterr().out

    def test_add_and_immediately_reload(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        reloaded = BookCollection()
        assert len(reloaded.books) == 1
        assert reloaded.books[0].title == "1984"


# ---------------------------------------------------------------------------
# TestInputValidation
# ---------------------------------------------------------------------------

class TestInputValidation:
    """Tests for input validation gaps identified in code review."""

    # --- Empty strings in add_book ---

    def test_add_book_empty_title_is_accepted(self, collection):
        """Current behaviour: empty title is stored without error."""
        book = collection.add_book("", "George Orwell", 1949)
        assert book.title == ""

    def test_add_book_empty_author_is_accepted(self, collection):
        """Current behaviour: empty author is stored without error."""
        book = collection.add_book("1984", "", 1949)
        assert book.author == ""

    # --- None inputs expose AttributeError ---

    def test_find_book_by_title_none_raises(self, populated_collection):
        """Passing None raises AttributeError because .lower() is called on None."""
        with pytest.raises(AttributeError):
            populated_collection.find_book_by_title(None)

    def test_find_by_author_none_raises(self, populated_collection):
        """Passing None raises AttributeError because .lower() is called on None."""
        with pytest.raises(AttributeError):
            populated_collection.find_by_author(None)

    def test_search_books_none_raises(self, collection):
        """Passing None raises AttributeError because .lower() is called on None."""
        with pytest.raises(AttributeError):
            collection.search_books(None)

    # --- search_books with empty string ---

    def test_search_books_empty_query_returns_all(self, populated_collection):
        """Empty string matches every book (substring of anything)."""
        results = populated_collection.search_books("")
        assert len(results) == len(populated_collection.books)

    # --- Malformed JSON records in load_books ---

    def test_load_record_missing_field_raises(self, tmp_path, monkeypatch):
        """A record missing 'year' causes TypeError when constructing Book(**b)."""
        import json
        bad_file = tmp_path / "missing_field.json"
        bad_file.write_text(json.dumps([{"title": "Incomplete", "author": "Author"}]))
        monkeypatch.setattr(books, "DATA_FILE", str(bad_file))
        with pytest.raises(TypeError):
            BookCollection()

    def test_load_record_extra_field_raises(self, tmp_path, monkeypatch):
        """A record with an unexpected field causes TypeError via Book(**b)."""
        import json
        bad_file = tmp_path / "extra_field.json"
        bad_file.write_text(json.dumps([
            {"title": "Dune", "author": "Frank Herbert", "year": 1965,
             "read": False, "rating": 5}
        ]))
        monkeypatch.setattr(books, "DATA_FILE", str(bad_file))
        with pytest.raises(TypeError):
            BookCollection()


# ---------------------------------------------------------------------------
# TestGetUnreadBooks
# ---------------------------------------------------------------------------

class TestGetUnreadBooks:
    """Tests for BookCollection.get_unread_books()."""

    # --- Happy path ---

    def test_returns_all_books_when_none_read(self, populated_collection):
        results = populated_collection.get_unread_books()
        assert len(results) == 3

    def test_returns_only_unread_books(self, populated_collection):
        populated_collection.mark_as_read("1984")
        results = populated_collection.get_unread_books()
        assert all(not b.read for b in results)

    def test_excludes_read_book_by_title(self, populated_collection):
        populated_collection.mark_as_read("1984")
        titles = [b.title for b in populated_collection.get_unread_books()]
        assert "1984" not in titles

    def test_returns_correct_count_after_marking_one_read(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        results = populated_collection.get_unread_books()
        assert len(results) == 2

    def test_returns_correct_count_after_marking_two_read(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        populated_collection.mark_as_read("1984")
        results = populated_collection.get_unread_books()
        assert len(results) == 1

    def test_returns_list_of_book_objects(self, populated_collection):
        from books import Book
        results = populated_collection.get_unread_books()
        assert all(isinstance(b, Book) for b in results)

    def test_returns_list_type(self, collection):
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert isinstance(collection.get_unread_books(), list)

    # --- Edge cases ---

    def test_empty_collection_returns_empty_list(self, collection):
        assert collection.get_unread_books() == []

    def test_all_read_returns_empty_list(self, populated_collection):
        for title in ["The Hobbit", "1984", "Dune"]:
            populated_collection.mark_as_read(title)
        assert populated_collection.get_unread_books() == []

    def test_single_unread_book_returned(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        results = collection.get_unread_books()
        assert len(results) == 1
        assert results[0].title == "1984"

    def test_does_not_modify_collection_size(self, populated_collection):
        before = len(populated_collection.books)
        populated_collection.get_unread_books()
        assert len(populated_collection.books) == before

    def test_does_not_modify_read_status(self, populated_collection):
        populated_collection.get_unread_books()
        assert all(not b.read for b in populated_collection.books)

    # --- Parametrized: mark N books read, expect M unread ---

    @pytest.mark.parametrize("titles_to_read,expected_unread", [
        ([], 3),
        (["1984"], 2),
        (["1984", "Dune"], 1),
        (["The Hobbit", "1984", "Dune"], 0),
    ])
    def test_unread_count_for_various_read_combinations(
        self, populated_collection, titles_to_read, expected_unread
    ):
        for title in titles_to_read:
            populated_collection.mark_as_read(title)
        assert len(populated_collection.get_unread_books()) == expected_unread

    # --- Integration ---

    def test_newly_added_book_appears_in_unread(self, populated_collection):
        populated_collection.add_book("Brave New World", "Aldous Huxley", 1932)
        titles = [b.title for b in populated_collection.get_unread_books()]
        assert "Brave New World" in titles

    def test_marked_read_book_not_in_unread(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")
        assert collection.get_unread_books() == []

    def test_unread_result_persists_after_reload(self, populated_collection):
        populated_collection.mark_as_read("1984")
        reloaded = BookCollection()
        titles = [b.title for b in reloaded.get_unread_books()]
        assert "1984" not in titles
        assert len(titles) == 2
