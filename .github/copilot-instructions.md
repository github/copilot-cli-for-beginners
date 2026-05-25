# Copilot Instructions

These instructions guide GitHub Copilot when working in this repository.

## Project Context

This is a **beginner-friendly educational course** teaching GitHub Copilot CLI. The repo contains Markdown chapters (00–07), Python/C#/JavaScript sample apps, and supporting assets (images, demo GIFs, glossary). It is **not** a software product — it is technical courseware.

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
