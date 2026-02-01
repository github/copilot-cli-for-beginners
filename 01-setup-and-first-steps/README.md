![Chapter 01: First Steps](images/chapter-header.png)

> **Watch AI find bugs instantly, explain confusing code, and generate working scripts. Then learn three different ways to use Copilot.**

This chapter is where the magic happens! You'll experience firsthand why developers describe Copilot CLI as having a senior engineer on speed dial. You'll watch AI find security bugs in seconds, get complex code explained in plain English, and generate working scripts instantly. Then you'll master the three interaction modes (Interactive, Plan, and Programmatic) so you know exactly which one to use for any task.

> ⚠️ **Prerequisites**: Make sure you've completed **[Chapter 00: Quick Start](../00-quick-start/README.md)** first. You'll need GitHub Copilot CLI installed and authenticated before running the demos below.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Experience why developers call this "having a senior engineer on speed dial"
- Choose the right mode (Interactive, Plan, or Programmatic) for any task
- Use essential slash commands to control your sessions
- Understand how Agents, Skills, and MCP extend GitHub Copilot CLI

---

## See It In Action

Before we learn the theory, let's see why developers are calling this "having a senior engineer on speed dial."

### Demo 1: Security Scan in 5 Seconds

The course includes sample files with intentional bugs. Let's scan one:

```bash
# Clone the course repository (if you haven't already)
git clone https://github.com/microsoft/github-copilot-cli-for-beginners
cd github-copilot-cli-for-beginners

# Run the security scan
copilot -p "Review @samples/buggy-code/js/userService.js for security vulnerabilities"
```

<details>
<summary>🎬 See it in action!</summary>

![Security Scan Demo](images/security-scan-demo.gif)

</details>

**What happens** (in about 5 seconds):

```
Security Review: userService.js

CRITICAL: SQL Injection (line 13)
    Code: `SELECT * FROM users WHERE id = ${userId}`
    Risk: Attacker can access/delete entire database
    Fix: Use parameterized queries

CRITICAL: SQL Injection (line 29)
    Code: `UPDATE users SET name = '${data.name}'...`
    Risk: Same vulnerability in update operation

HIGH: Sensitive Data Logged (line 36)
    Code: console.log(`Login attempt: ${email} / ${password}`)
    Risk: Passwords visible in production logs

HIGH: Hardcoded Secret (line 59)
    Code: const JWT_SECRET = 'super-secret-key-12345'
    Risk: Anyone with code access can forge JWT (JSON Web Token) authentication tokens

Summary: 8 issues found (4 critical/high, 4 medium)
```

**The takeaway**: A professional security audit in 5 seconds. Manual review would take...well...more time than that!

---

### Demo 2: Explain Confusing Code

Ever stared at code wondering what it does? Try this:

```bash
copilot -p "Explain this in simple terms: const debounce = (fn, ms) => { let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); }; }"
```

<details>
<summary>🎬 See it in action!</summary>

![Explain Code Demo](images/explain-code-demo.gif)

</details>

**What happens**:

```
This is a debounce function - it delays execution until activity stops.

Think of it like an elevator:
- When someone presses a button, the elevator doesn't move immediately
- It waits to see if more people are coming
- Only after a pause (ms milliseconds) does it actually move

How it works:
1. Takes a function (fn) and a delay time (ms)
2. Returns a new function that wraps the original
3. Each call resets the timer (clearTimeout)
4. The original function only runs after the delay passes with no new calls

Common uses:
- Search boxes that wait until you stop typing
- Window resize handlers that don't fire constantly
- Auto-save that triggers after you pause editing
```

**The takeaway**: Complex code explained like a patient mentor would explain it.

---

### Demo 3: Generate Working Code

Need a script you'd otherwise spend 15 minutes googling?

```bash
copilot -p "Write a bash script that finds all files over 100MB and lists them by size"
```

<details>
<summary>🎬 See it in action!</summary>

![Generate Script Demo](images/generate-script-demo.gif)

</details>

**What happens**: A complete, working script in seconds that you can copy-paste-run.

**The takeaway**: Instant gratification - immediately usable code.

---

You've just seen what Copilot CLI can do. Now let's understand *how* to use these capabilities effectively. The key is knowing which of the three interaction modes to use for different situations.

---

## Real-World Analogy: Learning to Drive

Think of GitHub Copilot CLI like a car with three driving modes:

| Mode | Car Analogy | When to Use |
|------|-------------|-------------|
| **Interactive** | Automatic transmission | Exploring, learning, iterating on ideas |
| **Plan** | GPS navigation | Complex tasks where you want to see the route first |
| **Programmatic** | Cruise control | Automation, scripts, CI/CD (Continuous Integration/Deployment) pipelines |

