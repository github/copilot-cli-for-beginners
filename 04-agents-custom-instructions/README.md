![Chapter 04: Agents and Custom Instructions](images/chapter-header.png)

> **What if you could hire a Python code reviewer, testing expert, and security reviewer... all in one tool?**

In Chapter 03, you mastered the essential workflows: code review, refactoring, debugging, test generation, and git integration. Those skills make you highly productive with GitHub Copilot CLI. Now, let's take it further.

In this chapter, you'll transform Copilot from a generalist into a team of specialists. You'll create agents with deep domain expertise: a Python code reviewer who automatically adds type hints and follows PEP 8, a testing specialist who knows pytest best practices, and more. You'll see how the same prompt produces dramatically better results when a specialist handles it, and learn to orchestrate multiple agents collaborating on a single feature.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Use built-in agents: Plan (`/plan`), Code-review (`/review`), and understand automatic agents (Explore, Task)
- Create specialized agents using agent files (`.agent.md`)
- Use agents for domain-specific tasks
- Delegate work across multiple agents
- Write custom instruction files for project-specific standards

> ⏱️ **Estimated Time**: ~60 minutes (25 min reading + 35 min hands-on)

---

## 🚀 Start Here: Your First 5 Minutes with Agents

**New to agents?** Here's the quickest path to understanding them:

1. **Try a built-in agent right now:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   This invokes the Plan agent to create a step-by-step implementation plan.

2. **Understand the core concept:** Agents are like hiring a specialist instead of asking a generalist. A "frontend agent" automatically thinks about accessibility and component patterns - you don't have to remind it.

3. **Two ways to use custom agents:**
   - **`/agent`** - Select an agent interactively *inside* a session
   - **`copilot --agent frontend`** - Start a session *with* a specific agent

Once you've tried the built-in agents, read on to create your own custom agents.

> 📦 **Don't want to write agents from scratch?** Copy ready-to-use templates from the [samples/agents](../samples/agents/) folder. Just copy the files to `~/.copilot/agents/` and customize them for your needs.

---

## Real-World Analogy: Hiring Specialists

When you need help with your house, you don't call one "general helper." You call specialists:

| Problem | Specialist | Why |
|---------|------------|-----|
| Leaky pipe | Plumber | Knows plumbing codes, has specialized tools |
| Rewiring | Electrician | Understands safety requirements, up to code |
| New roof | Roofer | Knows materials, local weather considerations |

Agents work the same way. Instead of a generic AI, you get specialists who understand specific domains deeply.

<img src="images/hiring-specialists-analogy.png" alt="Specialized Agents for Every Domain" width="800"/>

*Direct specialists, don't do everything yourself: Frontend, Backend, Security, and Testing experts at your command*

---

## Built-in Agents

GitHub Copilot CLI includes four built-in agents:

| Agent | How to Invoke | What It Does |
|-------|---------------|--------------|
| **Plan** | `/plan` or `Shift+Tab` | Creates step-by-step implementation plans before coding |
| **Code-review** | `/review` | Reviews staged/unstaged changes with focused, actionable feedback |
| **Explore** | *Automatic* | Used internally when you ask Copilot to explore or analyze the codebase |
| **Task** | *Automatic* | Executes commands like tests, builds, lints, and dependency installs |

### Using Built-in Agents

```bash
copilot

# Invoke the Plan agent to create an implementation plan
> /plan Add input validation for book year in the book app

# Invoke the Code-review agent on your changes
> /review

# Explore and Task agents are invoked automatically when relevant:
> Run the test suite        # Uses Task agent
> Explore how book data is loaded    # Uses Explore agent
```

**Key insight**: You directly invoke Plan and Code-review with slash commands. Explore and Task work behind the scenes. Copilot uses them automatically when appropriate.

### Understanding the Task Agent

The Task agent deserves special attention because of its smart output handling:

| Outcome | What You See |
|---------|--------------|
| ✅ **Success** | Brief summary (e.g., "All 247 tests passed", "Build succeeded") |
| ❌ **Failure** | Full output with stack traces, compiler errors, and detailed logs |

**Why this design?** It keeps your conversation context clean. You don't need 500 lines of passing test output - you just need to know it worked. But when something breaks, you get all the details needed to debug.

**Example prompts that use the Task agent:**
```bash
> Run the tests
> Build the project
> Install the dependencies
> Run the linter on src/
```

The Task agent uses a faster model since it's focused on command execution rather than complex reasoning.

