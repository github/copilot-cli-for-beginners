import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from book_app import (
    show_books, show_books_with_indices, handle_list, handle_add,
    handle_remove, handle_find, handle_mark, show_help
)
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    
    # Reset the global collection
    import book_app
    book_app.collection = BookCollection()


def test_show_books_empty(capsys):
    """Test displaying empty book list."""
    show_books([])
    captured = capsys.readouterr()
    assert "No books found." in captured.out


def test_show_books_with_books(capsys):
    """Test displaying books with proper formatting."""
    from books import Book
    
    books = [
        Book(title="1984", author="George Orwell", year=1949, read=True),
        Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, read=False),
    ]
    show_books(books)
    captured = capsys.readouterr()
    
    assert "Your Book Collection:" in captured.out
    assert "1984" in captured.out
    assert "✓" in captured.out  # read book
    assert " " in captured.out  # unread book


def test_show_books_with_indices(capsys):
    """Test displaying books with indices."""
    from books import Book
    
    books = [
        Book(title="1984", author="George Orwell", year=1949, read=False),
    ]
    show_books_with_indices(books)
    captured = capsys.readouterr()
    
    assert "Books Available:" in captured.out
    assert "1." in captured.out
    assert "1984" in captured.out


def test_handle_list(capsys):
    """Test list command."""
    from book_app import collection
    collection.add_book("1984", "George Orwell", 1949)
    
    handle_list()
    captured = capsys.readouterr()
    
    assert "Your Book Collection:" in captured.out
    assert "1984" in captured.out


def test_handle_add_valid(capsys, monkeypatch):
    """Test adding a book with valid input."""
    from book_app import collection
    
    inputs = iter(["The Hobbit", "J.R.R. Tolkien", "1937"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_add()
    captured = capsys.readouterr()
    
    assert "Book added successfully." in captured.out
    assert len(collection.list_books()) == 1


def test_handle_add_empty_title(capsys, monkeypatch):
    """Test adding book with empty title fails."""
    inputs = iter([""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_add()
    captured = capsys.readouterr()
    
    assert "Error: Title cannot be empty." in captured.out


def test_handle_add_empty_author(capsys, monkeypatch):
    """Test adding book with empty author fails."""
    inputs = iter(["The Hobbit", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_add()
    captured = capsys.readouterr()
    
    assert "Error: Author cannot be empty." in captured.out


def test_handle_add_negative_year(capsys, monkeypatch):
    """Test adding book with negative year fails."""
    inputs = iter(["The Hobbit", "J.R.R. Tolkien", "-1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_add()
    captured = capsys.readouterr()
    
    assert "Error: Year must be a positive number." in captured.out


def test_handle_add_invalid_year(capsys, monkeypatch):
    """Test adding book with non-numeric year fails."""
    inputs = iter(["The Hobbit", "J.R.R. Tolkien", "abc"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_add()
    captured = capsys.readouterr()
    
    assert "Error: Year must be a valid integer." in captured.out


def test_handle_remove_success(capsys, monkeypatch):
    """Test removing a book that exists."""
    from book_app import collection
    collection.add_book("1984", "George Orwell", 1949)
    
    monkeypatch.setattr('builtins.input', lambda _: "1984")
    
    handle_remove()
    captured = capsys.readouterr()
    
    assert "has been removed." in captured.out


def test_handle_remove_not_found(capsys, monkeypatch):
    """Test removing a book that doesn't exist."""
    monkeypatch.setattr('builtins.input', lambda _: "Nonexistent")
    
    handle_remove()
    captured = capsys.readouterr()
    
    assert "not found." in captured.out


def test_handle_find_success(capsys, monkeypatch):
    """Test finding books by author."""
    from book_app import collection
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    
    monkeypatch.setattr('builtins.input', lambda _: "George Orwell")
    
    handle_find()
    captured = capsys.readouterr()
    
    assert "1984" in captured.out
    assert "Animal Farm" in captured.out


def test_handle_find_no_results(capsys, monkeypatch):
    """Test finding books by non-existent author."""
    monkeypatch.setattr('builtins.input', lambda _: "Unknown Author")
    
    handle_find()
    captured = capsys.readouterr()
    
    assert "No books found." in captured.out


def test_handle_mark_by_title(capsys, monkeypatch):
    """Test marking book as read by title."""
    from book_app import collection
    collection.add_book("1984", "George Orwell", 1949)
    
    inputs = iter(["1", "1984"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_mark()
    captured = capsys.readouterr()
    
    assert "marked as read." in captured.out


def test_handle_mark_by_index(capsys, monkeypatch):
    """Test marking book as read by selecting from list."""
    from book_app import collection
    collection.add_book("1984", "George Orwell", 1949)
    
    inputs = iter(["2", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_mark()
    captured = capsys.readouterr()
    
    assert "marked as read." in captured.out


def test_handle_mark_invalid_choice(capsys, monkeypatch):
    """Test mark with invalid choice."""
    inputs = iter(["3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    handle_mark()
    captured = capsys.readouterr()
    
    assert "Invalid choice" in captured.out


def test_show_help(capsys):
    """Test help command displays all options."""
    show_help()
    captured = capsys.readouterr()
    
    assert "Book Collection Helper" in captured.out
    assert "list" in captured.out
    assert "add" in captured.out
    assert "remove" in captured.out
    assert "find" in captured.out
    assert "mark" in captured.out
    assert "help" in captured.out