Just like driving, you'll naturally learn when each mode feels right.

<img src="images/learning-to-drive-analogy.png" alt="Learning to Drive Analogy - Three Modes of GitHub Copilot CLI" width="800"/>

*Choose your gear based on the task: Interactive for exploration, Plan for structured work, Programmatic for automation*

### Which Mode Should I Start With?

**Start with Interactive mode.** It's the most forgiving and helps you learn:
- You can experiment and ask follow-up questions
- Context builds naturally through conversation
- Mistakes are easy to correct with `/clear`

Once you're comfortable, try:
- **Programmatic mode** (`-p`) for quick, one-off questions
- **Plan mode** (`/plan`) when you need to think before coding

---

## The Three Modes

> 📖 **Reading the Examples**: Throughout this course, you'll see two types of command prompts:
> - Lines starting with `>` are typed inside an interactive Copilot session
> - Lines starting with `#` are comments explaining what's happening
> - Lines without a prefix (in code blocks) are shell commands you run in your terminal

### Mode 1: Interactive Mode

**Best for**: Exploration, iteration, multi-turn conversations

Start an interactive session:

```bash
copilot
```

You'll see a prompt where you can type naturally:

```
> /help

Available commands:
  /help     - Show this help message
  /clear    - Clear conversation history
  /model    - Show or change the AI model
  /exit     - Exit the session

> What's the best way to handle errors in async JavaScript?

[Copilot explains try/catch, .catch(), and error boundaries]

> Show me an example with fetch()

[Copilot builds on the previous context to show a fetch example]

> /exit
```

**Key insight**: Interactive mode maintains context. Each message builds on previous ones, just like a real conversation.

#### Interactive Mode Example

```bash
copilot

# In the session:
> Create a Python class for managing a todo list
> Add a method to mark items as complete
> Add persistence using JSON file storage
> /exit
```

Notice how each prompt builds on the previous answer.

---

### Mode 2: Plan Mode

**Best for**: Complex tasks where you want to review the approach before execution

Plan mode shows you a step-by-step plan before writing any code. Use the `/plan` command or press **Shift+Tab** to toggle Plan Mode:

> 💡 **Tip**: You can also press **Shift+Tab** at any time to toggle between regular and plan modes.

```bash
copilot

> /plan Create a REST API for a blog with posts and comments using [Your_Language/Framework]
```

> 💡 **Replace `[Your_Language/Framework]`** with your preference, e.g., "Node.js with Express", "Python with FastAPI", "C# with ASP.NET Core", etc.

```bash
# Example with specific framework:
> /plan Create a REST API for a blog with posts and comments using Node.js with Express
```

**Plan mode output:**

```
📋 Implementation Plan

Step 1: Set up Express server
  - Initialize package.json
  - Install express, cors, body-parser
  - Create server.js with basic configuration

Step 2: Create data models
  - Post model (id, title, content, createdAt)
  - Comment model (id, postId, author, content, createdAt)

Step 3: Implement POST endpoints
  - POST /api/posts - Create new post
  - POST /api/posts/:id/comments - Add comment to post

Step 4: Implement GET endpoints
  - GET /api/posts - List all posts
  - GET /api/posts/:id - Get single post with comments

Step 5: Implement UPDATE/DELETE
  - PUT /api/posts/:id - Update post
  - DELETE /api/posts/:id - Delete post and its comments

Step 6: Add error handling
  - Validation middleware
  - Error response formatting

Proceed with implementation? [Y/n]
```

**Key insight**: Plan mode lets you review and modify the approach before any code is written. Perfect for complex features.

---

### Mode 3: Programmatic Mode

**Best for**: Automation, scripts, CI/CD, single-shot commands

Use the `-p` flag for one-time commands that don't need interaction:

```bash
# Generate code
copilot -p "Write a Python function to validate credit card numbers using the Luhn algorithm"
```

<details>
<summary>🎬 See it in action!</summary>

![Luhn Algorithm Demo](images/luhn-algorithm-demo.gif)

</details>

```bash
# Explain something
copilot -p "Explain the difference between let and const in JavaScript"

# Review a file
copilot -p "Review @myfile.js for performance issues"
```

#### Programmatic Mode in Scripts

```bash
#!/bin/bash

# Generate commit messages automatically
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Generate documentation
copilot -p "Generate JSDoc comments for @src/utils.js" > docs/utils.md

# Security scan before deploy
copilot -p "Security review of @src/ - list critical issues only"
```