> 📚 **Official Documentation**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Part 2: Creating Custom Agents

> 💡 **This section is optional.** The built-in agents (`/plan`, `/review`) are powerful enough for most workflows. Create custom agents when you need specialized expertise that's consistently applied across your work.

---

## Creating Your First Agent

Agents can be defined in several locations. Choose based on your use case:

| Location | Scope | Best For |
|----------|-------|----------|
| `~/.copilot/agents/` | Global (all projects) | Personal productivity agents you use everywhere |
| `.github/agents/` | Project-specific | Team-shared agents with project conventions |
| `*.agent.md` files | Single-file | Quick experiments, VS Code compatibility |

### Which Location Should I Use?

```
Are you just experimenting?
    └─ YES → Create `my-agent.agent.md` in your current folder
    └─ NO ↓

Will your team use this agent?
    └─ YES → Create in `.github/agents/` (gets version controlled)
    └─ NO ↓

Do you want this agent everywhere?
    └─ YES → Create in `~/.copilot/agents/` (your personal agents)
```

**Start simple:** Create a single `*.agent.md` file in your project folder. Move it to a permanent location once you're happy with it.

### Agent File Structure

Let's start with a **minimal agent** to understand the format.

> 💡 **New to YAML frontmatter?** Agent files use a format common in many tools: a small block of configuration data (called "frontmatter") at the top of the file, surrounded by `---` markers. This uses YAML syntax, which is just a simple way to write settings as `key: value` pairs. The rest of the file is regular markdown with your instructions.

Create `my-reviewer.agent.md` in your project folder:

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

That's it! The YAML frontmatter (between `---` markers) provides metadata, and the markdown below is your agent's instructions.

> 💡 **Required vs Optional**: The `description` field is required. Other fields like `name`, `tools`, and `model` are optional.

### A More Complete Example

Once you're comfortable, here's a more comprehensive agent. Create `~/.copilot/agents/python-reviewer.agent.md`:

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### Agent YAML Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | No | Display name (defaults to filename) |
| `description` | **Yes** | What the agent does - helps Copilot understand when to suggest it |
| `tools` | No | List of allowed tools (omit = all tools available). See tool aliases below. |
| `target` | No | Limit to `vscode` or `github-copilot` only |

**Tool Aliases**: Use these names in the `tools` list:
- `read` - Read file contents
- `edit` - Edit files
- `search` - Search files (grep/glob)
- `execute` - Run shell commands (also: `shell`, `Bash`)
- `agent` - Invoke other custom agents

> 📖 **Official docs**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Code Only**: The `model` property (for selecting AI models) works in VS Code but is not supported in GitHub Copilot CLI. You can safely include it for cross-platform agent files. GitHub Copilot CLI will ignore it.

### Using the Agent

Select an agent interactively or via command line:

```bash
# Select from available agents interactively
copilot
> /agent

# Start with a specific agent
copilot --agent python-reviewer

# The python-reviewer agent knows to:
# - Add type hints to all functions
# - Follow PEP 8 naming conventions
# - Use proper error handling patterns
# - Validate input data
```

---

## Multiple Agent Files

Create separate agent files for different specialties. Here are examples for a complete team:

> 💡 **Note for beginners**: The examples below are templates. **Replace the specific technologies with whatever your project uses.** The important thing is the *structure* of the agent, not the specific technologies mentioned.

**`~/.copilot/agents/python-reviewer.agent.md`**:

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Code standards:**
- Use Python 3.10+ features (dataclasses, type hints)
- Follow PEP 8 naming conventions
- Proper error handling (no bare except)
- Use context managers for file I/O

**Always check for:**
- Missing type hints on function signatures
- Mutable default arguments
- Input validation completeness
```

**`~/.copilot/agents/pytest-helper.agent.md`**:

```markdown
---
name: pytest-helper
description: Testing specialist for Python projects using pytest
tools: ["read", "edit", "search", "execute"]
---

# Pytest Testing Specialist

You are a testing expert focused on pytest best practices.

**Testing philosophy:**
- Test behavior, not implementation
- Use descriptive test names: test_<what>_<condition>_<expected>
- Use fixtures for shared setup
- Always test: happy path, edge cases, error cases

**Code standards:**
- Use pytest fixtures instead of setup/teardown
- Parametrize tests for multiple scenarios
- Use clear assertion messages
- Mock external dependencies properly
```

**`~/.copilot/agents/hello-world.agent.md`**:

```markdown
---
name: hello-world
description: Minimal example agent for learning
---

