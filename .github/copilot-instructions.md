# Copilot Instructions (project-specific)

Purpose
- Short guide for GitHub Copilot CLI sessions working on this repository (courseware, not a production product).

Build, test, and lint commands
- Python (primary sample: samples/book-app-project):
  - Run all tests: python -m pytest samples/book-app-project -q
  - Run a single test: python -m pytest samples/book-app-project/tests/test_books.py::test_name -q
  - Install deps: follow pyproject.toml (e.g., `poetry install`), or `python -m pip install -r samples/book-app-project/requirements.txt` if present
  - Lint (if available): python -m flake8 samples/book-app-project

- JavaScript (samples/book-app-project-js):
  - Install & test: cd samples/book-app-project-js && npm install && npm test
  - Run a single test (Jest): npm test -- -t "test name"  (or use npx jest <path>)
  - Lint: npm run lint (if script exists)

- C# (samples/book-app-project-cs):
  - Run tests: dotnet test samples/book-app-project-cs
  - Run a single test: dotnet test samples/book-app-project-cs --filter "FullyQualifiedName~TestName"

High-level architecture
- Course chapters live in top-level folders 00-07; each chapter is self-contained with a README following the same structure.
- Primary sample: samples/book-app-project (Python). JS and C# variants exist under samples/book-app-project-js and samples/book-app-project-cs.
- Agents and skills:
  - .github/agents and .github/skills store agent & skill templates used by course demos
  - samples/agents and samples/skills contain example implementations
- CI / automation: .github/workflows and .github/scripts contain helper scripts for building demo assets and translations.
- MCP examples: samples/mcp-configs/ and chapter 06 contain MCP server configs and docs.

Key conventions (repo-specific)
- Primary-sample-first: Use samples/book-app-project for Python-centric examples in chapters.
- Test file naming: pytest tests are under samples/book-app-project/tests/ and use test_*.py naming.
- Python version: 3.10+ (see samples/book-app-project/pyproject.toml).
- Intentional-bugs: Do NOT fix files in samples/book-app-buggy/ or samples/buggy-code/ — they are exercises.
- Chapter README format: Every chapter README must include: Real-World Analogy; Core Concepts; Hands-On Examples; Assignment; What's Next.
- Filenames & identifiers: prefer kebab-case for session names and examples used in text and commands.
- Command flag style: use `--flag=value` when a value is required and `--flag` for booleans in examples.
- Docs-first edits: When changing sample behavior, update corresponding chapter README and tests.

Files & places to check for AI sessions
- Primary sample code: samples/book-app-project/
- Tests: samples/book-app-project/tests/
- Agent templates: .github/agents/ and samples/agents/
- Skill templates: .github/skills/ and samples/skills/
- MCP server examples: samples/mcp-configs/ and 06-mcp-servers/

MCP servers
- This repo includes MCP examples (samples/mcp-configs/) and a chapter (06-mcp-servers). Would you like assistance configuring an MCP server for local testing? (Ask to configure: Playwright or other demo servers.)

Summary
- This file adds actionable build/test/lint commands, a concise architecture overview, and repo-specific conventions to help future Copilot sessions behave usefully and avoid common mistakes.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
