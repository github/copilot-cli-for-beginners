import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import Book, BookCollection


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Redirect DATA_FILE to a temp location so tests never touch the real file."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


@pytest.fixture
def collection():
    """Return a fresh, empty BookCollection."""
    return BookCollection()


@pytest.fixture
def populated_collection():
    """Return a BookCollection with several books pre-loaded."""
    col = BookCollection()
    col.add_book("1984", "George Orwell", 1949)
    col.add_book("Animal Farm", "George Orwell", 1945)
    col.add_book("Dune", "Frank Herbert", 1965)
    col.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    return col


# ---------------------------------------------------------------------------
# Book dataclass validation
# ---------------------------------------------------------------------------

class TestBookValidation:
    """Tests for Book.__post_init__ validation."""

    def test_valid_book_creation(self):
        book = Book(title="1984", author="George Orwell", year=1949)
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year == 1949
        assert book.read is False
        assert book.rating is None
        assert book.review is None

    def test_whitespace_normalization(self):
        book = Book(title="  1984  ", author="  George Orwell  ", year=1949)
        assert book.title == "1984"
        assert book.author == "George Orwell"

    @pytest.mark.parametrize("bad_title", ["", "   ", 123, None])
    def test_invalid_title_raises(self, bad_title):
        with pytest.raises((ValueError, TypeError)):
            Book(title=bad_title, author="Author", year=2000)

    @pytest.mark.parametrize("bad_author", ["", "   ", 42, None])
    def test_invalid_author_raises(self, bad_author):
        with pytest.raises((ValueError, TypeError)):
            Book(title="Title", author=bad_author, year=2000)

    @pytest.mark.parametrize("bad_year", [999, 2101, "2000", 1.5])
    def test_invalid_year_raises(self, bad_year):
        with pytest.raises((ValueError, TypeError)):
            Book(title="Title", author="Author", year=bad_year)

    def test_year_zero_is_valid(self):
        """Year 0 represents an unknown publication year."""
        book = Book(title="Ancient Text", author="Unknown", year=0)
        assert book.year == 0

    @pytest.mark.parametrize("valid_rating", [1, 2, 3, 4, 5])
    def test_valid_ratings(self, valid_rating):
        book = Book(title="Title", author="Author", year=2000, rating=valid_rating)
        assert book.rating == valid_rating

    @pytest.mark.parametrize("bad_rating", [0, 6, -1, "5", 3.5])
    def test_invalid_rating_raises(self, bad_rating):
        with pytest.raises((ValueError, TypeError)):
            Book(title="Title", author="Author", year=2000, rating=bad_rating)

    def test_none_rating_is_valid(self):
        book = Book(title="Title", author="Author", year=2000, rating=None)
        assert book.rating is None


# ---------------------------------------------------------------------------
# Adding books
# ---------------------------------------------------------------------------

