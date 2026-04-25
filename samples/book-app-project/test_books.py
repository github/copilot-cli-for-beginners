import pytest
from books import Book, BookCollection


@pytest.fixture
def collection():
    c = BookCollection()
    # avoid loading from disk for tests
    c.books = [
        Book(title="Old Book", author="A", year=1900),
        Book(title="Mid Book", author="B", year=1950),
        Book(title="New Book", author="C", year=2005),
    ]
    return c


def test_list_by_year_full_range(collection):
    assert len(collection.list_by_year(1900, 2005)) == 3


def test_list_by_year_partial_open_start(collection):
    assert [b.title for b in collection.list_by_year(None, 1950)] == ["Old Book", "Mid Book"]


def test_list_by_year_partial_open_end(collection):
    assert [b.title for b in collection.list_by_year(1951, None)] == ["New Book"]


def test_list_by_year_no_matches(collection):
    assert collection.list_by_year(1800, 1801) == []
