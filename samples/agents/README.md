# Sample Agent Definitions

This folder contains some simple agent templates for GitHub Copilot CLI intended to help you get started using agents.

## Quick Start

```bash
# Copy an agent to your personal agents folder
cp hello-world.agent.md ~/.copilot/agents/

# Or copy to your project for team sharing
cp python-reviewer.agent.md .github/agents/
```

## Sample Files in This Folder

| File | Description | Best For |
|------|-------------|----------|
| `hello-world.agent.md` | Minimal example (11 lines) | Learning the format |
| `python-reviewer.agent.md` | Python code quality reviewer | Code reviews, PEP 8, type hints |
| `pytest-helper.agent.md` | Pytest testing specialist | Test generation, fixtures, edge cases |

## Finding More Agents

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - Official GitHub resources with community agents and instructions

---

## Agent File Format

Each agent file requires YAML frontmatter with at least a `description` field:

```markdown
---
name: my-agent
description: Brief description of what this agent does
tools: ["read", "edit", "search"]  # Optional: limit available tools
---

# Agent Name

Agent instructions go here...
```

**Available YAML Properties:**

| Property | Required | Description |
|----------|----------|-------------|
| `description` | **Yes** | What the agent does |
| `name` | No | Display name (defaults to filename) |
| `tools` | No | List of allowed tools (omit = all). See aliases below. |
| `target` | No | Limit to `vscode` or `github-copilot` only |

**Tool Aliases**: `read`, `edit`, `search`, `execute` (shell), `web`, `agent`

> 💡 **Note**: The `model` property works in VS Code but is not yet supported in Copilot CLI.
>
> 📖 **Official docs**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)

## Agent File Locations

Agents can be stored in:
- `~/.copilot/agents/` - Global agents available in all projects
- `.github/agents/` - Project-specific agents
- `.agent.md` files - VS Code-compatible format

Each agent is a separate file with the `.agent.md` extension.

---

## Usage Examples

```bash
# Start with a specific agent
copilot --agent python-reviewer

# Or select an agent interactively during a session
copilot
> /agent
# Select "python-reviewer" from the list

# The agent's expertise applies to your prompts
> @samples/book-app-project/books.py Review this code for quality issues

# Switch to a different agent
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py What additional tests should we add?
```

---

## Creating Your Own Agents

1. Create a new file in `~/.copilot/agents/` with `.agent.md` extension
2. Add YAML frontmatter with at least a `description` field
3. Add a descriptive header (e.g., `# Security Agent`)
4. Define the agent's expertise, standards, and behaviors
5. Use the agent with `/agent` or `--agent <name>`

**Tips for effective agents:**
- Be specific about expertise areas
- Include code standards and patterns
- Define what the agent checks for
- Include output format preferences