**Key insight**: Programmatic mode is perfect for automation. No interaction needed - just input and output.

---

## Essential Slash Commands

These commands work in interactive mode.

### 🚀 Start With These 4 Commands

Master these first - they cover 90% of daily use:

| Command | What It Does | Example |
|---------|--------------|---------|
| `/help` | Show all available commands | When you forget a command |
| `/clear` | Clear conversation and start fresh | When switching topics |
| `/plan` | Preview steps before coding | For complex features |
| `/exit` | End the session | When you're done |

### All Core Commands

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `/help` | Show available commands | When you're unsure what's possible |
| `/clear` | Clear conversation history | Starting a new topic in same session |
| `/model` | Show or switch AI model | Testing different models |
| `/exit` | End the session | When you're done |
| `/plan` | Create implementation plan before coding | Complex features needing structure |
| `/review` | Run code-review agent | Before committing changes |
| `/delegate` | Hand off task to Copilot coding agent | Background work on GitHub |

### Session Commands

| Command | What It Does |
|---------|--------------|
| `/session` | Show session info and workspace summary |
| `/usage` | Display session usage metrics and statistics |
| `/context` | Show context window token usage |
| `/compact` | Summarize conversation to reduce context usage |
| `/share` | Export session as markdown file or GitHub gist |
| `/rename` | Rename the current session |
| `/resume` | Switch to a different session |

### Directory Access

| Command | What It Does |
|---------|--------------|
| `/add-dir <directory>` | Add a directory to allowed list |
| `/list-dirs` | Show all allowed directories |
| `/cwd`, `/cd [directory]` | View or change working directory |

### Configuration

| Command | What It Does |
|---------|--------------|
| `/theme` | View or set terminal theme (auto/dark/light/GitHub Dark/GitHub Light) |
| `/terminal-setup` | Enable multiline input support |
| `/user` | Manage GitHub accounts (show/list/switch) |
| `/feedback` | Submit feedback to GitHub |
| `/init` | Initialize Copilot instructions for your repository |

### Skills Management

| Command | What It Does |
|---------|--------------|
| `/skills list` | Show all available skills |
| `/skills info <name>` | Get details about a specific skill |
| `/skills reload` | Reload skills after editing |

> 💡 Skills are covered in detail in [Chapter 05](../05-skills/README.md).

### Permissions

| Command | What It Does |
|---------|--------------|
| `/allow-all` | Auto-approve all permission prompts for this session |
| `/yolo` | Alias for `/allow-all` (same behavior) |

> ⚠️ **Use with caution**: `/allow-all` and `/yolo` skip confirmation prompts. Great for trusted projects, but be careful with untrusted code.

### Quick Shell Commands

Run shell commands directly without AI by prefixing with `!`:

```bash
copilot

> !git status
# Runs git status directly, bypassing the AI

> !npm test
# Runs npm test directly
```

### The /delegate Command

The `/delegate` command hands off tasks to the Copilot coding agent on GitHub:

```bash
copilot

> /delegate Complete the API integration tests and fix any failing edge cases

# Or use the & prefix shortcut:
> & Add error handling to the login function

# Copilot:
# 1. Commits your changes to a new branch
# 2. Opens a draft pull request
# 3. Works on the task in the background
# 4. Requests your review when done
```

This is useful for tasks you want Copilot to complete independently while you work on something else.

### Switching Models

Different AI models have different strengths:

```bash
copilot
> /model

# Example output (your available models will vary):
Available models:
  - Claude Sonnet 4.5 (default)
  - Claude Opus 4.5
  - Gemini 3 Pro
  - GPT-5.2 Codex
  - GPT-5.1-Codex-Mini
  - More ...
```

> ⚠️ **Important**: The models shown above are examples only. Available models change frequently and vary based on your subscription, region, and GitHub Copilot updates. Always run `/model` to see your current options.

```bash
# Switch to a specific model
> /model gpt-5.2-codex
Model switched to gpt-5.2-codex

# Now use the new model
> Write a creative story opening about a space explorer
```

**Tips**:
- Try the same prompt with different models to see how their outputs differ
- Use `/model` to see currently available models (availability changes frequently)

---

## Preview: Three Ways to Extend Copilot CLI

Before we continue, let's understand the three extension mechanisms you'll learn in this course. This mental model will help everything make sense.

### Agents (Chapter 04): Change HOW the AI Thinks

Agents are specialized AI personalities with specific expertise. You define them in agent files and invoke them with the `/agent` command.

```bash
# Select an agent interactively
> /agent

# Or start with a specific agent
copilot --agent frontend
```

