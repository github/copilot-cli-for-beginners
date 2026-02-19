# Book App - Buggy Version

This directory contains an intentionally buggy version of the book collection app for debugging exercises in Chapter 03.

**Do NOT fix these bugs directly.** They exist so learners can practice using GitHub Copilot CLI to identify and debug issues.

---

## Intentional Bugs

### books_buggy.py

| # | Bug | Symptom |
|---|-----|---------|
| 1 | `find_book_by_title()` uses exact case match | Searching for "the hobbit" returns nothing even though "The Hobbit" exists |
| 2 | `save_books()` doesn't use context manager | File handle leak; no error handling for permission issues |
| 3 | `add_book()` has no year validation | Accepts negative years, year 0, and years far in the future |
| 4 | `remove_book()` uses `in` substring check | Removing "Dune" also matches and removes "Dune Messiah" |
| 5 | `mark_as_read()` marks ALL books as read | Loop variable bug - iterates all books instead of just the match |
| 6 | `find_by_author()` requires exact match | "Tolkien" won't find "J.R.R. Tolkien" (no partial matching) |

### book_app_buggy.py

| # | Bug | Symptom |
|---|-----|---------|
| 7 | `show_books()` numbering starts at 0 | Books display as "0. ...", "1. ..." instead of "1. ...", "2. ..." |
| 8 | `handle_add()` accepts empty title/author | Can add books with blank titles and authors |
| 9 | `handle_remove()` always prints success | Says "Book removed" even when the book wasn't found |

---

## How to Use in Chapter 03

```bash
copilot

> @samples/book-app-buggy/books_buggy.py Users report that searching for
> "The Hobbit" returns no results even though it's in the data. Debug why.

> @samples/book-app-buggy/book_app_buggy.py When I remove a book that
> doesn't exist, the app says it was removed. Help me find why.
```
