![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg) ![Copilot CLI](https://img.shields.io/badge/GitHub-Copilot%20CLI-blue)

🎯 [What You'll Learn](#what-youll-learn) | 🤖 [Copilot Family](#understanding-the-github-copilot-family) | 📚 [Course Structure](#course-structure) | ✅ [Prerequisites](#prerequisites) | 🚀 [Quick Start](#quick-start) | 📋 [Quick Reference](#quick-reference-card) | 📖 [Glossary](#glossary)

# GitHub Copilot CLI for Beginners [Work in Progress]

Learn to supercharge your development workflow with AI-powered command-line assistance.

## What You'll Learn

This hands-on course takes you from zero to productive with GitHub Copilot CLI. By the end, you'll confidently use AI to review code, generate tests, debug issues, and automate workflows: all from your terminal.

**No AI experience required.** If you can use a terminal, you can learn this.

**Perfect for:** Developers, students, and anyone who has experience with software development.

## Who This Course Is For

This course is designed for:

- **Software Developers** who want to use AI from the command line
- **Terminal users** who prefer keyboard-driven workflows over IDE integrations
- **Teams looking to standardize** AI-assisted code review and development practices

---

## What Is GitHub Copilot CLI?

**GitHub Copilot CLI brings AI assistance directly to your terminal.** Instead of switching to a browser or code editor, you can ask questions, review code, generate tests, and debug issues without leaving your command line.

Think of it as having a knowledgeable colleague available 24/7 who can read your code, explain confusing patterns, and help you work faster.

---

## Understanding the GitHub Copilot Family

GitHub Copilot has evolved into a family of AI-powered tools. Here's where each one lives:

| Product | Where It Runs | Description |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started) (this course) | Your terminal |  Terminal-native AI coding assistant  |
| [**GitHub Copilot**](https://docs.github.com/en/copilot) | VS Code, Visual Studio, JetBrains, etc. | Agent mode, chat, inline suggestions  |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | Immersive chat about your repos, create agents, and more |
| [**GitHub Copilot coding agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub  | Assign issues to agents, get PRs back |

This course focuses on **GitHub Copilot CLI**, bringing AI assistance directly to your terminal.

## Course Structure

![GitHub Copilot CLI Learning Path](images/learning-path.png)

| Chapter | Title | What You'll Build |
|:-------:|-------|-------------------|
| 00 | 🚀 [Quick Start](./00-quick-start/README.md) | Installation and verification |
| 01 | 👋 [First Steps](./01-setup-and-first-steps/README.md) | Live demos + three interaction modes |
| 02 | 🔍 [Context and Conversations](./02-context-conversations/README.md) | Multi-file project analysis |
| 03 | ⚡ [Development Workflows](./03-development-workflows/README.md) | Code review, debug, test generation |
| 04 | 🤖 [Create Specialized AI Assistants](./04-agents-custom-instructions/README.md) | Custom agents for your workflow |
| 05 | 🛠️ [Automate Repetitive Tasks](./05-skills/README.md) | Skills that load automatically |
| 06 | 🔌 [Connect to GitHub, Databases & APIs](./06-mcp-servers/README.md) | MCP server integration |
| 07 | 🎯 [Putting It All Together](./07-putting-it-together/README.md) | Complete feature workflows |

## Prerequisites

Before starting, ensure you have:

- [ ] **GitHub account**: [Create one free](https://github.com/signup)
- [ ] **GitHub Copilot access**: [Monthly subscription](https://github.com/features/copilot/plans) or [Free for students/teachers](https://education.github.com/pack)
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

## Getting Help

- 💬 **Questions?** [Start a Discussion](https://github.com/microsoft/github-copilot-cli-for-beginners/discussions)
- 🐛 **Found a bug?** [Open an Issue](https://github.com/microsoft/github-copilot-cli-for-beginners/issues)
- 🤝 **Want to contribute?** PRs welcome!
- 📚 **Official Docs:** [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot)

## Start Learning

Ready? Let's see what GitHub Copilot CLI can do!

**[Begin with Chapter 00: Quick Start →](./00-quick-start/README.md)**

---

## Glossary

Quick reference for technical terms used throughout this course. Don't worry about memorizing these now - refer back as needed.

**[View Full Glossary →](./GLOSSARY.md)**

Key terms: [Agent](./GLOSSARY.md#agent) | [Context Window](./GLOSSARY.md#context-window) | [Token](./GLOSSARY.md#token) | [MCP](./GLOSSARY.md#mcp) | [Skill](./GLOSSARY.md#skill) | [OWASP](./GLOSSARY.md#owasp) | [WCAG](./GLOSSARY.md#wcag)

