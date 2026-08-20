import json

import pytest

from books_buggy import Book, BookCollection


@pytest.fixture
def collection(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    c = BookCollection()
    c.books = [
        Book(title="Dune", author="Frank Herbert", year=1965, read=False),
        Book(title="Neuromancer", author="William Gibson", year=1984, read=False),
    ]
    c.save_books()
    return c


class TestMarkAsRead:
    def test_marks_only_matching_book_as_read(self, collection):
        result = collection.mark_as_read("Dune")

        assert result is True
        assert collection.books[0].read is True
        assert collection.books[1].read is False

    def test_returns_false_when_book_not_found(self, collection):
        result = collection.mark_as_read("Foundation")

        assert result is False
        assert [b.read for b in collection.books] == [False, False]

    def test_persists_read_state_for_only_target_book(self, collection, tmp_path):
        collection.mark_as_read("Neuromancer")

        data = json.loads((tmp_path / "data.json").read_text())
        assert data[0]["title"] == "Dune"
        assert data[0]["read"] is False
        assert data[1]["title"] == "Neuromancer"
        assert data[1]["read"] is True
