![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) ![Copilot CLI](https://img.shields.io/badge/GitHub-Copilot%20CLI-blue)

🎯 [What You'll Learn](#what-youll-learn) | 📚 [Course Structure](#course-structure) | ✅ [Prerequisites](#prerequisites) | 🚀 [Quick Start](#quick-start) | 📋 [Quick Reference](#quick-reference-card) | 📖 [Glossary](#glossary)

# GitHub Copilot CLI for Beginners

Learn to supercharge your development workflow with AI-powered command-line assistance.

## What You'll Learn

This hands-on course takes you from zero to productive with GitHub Copilot CLI. By the end, you'll confidently use AI to review code, generate tests, debug issues, and automate workflows: all from your terminal.

**No AI experience required.** If you can use a terminal, you can learn this.

**Perfect for:** Developers, students, and anyone who uses a terminal daily.

## Course Structure

| Chapter | Title | What You'll Build |
|:-------:|-------|-------------------|
| 00 | 🚀 [Quick Start](./00-quick-start/README.md) | Installation and verification |
| 01 | 👋 [First Steps](./01-setup-and-first-steps/README.md) | Live demos + three interaction modes |
| 02 | 🔍 [Context and Conversations](./02-context-conversations/README.md) | Multi-file project analysis |
| 03 | ⚡ [Development Workflows](./03-development-workflows/README.md) | Code review, debug, test generation |
| 04 | 🤖 [Agents and Custom Instructions](./04-agents-custom-instructions/README.md) | Specialized AI assistants |
| 05 | 🛠️ [Skills System](./05-skills/README.md) | Auto-loaded task instructions |
| 06 | 🔌 [MCP Servers](./06-mcp-servers/README.md) | Connect to GitHub, databases, APIs |
| 07 | 🎯 [Putting It All Together](./07-putting-it-together/README.md) | Complete feature workflows |

## Prerequisites

Before starting, ensure you have:

- [ ] **GitHub account**: [Create one free](https://github.com/signup)
- [ ] **GitHub Copilot access**: [Free for students/teachers](https://education.github.com/pack), get started with the [Free option](https://github.com/features/copilot/plans), or [Monthly subscription](https://github.com/features/copilot/plans)
- [ ] **Node.js LTS**: [Download here](https://nodejs.org/) (for npm installation)
- [ ] **Terminal basics**: Comfortable with `cd`, `ls`, running commands

## Quick Start

Can't wait? Run this in your terminal right now:

```bash
# Install (choose one)
npm install -g @github/copilot    # All platforms
brew install copilot-cli          # macOS/Linux
winget install GitHub.Copilot     # Windows

# Start and authenticate
copilot
> /login

# See the magic
copilot -p "Explain what GitHub Copilot CLI can do for developers"
```

Want more details? Head to [Chapter 00](./00-quick-start/README.md) for the full quick start experience.

## How This Course Works

Each chapter follows the same pattern:

1. **Real-World Analogy**: Understand the concept through familiar comparisons
2. **Core Concepts**: Learn the essential knowledge
3. **Hands-On Examples**: Run actual commands and see results
4. **Assignment**: Practice what you learned
5. **What's Next**: Preview of the following chapter

**Code examples are runnable.** Every copilot text block in this course can be copied and run in your terminal.

## Quick Reference Card

Need a cheat sheet? The **[Quick Reference Card](./QUICK-REFERENCE.md)** has all commands, syntax, and workflows on one page.

A PDF version is also available: [QUICK-REFERENCE.pdf](./QUICK-REFERENCE.pdf)

### Keeping It Updated

The Quick Reference can be automatically updated using Copilot CLI itself:

```bash
npm install

# Update content by scanning docs with Copilot, then generate PDF
npm run refresh

# Or run steps separately:
npm run update:reference  # Uses Copilot CLI to scan docs and update content
npm run generate:pdf      # Generates PDF from markdown
```

## Glossary

Quick reference for technical terms used throughout this course:

| Term | Definition |
|------|------------|
| **Agent** | A specialized AI personality with domain expertise (e.g., frontend, security). Defined in `.agent.md` files. |
| **API** | Application Programming Interface - a way for programs to communicate with each other. |
| **CI/CD** | Continuous Integration/Continuous Deployment - automated testing and deployment pipelines. |
| **CLI** | Command Line Interface - a text-based way to interact with software (like this tool!). |
| **Context Window** | The amount of text an AI can consider at once. Like a desk that can only hold so much. |
| **Glob Pattern** | A pattern using wildcards to match file paths (e.g., `*.js` matches all JavaScript files). |
| **JWT** | JSON Web Token - a secure way to transmit authentication information between systems. |
| **MCP** | Model Context Protocol - a standard for connecting AI assistants to external data sources. |
| **OWASP** | Open Web Application Security Project - organization that publishes security best practices. |
| **Programmatic Mode** | Running Copilot with `-p` flag for single commands without interaction. |
| **Session** | A conversation with Copilot that maintains context and can be resumed later. |
| **Skill** | A folder with instructions that Copilot automatically loads when relevant to your prompt. |
| **Slash Command** | Commands starting with `/` that control Copilot (e.g., `/help`, `/clear`, `/model`). |
| **Token** | A unit of text that AI models process. Roughly 4 characters or 0.75 words. |
| **WCAG** | Web Content Accessibility Guidelines - standards for making web content accessible. |

## Getting Help

- 💬 **Questions?** [Start a Discussion](https://github.com/microsoft/github-copilot-cli-for-beginners/discussions)
- 🐛 **Found a bug?** [Open an Issue](https://github.com/microsoft/github-copilot-cli-for-beginners/issues)
- 🤝 **Want to contribute?** PRs welcome!
- 📚 **Official Docs:** [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot)

## Start Learning

Ready? Let's see what GitHub Copilot CLI can do!

**[Begin with Chapter 00: Quick Start →](./00-quick-start/README.md)**

