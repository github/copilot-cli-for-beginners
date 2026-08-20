import importlib
import sys

import pytest


class FakeCollection:
    def __init__(self):
        self.calls = []

    def add_book(self, title, author, year):
        self.calls.append((title, author, year))


@pytest.fixture
def app_module(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sys.modules.pop("book_app_buggy", None)
    module = importlib.import_module("book_app_buggy")
    return module


class TestHandleAdd:
    def test_adds_book_with_valid_input(self, app_module, monkeypatch, capsys):
        fake_collection = FakeCollection()
        monkeypatch.setattr(app_module, "collection", fake_collection)

        inputs = iter(["Dune", "Frank Herbert", "1965"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        app_module.handle_add()

        assert fake_collection.calls == [("Dune", "Frank Herbert", 1965)]
        assert "Book added successfully." in capsys.readouterr().out

    def test_defaults_year_to_zero_when_empty(self, app_module, monkeypatch):
        fake_collection = FakeCollection()
        monkeypatch.setattr(app_module, "collection", fake_collection)

        inputs = iter(["Neuromancer", "William Gibson", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        app_module.handle_add()

        assert fake_collection.calls == [("Neuromancer", "William Gibson", 0)]

    @pytest.mark.parametrize("year_input", ["abc", "19.5", "two thousand"])
    def test_shows_error_for_non_integer_year(
        self, app_module, monkeypatch, capsys, year_input
    ):
        fake_collection = FakeCollection()
        monkeypatch.setattr(app_module, "collection", fake_collection)

        inputs = iter(["Dune", "Frank Herbert", year_input])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        app_module.handle_add()

        assert fake_collection.calls == []
        assert "Error:" in capsys.readouterr().out

    def test_passes_empty_title_and_author_through(self, app_module, monkeypatch):
        fake_collection = FakeCollection()
        monkeypatch.setattr(app_module, "collection", fake_collection)

        inputs = iter(["", "", "2000"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        app_module.handle_add()

        assert fake_collection.calls == [("", "", 2000)]
