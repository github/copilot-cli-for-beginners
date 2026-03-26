import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    return str(temp_file)


@pytest.fixture(autouse=True)
def collection(use_temp_data_file):
    """Create a BookCollection with temporary storage."""
    return BookCollection(data_file=use_temp_data_file)


def test_add_book(collection):
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False


def test_mark_book_as_read(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_by_title("Dune")
    assert book.read is True


def test_mark_book_as_read_invalid(collection):
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False


def test_remove_book(collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_by_title("The Hobbit")
    assert book is None


def test_remove_book_invalid(collection):
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_list_by_year_range(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.list_by_year(1940, 1970)
    assert len(results) == 2
    titles = {b.title for b in results}
    assert titles == {"1984", "Dune"}


def test_list_by_year_no_matches(collection):
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.list_by_year(2000, 2020)
    assert len(results) == 0


def test_list_by_year_single_year(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    results = collection.list_by_year(1949, 1949)
    assert len(results) == 1
    assert results[0].title == "1984"


def test_list_by_year_reversed_range(collection):
    with pytest.raises(ValueError):
        collection.list_by_year(2000, 1900)


def test_list_by_year_empty_collection(collection):
    results = collection.list_by_year(1900, 2000)
    assert len(results) == 0
