import json
import os

import pytest
from books import Book, BookCollection, BookNotFoundError, BookValidationError, StorageError


@pytest.fixture()
def collection(tmp_path):
    """Create a BookCollection with temporary storage."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    return BookCollection(data_file=str(temp_file))


# --- Adding Books ---


def test_add_book(collection):
    book = collection.add_book("1984", "George Orwell", 1949)
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False
    assert len(collection.books) == 1


def test_add_book_persists(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    reloaded = BookCollection(data_file=collection.data_file)
    assert len(reloaded.books) == 1
    assert reloaded.books[0].title == "Dune"


def test_add_multiple_books(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    assert len(collection.books) == 3


def test_add_book_empty_title(collection):
    with pytest.raises(BookValidationError, match="Title cannot be empty"):
        collection.add_book("", "Author", 2020)


def test_add_book_whitespace_title(collection):
    with pytest.raises(BookValidationError, match="Title cannot be empty"):
        collection.add_book("   ", "Author", 2020)


def test_add_book_empty_author(collection):
    with pytest.raises(BookValidationError, match="Author cannot be empty"):
        collection.add_book("Title", "", 2020)


def test_add_book_whitespace_author(collection):
    with pytest.raises(BookValidationError, match="Author cannot be empty"):
        collection.add_book("Title", "  \t ", 2020)


def test_add_book_negative_year(collection):
    with pytest.raises(BookValidationError):
        collection.add_book("Ancient Text", "Unknown", -500)


def test_add_book_duplicate_title(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert len(collection.books) == 2


def test_add_book_storage_error(tmp_path):
    temp_file = tmp_path / "readonly" / "data.json"
    c = BookCollection(data_file=str(temp_file))
    # Parent dir doesn't exist, so write will fail
    with pytest.raises(StorageError):
        c.add_book("Title", "Author", 2020)


# --- Removing Books ---


def test_remove_book(collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    assert collection.find_by_title("The Hobbit") is None
    assert len(collection.books) == 0


def test_remove_book_persists(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.remove_book("1984")
    reloaded = BookCollection(data_file=collection.data_file)
    assert len(reloaded.books) == 0


def test_remove_book_not_found(collection):
    with pytest.raises(BookNotFoundError):
        collection.remove_book("Nonexistent Book")


def test_remove_book_case_insensitive(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.remove_book("dune")
    assert len(collection.books) == 0


def test_remove_book_leaves_others(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.remove_book("1984")
    assert len(collection.books) == 1
    assert collection.books[0].title == "Dune"


# --- Finding by Title ---


def test_find_by_title(collection):
    collection.add_book("1984", "George Orwell", 1949)
    book = collection.find_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"


def test_find_by_title_case_insensitive(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.find_by_title("dune") is not None
    assert collection.find_by_title("DUNE") is not None
    assert collection.find_by_title("DuNe") is not None


def test_find_by_title_not_found(collection):
    assert collection.find_by_title("Nonexistent") is None


def test_find_by_title_empty_collection(collection):
    assert collection.find_by_title("Anything") is None


def test_find_by_title_returns_first_match(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune", "Other Author", 2000)
    book = collection.find_by_title("Dune")
    assert book.author == "Frank Herbert"


# --- Finding by Author ---


def test_find_by_author(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("Dune", "Frank Herbert", 1965)
    results = collection.find_by_author("George Orwell")
    assert len(results) == 2
    titles = {b.title for b in results}
    assert titles == {"1984", "Animal Farm"}


def test_find_by_author_case_insensitive(collection):
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.find_by_author("george orwell")) == 1
    assert len(collection.find_by_author("GEORGE ORWELL")) == 1


def test_find_by_author_no_match(collection):
    collection.add_book("1984", "George Orwell", 1949)
    assert collection.find_by_author("Unknown Author") == []


def test_find_by_author_empty_collection(collection):
    assert collection.find_by_author("Anyone") == []


# --- Marking as Read ---


def test_mark_as_read(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    assert collection.find_by_title("Dune").read is True


def test_mark_as_read_persists(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    reloaded = BookCollection(data_file=collection.data_file)
    assert reloaded.books[0].read is True


def test_mark_as_read_not_found(collection):
    with pytest.raises(BookNotFoundError):
        collection.mark_as_read("Nonexistent Book")


def test_mark_as_read_case_insensitive(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("dune")
    assert collection.find_by_title("Dune").read is True


def test_mark_as_read_only_target(collection):
    """Marking one book as read should NOT affect others."""
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    assert collection.find_by_title("Dune").read is True
    assert collection.find_by_title("1984").read is False


def test_mark_as_read_already_read(collection):
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.mark_as_read("Dune")
    collection.mark_as_read("Dune")
    assert collection.find_by_title("Dune").read is True


# --- Edge Cases with Empty Data ---


def test_empty_collection_list(collection):
    assert collection.list_books() == []


def test_empty_collection_find_by_author(collection):
    assert collection.find_by_author("Anyone") == []


def test_empty_collection_find_by_title(collection):
    assert collection.find_by_title("Anything") is None


def test_empty_collection_remove(collection):
    with pytest.raises(BookNotFoundError):
        collection.remove_book("Nothing")


def test_empty_collection_mark_as_read(collection):
    with pytest.raises(BookNotFoundError):
        collection.mark_as_read("Nothing")


def test_empty_collection_list_by_year(collection):
    assert collection.list_by_year(1900, 2100) == []


def test_load_missing_file(tmp_path):
    c = BookCollection(data_file=str(tmp_path / "nonexistent.json"))
    assert c.books == []


def test_load_corrupted_json(tmp_path):
    bad_file = tmp_path / "data.json"
    bad_file.write_text("{not valid json")
    c = BookCollection(data_file=str(bad_file))
    assert c.books == []


def test_load_wrong_type_in_json(tmp_path):
    bad_file = tmp_path / "data.json"
    bad_file.write_text('[{"title": "X", "author": "Y", "year": "not_int"}]')
    c = BookCollection(data_file=str(bad_file))
    # Loads successfully (dataclass doesn't validate types at runtime)
    assert len(c.books) == 1


def test_load_extra_fields_in_json(tmp_path):
    """Extra fields in JSON cause TypeError, handled gracefully."""
    bad_file = tmp_path / "data.json"
    bad_file.write_text('[{"title": "X", "author": "Y", "year": 2000, "extra": true}]')
    c = BookCollection(data_file=str(bad_file))
    assert c.books == []


def test_persistence_across_instances(tmp_path):
    temp_file = str(tmp_path / "data.json")
    with open(temp_file, "w") as f:
        json.dump([], f)

    c1 = BookCollection(data_file=temp_file)
    c1.add_book("1984", "George Orwell", 1949)

    c2 = BookCollection(data_file=temp_file)
    assert len(c2.books) == 1
    assert c2.books[0].title == "1984"


def test_atomic_write_creates_no_leftover_tmp(collection):
    collection.add_book("Test", "Author", 2020)
    tmp_file = collection.data_file + ".tmp"
    assert not os.path.exists(tmp_file)


# --- list_by_year ---


def test_list_by_year_range(collection):
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.list_by_year(1940, 1970)
    assert len(results) == 2
    titles = {b.title for b in results}
    assert titles == {"1984", "Dune"}


def test_list_by_year_single_year(collection):
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.list_by_year(1949, 1949)
    assert len(results) == 1


def test_list_by_year_reversed_range(collection):
    with pytest.raises(BookValidationError):
        collection.list_by_year(2000, 1900)


def test_list_by_year_boundary_inclusive(collection):
    collection.add_book("Start", "A", 1940)
    collection.add_book("End", "B", 1970)
    collection.add_book("Outside", "C", 1971)
    results = collection.list_by_year(1940, 1970)
    assert len(results) == 2
    titles = {b.title for b in results}
    assert titles == {"Start", "End"}


# --- Partial Match Behavior ---


def test_remove_partial_title_does_not_match(collection):
    """Removing 'Dune' must NOT remove 'Dune Messiah' (exact match only)."""
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    collection.remove_book("Dune")
    assert len(collection.books) == 1
    assert collection.books[0].title == "Dune Messiah"


def test_find_by_title_partial_does_not_match(collection):
    """find_by_title('Dune') must NOT return 'Dune Messiah'."""
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    assert collection.find_by_title("Dune") is None


# --- File Permission / Storage Errors ---


def test_save_raises_storage_error_on_open_failure(tmp_path):
    """Patching builtins.open to raise OSError triggers StorageError on save."""
    from unittest.mock import patch

    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    c = BookCollection(data_file=str(temp_file))
    c.books.append(Book(title="X", author="Y", year=2000))

    with patch("tempfile.mkstemp", side_effect=OSError("disk full")):
        with pytest.raises(StorageError):
            c.save_books()


# --- Concurrent-like Access ---


def test_concurrent_like_access(tmp_path):
    """Two instances sharing a file: writes from one are visible after reload."""
    shared_file = str(tmp_path / "shared.json")
    with open(shared_file, "w") as f:
        json.dump([], f)

    c1 = BookCollection(data_file=shared_file)
    c2 = BookCollection(data_file=shared_file)

    c1.add_book("1984", "George Orwell", 1949)

    # c2 doesn't see it yet (stale in-memory)
    assert len(c2.books) == 0

    # After reload, c2 sees the change
    c2.load_books()
    assert len(c2.books) == 1
    assert c2.books[0].title == "1984"


# --- Add then Find ---


def test_add_book_then_find(collection):
    """A just-added book is immediately findable by title."""
    collection.add_book("Neuromancer", "William Gibson", 1984)
    found = collection.find_by_title("Neuromancer")
    assert found is not None
    assert found.author == "William Gibson"
    assert found.year == 1984


# --- Remove All One by One ---


def test_remove_all_books_one_by_one(collection):
    """Adding 3 books and removing them all leaves an empty collection."""
    collection.add_book("A", "Author A", 2001)
    collection.add_book("B", "Author B", 2002)
    collection.add_book("C", "Author C", 2003)
    assert len(collection.books) == 3

    collection.remove_book("A")
    collection.remove_book("B")
    collection.remove_book("C")
    assert len(collection.books) == 0
    assert collection.list_books() == []


# --- Large Collection ---


def test_large_collection(collection):
    """Adding 100 books — all should be individually findable."""
    for i in range(100):
        collection.add_book(f"Book {i}", f"Author {i}", 1900 + i)

    assert len(collection.books) == 100
    for i in range(100):
        found = collection.find_by_title(f"Book {i}")
        assert found is not None
        assert found.author == f"Author {i}"


# --- find_by_author: extended scenarios ---


def test_find_by_author_hyphenated_name(collection):
    collection.add_book("Nausea", "Jean-Paul Sartre", 1938)
    results = collection.find_by_author("Jean-Paul Sartre")
    assert len(results) == 1
    assert results[0].title == "Nausea"


def test_find_by_author_hyphenated_case_insensitive(collection):
    collection.add_book("Nausea", "Jean-Paul Sartre", 1938)
    results = collection.find_by_author("jean-paul sartre")
    assert len(results) == 1
    assert results[0].title == "Nausea"


def test_find_by_author_multiple_first_names(collection):
    collection.add_book("One Hundred Years of Solitude", "Gabriel García Márquez", 1967)
    results = collection.find_by_author("Gabriel García Márquez")
    assert len(results) == 1
    assert results[0].title == "One Hundred Years of Solitude"


def test_find_by_author_accented_characters(collection):
    collection.add_book("Love in the Time of Cholera", "García Márquez", 1985)
    results = collection.find_by_author("García Márquez")
    assert len(results) == 1
    assert results[0].title == "Love in the Time of Cholera"


def test_find_by_author_accented_case_sensitivity(collection):
    collection.add_book("Love in the Time of Cholera", "García Márquez", 1985)
    results = collection.find_by_author("garcía márquez")
    assert len(results) == 1
    assert results[0].title == "Love in the Time of Cholera"


def test_find_by_author_empty_string(collection):
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.find_by_author("")
    assert results == []


def test_find_by_author_apostrophe(collection):
    collection.add_book("The Third Policeman", "O'Brien", 1967)
    results = collection.find_by_author("O'Brien")
    assert len(results) == 1
    assert results[0].title == "The Third Policeman"


def test_find_by_author_periods(collection):
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    results = collection.find_by_author("J.R.R. Tolkien")
    assert len(results) == 1
    assert results[0].title == "The Hobbit"


def test_find_by_author_multiple_books_same_author(collection):
    collection.add_book("Book A", "Prolific Writer", 2001)
    collection.add_book("Book B", "Prolific Writer", 2002)
    collection.add_book("Book C", "Prolific Writer", 2003)
    results = collection.find_by_author("Prolific Writer")
    assert len(results) == 3
    titles = {b.title for b in results}
    assert titles == {"Book A", "Book B", "Book C"}


def test_find_by_author_whitespace_only(collection):
    collection.add_book("1984", "George Orwell", 1949)
    results = collection.find_by_author("   ")
    assert results == []
