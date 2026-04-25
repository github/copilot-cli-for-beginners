import threading
import json
import os
import time
import pytest
import sys
from types import SimpleNamespace
from pathlib import Path

import books as books_module

# Helper to inject utils with controllable behaviors
def make_utils_module(atomic_write_success=True, raise_on_write=False, warn_calls=None, error_calls=None):
    warn_calls = warn_calls if warn_calls is not None else []
    error_calls = error_calls if error_calls is not None else []

    def safe_load_json(path, default=None):
        try:
            return json.loads(Path(path).read_text())
        except Exception:
            return default

    def atomic_write_json(path, payload):
        if raise_on_write:
            raise OSError("permission denied")
        Path(path).write_text(json.dumps(payload))
        return atomic_write_success

    def log_warn(msg):
        warn_calls.append(msg)

    def log_error(msg):
        error_calls.append(msg)

    return SimpleNamespace(
        safe_load_json=safe_load_json,
        atomic_write_json=atomic_write_json,
        log_warn=log_warn,
        log_error=log_error,
    ), warn_calls, error_calls


@pytest.fixture(autouse=True)
def isolated_utils(monkeypatch, tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    mod, warn_calls, error_calls = make_utils_module()
    monkeypatch.setitem(sys.modules, "utils", mod)
    monkeypatch.setattr(books_module, "DATA_FILE", str(data_file))
    return mod, warn_calls, error_calls


def test_adding_duplicate_books(isolated_utils, tmp_path):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.add_book("Dune", "Frank Herbert", 1965)
    col.add_book("Dune", "Frank Herbert", 1965)
    # duplicates are allowed; both entries present
    matches = [b for b in col.list_books() if b.title == "Dune" and b.author == "Frank Herbert"]
    assert len(matches) == 2


def test_remove_by_partial_title_does_not_remove(isolated_utils, tmp_path):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    col.add_book("The Hobbit", "Tolkien", 1937)
    # attempt to remove by partial title
    result = col.remove_book("Hobbit")
    assert result is False
    assert col.find_book_by_title("The Hobbit") is not None


def test_find_when_collection_empty(isolated_utils, tmp_path):
    mod, warn_calls, error_calls = isolated_utils
    col = books_module.BookCollection(str(tmp_path / "d.json"))
    assert col.list_books() == []
    assert col.find_book_by_title("Anything") is None
    assert col.find_by_author("Nobody") == []


def test_file_permission_error_during_save(monkeypatch, tmp_path):
    # create utils that raise on write
    mod, warn_calls, error_calls = make_utils_module(raise_on_write=True)
    monkeypatch.setitem(sys.modules, "utils", mod)
    data_file = tmp_path / "readonly.json"
    data_file.write_text("[]")
    col = books_module.BookCollection(str(data_file))
    # add_book triggers save_books which will raise OSError from our utils; ensure exception propagates
    with pytest.raises(OSError):
        col.add_book("Dune", "H", 1965)

    # calling save_books directly also raises
    with pytest.raises(OSError):
        col.save_books()


def test_concurrent_access_adds_items(monkeypatch, tmp_path):
    # use real utils implementation in module (already present) by pointing PYTHONPATH; here reuse module's atomic_write_json
    # prepare two collection instances sharing same file
    data_file = tmp_path / "shared.json"
    data_file.write_text("[]")

    # inject utils that perform normal atomic write
    mod, warn_calls, error_calls = make_utils_module()
    monkeypatch.setitem(sys.modules, "utils", mod)

    col1 = books_module.BookCollection(str(data_file))
    col2 = books_module.BookCollection(str(data_file))

    def add_many(col, prefix):
        for i in range(10):
            col.add_book(f"Book {prefix}-{i}", "Author", 2000 + i)
            # small delay to increase chance of interleaving
            time.sleep(0.01)

    t1 = threading.Thread(target=add_many, args=(col1, "A"))
    t2 = threading.Thread(target=add_many, args=(col2, "B"))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # reload from disk into a fresh collection to observe final persisted state
    col_final = books_module.BookCollection(str(data_file))
    titles = {b.title for b in col_final.list_books()}
    # concurrent writes may race; ensure there are at least 10 and at most 20 unique titles
    assert 10 <= len(titles) <= 20
    # ensure no crash; at least one thread's items should be present
    assert len(titles) >= 10
