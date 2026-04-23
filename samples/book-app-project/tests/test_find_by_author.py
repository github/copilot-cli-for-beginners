import sys
import os
import pytest

# ensure package can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_find_by_author_partial_match_returns_multiple():
    # arrange
    collection = BookCollection()
    collection.add_book("Pride and Prejudice", "Jane Austen", 1813)
    collection.add_book("Sense and Sensibility", "Austen, Jane", 1811)
    collection.add_book("Dune", "Frank Herbert", 1965)

    # act
    results = collection.find_by_author("Austen")

    # assert
    assert len(results) == 2


def test_find_by_author_case_variation_matches():
    # arrange
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    # act
    results = collection.find_by_author("gEoRgE orWeLL")

    # assert
    assert len(results) == 1
    assert results[0].title == "1984"


def test_find_by_author_no_matches_returns_empty_list():
    # arrange
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    # act
    results = collection.find_by_author("Nonexistent Author")

    # assert
    assert results == []
