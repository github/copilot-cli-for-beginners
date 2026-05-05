# System Overview

## Repo
**github/copilot-cli-for-beginners** — A structured course teaching GitHub Copilot CLI usage through a single Python book-collection app that evolves across chapters.

## Languages & Runtimes
- **Python** (primary) — `samples/book-app-project/`
- **C#** — `samples/book-app-project-cs/`
- **JavaScript** — `samples/book-app-project-js/`
- **Markdown** — course content in `00-quick-start/` through `07-putting-it-together/`

## Entry Points
| App | File |
|-----|------|
| Python book app | `samples/book-app-project/book_app.py` |
| Python books module | `samples/book-app-project/books.py` |
| Python utils | `samples/book-app-project/utils.py` |

## Test Approach
- **Framework:** pytest
- **Test files:** `samples/book-app-project/tests/test_books.py`
- **Config:** `samples/book-app-project/pyproject.toml`

## Key Paths
| Path | Purpose |
|------|---------|
| `samples/book-app-project/` | Primary Python sample app (used for most exercises) |
| `samples/book-app-buggy/` | Intentionally broken version for debugging exercises |
| `00-quick-start/` → `07-putting-it-together/` | Course chapter content |
| `AGENTS.md` | Copilot agent customization instructions |
| `.github/` | CI workflows |

## Chosen Low-Risk Module
> _To be filled in during Ex 1 — Repo Orientation_

**Module:** TBD  
**Justification:** TBD
