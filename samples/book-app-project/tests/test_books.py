import importlib
import sys
from types import SimpleNamespace
import json
import tempfile
from pathlib import Path

import pytest

# Import target module (module uses local `utils` imports inside functions)
import books as books_module

# Helper to inject a fake utils module into sys.modules for isolation

def make_utils_module(data=None, atomic_write_success=True, warn_calls=None, error_calls=None):
    data = [] if data is None else data
    warn_calls = warn_calls if warn_calls is not None else []
    error_calls = error_calls if error_calls is not None else []

    def safe_load_json(path, default=None):
        # ignore path and return provided data copy
        return list(data)

    def atomic_write_json(path, payload):
        # write payload to the path so tests can inspect it
        Path(path).write_text(json.dumps(payload))
        return atomic_write_success

    def log_warn(msg):
        warn_calls.append(msg)

    def log_error(msg):
        error_calls.append(msg)

    mod = SimpleNamespace(
        safe_load_json=safe_load_json,
        atomic_write_json=atomic_write_json,
        log_warn=log_warn,
        log_error=log_error,
    )
    return mod, warn_calls, error_calls


@pytest.fixture(autouse=True)
def isolated_utils(monkeypatch, tmp_path):
    """Provide an isolated fake utils module for each test and point DATA_FILE to a temp file."""
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    mod, warn_calls, error_calls = make_utils_module()
    # ensure imports of 'utils' inside books module resolve to our fake module
    monkeypatch.setitem(sys.modules, "utils", mod)
    # ensure BookCollection default DATA_FILE points at our temp file path
    monkeypatch.setattr(books_module, "DATA_FILE", str(data_file))
    yield mod, warn_calls, error_calls


def test_add_and_list_books(tmp_path, isolated_utils, monkeypatch):
    mod, warn_calls, error_calls = isolated_utils
    data_file = tmp_path / "data.json"

    col = books_module.BookCollection(str(data_file))
    # initially empty
    assert col.list_books() == []

    b = col.add_book("Dune", "Frank Herbert", 1965)
    assert isinstance(b, books_module.Book)
    assert b.title == "Dune"
    assert b.author == "Frank Herbert"
    assert b.year == 1965
    assert b.read is False

    # list_books returns same instance list
    assert col.list_books()[0] is b

    # adding invalid title raises
    with pytest.raises(ValueError):
        col.add_book("   ", "No One", 2000)


def test_load_skips_invalid_records(tmp_path, monkeypatch):
    # prepare utils to return a mix of good and bad records
    data = [
        {"title": " Good ", "author": "A", "year": "1999", "read": True},
        "not-a-dict",
        {"title": "", "author": "B"},
        {"author": "C"},
        {"title": "Ok", "year": None},
    ]
    mod, warn_calls, error_calls = make_utils_module(data=data)
    monkeypatch.setitem(sys.modules, "utils", mod)

    col = importlib.reload(books_module).BookCollection(str(tmp_path / "d.json"))
    # should have loaded only the valid records with titles "Good" and "Ok"
    titles = [b.title for b in col.list_books()]
    assert "Good" in titles
    assert "Ok" in titles
    # ensure warnings were issued
    assert any("skipped" in w or "does not contain" in w for w in warn_calls)


def test_save_books_logs_error_when_write_fails(tmp_path, isolated_utils, monkeypatch):
    # make atomic_write_json return False
    mod, warn_calls, error_calls = make_utils_module(atomic_write_success=False)
    monkeypatch.setitem(sys.modules, "utils", mod)

    data_file = tmp_path / "d.json"
    col = importlib.reload(books_module).BookCollection(str(data_file))
    col.add_book("Nineteen Eighty-Four", "Orwell", 1949)

    # save_books should call atomic_write_json and log_error when it returns False
    col.save_books()
    assert any("failed to save" in e for e in error_calls)


def test_list_by_year_and_invalid_range(tmp_path, isolated_utils):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("A", "X", 1990),
        books_module.Book("B", "Y", 2000),
        books_module.Book("C", "Z", 2010),
    ]

    with pytest.raises(ValueError):
        col.list_by_year(2001, 2000)

    res = col.list_by_year(1995, 2005)
    assert [b.title for b in res] == ["B"]


def test_find_by_title_case_insensitive(tmp_path, isolated_utils):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [books_module.Book("Dune", "H", 1965)]

    assert col.find_book_by_title("dune").title == "Dune"
    assert col.find_book_by_title("DUNE").title == "Dune"
    assert col.find_book_by_title("Nope") is None


def test_mark_as_read_and_remove(tmp_path, isolated_utils, monkeypatch):
    mod, warn_calls, error_calls = isolated_utils
    # ensure atomic write succeeds so no exceptions
    mod.atomic_write_json = lambda p, payload: True
    monkeypatch.setitem(sys.modules, "utils", mod)

    col = importlib.reload(books_module).BookCollection(str(tmp_path / "d.json"))
    col.add_book("Dune", "H", 1965)

    assert col.mark_as_read("Dune") is True
    assert col.find_book_by_title("Dune").read is True

    assert col.remove_book("Dune") is True
    assert col.find_book_by_title("Dune") is None

    # removing non-existent returns False
    assert col.remove_book("NotHere") is False


def test_find_by_author(tmp_path, isolated_utils):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("A", "Same", 2001),
        books_module.Book("B", "same", 2002),
        books_module.Book("C", "Other", 2003),
    ]
    res = col.find_by_author("same")
    assert len(res) == 2


def test_search_basic_and_edge_cases(tmp_path, isolated_utils):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("Dune", "Frank Herbert", 1965),
        books_module.Book("Neuromancer", "William Gibson", 1984),
        books_module.Book("Good Omens", "Terry Pratchett", 1990),
    ]

    # empty query returns empty
    assert col.search("") == []

    # basic substring search case-insensitive across fields
    r = col.search("dune")
    assert len(r) == 1 and r[0].title == "Dune"

    # author search
    r = col.search("gibson", fields=["author"])
    assert len(r) == 1 and r[0].title == "Neuromancer"

    # case sensitive search
    r = col.search("Dune", case_sensitive=True)
    assert len(r) == 1
    r = col.search("dune", case_sensitive=True)
    assert len(r) == 0

    # invalid field raises
    with pytest.raises(ValueError):
        col.search("x", fields=["publisher"]) 


# Ensure tests importable module path mapping
if __name__ == "__main__":
    pytest.main(["-q"])
