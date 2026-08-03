"""
Comprehensive tests for books.py covering all methods and edge cases.

This test suite documents the current behavior of the BookCollection and Book
classes, providing baseline coverage before any refactoring.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
import books
from books import Book, BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


# ============================================================================
# Book Dataclass Tests
# ============================================================================

class TestBook:
    """Tests for the Book dataclass."""

    def test_book_creation_with_all_fields(self):
        """Test creating a Book with all fields specified."""
        book = Book(title="1984", author="George Orwell", year=1949, read=True)
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.year == 1949
        assert book.read is True

    def test_book_creation_with_defaults(self):
        """Test creating a Book uses default read value."""
        book = Book(title="1984", author="George Orwell", year=1949)
        assert book.read is False

    def test_book_read_modification(self):
        """Test modifying the read attribute."""
        book = Book(title="1984", author="George Orwell", year=1949)
        assert book.read is False
        book.read = True
        assert book.read is True

    @pytest.mark.parametrize("year", [0, 1000, 1949, 2024, 5000])
    def test_book_with_various_years(self, year):
        """Test Book accepts various year values."""
        book = Book(title="Test", author="Author", year=year)
        assert book.year == year

    def test_book_with_empty_title(self):
        """Test Book allows empty title (validation is at application level)."""
        book = Book(title="", author="Author", year=2024)
        assert book.title == ""

    def test_book_with_empty_author(self):
        """Test Book allows empty author (validation is at application level)."""
        book = Book(title="Title", author="", year=2024)
        assert book.author == ""

    def test_book_with_special_characters(self):
        """Test Book handles special characters in title and author."""
        book = Book(
            title="The Catcher in the Rye: A Study",
            author="J.D. Salinger (Author)",
            year=1951
        )
        assert ":" in book.title
        assert "(" in book.author


# ============================================================================
# BookCollection Initialization Tests
# ============================================================================

class TestBookCollectionInit:
    """Tests for BookCollection initialization."""

    def test_init_empty_collection(self):
        """Test initializing BookCollection with empty data file."""
        collection = BookCollection()
        assert isinstance(collection.books, list)
        assert len(collection.books) == 0

    def test_init_loads_existing_books(self, tmp_path, monkeypatch):
        """Test that __init__ loads books from file."""
        # Pre-populate data file
        data_file = tmp_path / "data.json"
        books_data = [
            {"title": "1984", "author": "Orwell", "year": 1949, "read": False},
            {"title": "Dune", "author": "Herbert", "year": 1965, "read": True},
        ]
        data_file.write_text(json.dumps(books_data))
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        assert len(collection.books) == 2
        assert collection.books[0].title == "1984"
        assert collection.books[1].read is True

    def test_init_with_missing_file(self, tmp_path, monkeypatch):
        """Test that __init__ handles missing data file gracefully."""
        # Point to non-existent file
        data_file = tmp_path / "missing.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        assert len(collection.books) == 0

    def test_init_with_corrupted_json(self, tmp_path, monkeypatch):
        """Test that corrupted JSON is reported without risking data loss."""
        data_file = tmp_path / "data.json"
        data_file.write_text("{ invalid json }")
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        with pytest.raises(books.DataFileError, match="invalid JSON"):
            BookCollection()


# ============================================================================
# Load and Save Tests
# ============================================================================

class TestLoadSaveBooks:
    """Tests for load_books and save_books methods."""

    def test_save_books_creates_file(self, tmp_path, monkeypatch):
        """Test that save_books creates the data file."""
        data_file = tmp_path / "new_file.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        assert data_file.exists()

    def test_save_books_formats_json(self, tmp_path, monkeypatch):
        """Test that save_books produces valid, indented JSON."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        with open(data_file) as f:
            content = f.read()
            data = json.loads(content)
        
        assert len(data) == 1
        assert data[0]["title"] == "1984"
        assert "  " in content  # indented

    def test_load_books_reload(self, tmp_path, monkeypatch):
        """Test that load_books can reload data from file."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("Book 1", "Author 1", 2020)
        
        # Create new collection and reload
        collection2 = BookCollection()
        assert len(collection2.books) == 1
        assert collection2.books[0].title == "Book 1"

    def test_save_preserves_all_fields(self, tmp_path, monkeypatch):
        """Test that save/load preserves all book fields."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        collection.mark_as_read("1984")
        
        collection2 = BookCollection()
        book = collection2.books[0]
        assert book.title == "1984"
        assert book.author == "Orwell"
        assert book.year == 1949
        assert book.read is True


