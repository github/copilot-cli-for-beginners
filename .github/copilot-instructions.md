# Copilot Instructions

These instructions guide GitHub Copilot when working in this repository.

## Project Context

This is a **beginner-friendly educational course** teaching GitHub Copilot CLI. The repo contains Markdown chapters (00–07), Python/C#/JavaScript sample apps, and supporting assets (images, demo GIFs, glossary). It is **not** a software product — it is technical courseware.

## Build, Test, and Lint Commands

### Repository-level (course asset generation)

```bash
npm install
npm run release
```

- `npm run release` runs the demo generation pipeline (`create:tapes` → `generate:vhs` → `verify:gifs`).
- CI-friendly command:

```bash
npm run release:ci
```

### Primary sample app (Python)

```bash
cd samples/book-app-project
python book_app.py help
python -m pytest tests/
python -m pytest tests/test_books.py::test_add_book
```

### JavaScript sample app

```bash
cd samples/book-app-project-js
npm test
node --test --test-name-pattern="should add a book" tests/test_books.js
```

### C# sample app

```bash
cd samples/book-app-project-cs
dotnet run -- help
cd Tests
dotnet test
dotnet test --filter "AddBook_ShouldAddAndPersist"
```

### Linting

No dedicated lint command is currently defined in root `package.json` or sample app manifests.

## High-Level Architecture

### 1) Course content layer

- Chapters `00-quick-start` through `07-putting-it-together` are the main curriculum.
- Each chapter is a standalone `README.md` with images/GIF demos in that chapter’s `images/` folder.
- Root `README.md` is the course entrypoint and links all chapters as the learning path.

### 2) Sample application layer

