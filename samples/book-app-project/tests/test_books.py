import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_handle_read_found(monkeypatch, capsys):
    import book_app
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    book_app.handle_read()

    captured = capsys.readouterr()
    assert "marked as read" in captured.out
    book = collection.find_book_by_title("Dune")
    assert book.read is True


def test_search_by_title_partial():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.search("hobbit")
    assert len(results) == 1
    assert results[0].title == "The Hobbit"


def test_search_by_author_partial():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("Dune", "Frank Herbert", 1965)
    results = collection.search("orwell")
    assert len(results) == 2


def test_search_case_insensitive():
    collection = BookCollection()
    collection.add_book("Brave New World", "Aldous Huxley", 1932)
    results = collection.search("BRAVE")
    assert len(results) == 1
    results = collection.search("HUXLEY")
    assert len(results) == 1


def test_search_no_results():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.search("tolkien")
    assert results == []


def test_handle_search(monkeypatch, capsys):
    import book_app
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr("builtins.input", lambda _: "dune")

    book_app.handle_search()

    captured = capsys.readouterr()
    assert "Dune" in captured.out
    assert "Dune Messiah" in captured.out


# ---------------------------------------------------------------------------
# get_unread_books
# ---------------------------------------------------------------------------

class TestGetUnreadBooks:
    """Tests for BookCollection.get_unread_books."""

    def test_returns_only_unread_books(self):
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)
        collection.mark_as_read("1984")

        unread = collection.get_unread_books()

        assert len(unread) == 1
        assert unread[0].title == "Dune"

    def test_all_unread_returns_all_books(self):
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.add_book("Dune", "Frank Herbert", 1965)

        unread = collection.get_unread_books()

        assert len(unread) == 2

    def test_all_read_returns_empty_list(self):
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")

        unread = collection.get_unread_books()

        assert unread == []

    def test_empty_collection_returns_empty_list(self):
        collection = BookCollection()

        unread = collection.get_unread_books()

        assert unread == []

    def test_returned_list_is_not_internal_reference(self):
        """Mutating the returned list must not affect the collection."""
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)

        unread = collection.get_unread_books()
        unread.clear()

        assert len(collection.books) == 1

    def test_unread_books_have_read_false(self):
        collection = BookCollection()
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        collection.add_book("1984", "George Orwell", 1949)

        unread = collection.get_unread_books()

        assert all(not b.read for b in unread)

    @pytest.mark.parametrize("read_count,total", [
        (0, 3),
        (1, 3),
        (2, 3),
        (3, 3),
    ])
    def test_unread_count_matches_expected(self, read_count, total):
        collection = BookCollection()
        titles = ["Book A", "Book B", "Book C"]
        for i, title in enumerate(titles):
            collection.add_book(title, "Author", 2000 + i)
        for title in titles[:read_count]:
            collection.mark_as_read(title)

        unread = collection.get_unread_books()

        assert len(unread) == total - read_count

    def test_marking_book_as_read_removes_it_from_unread(self):
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        assert len(collection.get_unread_books()) == 1

        collection.mark_as_read("Dune")

        assert collection.get_unread_books() == []

    def test_adding_book_appears_in_unread(self):
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")
        assert collection.get_unread_books() == []

        collection.add_book("Dune", "Frank Herbert", 1965)

        unread = collection.get_unread_books()
        assert len(unread) == 1
        assert unread[0].title == "Dune"


# ---------------------------------------------------------------------------
# handle_list_unread (CLI handler)
# ---------------------------------------------------------------------------

class TestHandleListUnread:
    """Tests for book_app.handle_list_unread."""

    def test_shows_unread_books(self, monkeypatch, capsys):
        import book_app
        collection = BookCollection()
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")
        monkeypatch.setattr(book_app, "collection", collection)

        book_app.handle_list_unread()

        captured = capsys.readouterr()
        assert "The Hobbit" in captured.out

    def test_excludes_read_books(self, monkeypatch, capsys):
        import book_app
        collection = BookCollection()
        collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")
        monkeypatch.setattr(book_app, "collection", collection)

        book_app.handle_list_unread()

        captured = capsys.readouterr()
        assert "1984" not in captured.out

    def test_empty_collection_prints_no_books_found(self, monkeypatch, capsys):
        import book_app
        collection = BookCollection()
        monkeypatch.setattr(book_app, "collection", collection)

        book_app.handle_list_unread()

        captured = capsys.readouterr()
        assert "No books found" in captured.out

    def test_all_read_prints_no_books_found(self, monkeypatch, capsys):
        import book_app
        collection = BookCollection()
        collection.add_book("1984", "George Orwell", 1949)
        collection.mark_as_read("1984")
        monkeypatch.setattr(book_app, "collection", collection)

        book_app.handle_list_unread()

        captured = capsys.readouterr()
        assert "No books found" in captured.out

    def test_command_registered_in_commands_dict(self):
        import book_app
        assert "list-unread" in book_app.COMMANDS
        assert book_app.COMMANDS["list-unread"] is book_app.handle_list_unread

    def test_list_unread_command_via_main(self, monkeypatch, capsys):
        import book_app
        collection = BookCollection()
        collection.add_book("Dune", "Frank Herbert", 1965)
        monkeypatch.setattr(book_app, "collection", collection)
        monkeypatch.setattr("sys.argv", ["book_app.py", "list-unread"])

        book_app.main()

        captured = capsys.readouterr()
        assert "Dune" in captured.out
