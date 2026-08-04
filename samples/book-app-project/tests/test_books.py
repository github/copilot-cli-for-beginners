import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import Book, BookCollection


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
    book = collection.find_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_find_by_title():
    collection = BookCollection()
    collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    book = collection.find_by_title("The Great Gatsby")
    assert book is not None
    assert book.author == "F. Scott Fitzgerald"


def test_find_by_title_case_insensitive():
    collection = BookCollection()
    collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    book = collection.find_by_title("the great gatsby")
    assert book is not None
    assert book.title == "The Great Gatsby"


def test_find_by_title_not_found():
    collection = BookCollection()
    book = collection.find_by_title("Nonexistent Book")
    assert book is None


def test_find_by_author():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    
    orwell_books = collection.find_by_author("George Orwell")
    assert len(orwell_books) == 2
    assert all(book.author == "George Orwell" for book in orwell_books)


def test_find_by_author_case_insensitive():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    books = collection.find_by_author("george orwell")
    assert len(books) == 1


def test_find_by_author_not_found():
    collection = BookCollection()
    books = collection.find_by_author("Unknown Author")
    assert len(books) == 0


def test_list_books():
    collection = BookCollection()
    assert len(collection.list_books()) == 0
    
    collection.add_book("Book 1", "Author 1", 2020)
    collection.add_book("Book 2", "Author 2", 2021)
    
    books = collection.list_books()
    assert len(books) == 2
    assert books[0].title == "Book 1"
    assert books[1].title == "Book 2"


class TestGetUnreadBooks:
    """Tests for get_unread_books."""

    def test_get_unread_books_returns_empty_list_for_empty_collection(self):
        collection = BookCollection()

        unread_books = collection.get_unread_books()

        assert unread_books == []

    @pytest.mark.parametrize(
        ("read_states", "expected_titles"),
        [
            ([False], ["Book 1"]),
            ([True, False], ["Book 2"]),
            ([False, True, False], ["Book 1", "Book 3"]),
            ([True, True], []),
            ([False, False], ["Book 1", "Book 2"]),
        ],
    )
    def test_get_unread_books_filters_books_and_preserves_order(
        self, read_states, expected_titles
    ):
        collection = BookCollection()
        collection.books = [
            Book(f"Book {index}", "Author", 2020, read)
            for index, read in enumerate(read_states, start=1)
        ]

        unread_books = collection.get_unread_books()

        assert [book.title for book in unread_books] == expected_titles

    def test_get_unread_books_reflects_book_marked_as_read(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)

        collection.mark_as_read("Dune")
        unread_books = collection.get_unread_books()

        assert unread_books == []

    def test_get_unread_books_excludes_removed_unread_book(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)

        collection.remove_book("Dune")
        unread_books = collection.get_unread_books()

        assert unread_books == []
