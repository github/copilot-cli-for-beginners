# Glossary

Quick reference for technical terms used throughout this course. Don't worry about memorizing these now - refer back as needed.

---

## A

### Agent

A specialized AI personality with domain expertise (e.g., frontend, security). Defined in `.agent.md` files with YAML frontmatter containing at minimum a `description` field.

### API

Application Programming Interface. A way for programs to communicate with each other.

---

## C

### CI/CD

Continuous Integration/Continuous Deployment. Automated testing and deployment pipelines.

### CLI

Command Line Interface. A text-based way to interact with software (like this tool!).

### Context Window

The amount of text an AI can consider at once. Like a desk that can only hold so much. When you add files, conversation history, and system prompts, they all take up space in this window.

### Context Manager

A Python construct using the `with` statement that automatically handles setup and cleanup (like opening and closing files). Example: `with open("file.txt") as f:` ensures the file is closed even if an error occurs.

### Conventional Commit

A commit message format that follows a standardized structure: `type(scope): description`. Common types include `feat` (new feature), `fix` (bug fix), `docs` (documentation), `refactor`, and `test`. Example: `feat(auth): add password reset flow`.

### Dataclass

A Python decorator (`@dataclass`) that automatically generates `__init__`, `__repr__`, and other methods for classes that primarily store data. Used in the book app to define the `Book` class with fields like `title`, `author`, `year`, and `read`.

---

## F

### Frontmatter

Metadata at the top of a Markdown file enclosed in `---` delimiters. Used in agent and skill files to define properties like `description` and `name` in YAML format.

---

## G

### Glob Pattern

A pattern using wildcards to match file paths (e.g., `*.js` matches all JavaScript files).

---

## J

### JWT

JSON Web Token. A secure way to transmit authentication information between systems.

---

## M

### MCP

Model Context Protocol. A standard for connecting AI assistants to external data sources.

---

## N

### npx

A Node.js tool that runs npm packages without installing them globally. Used in MCP server configurations to launch servers (e.g., `npx @modelcontextprotocol/server-filesystem`).

---

## O

### OWASP

Open Web Application Security Project. An organization that publishes security best practices and maintains the "OWASP Top 10" list of most critical web application security risks.

---

## P

### PEP 8

Python Enhancement Proposal 8. The official style guide for Python code, covering naming conventions (snake_case for functions, PascalCase for classes), indentation (4 spaces), and code layout. Following PEP 8 makes Python code consistent and readable.

### Pre-commit Hook

A script that runs automatically before each `git commit`. Can be used to run Copilot security reviews or code quality checks before code is committed.

### pytest

A popular Python testing framework known for its simple syntax, powerful fixtures, and rich plugin ecosystem. Used throughout this course for testing the book app. Tests are run with `python -m pytest tests/`.

### Programmatic Mode

Running Copilot with `-p` flag for single commands without interaction.

---

## R

### Rate Limiting

Restrictions on how many requests you can make to an API within a time period. Copilot may temporarily limit responses if you exceed your plan's usage quota.

---

## S

### Session

A conversation with Copilot that maintains context and can be resumed later.

### Skill

A folder with instructions that Copilot automatically loads when relevant to your prompt. Defined in `SKILL.md` files with YAML frontmatter.

### Slash Command

Commands starting with `/` that control Copilot (e.g., `/help`, `/clear`, `/model`).

---

## T

### Token

A unit of text that AI models process. Roughly 4 characters or 0.75 words. Used to measure both input (your prompts and context) and output (AI responses).

### Type Hints

Python annotations that indicate the expected types of function parameters and return values (e.g., `def add_book(title: str, year: int) -> Book:`). They don't enforce types at runtime but help with code clarity, IDE support, and static analysis tools like mypy.

---

## W

### WCAG

Web Content Accessibility Guidelines. Standards published by W3C for making web content accessible to people with disabilities. WCAG 2.1 AA is a common compliance target.

---

## Y

### YAML

YAML Ain't Markup Language. A human-readable data format used for configuration. In this course, YAML appears in agent and skill frontmatter (the `---` delimited block at the top of `.agent.md` and `SKILL.md` files).
