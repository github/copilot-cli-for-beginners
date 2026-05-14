import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import utils


def test_parse_year_valid():
    """Test parse_year with valid year."""
    result = utils.parse_year("1925")
    assert result == 1925
    assert isinstance(result, int)


def test_parse_year_invalid():
    """Test parse_year with invalid year defaults to 0."""
    result = utils.parse_year("not_a_year")
    assert result == 0
    assert isinstance(result, int)


def test_parse_year_empty():
    """Test parse_year with empty string defaults to 0."""
    result = utils.parse_year("")
    assert result == 0


def test_get_book_details_valid_year(monkeypatch):
    """Test get_book_details with valid year input."""
    inputs = iter(["The Great Gatsby", "F. Scott Fitzgerald", "1925"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    title, author, year = utils.get_book_details()
    
    assert title == "The Great Gatsby"
    assert author == "F. Scott Fitzgerald"
    assert year == 1925
    assert isinstance(year, int)


def test_get_book_details_invalid_year(monkeypatch):
    """Test get_book_details with invalid year input defaults to 0."""
    inputs = iter(["1984", "George Orwell", "not_a_year"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    title, author, year = utils.get_book_details()
    
    assert title == "1984"
    assert author == "George Orwell"
    assert year == 0  # Defaults to 0 for invalid input
    assert isinstance(year, int)


def test_get_book_details_strips_whitespace(monkeypatch):
    """Test get_book_details strips leading/trailing whitespace."""
    inputs = iter(["  Dune  ", "  Frank Herbert  ", "  1965  "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    
    title, author, year = utils.get_book_details()
    
    assert title == "Dune"
    assert author == "Frank Herbert"
    assert year == 1965
