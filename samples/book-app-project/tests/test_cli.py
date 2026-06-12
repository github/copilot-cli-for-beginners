import sys
import importlib
import books
import book_app


def test_mark_cli_noninteractive(tmp_path, monkeypatch, capsys):
    # Use a temporary data file
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    # Reload book_app so its global collection picks up the patched DATA_FILE
    importlib.reload(book_app)

    # Add a book and mark it via CLI
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)

    monkeypatch.setattr(sys, "argv", ["book_app.py", "mark", "Dune"])
    book_app.main()
    captured = capsys.readouterr()
    assert 'Marked "Dune" as read' in captured.out


def test_mark_cli_interactive(tmp_path, monkeypatch, capsys):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    importlib.reload(book_app)
    book_app.collection.add_book("1984", "George Orwell", 1949)

    # Simulate interactive input of the title
    monkeypatch.setattr(sys, "argv", ["book_app.py", "mark"])
    monkeypatch.setattr('builtins.input', lambda prompt='': '1984')

    book_app.main()
    captured = capsys.readouterr()
    assert 'Marked "1984" as read' in captured.out