class TestAddBook:
    """Tests for BookCollection.add_book."""

    def test_add_single_book(self, collection):
        book = collection.add_book("1984", "George Orwell", 1949)
        assert len(collection.books) == 1
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year == 1949
        assert book.read is False

    def test_add_multiple_books(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        assert len(collection.books) == 3

    def test_add_book_returns_book_object(self, collection):
        result = collection.add_book("Dune", "Frank Herbert", 1965)
        assert isinstance(result, Book)

    def test_add_book_persists_to_disk(self, collection):
        collection.add_book("Dune", "Frank Herbert", 1965)
        reloaded = BookCollection()
        assert len(reloaded.books) == 1
        assert reloaded.books[0].title == "Dune"

    def test_add_book_strips_whitespace(self, collection):
        collection.add_book("  1984  ", "  George Orwell  ", 1949)
        book = collection.find_book_by_title("1984")
        assert book is not None
        assert book.title == "1984"
        assert book.author == "George Orwell"

    @pytest.mark.parametrize("bad_title", ["", "   "])
    def test_add_book_empty_title_raises(self, collection, bad_title):
        with pytest.raises(ValueError):
            collection.add_book(bad_title, "Author", 2000)

    @pytest.mark.parametrize("bad_author", ["", "   "])
    def test_add_book_empty_author_raises(self, collection, bad_author):
        with pytest.raises(ValueError):
            collection.add_book("Title", bad_author, 2000)

    @pytest.mark.parametrize("bad_year", [999, 2101])
    def test_add_book_invalid_year_raises(self, collection, bad_year):
        with pytest.raises(ValueError):
            collection.add_book("Title", "Author", bad_year)

    def test_add_book_to_empty_collection(self, collection):
        assert len(collection.books) == 0
        collection.add_book("First Book", "Some Author", 2001)
        assert len(collection.books) == 1


# ---------------------------------------------------------------------------
# Removing books
# ---------------------------------------------------------------------------

class TestRemoveBook:
    """Tests for BookCollection.remove_book."""

    def test_remove_existing_book(self, populated_collection):
        result = populated_collection.remove_book("The Hobbit")
        assert result is True
        assert populated_collection.find_book_by_title("The Hobbit") is None

    def test_remove_decrements_count(self, populated_collection):
        count_before = len(populated_collection.books)
        populated_collection.remove_book("Dune")
        assert len(populated_collection.books) == count_before - 1

    def test_remove_nonexistent_book_returns_false(self, collection):
        result = collection.remove_book("Ghost Book")
        assert result is False

    def test_remove_from_empty_collection_returns_false(self, collection):
        result = collection.remove_book("Anything")
        assert result is False

    def test_remove_only_target_book(self, populated_collection):
        populated_collection.remove_book("Dune")
        assert populated_collection.find_book_by_title("1984") is not None
        assert populated_collection.find_book_by_title("Animal Farm") is not None
        assert populated_collection.find_book_by_title("The Hobbit") is not None

    def test_remove_persists_to_disk(self, populated_collection):
        populated_collection.remove_book("Dune")
        reloaded = BookCollection()
        assert reloaded.find_book_by_title("Dune") is None
        assert reloaded.find_book_by_title("1984") is not None

    def test_remove_same_book_twice(self, populated_collection):
        assert populated_collection.remove_book("Dune") is True
        assert populated_collection.remove_book("Dune") is False


# ---------------------------------------------------------------------------
# Finding by title
# ---------------------------------------------------------------------------

class TestFindByTitle:
    """Tests for BookCollection.find_book_by_title."""

    def test_find_existing_book(self, populated_collection):
        book = populated_collection.find_book_by_title("1984")
        assert book is not None
        assert book.title == "1984"

    def test_find_is_case_insensitive(self, populated_collection):
        assert populated_collection.find_book_by_title("1984") is not None
        assert populated_collection.find_book_by_title("1984".upper()) is not None
        assert populated_collection.find_book_by_title("dune") is not None
        assert populated_collection.find_book_by_title("DUNE") is not None

    def test_find_nonexistent_returns_none(self, populated_collection):
        assert populated_collection.find_book_by_title("Not A Real Book") is None

    def test_find_in_empty_collection_returns_none(self, collection):
        assert collection.find_book_by_title("1984") is None

    def test_find_returns_correct_book_object(self, populated_collection):
        book = populated_collection.find_book_by_title("Dune")
        assert book.author == "Frank Herbert"
        assert book.year == 1965


# ---------------------------------------------------------------------------
# Finding by author
# ---------------------------------------------------------------------------

class TestFindByAuthor:
    """Tests for BookCollection.find_by_author."""

    def test_find_books_by_author(self, populated_collection):
        results = populated_collection.find_by_author("George Orwell")
        assert len(results) == 2
        titles = {b.title for b in results}
        assert titles == {"1984", "Animal Farm"}

    def test_find_by_author_case_insensitive(self, populated_collection):
        lower = populated_collection.find_by_author("george orwell")
        upper = populated_collection.find_by_author("GEORGE ORWELL")
        assert len(lower) == 2
        assert len(upper) == 2

    def test_find_by_author_partial_match(self, populated_collection):
        results = populated_collection.find_by_author("Orwell")
        assert len(results) == 2

    def test_find_by_author_no_match_returns_empty_list(self, populated_collection):
        results = populated_collection.find_by_author("Unknown Author")
        assert results == []

    def test_find_by_author_in_empty_collection(self, collection):
        results = collection.find_by_author("George Orwell")
        assert results == []

    def test_find_by_author_single_result(self, populated_collection):
        results = populated_collection.find_by_author("Frank Herbert")
        assert len(results) == 1
        assert results[0].title == "Dune"


# ---------------------------------------------------------------------------
# Marking as read
# ---------------------------------------------------------------------------

class TestMarkAsRead:
    """Tests for BookCollection.mark_as_read."""

    def test_mark_existing_book_as_read(self, populated_collection):
        result = populated_collection.mark_as_read("Dune")
        assert result is True
        book = populated_collection.find_book_by_title("Dune")
        assert book.read is True

    def test_mark_nonexistent_book_returns_false(self, collection):
        result = collection.mark_as_read("Nonexistent Book")
        assert result is False

    def test_mark_as_read_on_empty_collection(self, collection):
        assert collection.mark_as_read("Any Title") is False

    def test_mark_as_read_persists_to_disk(self, populated_collection):
        populated_collection.mark_as_read("1984")
        reloaded = BookCollection()
        book = reloaded.find_book_by_title("1984")
        assert book.read is True

    def test_mark_already_read_book_stays_read(self, populated_collection):
        populated_collection.mark_as_read("1984")
        result = populated_collection.mark_as_read("1984")
        assert result is True
        book = populated_collection.find_book_by_title("1984")
        assert book.read is True

    def test_mark_as_read_does_not_affect_other_books(self, populated_collection):
        populated_collection.mark_as_read("Dune")
        others = [b for b in populated_collection.books if b.title != "Dune"]
        for book in others:
            assert book.read is False


# ---------------------------------------------------------------------------
# Rating and review
# ---------------------------------------------------------------------------

class TestRatingAndReview:
    """Tests for BookCollection.set_rating, get_rating, and get_review."""

    def test_set_valid_rating(self, populated_collection):
        assert populated_collection.set_rating("1984", 5) is True
        assert populated_collection.get_rating("1984") == 5

    def test_set_rating_with_review(self, populated_collection):
        populated_collection.set_rating("1984", 4, "A masterpiece about totalitarianism")
        assert populated_collection.get_rating("1984") == 4
        assert populated_collection.get_review("1984") == "A masterpiece about totalitarianism"

    def test_set_rating_nonexistent_book_returns_false(self, collection):
        assert collection.set_rating("Ghost Book", 3) is False

    @pytest.mark.parametrize("bad_rating", [0, 6, -1])
    def test_set_invalid_rating_raises(self, populated_collection, bad_rating):
        with pytest.raises(ValueError):
            populated_collection.set_rating("1984", bad_rating)

    def test_get_rating_unrated_book_returns_none(self, populated_collection):
        assert populated_collection.get_rating("Dune") is None

    def test_get_review_unrated_book_returns_none(self, populated_collection):
        assert populated_collection.get_review("Dune") is None

    def test_update_rating(self, populated_collection):
        populated_collection.set_rating("1984", 3)
        populated_collection.set_rating("1984", 5, "Changed my mind — incredible!")
        assert populated_collection.get_rating("1984") == 5
        assert populated_collection.get_review("1984") == "Changed my mind — incredible!"

    def test_rating_persists_to_disk(self, populated_collection):
        populated_collection.set_rating("Dune", 4, "Epic world-building")
        reloaded = BookCollection()
        assert reloaded.get_rating("Dune") == 4
        assert reloaded.get_review("Dune") == "Epic world-building"

    def test_review_whitespace_stripped(self, populated_collection):
        populated_collection.set_rating("1984", 5, "  Great book  ")
        assert populated_collection.get_review("1984") == "Great book"


# ---------------------------------------------------------------------------
# Edge cases — empty collection
# ---------------------------------------------------------------------------

class TestEmptyCollection:
    """Verify all query/mutation methods behave correctly on an empty collection."""

    def test_list_books_empty(self, collection):
        assert collection.list_books() == []

    def test_find_by_title_empty(self, collection):
        assert collection.find_book_by_title("1984") is None

    def test_find_by_author_empty(self, collection):
        assert collection.find_by_author("Orwell") == []

    def test_mark_as_read_empty(self, collection):
        assert collection.mark_as_read("1984") is False

    def test_remove_book_empty(self, collection):
        assert collection.remove_book("1984") is False

    def test_get_rating_empty(self, collection):
        assert collection.get_rating("1984") is None

    def test_get_review_empty(self, collection):
        assert collection.get_review("1984") is None


# ---------------------------------------------------------------------------
# Persistence — load/save round-trip
# ---------------------------------------------------------------------------

class TestPersistence:
    """Tests for BookCollection.load_books and save_books."""

    def test_collection_persists_across_instances(self, collection):
        collection.add_book("1984", "George Orwell", 1949)
        reloaded = BookCollection()
        assert len(reloaded.books) == 1
        assert reloaded.books[0].title == "1984"

    def test_empty_collection_persists(self, collection):
        collection.save_books()
        reloaded = BookCollection()
        assert reloaded.books == []

    def test_load_skips_invalid_records(self, tmp_path, monkeypatch):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text('[{"title": "", "author": "X", "year": 2000, "read": false}]')
        monkeypatch.setattr(books, "DATA_FILE", str(bad_file))
        col = BookCollection()
        assert col.books == []

    def test_load_handles_corrupted_json(self, tmp_path, monkeypatch):
        bad_file = tmp_path / "corrupt.json"
        bad_file.write_text("not valid json {{")
        monkeypatch.setattr(books, "DATA_FILE", str(bad_file))
        col = BookCollection()
        assert col.books == []

    def test_load_handles_missing_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(books, "DATA_FILE", str(tmp_path / "nonexistent.json"))
        col = BookCollection()
        assert col.books == []


# ---------------------------------------------------------------------------
# list_by_year
# ---------------------------------------------------------------------------

class TestListByYear:
    """Tests for BookCollection.list_by_year."""

    def test_list_books_in_range(self, populated_collection):
        results = populated_collection.list_by_year(1940, 1970)
        titles = {b.title for b in results}
        assert "1984" in titles
        assert "Dune" in titles
        assert "The Hobbit" not in titles

    def test_range_is_inclusive(self, populated_collection):
        results = populated_collection.list_by_year(1937, 1937)
        assert len(results) == 1
        assert results[0].title == "The Hobbit"

    def test_no_books_in_range_returns_empty(self, populated_collection):
        assert populated_collection.list_by_year(2000, 2010) == []

    @pytest.mark.parametrize("start,end", [(2000, 1999), (1500, 1400)])
    def test_start_greater_than_end_raises(self, populated_collection, start, end):
        with pytest.raises(ValueError):
            populated_collection.list_by_year(start, end)

    @pytest.mark.parametrize("bad_year", [999, 2101])
    def test_invalid_start_year_raises(self, populated_collection, bad_year):
        with pytest.raises(ValueError):
            populated_collection.list_by_year(bad_year, 2000)

    @pytest.mark.parametrize("bad_year", [999, 2101])
    def test_invalid_end_year_raises(self, populated_collection, bad_year):
        with pytest.raises(ValueError):
            populated_collection.list_by_year(1000, bad_year)