# Hello World Agent

You are a friendly assistant who always says hello.

**Your behavior:**
- Start responses with a greeting
- Keep explanations simple
```

---

## Generic vs Specialist: See the Difference

This is where agents prove their value. Watch the difference:

### Without an Agent (Generic Copilot)

```bash
copilot

> Add a function to search books by year range in the book app
```

**Generic output**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

Basic. Works. But missing a lot.

---

### With the Python Reviewer Agent

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
```

**Specialist output**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**What the python-reviewer agent automatically includes**:
- ✅ Type hints on all parameters and return values
- ✅ Comprehensive docstring with Args/Returns/Raises
- ✅ Input validation with proper error handling
- ✅ List comprehension for better performance
- ✅ Edge case handling (missing/invalid year values)
- ✅ PEP 8 compliant formatting
- ✅ Defensive programming practices

**The difference**: Same prompt, dramatically better output. The agent brings expertise you'd forget to ask for.

---

## Multi-Agent Collaboration

The real power comes when specialists work together on a feature.

### Example: Building a Simple Feature

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Use python-reviewer for design
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Switch to pytest-helper for test design
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Synthesize both designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**The key insight**: You're the architect directing specialists. They handle the details, you handle the vision.

---

## Using Agents in Practice

### Single Agent Tasks

```bash
# Start Copilot with the python-reviewer agent
copilot --agent python-reviewer

> Create a function to filter books by genre in the book app.
> It should:
> - Accept a list of books and a genre
> - Return matching books
> - Handle case-insensitive searches
> - Validate inputs

# The python-reviewer agent applies all its specialized standards
```

<details>
<summary>🎬 See it in action!</summary>

![Python Reviewer Demo](images/python-reviewer-demo.gif)

</details>

### Switching Agents Mid-Session

```bash
copilot

> I need to add a "favorites" feature to the book app where users can mark books as favorites.

# Switch to python-reviewer agent for implementation design
> /agent
# Select "python-reviewer" from the list
> Design the methods needed for managing favorite books

# Switch to pytest-helper agent for testing
> /agent
# Select "pytest-helper"
> Design comprehensive tests for the favorites feature
```

### Agent as Tools

When agents are configured, Copilot can also call them as tools during complex tasks. If you ask for a full-stack feature, Copilot may automatically delegate parts to the appropriate specialist agents.

---

## Agent Naming Best Practices

Good agent names are short, descriptive, and indicate the specialty:

| ✅ Good Names | ❌ Avoid |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**Naming conventions:**
- Use lowercase with hyphens: `my-agent-name.agent.md`
- Include the domain: `frontend`, `backend`, `devops`, `security`
- Be specific when needed: `react-typescript` vs just `frontend`

---

## Project-Level Instructions

So far, you've learned how to create **agents** - specialized AI personalities you invoke with `/agent`. Now let's look at a related concept: **custom instructions** that apply automatically to every Copilot session in a project, without needing to invoke them. Think of agents as specialists you call on, and custom instructions as team standards that are always active.

### Instruction File Formats

Copilot supports multiple instruction file formats for cross-platform compatibility:

| File | Scope | Notes |
|------|-------|-------|
| `AGENTS.md` | Project root or nested | **Cross-platform standard** - works with Copilot and other AI assistants |
| `.github/copilot-instructions.md` | Project | GitHub Copilot specific |
| `.github/instructions/*.instructions.md` | Project | Granular, topic-specific instructions |
| `*.agent.md` | Anywhere | Individual agent definitions |
| `CLAUDE.md`, `GEMINI.md` | Project root | Supported for compatibility |

> 🎯 **Just getting started?** Use `*.agent.md` files for agents and `AGENTS.md` for project instructions. You can explore the other formats later as needed.

> 💡 **Cross-Platform Tip**: If you want your instructions to work across multiple AI coding tools, use `AGENTS.md`. It's an [open standard](https://agents.md/) supported by GitHub Copilot and many others.

### Quick Setup with /init

Use `/init` to create instructions for your repository:

```bash
copilot
> /init
```

This generates configuration files that customize Copilot's behavior for your project.

### AGENTS.md File (Recommended)

Create an `AGENTS.md` file in your repository root. This is the recommended approach because it works across multiple AI coding tools:

