import sys
import json
from types import SimpleNamespace
from pathlib import Path
import pytest

import books as books_module


def make_utils_module(data=None):
    data = [] if data is None else data
    def safe_load_json(path, default=None):
        try:
            return json.loads(Path(path).read_text())
        except Exception:
            return default
    def atomic_write_json(path, payload):
        Path(path).write_text(json.dumps(payload))
        return True
    def log_warn(msg):
        pass
    def log_error(msg):
        pass
    return SimpleNamespace(
        safe_load_json=safe_load_json,
        atomic_write_json=atomic_write_json,
        log_warn=log_warn,
        log_error=log_error,
    )


@pytest.fixture(autouse=True)
def isolated_utils(monkeypatch, tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    mod = make_utils_module()
    monkeypatch.setitem(sys.modules, "utils", mod)
    monkeypatch.setattr(books_module, "DATA_FILE", str(data_file))
    return mod


def test_find_by_author_hyphenated(monkeypatch, tmp_path, isolated_utils):
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("Being and Nothingness", "Jean-Paul Sartre", 1943),
        books_module.Book("No Exit", "Jean Paul Sartre", 1944),
    ]
    res = col.find_by_author("Jean-Paul Sartre")
    assert len(res) == 1
    assert res[0].title == "Being and Nothingness"


def test_find_by_author_multiple_first_names(isolated_utils, tmp_path):
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("Book1", "Mary Anne Evans", 1860),
        books_module.Book("Book2", "George Eliot", 1861),
    ]
    res = col.find_by_author("Mary Anne Evans")
    assert len(res) == 1
    assert res[0].title == "Book1"


def test_find_by_author_empty_string(isolated_utils, tmp_path):
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("Unknown", "", 0),
        books_module.Book("Known", "Author", 2000),
    ]
    res = col.find_by_author("")
    # should match the book with empty author
    assert len(res) == 1
    assert res[0].title == "Unknown"


def test_find_by_author_accented(isolated_utils, tmp_path):
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.books = [
        books_module.Book("Les Misérables", "Victor Hugo", 1862),
        books_module.Book("L'Étranger", "Albert Camus", 1942),
        books_module.Book("Play", "José Saramago", 1995),
    ]
    res = col.find_by_author("José Saramago")
    assert len(res) == 1
    assert res[0].title == "Play"
