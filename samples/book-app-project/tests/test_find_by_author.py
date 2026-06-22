import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_find_by_author_full_match():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)

    results = collection.find_by_author("J.R.R. Tolkien")
    titles = [b.title for b in results]
    assert "The Hobbit" in titles
    assert len(titles) == 1


def test_find_by_author_partial_match():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("The Lord of the Rings", "J.R.R. Tolkien", 1954)
    collection.add_book("Dune", "Frank Herbert", 1965)

    results = collection.find_by_author("Tolkien")
    titles = {b.title for b in results}
    assert "The Hobbit" in titles
    assert "The Lord of the Rings" in titles
    assert len(titles) == 2


def test_find_by_author_case_insensitive():
    collection = BookCollection()
    collection.add_book("To Kill a Mockingbird", "Harper Lee", 1960)
    collection.add_book("Go Set a Watchman", "Harper Lee", 2015)

    results = collection.find_by_author("harper lee")
    authors = {b.author for b in results}
    assert "Harper Lee" in authors


def test_find_by_author_not_found():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    results = collection.find_by_author("Nonexistent Author")
    assert results == []