```markdown
# Project Instructions

## Project Context
This is a Python CLI book management application.

## Code Style
- Use Python 3.10+ features (dataclasses, type hints)
- Follow PEP 8 naming conventions
- Use pytest for all testing
- Handle all file I/O with context managers

## Security Requirements
- Validate all user input
- Use proper exception handling
- Never expose sensitive file paths in error messages

## Testing Standards
- Minimum 80% coverage for new code
- Use pytest fixtures for shared setup
- Test happy path, edge cases, and error conditions
```

### Custom Instruction Files (.instructions.md)

For more granular control, create instruction files in `.github/instructions/`:

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

**Example: `.github/instructions/python-standards.instructions.md`**

> 💡 **Note**: Instruction files work with any language. This example uses Python to match our course project, but you can create similar files for TypeScript, Go, Rust, or any technology your team uses.

```markdown
# Python Standards

Apply these standards to all Python files in this project.

## Type Safety
- Add type hints to all function signatures
- Use `Optional[T]` for parameters that can be None
- Use `typing` module for complex types (List, Dict, Tuple)
- Prefer dataclasses for structured data

## Naming Conventions
- snake_case for functions, methods, and variables
- PascalCase for classes
- SCREAMING_SNAKE_CASE for constants
- Prefix private methods with underscore

## Error Handling
- Use specific exception types (ValueError, TypeError, etc.)
- Never use bare `except:` clauses
- Include descriptive error messages
- Use context managers for resource cleanup

## Code Quality
- Follow PEP 8 style guidelines
- Keep functions under 50 lines
- Use list comprehensions where readable
- Add docstrings with Args/Returns/Raises sections
```

