import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import importlib
import books


def test_mark_command_interactive(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    # Reload book_app after DATA_FILE is patched so it uses the temp file
    import book_app
    importlib.reload(book_app)

    # Add a book and mark it via interactive prompt
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr('builtins.input', lambda prompt='': "Dune")
    monkeypatch.setattr(sys, 'argv', ['book_app.py', 'mark'])
    book_app.main()

    book = book_app.collection.find_book_by_title("Dune")
    assert book.read is True


def test_mark_command_with_arg(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    import book_app
    importlib.reload(book_app)

    book_app.collection.add_book("1984", "George Orwell", 1949)
    monkeypatch.setattr(sys, 'argv', ['book_app.py', 'mark', '1984'])
    book_app.main()

    book = book_app.collection.find_book_by_title("1984")
    assert book.read is True
