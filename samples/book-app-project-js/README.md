# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A JavaScript app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.js` - Main CLI entry point
* `books.js` - BookCollection class with data logic
* `utils.js` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.js` - Starter tests using Node's built-in test runner

---

## Running the App

```bash
node book_app.js list
node book_app.js add
node book_app.js find
node book_app.js remove
node book_app.js help
```

## Running Tests

```bash
npm test
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
