# Book Collection App

A Python CLI app for managing your book collection.
Add, remove, search, and track books you've read.

---

## Features

* Store books in a JSON file with title, author, year, and read status
* Input validation on all user-facing commands
* Search by author or year range
* Mark books as read

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Unit tests for BookCollection
* `test_book_app.py` - Unit tests for CLI handlers

---

## Running the App

```bash
python book_app.py list
python book_app.py add
python book_app.py remove
python book_app.py find
python book_app.py find-title
python book_app.py mark-read
python book_app.py search-year
python book_app.py help
```

## Running Tests

```bash
python -m pytest
```

---

## Notes

* This is a teaching sample for the GitHub Copilot CLI course
* Intentionally kept simple for learning purposes