# ============================================================================
# Add Book Tests
# ============================================================================

class TestAddBook:
    """Tests for add_book method."""

    def test_add_book_returns_book_object(self):
        """Test that add_book returns the created Book."""
        collection = BookCollection()
        book = collection.add_book("1984", "Orwell", 1949)
        
        assert isinstance(book, Book)
        assert book.title == "1984"

    def test_add_book_increments_collection(self):
        """Test that add_book increases collection size."""
        collection = BookCollection()
        assert len(collection.books) == 0
        
        collection.add_book("Book 1", "Author 1", 2020)
        assert len(collection.books) == 1
        
        collection.add_book("Book 2", "Author 2", 2021)
        assert len(collection.books) == 2

    def test_add_multiple_same_title_allowed(self):
        """Test that same title can be added multiple times."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        collection.add_book("1984", "Orwell", 1949)
        
        assert len(collection.books) == 2

    def test_add_book_persists_to_file(self, tmp_path, monkeypatch):
        """Test that add_book saves to file immediately."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        # Load fresh collection
        collection2 = BookCollection()
        assert len(collection2.books) == 1

    def test_add_book_with_empty_title(self):
        """Test that add_book allows empty title."""
        collection = BookCollection()
        book = collection.add_book("", "Author", 2020)
        assert book.title == ""
        assert len(collection.books) == 1

    def test_add_book_with_zero_year(self):
        """Test that add_book allows year 0."""
        collection = BookCollection()
        book = collection.add_book("Unknown", "Unknown", 0)
        assert book.year == 0

    def test_add_book_with_future_year(self):
        """Test that add_book allows future years."""
        collection = BookCollection()
        book = collection.add_book("Future", "Author", 5000)
        assert book.year == 5000


# ============================================================================
# List Books Tests
# ============================================================================

class TestListBooks:
    """Tests for list_books method."""

    def test_list_books_empty_collection(self):
        """Test list_books returns empty list for empty collection."""
        collection = BookCollection()
        books_list = collection.list_books()
        assert isinstance(books_list, list)
        assert len(books_list) == 0

    def test_list_books_returns_all_books(self):
        """Test list_books returns all books in collection."""
        collection = BookCollection()
        collection.add_book("Book 1", "Author 1", 2020)
        collection.add_book("Book 2", "Author 2", 2021)
        
        books_list = collection.list_books()
        assert len(books_list) == 2

    def test_list_books_returns_reference(self):
        """Test that list_books returns reference to internal list."""
        collection = BookCollection()
        collection.add_book("Book 1", "Author 1", 2020)
        
        books_list1 = collection.list_books()
        books_list2 = collection.list_books()
        assert books_list1 is books_list2  # Same object

    def test_list_books_preserves_order(self):
        """Test that list_books preserves insertion order."""
        collection = BookCollection()
        collection.add_book("Book 1", "Author 1", 2020)
        collection.add_book("Book 2", "Author 2", 2021)
        collection.add_book("Book 3", "Author 3", 2022)
        
        books_list = collection.list_books()
        assert books_list[0].title == "Book 1"
        assert books_list[1].title == "Book 2"
        assert books_list[2].title == "Book 3"


# ============================================================================
# Find By Title Tests
# ============================================================================

