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


def test_search_by_title_and_author():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    collection.add_book("1984", "George Orwell", 1949)

    # Title partial match
    results = collection.search("Dune")
    assert len(results) == 2

    # Author partial match
    results = collection.search("Orwell")
    assert len(results) == 1
    assert results[0].title == "1984"

    # Case-insensitive search
    results = collection.search("frank")
    assert len(results) == 2


def test_find_by_author_partial():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("Another Book", "Someone Else", 2000)

    res = collection.find_by_author("Tolkien")
    assert len(res) == 1
    assert res[0].title == "The Hobbit"

    # Partial, case-insensitive
    res2 = collection.find_by_author("r.r.")
    assert any("Tolkien" in b.author for b in res2)


def test_add_book_duplicate_case_insensitive():
    collection = BookCollection()
    collection.add_book("Unique Title", "Author", 2001)
    with pytest.raises(ValueError):
        collection.add_book("unique title", "Author2", 2002)


def test_save_and_load_persistence():
    coll1 = BookCollection()
    coll1.add_book("Persisted", "Author", 1999)

    coll2 = BookCollection()
    titles = [b.title for b in coll2.list_books()]
    assert "Persisted" in titles


def test_get_unread_books_mixed_returns_only_unread():
    collection = BookCollection()
    collection.add_book("A", "Author A", 2000)
    collection.add_book("B", "Author B", 2001)
    collection.add_book("C", "Author C", 2002)
    collection.mark_as_read("B")
    titles = {b.title for b in collection.get_unread_books()}
    assert titles == {"A", "C"}


def test_get_unread_books_all_read_returns_empty():
    collection = BookCollection()
    collection.add_book("One", "Author One", 1990)
    collection.add_book("Two", "Author Two", 1991)
    collection.mark_as_read("One")
    collection.mark_as_read("Two")
    assert collection.get_unread_books() == []


def test_get_unread_books_no_books_returns_empty():
    collection = BookCollection()
    assert collection.get_unread_books() == []


def test_get_unread_books_treats_none_as_unread():
    from books import Book
    collection = BookCollection()
    # append a book with a non-boolean 'read' value to observe behavior
    collection.books.append(Book("Maybe", "Author Maybe", 2000, read=None))
    assert [b.title for b in collection.get_unread_books()] == ["Maybe"]


def test_cli_list_unread_prints_only_unread(capsys):
    import importlib
    import book_app
    importlib.reload(book_app)
    coll = book_app.get_collection()
    coll.add_book("A", "Author A", 2000)
    coll.add_book("B", "Author B", 2001)
    coll.add_book("C", "Author C", 2002)
    coll.mark_as_read("B")
    book_app.handle_list_unread()
    out = capsys.readouterr().out
    import re
    titles = set(re.findall(r'^\s*\d+\.\s*(.+?)\s+by\s', out, flags=re.MULTILINE))
    assert titles == {"A", "C"}