- `samples/book-app-project/` (Python) is the canonical sample used throughout the course.
- Parallel implementations exist in:
  - `samples/book-app-project-js/` (Node.js)
  - `samples/book-app-project-cs/` (C#/.NET)
- In each variant, architecture is intentionally simple:
  - CLI entrypoint (`book_app.py`, `book_app.js`, `Program.cs`)
  - collection/data logic (`books.py`, `books.js`, `Services/BookCollection.cs`)
  - JSON file persistence (`data.json`)
  - tests colocated in each sample project (`tests/`, `Tests/`)

### 3) Demo automation layer

- `.github/scripts/demos.json` is the source of truth for recorded chapter demos (prompt text, chapter mapping, timing overrides).
- `npm run release` uses:
  - `.github/scripts/create-tapes.js` to generate `.tape` files
  - `.github/scripts/generate-demos.js` to render GIFs via VHS
  - `.github/scripts/verify-gifs.js` to validate generated GIF completion

### 4) Copilot customization layer

- Repository-level assistants are in `.github/agents/` and `.github/skills/`.
- Matching templates/examples are in `samples/agents/` and `samples/skills/` for teaching purposes.

## Writing Conventions

- **Audience**: Beginners with no AI/ML experience. Explain every technical term on first use.
- **Tone**: Friendly, encouraging, practical. Avoid jargon without explanation.
- **Examples**: All code blocks and `copilot` commands must be copy-paste ready. Test them mentally before including.
- **Naming**: Use kebab-case for session names, file names, and identifiers (e.g., `book-app-review`, not `book app review`).
- **Command syntax**: Standardize flag format — use `--flag=value` consistently when a value is required, `--flag` when boolean.
- **Precision**: Don't over-specify tool behavior that may vary across shells or OS. Describe what the user will see, not implementation details.
- **Fallbacks**: When referencing tool version requirements (e.g., `gh` CLI version), always include upgrade instructions or a manual alternative.

## Content Conventions (from PR review patterns)

These patterns were mined from actual PR review feedback and represent recurring maintainer expectations:

- When showing multi-step workflows, ensure all prerequisite steps are included (e.g., `git add` before `git diff --staged`).
- When introducing a concept with an example, use consistent naming throughout the section — don't mix kebab-case and quoted names.
- When describing a command's behavior, match the level of specificity in the official release notes — don't state behavior that may differ across environments.
- If a feature requires a minimum tool version, mention the version AND provide a fallback path for users who can't upgrade yet.

## Sample Code Conventions

- **Primary sample**: Always use `samples/book-app-project/` (Python) for examples in chapters.
- **Test framework**: pytest — test files go in `samples/book-app-project/tests/` and follow `test_*.py` naming.
- **Python version**: 3.10+ (per `samples/book-app-project/pyproject.toml`).
- **Intentional bugs**: Files in `samples/book-app-buggy/` and `samples/buggy-code/` contain **deliberate bugs** for exercises. Never fix them.

## Chapter Structure

Every chapter (00–07) follows the same pattern in its `README.md`:

1. Real-World Analogy
2. Core Concepts
3. Hands-On Examples
4. Assignment
5. What's Next

Do not deviate from this structure when editing or adding chapter content.

## Markdown Formatting

- Use standard GitHub-Flavored Markdown.
- Images go in the repo-root `images/` directory.
- Use relative links for cross-chapter references (e.g., `../03-development-workflows/README.md`).
- Emoji usage is encouraged for section headers (matching existing style).

## Key Repository Conventions

- Treat this as **courseware first**: edits should preserve teaching intent, not just code correctness.
- Prefer `samples/book-app-project/` (Python) in chapter examples unless a chapter explicitly compares languages.
- For `samples/book-app-buggy/` and `samples/buggy-code/`, default to **debugging explanations** (root cause + proposed patch). Only edit those files when the user explicitly asks to apply the fix in-file.
- Keep chapter structure consistent: Real-World Analogy → Core Concepts → Hands-On Examples → Assignment → What’s Next.
- Use kebab-case consistently for session names, filenames, and identifiers shown to learners.
- Use `--flag=value` style when a command flag requires a value.
- If a change affects cross-file course consistency, update linked surfaces from the maintenance matrix below.
- Keep glossary additions in `GLOSSARY.md` alphabetized when introducing new terms.

## Session-History Guardrails

- For direct implementation requests (e.g., “add/fix/refactor X”), **implement immediately**. Do not block on “say start” or planning-only loops unless the user explicitly asks for planning first.
- When behavior changes in `samples/book-app-project/`, update or add pytest coverage in `samples/book-app-project/tests/test_*.py` within the same task.
- If the user repeats the same prompt verbatim, treat it as a recovery signal: avoid re-sending near-identical output, acknowledge the miss briefly, and respond with a different, more actionable format.

## Maintenance Matrix

| Change Made | Files to Update |
|---|---|
| New chapter added | `README.md` (course table), `AGENTS.md` (structure table), `images/learning-path.png` |
| Chapter content updated | The chapter's `README.md`, verify cross-references in adjacent chapters |
| New sample app variant added | `AGENTS.md` (structure table), `samples/` directory, relevant chapter references |
| Sample app code changed | `samples/book-app-project/tests/` (update/add tests), chapters referencing that code |
| Bug intentionally added to buggy samples | `samples/book-app-buggy/` or `samples/buggy-code/` only — do NOT update tests |
| New skill added | `.github/skills/{skill-name}/SKILL.md`, `samples/skills/` (example copy), Chapter 05 |
| New agent template added | `samples/agents/`, Chapter 04 |
| New MCP config added | `samples/mcp-configs/`, Chapter 06 |
| Glossary term introduced | `GLOSSARY.md` — add definition in alphabetical order |
| npm scripts changed | `package.json`, `AGENTS.md` (build section) |
| Devcontainer updated | `.devcontainer/devcontainer.json`, Chapter 00 (setup instructions) |
| Image or banner changed | `images/` directory, any README referencing the image |
| Copilot CLI version requirements change | Chapter 00, Chapter 01, `.devcontainer/devcontainer.json` |
