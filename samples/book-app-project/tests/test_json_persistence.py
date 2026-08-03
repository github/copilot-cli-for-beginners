import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import books
from books import Book, BookCollection


class TestJsonBookStorage:
    """Tests for JSON persistence safeguards."""

    def test_saves_unicode_as_utf8(self, tmp_path):
        data_file = tmp_path / "data.json"
        collection = BookCollection(data_file)

        collection.add_book("Cien años de soledad", "Gabriel García Márquez", 1967)

        assert "Cien años de soledad" in data_file.read_text(encoding="utf-8")

    def test_replaces_existing_file_atomically(self, tmp_path, monkeypatch):
        data_file = tmp_path / "data.json"
        data_file.write_text("[]", encoding="utf-8")
        collection = BookCollection(data_file)
        collection.books.append(Book("Dune", "Frank Herbert", 1965))
        replaced = False
        original_replace = os.replace

        def track_replace(source, destination):
            nonlocal replaced
            replaced = True
            original_replace(source, destination)

        monkeypatch.setattr(books.os, "replace", track_replace)

        collection.save_books()

        assert replaced
        assert json.loads(data_file.read_text(encoding="utf-8"))[0]["title"] == "Dune"
        assert not list(tmp_path.glob(".data.json.*.tmp"))

    def test_failed_replace_preserves_existing_file(self, tmp_path, monkeypatch):
        data_file = tmp_path / "data.json"
        original_contents = "[]\n"
        data_file.write_text(original_contents, encoding="utf-8")
        collection = BookCollection(data_file)
        collection.books.append(Book("Dune", "Frank Herbert", 1965))

        def fail_replace(source, destination):
            raise OSError("disk error")

        monkeypatch.setattr(books.os, "replace", fail_replace)

        with pytest.raises(books.DataFileError, match="Cannot save"):
            collection.save_books()

        assert data_file.read_text(encoding="utf-8") == original_contents
        assert not list(tmp_path.glob(".data.json.*.tmp"))

    @pytest.mark.parametrize(
        "data, message",
        [
            ({}, "JSON array"),
            ([{"title": "Dune"}], "must contain"),
            (
                [
                    {
                        "title": "Dune",
                        "author": "Frank Herbert",
                        "year": "1965",
                        "read": False,
                    }
                ],
                "invalid types",
            ),
        ],
    )
    def test_rejects_invalid_persisted_records(self, tmp_path, data, message):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(books.DataFileError, match=message):
            BookCollection(data_file)

    def test_missing_file_creates_empty_collection(self, tmp_path):
        collection = BookCollection(tmp_path / "missing.json")

        assert collection.books == []
