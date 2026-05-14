# System Overview

## Repository Purpose

This is the **GitHub Copilot CLI for Beginners** — an educational course teaching AI-assisted development workflows. The repo contains:
- Chapters 00–07 (Markdown lessons with hands-on exercises)
- Sample applications: Python (primary), C#, and JavaScript versions of a book collection CLI
- Supporting assets: images, skills, agent templates, MCP configs

**Primary Languages:** Python (exercise focus), C#, JavaScript, Markdown

## Entry Points

| Language | Entry Point | Purpose |
|----------|------------|---------|
| **Python** | `samples/book-app-project/book_app.py` | CLI: add/list/mark-as-read books |
| **C#** | `samples/book-app-project-cs/Program.cs` | CLI equivalent in C# |
| **JavaScript** | `samples/book-app-project-js/book_app.js` | CLI equivalent in JavaScript |

All three versions manage a book collection stored in `data.json`.

## Architecture

**Python Book App Structure:**
```
samples/book-app-project/
├── book_app.py       # Main CLI handler (menu, user I/O)
├── books.py          # BookCollection class + persistence (data.json)
├── utils.py          # UI helpers (print_menu, get_user_choice, format output)
├── data.json         # Persistent storage (book list)
└── tests/
    └── test_books.py # Unit tests for BookCollection
```

**Key Components:**
- `BookCollection` — in-memory list with JSON persistence
- `Book` — dataclass representing a single book
- CLI handlers — user input/output management

## Test Approach

**Framework:** pytest (Python 3.10+)

**Test Coverage:**
- `samples/book-app-project/tests/test_books.py` — unit tests for `BookCollection`
- Uses monkeypatch fixture to isolate tests with temp data files
- Covers: add, list, find, mark-as-read, invalid operations

**Command to run tests:**
```bash
cd samples/book-app-project
pytest tests/ -v
```

## Dependencies

**Python (see `pyproject.toml`):**
- `Python >= 3.10`
- `pytest` (dev/test)

**C# & JavaScript:** Refer to respective package managers and project files.

## Low-Risk Module Selection (Exercise 1)

**Recommended: `samples/book-app-project/utils.py`**

| Module | Risk | Reasoning |
|--------|------|-----------|
| **utils.py** | **Low** | Isolated UI helpers; no state; easy to test; changes don't cascade |
| books.py | Medium | Core data model; tested but has broader impact |
| appendices/additional-context.md | Low | Documentation only; safe but not code-oriented |

**Why utils.py:** Functions like `print_menu()`, `get_user_choice()`, `get_book_details()`, and `print_books()` are perfect for practicing small, safe improvements (validation, error handling, formatting) without risking the core app logic.

## References
- See `build-test.md` for exact build and test commands
- See `architecture.mmd` for system diagram
