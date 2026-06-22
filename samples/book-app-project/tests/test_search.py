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


def test_search_by_title_substring():
    collection = BookCollection()
    collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    collection.add_book("Great Expectations", "Charles Dickens", 1861)

    results = collection.search("great")
    titles = [b.title for b in results]
    assert "The Great Gatsby" in titles
    assert "Great Expectations" in titles


def test_search_by_author_case_insensitive():
    collection = BookCollection()
    collection.add_book("To Kill a Mockingbird", "Harper Lee", 1960)
    collection.add_book("Go Set a Watchman", "Harper Lee", 2015)

    results = collection.search("harper")
    authors = {b.author for b in results}
    assert "Harper Lee" in authors


def test_search_no_results():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    results = collection.search("nonexistent")
    assert results == []
