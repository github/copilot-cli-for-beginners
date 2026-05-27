# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests

---

## Running the App

Available commands (run from samples/book-app-project/):

```bash
python book_app.py list       # Show all books
python book_app.py add        # Interactive add
python book_app.py find       # Find books by author (exact match)
python book_app.py remove     # Remove a book by title
python book_app.py search     # Interactive search prompt
python book_app.py search "dune" title    # Search titles containing "dune"
python book_app.py search "gibson" author # Search authors containing "gibson"
python book_app.py help
```

## Running Tests

Run the full test suite for the sample:

```bash
python -m pytest samples/book-app-project -q
```

Run a single test by node (example):

```bash
python -m pytest samples/book-app-project/tests/test_books.py::test_search_by_title_exact -q
```


---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