**When to use**: When you need specialized domain expertise.

### Skills (Chapter 05): Automatic Task Instructions

Skills are folders of instructions stored in `~/.copilot/skills/`. Copilot **automatically loads** them when your prompt matches the skill's description.

```bash
# Just ask naturally - Copilot loads matching skills automatically
> Review this code for security issues
# Copilot detects this matches your "security-audit" skill
# and applies its checklist automatically
```

**When to use**: For repetitive tasks that need consistent behavior.

### MCP Servers (Chapter 06): Connect to EXTERNAL Services

MCP (Model Context Protocol) connects Copilot to external data sources. Configure servers, then their tools become available.

```bash
# Configure MCP servers
> /mcp add

# Once configured, the tools are available to Copilot
# and it can use them automatically when relevant
```

**When to use**: When you need live data from external systems like GitHub, databases, or APIs.

### How They Work Together (Chapter 07)

```bash
# A complete workflow combining extensions
copilot --agent backend

# Copilot (with backend expertise) can now:
# - Access GitHub issues via MCP
# - Use your custom skills
# - Apply backend best practices
```

This is the power of GitHub Copilot CLI - and you'll master all of it by Chapter 07.

---

## Hands-On Examples

### Example 1: Interactive Exploration

```bash
copilot

> I'm building a Node.js API. What's the best way to structure the project?

> I want to use TypeScript. How does that change the structure?

> Create the initial folder structure and package.json for me

> /exit
```

### Example 2: Plan a Feature

```bash
copilot

> /plan Add user authentication with JWT to my Express app

# Review the plan
# Approve or modify
# Watch it implement step by step
```

### Example 3: Automate with Programmatic Mode

```bash

# Review all JavaScript files in src/
for file in src/*.js; do
  echo "Reviewing $file..."
  copilot -p "Quick security review of @$file - critical issues only"
done
```

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **Interactive Challenge**: Start `copilot` and build a function that validates email addresses. Ask for improvements 3 times in a row.

2. **Plan Mode Challenge**: Run `/plan Create a REST API for a todo list using [Your_Language/Framework]`. Read the plan carefully - does it make sense?

3. **Programmatic Challenge**: Run `copilot -p "Write a regex that matches phone numbers in format (XXX) XXX-XXXX"`. Did it work on the first try?

**Self-Check**: You understand the three modes when you can explain when NOT to use interactive mode (hint: one-off questions are faster with `-p`).

---

## Assignment

### Main Challenge: Master Interactive Mode

1. Start an interactive session: `copilot`
2. Ask Copilot to create a Python function that calculates factorials
3. Ask for error handling: "Add error handling for negative numbers"
4. Ask for a docstring: "Add a comprehensive docstring"
5. Observe how context carries between prompts
6. Exit with `/exit`

**Success criteria**: You should have a complete, documented factorial function with error handling, built through conversation.

### Bonus Challenge: Compare the Modes

Try this same task in all three modes:

1. **Interactive**: Build the function through conversation (as above)
2. **Plan**: Use `/plan Write a factorial function` to see the plan first
3. **Programmatic**: `copilot -p "Write a Python factorial function with error handling and docstring"`

**Reflection**: Which mode felt most natural? When would you use each?

---

## Troubleshooting

### "Model not available"

Your subscription may not include all models. Use `/model` to see what's available.

### "Context too long"

Your conversation has used the full context window. Use `/clear` to reset, or start a new session.

### "Rate limit exceeded"

Wait a few minutes and try again. Consider using programmatic mode for batch operations with delays.

### Interactive mode exits unexpectedly

Check your terminal configuration. Some terminals don't handle interactive sessions well. Try a different terminal emulator.

---

## Key Takeaways

1. **Interactive mode** is for exploration and iteration - context carries forward
2. **Plan mode** is for complex tasks - review before implementation
3. **Programmatic mode** is for automation - no interaction needed
4. **Slash commands** (`/help`, `/clear`, `/model`, `/exit`) control your sessions
5. **Agents, Skills, and MCP** extend Copilot's capabilities - you'll learn each in upcoming chapters

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

## What's Next

Now that you understand the three modes, let's learn how to give Copilot context about your code.

In **[Chapter 02: Context and Conversations](../02-context-conversations/README.md)**, you'll learn:

- The `@` syntax for referencing files and directories
- Session management with `--resume` and `--continue`
- How context management makes Copilot truly powerful

---

**[← Back to Course Home](../README.md)** | **[Continue to Chapter 02 →](../02-context-conversations/README.md)**