class TestFindByTitle:
    """Tests for find_by_title method."""

    def test_find_by_title_exact_match(self):
        """Test finding book with exact title match."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        book = collection.find_by_title("1984")
        assert book is not None
        assert book.title == "1984"

    def test_find_by_title_case_insensitive(self):
        """Test that find_by_title is case-insensitive."""
        collection = BookCollection()
        collection.add_book("The Great Gatsby", "Fitzgerald", 1925)
        
        assert collection.find_by_title("the great gatsby") is not None
        assert collection.find_by_title("THE GREAT GATSBY") is not None
        assert collection.find_by_title("ThE gReAt GaTsBy") is not None

    def test_find_by_title_not_found(self):
        """Test find_by_title returns None when not found."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        book = collection.find_by_title("Unknown")
        assert book is None

    def test_find_by_title_empty_collection(self):
        """Test find_by_title on empty collection."""
        collection = BookCollection()
        book = collection.find_by_title("Anything")
        assert book is None

    def test_find_by_title_duplicate_titles_returns_first(self):
        """Test that find_by_title returns first match with duplicate titles."""
        collection = BookCollection()
        book1 = collection.add_book("1984", "Orwell", 1949)
        book2 = collection.add_book("1984", "Unknown", 2000)
        
        found = collection.find_by_title("1984")
        assert found is book1  # Returns first one

    def test_find_by_title_whitespace_handling(self):
        """Test find_by_title with whitespace."""
        collection = BookCollection()
        collection.add_book("Book Title", "Author", 2020)
        
        # Exact match still works with different spacing
        assert collection.find_by_title("Book Title") is not None


# ============================================================================
# Find By Author Tests
# ============================================================================