**Finding community instruction files**: Browse [github/awesome-copilot](https://github.com/github/awesome-copilot) for pre-made instruction files covering .NET, Angular, Azure, Python, Docker, and many more technologies.

### Disabling Custom Instructions

If you want Copilot to ignore project-specific configurations:

```bash
copilot --no-custom-instructions
```

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **Agent Comparison Challenge**: Ask for the same thing with and without an agent:
   ```bash
   # Without agent
   copilot
   > Add a function to find books by author in the book app

   # With python-reviewer agent
   copilot
   > /agent
   # Select "python-reviewer" from the list
   > Add a function to find books by author in the book app
   ```
   Compare the outputs. What did the agent add that generic Copilot missed?

2. **Multi-Agent Challenge**: Design a "book rating" feature using python-reviewer agent for implementation, pytest-helper agent for testing. Can you synthesize them into one implementation plan?

3. **Create Your Own Agent**: Create a simple agent file at `~/.copilot/agents/my-agent.agent.md` with just 5 lines of instructions. Test it with `/agent` and select "my-agent".

**Self-Check**: You understand agents when you can explain why having a "security agent" review code is better than just asking "check for security issues."

---

## Hands-On Examples

### Example 1: Create Your Own Agent

```bash

# Create the agents directory
mkdir -p ~/.copilot/agents

# Create a code reviewer agent
cat > ~/.copilot/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# Create a documentation agent
cat > ~/.copilot/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Now use them
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# Or switch agents
copilot
> /agent
# Select "documentor"
> Document @samples/book-app-project/books.py
```

### Example 2: Agent-Driven Feature Development

```bash

# Start with python-reviewer expertise
copilot --agent python-reviewer

> I need to add a book rating system. Users can rate books from 1-5 stars.
> Design the methods and data structures needed

# Switch to pytest-helper for testing
> /agent
# Select "pytest-helper"
> Design comprehensive tests for the rating system

# Let Copilot synthesize everything
> Create an implementation plan that includes both the implementation and tests
```

---

## Sample Files

Ready-to-use agent templates are available in the [samples/agents/](../samples/agents/) folder:

| File | Description |
|------|-------------|
| `hello-world.agent.md` | Minimal example - start here |
| `python-reviewer.agent.md` | Python code quality reviewer |
| `pytest-helper.agent.md` | Pytest testing specialist |

```bash
# Quick install: copy an agent to your personal folder
cp samples/agents/python-reviewer.agent.md ~/.copilot/agents/
```

For more community agents, see [github/awesome-copilot](https://github.com/github/awesome-copilot)

---

## Assignment

### Main Challenge: Build Your Team

1. Create at least 3 agents relevant to a project you work on. You can either:
   - Create individual `.agent.md` files (one per agent, as shown earlier in the chapter), **or**
   - Define them all in a single `AGENTS.md` file (see the hint below for a template)
2. Each agent should have:
   - Clear expertise area
   - Specific code standards
   - Output format preferences
3. Use each agent to complete a task
4. Have agents collaborate on a feature

**Success criteria**: You have agents that improve your workflow and produce consistent, high-quality output.

<details>
<summary>💡 Hints (click to expand)</summary>

**Starter template** - Copy this to `AGENTS.md` in your project root:

```markdown
---
name: project-team
description: A team of specialized agents for this project
---

## Python Reviewer

You are a Python specialist focused on code quality and best practices.

**Standards:**
- Use Python 3.10+ features (dataclasses, type hints)
- Follow PEP 8 naming conventions
- Add comprehensive docstrings
- Use proper error handling

## Pytest Helper

You are a testing specialist focused on pytest best practices.

**Standards:**
- Test behavior, not implementation
- Use descriptive test names
- Use fixtures for shared setup
- Parametrize tests for multiple scenarios

## Code Reviewer

You analyze code without making changes.

**Focus areas:**
- Security vulnerabilities
- Performance issues
- Code maintainability
```

**Testing your agents:**
```bash
copilot
> /agent
# Select "Python Reviewer" from the list
> Add a function to search books by title in @samples/book-app-project/books.py
```

**Tip:** The `description` field in the YAML frontmatter is required for agents to work.

</details>

### Bonus Challenge: Instruction Library

Create a `.github/instructions/` folder with at least 3 instruction files:
- `security-audit.md` for security reviews
- `api-documentation.md` for documenting APIs
- `migration-guide.md` for planning migrations

Test each instruction file on real code in your project.

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong> (click to expand)</summary>

### Common Mistakes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Missing `description` in agent frontmatter | Agent won't load or won't be discoverable | Always include `description:` in YAML frontmatter |
| Wrong file location for agents | Agent not found when you try to use it | Place in `~/.copilot/agents/` (personal) or `.github/agents/` (project) |
| Using `.md` instead of `.agent.md` | File may not be recognized as an agent | Name files like `python-reviewer.agent.md` |
| Overly long agent prompts | May hit the 30,000 character limit | Keep agent definitions focused; use skills for detailed instructions |

### Troubleshooting

**Agent not found** - Check that the agent file exists in one of these locations:
- `~/.copilot/agents/`
- `.github/agents/`

List available agents:

```bash
copilot
> /agent
# Shows all available agents
```

**Agent not following instructions** - Be explicit in your prompts and add more detail to agent definitions:
- Specific frameworks/libraries with versions
- Team conventions
- Example code patterns

**Custom instructions not loading** - Run `/init` in your project to set up project-specific instructions:

```bash
copilot
> /init
```

Or check if they're disabled:
```bash
# Don't use --no-custom-instructions if you want them loaded
copilot  # This loads custom instructions by default
```

</details>

---

## Key Takeaways

1. **Built-in agents**: `/plan` and `/review` are directly invoked; Explore and Task work automatically
2. **Custom agents** are specialists defined in `.agent.md` files
3. **Good agents** have clear expertise, standards, and output formats
4. **Multi-agent collaboration** solves complex problems by combining expertise
5. **Instruction files** (`.instructions.md`) encode team standards for automatic application
6. **Consistent output** comes from well-defined agent instructions

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

## Preview: Agents vs Skills

Before moving to the next chapter, here's a preview of how agents differ from skills:

| | Agents | Skills |
|---|---|---|
| **Analogy** | Hiring a specialist (frontend expert) | Giving someone a detailed checklist |
| **What it provides** | Persona, expertise, coding standards | Step-by-step instructions for a specific task |
| **How it's invoked** | **Manual** - `/agent` or `--agent frontend` | **Automatic** - triggered when your prompt matches |
| **Scope** | Broad domain expertise | Narrow, specific task |
| **Example** | "Frontend agent" knows React patterns, accessibility, TypeScript | "Security audit skill" runs OWASP Top 10 checks |

**The key insight**: An agent is *who* is helping you (a frontend specialist with years of experience). A skill is *what procedure* they follow (run this specific security checklist step by step).

You can combine them: Ask your **security agent** to use your **penetration-testing skill** for a comprehensive security review.

---

## What's Next

Agents change *how* Copilot thinks. Now let's add new *capabilities* with the Skills system.

In **[Chapter 05: Skills System](../05-skills/README.md)**, you'll learn:

- Installing community skills
- Creating custom skills
- How skills auto-trigger from prompts
- When to use skills vs agents

---

**[← Back to Chapter 03](../03-development-workflows/README.md)** | **[Continue to Chapter 05 →](../05-skills/README.md)**
