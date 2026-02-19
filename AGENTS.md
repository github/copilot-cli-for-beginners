# AGENTS.md

Beginner-friendly course teaching GitHub Copilot CLI. Educational content, not software.

## Structure

| Path | Purpose |
|------|---------|
| `00-07/` | Chapters: analogy → concepts → hands-on → assignment → next |
| `samples/book-app-project/` | **Primary sample**: Python CLI book collection app used throughout all chapters |
| `samples/book-app-project-cs/` | C# version of the book collection app |
| `samples/book-app-project-js/` | JavaScript version of the book collection app |
| `samples/book-app-buggy/` | **Intentional bugs** for debugging exercises (Ch 03) |
| `samples/agents/` | Agent template examples (python-reviewer, pytest-helper, hello-world) |
| `samples/skills/` | Skill template examples (code-checklist, pytest-gen, commit-message, hello-world) |
| `samples/mcp-configs/` | MCP server configuration examples |
| `samples/buggy-code/` | **Optional extra**: Security-focused buggy code (JS and Python) |
| `samples/src/` | **Optional extra**: Legacy JS/React samples from earlier course version |
| `appendices/` | Supplementary reference material |

## Do

- Keep explanations beginner-friendly; explain AI/ML jargon when used
- Ensure bash examples are copy-paste ready
- Tone: friendly, encouraging, practical
- Use `samples/book-app-project/` paths in all primary examples
- Use Python/pytest context for code examples

## Don't

- Fix bugs in `samples/book-app-buggy/` or `samples/buggy-code/` — they're intentional
- Add chapters without updating README.md course table
- Assume readers know AI/ML terminology

## Build

```bash
npm install && npm run release
```
