import json
import os
from pathlib import Path
import pytest
from samples.book_app_project.books import BookCollection, Book


def write_json(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def test_add_remove_mark_list(tmp_path):
    data_file = tmp_path / "data.json"
    coll = BookCollection(str(data_file))

    b = coll.add_book("Title A", "Author A", 2000)
    assert isinstance(b, Book)
    assert len(coll.list_books()) == 1

    assert coll.mark_as_read("Title A") is True
    assert coll.find_book_by_title("Title A").read is True

    assert coll.remove_book("Title A") is True
    assert coll.find_book_by_title("Title A") is None
    assert len(coll.list_books()) == 0


def test_list_by_year_and_find_by_author(tmp_path):
    data_file = tmp_path / "data.json"
    coll = BookCollection(str(data_file))

    coll.add_book("Old Book", "Author X", 1900)
    coll.add_book("Modern Book", "Author X", 2005)
    coll.add_book("Recent Book", "Author Y", 2018)

    res = coll.list_by_year(2000, 2020)
    assert any(b.title == "Modern Book" for b in res)
    assert any(b.title == "Recent Book" for b in res)

    by_author = coll.find_by_author("author x")
    assert len(by_author) == 2


def test_search_validation_and_case(tmp_path):
    data_file = tmp_path / "data.json"
    coll = BookCollection(str(data_file))

    coll.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    coll.add_book("Hobbit Tales", "Someone", 2000)

    # default fields (title and author)
    res = coll.search("hobbit")
    assert len(res) >= 2

    res_title_only = coll.search("hobbit", fields=["title"]) 
    assert all("hobbit" in b.title.lower() for b in res_title_only)

    with pytest.raises(ValueError):
        coll.search("x", fields=["invalid_field"])


def test_load_skips_bad_records(tmp_path):
    data_file = tmp_path / "data.json"
    good = {"title": "Good", "author": "A", "year": 1999}
    bad1 = "not-a-dict"
    bad2 = {"author": "NoTitle"}
    write_json(data_file, [good, bad1, bad2])

    coll = BookCollection(str(data_file))
    # Only the good record should be loaded
    books = coll.list_books()
    assert len(books) == 1
    assert books[0].title == "Good"


def test_atomic_save(tmp_path):
    data_file = tmp_path / "data.json"
    coll = BookCollection(str(data_file))

    coll.add_book("A", "B", 1)
    # After save, file should exist and be valid JSON
    assert data_file.exists()
    parsed = json.loads(data_file.read_text(encoding="utf-8"))
    assert isinstance(parsed, list)

    # Simulate permission error by making directory read-only (best-effort)
    dirpath = data_file.parent
    # On some CI environments changing permissions may not behave as expected; skip if not possible
    try:
        os.chmod(dirpath, 0o500)
        coll.add_book("C", "D", 2)  # this will attempt to save and should catch the error
    finally:
        # restore permissions so tmp_path can be cleaned up
        os.chmod(dirpath, 0o700)


# End of file