class TestFindByAuthor:
    """Tests for find_by_author method."""

    def test_find_by_author_single_book(self):
        """Test finding single book by author."""
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        
        books_list = collection.find_by_author("George Orwell")
        assert len(books_list) == 1
        assert books_list[0].title == "1984"

    def test_find_by_author_multiple_books(self):
        """Test finding multiple books by same author."""
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Animal Farm", "George Orwell", 1945)
        
        books_list = collection.find_by_author("George Orwell")
        assert len(books_list) == 2
        assert all(b.author == "George Orwell" for b in books_list)

    def test_find_by_author_case_insensitive(self):
        """Test that find_by_author is case-insensitive."""
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        
        assert len(collection.find_by_author("george orwell")) == 1
        assert len(collection.find_by_author("GEORGE ORWELL")) == 1

    def test_find_by_author_not_found(self):
        """Test find_by_author returns empty list when not found."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        books_list = collection.find_by_author("Unknown Author")
        assert books_list == []

    def test_find_by_author_empty_collection(self):
        """Test find_by_author on empty collection."""
        collection = BookCollection()
        books_list = collection.find_by_author("Any Author")
        assert books_list == []

    def test_find_by_author_preserves_order(self):
        """Test that find_by_author preserves insertion order."""
        collection = BookCollection()
        collection.add_book("Animal Farm", "Orwell", 1945)
        collection.add_book("1984", "Orwell", 1949)
        
        books_list = collection.find_by_author("Orwell")
        assert books_list[0].year == 1945
        assert books_list[1].year == 1949


# ============================================================================
# Mark As Read Tests
# ============================================================================

class TestMarkAsRead:
    """Tests for mark_as_read method."""

    def test_mark_as_read_success(self):
        """Test successfully marking a book as read."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        result = collection.mark_as_read("1984")
        assert result is True
        
        book = collection.find_by_title("1984")
        assert book.read is True

    def test_mark_as_read_not_found(self):
        """Test mark_as_read with non-existent book."""
        collection = BookCollection()
        
        result = collection.mark_as_read("Unknown")
        assert result is False

    def test_mark_as_read_already_read(self):
        """Test marking already read book (idempotent)."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        collection.mark_as_read("1984")
        
        # Mark again
        result = collection.mark_as_read("1984")
        assert result is True
        assert collection.find_by_title("1984").read is True

    def test_mark_as_read_case_insensitive(self):
        """Test mark_as_read is case-insensitive."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        result = collection.mark_as_read("1984")
        assert result is True

    def test_mark_as_read_persists(self, tmp_path, monkeypatch):
        """Test that mark_as_read persists to file."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        collection.mark_as_read("1984")
        
        # Load fresh collection
        collection2 = BookCollection()
        assert collection2.find_by_title("1984").read is True

    def test_mark_as_read_duplicate_titles_first_one(self):
        """Test mark_as_read with duplicate titles marks first one."""
        collection = BookCollection()
        book1 = collection.add_book("1984", "Orwell", 1949)
        book2 = collection.add_book("1984", "Unknown", 2000)
        
        collection.mark_as_read("1984")
        assert book1.read is True
        assert book2.read is False


# ============================================================================
# Remove Book Tests
# ============================================================================

class TestRemoveBook:
    """Tests for remove_book method."""

    def test_remove_book_success(self):
        """Test successfully removing a book."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        result = collection.remove_book("1984")
        assert result is True
        assert len(collection.books) == 0

    def test_remove_book_not_found(self):
        """Test remove_book with non-existent book."""
        collection = BookCollection()
        
        result = collection.remove_book("Unknown")
        assert result is False

    def test_remove_book_case_insensitive(self):
        """Test remove_book is case-insensitive."""
        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        
        result = collection.remove_book("1984")
        assert result is True

    def test_remove_book_persists(self, tmp_path, monkeypatch):
        """Test that remove_book persists to file."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        collection = BookCollection()
        collection.add_book("1984", "Orwell", 1949)
        collection.remove_book("1984")
        
        # Load fresh collection
        collection2 = BookCollection()
        assert len(collection2.books) == 0

    def test_remove_book_duplicate_titles_first_one(self):
        """Test remove_book with duplicate titles removes first one."""
        collection = BookCollection()
        book1 = collection.add_book("1984", "Orwell", 1949)
        book2 = collection.add_book("1984", "Unknown", 2000)
        
        collection.remove_book("1984")
        assert len(collection.books) == 1
        assert collection.books[0] is book2

    def test_remove_reduces_collection_size(self):
        """Test that remove_book reduces collection size."""
        collection = BookCollection()
        collection.add_book("Book 1", "Author 1", 2020)
        collection.add_book("Book 2", "Author 2", 2021)
        collection.add_book("Book 3", "Author 3", 2022)
        
        assert len(collection.books) == 3
        collection.remove_book("Book 2")
        assert len(collection.books) == 2


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple operations."""

    def test_complete_workflow(self, tmp_path, monkeypatch):
        """Test complete workflow: add, mark, find, remove."""
        data_file = tmp_path / "data.json"
        monkeypatch.setattr(books, "DATA_FILE", str(data_file))

        # Create and populate collection
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Animal Farm", "George Orwell", 1945)
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        
        # Mark one as read
        collection.mark_as_read("1984")
        
        # Find by author
        orwell_books = collection.find_by_author("George Orwell")
        assert len(orwell_books) == 2
        
        # Remove one
        collection.remove_book("Animal Farm")
        assert len(collection.books) == 2
        
        # Verify persistence
        collection2 = BookCollection()
        assert len(collection2.books) == 2
        assert collection2.find_by_title("1984").read is True

    def test_state_consistency_after_operations(self):
        """Test that collection state is consistent after various operations."""
        collection = BookCollection()
        
        # Add multiple books
        for i in range(5):
            collection.add_book(f"Book {i}", f"Author {i}", 2020 + i)
        
        # Mark some as read
        collection.mark_as_read("Book 1")
        collection.mark_as_read("Book 3")
        
        # Remove some
        collection.remove_book("Book 2")
        
        # Verify state
        assert len(collection.books) == 4
        assert sum(1 for b in collection.books if b.read) == 2
        assert collection.find_by_title("Book 0") is not None
        assert collection.find_by_title("Book 2") is None
