import pytest
import utils


def test_get_book_details_valid(monkeypatch):
    inputs = iter(["Dune", "Frank Herbert", "1965"])
    monkeypatch.setattr("builtins.input", lambda prompt='': next(inputs))
    title, author, year = utils.get_book_details()
    assert title == "Dune"
    assert author == "Frank Herbert"
    assert isinstance(year, int) and year == 1965


def test_get_book_details_empty_strings(monkeypatch):
    # first provide empty title then valid title
    inputs = iter(["", "Title", "Some Author", "2000"])
    monkeypatch.setattr("builtins.input", lambda prompt='': next(inputs))
    # get_book_details loops until non-empty title; should return successfully
    title, author, year = utils.get_book_details()
    assert title == "Title"
    assert author == "Some Author"
    assert year == 2000


def test_get_book_details_invalid_year_formats(monkeypatch, capsys):
    # non-numeric year falls back to 0 and logs a warning
    inputs = iter(["Title", "Author", "not-a-year"])
    monkeypatch.setattr("builtins.input", lambda prompt='': next(inputs))
    title, author, year = utils.get_book_details()
    assert isinstance(year, int)
    assert year == 0

    # float-like string results in ValueError in int() -> fallback to 0 per implementation
    inputs = iter(["Title2", "Author2", "1999.0"])
    monkeypatch.setattr("builtins.input", lambda prompt='': next(inputs))
    title, author, year = utils.get_book_details()
    assert isinstance(year, int)


def test_get_book_details_very_long_titles(monkeypatch):
    long_title = "A" * 1000
    inputs = iter([long_title, "Author", "2020"])
    monkeypatch.setattr("builtins.input", lambda prompt='': next(inputs))
    title, author, year = utils.get_book_details()
    assert title == long_title
    assert year == 2020


def test_get_book_details_special_characters_in_author(monkeypatch):
    special_author = "José María \u2603 O'Conner-Ł"
    inputs = iter(["Some Title", special_author, "1980"])
    monkeypatch.setattr("builtins.input", lambda prompt='': next(inputs))
    title, author, year = utils.get_book_details()
    assert author == special_author
    assert title == "Some Title"
    assert year == 1980


if __name__ == "__main__":
    pytest.main()
