![Chapter 01: First Steps](images/chapter-header.png)

> **Watch AI find bugs instantly, explain confusing code, and generate working scripts. Then learn three different ways to use Copilot.**

This chapter is where the magic happens! You'll experience firsthand why developers describe Copilot CLI as having a senior engineer on speed dial. You'll watch AI find security bugs in seconds, get complex code explained in plain English, and generate working scripts instantly. Then you'll master the three interaction modes (Interactive, Plan, and Programmatic) so you know exactly which one to use for any task.

> ⚠️ **Prerequisites**: Make sure you've completed **[Chapter 00: Quick Start](../00-quick-start/README.md)** first. You'll need GitHub Copilot CLI installed and authenticated before running the demos below.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Experience why developers call this "having a senior engineer on speed dial"
- Choose the right mode (Interactive, Plan, or Programmatic) for any task
- Use essential slash commands to control your sessions

> ⏱️ **Estimated Time**: ~50 minutes (20 min reading + 30 min hands-on)

---

## Getting Comfortable: Your First Prompts

Before diving into the impressive demos, let's start with some simple prompts you can try right now. **No code repository needed**! Just open a terminal and start Copilot:

```bash
copilot
```

Try these beginner-friendly prompts:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Notice how natural it feels. Just ask questions like you would to a colleague. When you're done exploring, type `/exit` to leave the session.

**The key insight**: GitHub Copilot CLI is conversational. You don't need special syntax to get started. Just ask questions in plain English.

## See It In Action

Now let's see why developers are calling this "having a senior engineer on speed dial."

> 📖 **Reading the Examples**: Lines starting with `>` are prompts you type inside an interactive Copilot session. Lines without a `>` prefix are shell commands you run in your terminal.

> 💡 **About Example Outputs**: The sample outputs shown throughout this course are illustrative. Because Copilot's responses vary each time, your results will differ in wording, formatting, and detail. Focus on the *type* of information returned, not the exact text.

### Demo 1: Code Review in Seconds

The course includes sample files with intentional code quality issues. Let's review one:

```bash
# Clone the course repository (if you haven't already)
git clone https://github.com/github/github-copilot-cli-for-beginners
cd github-copilot-cli-for-beginners

# Start Copilot
copilot
```

Once inside the interactive session:

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **What's the `@`?** The `@` symbol tells Copilot to read a file. You'll learn all about this in Chapter 02 - for now, just copy the command exactly as shown.

<details>
<summary>🎬 See it in action!</summary>

![Code Review Demo](images/code-review-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

**What happens** (your output will look different - Copilot's responses vary each time):

```
Code Quality Review: book_app.py

MEDIUM: Missing Type Hints (throughout)
    Most functions lack type hints
    Fix: Add type hints for better code clarity and IDE support
    Example: def handle_add() -> None:

MEDIUM: Weak Input Validation (lines 32-37)
    Code: year = int(year_str) if year_str else 0
    Issue: Doesn't validate year is reasonable (e.g., not negative, not far future)
    Fix: Add range validation: if year < 0 or year > 2100: raise ValueError

LOW: If/Elif Chain Could Be Dict (lines 82-94)
    Long if/elif chain for command routing
    Consider: Command pattern or dict mapping for cleaner code
    More maintainable as commands grow

LOW: Global State (line 6)
    Global collection instance makes testing harder
    Consider: Pass collection as parameter or use dependency injection

Summary: 4 main issues found - focus on type hints and validation
```

**The takeaway**: A professional code review in seconds. Manual review would take...well...more time than that!

---

### Demo 2: Explain Confusing Code

Ever stared at code wondering what it does? Try this in your Copilot session:

```
> Explain what this does in simple terms:
> @samples/book-app-project/books.py
```

<details>
<summary>🎬 See it in action!</summary>

![Explain Code Demo](images/explain-code-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

**What happens**:

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**The takeaway**: Complex code explained like a patient mentor would explain it.

---

### Demo 3: Generate Working Code

Need a function you'd otherwise spend 15 minutes googling? Still in your session:

```
> Write a Python function that takes a list of books and returns statistics:
> total count, number read, number unread, oldest and newest book
```

<details>
<summary>🎬 See it in action!</summary>

![Generate Code Demo](images/generate-code-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

**What happens**: A complete, working function in seconds that you can copy-paste-run.

When you're done exploring, exit the session:

```
> /exit
```

**The takeaway**: Instant gratification, and you stayed in one continuous session the whole time.

---

You've just seen what Copilot CLI can do. Now let's understand *how* to use these capabilities effectively. The key is knowing which of the three interaction modes to use for different situations.

---

## Real-World Analogy: Dining Out

Think of using GitHub Copilot CLI like going out to eat - from planning the trip to placing your order, different situations call for different approaches:

| Mode | Dining Analogy | When to Use |
|------|----------------|-------------|
| **Plan** | GPS route to the restaurant | Complex tasks - map out the route, review stops, agree on the plan, then drive |
| **Interactive** | Talking to the waiter | Exploration and iteration - ask questions, customize, get real-time feedback |
| **Programmatic** | Drive-through ordering | Quick, specific tasks - stay in your environment, get a result fast |

Just like dining out, you'll naturally learn when each approach feels right.

<img src="images/ordering-food-analogy.png" alt="Three Ways to Use GitHub Copilot CLI - Plan Mode (GPS route to restaurant), Interactive Mode (talking to waiter), Programmatic Mode (drive-through)" width="800"/>

*Choose your mode based on the task: Plan for mapping it out first, Interactive for back-and-forth collaboration, Programmatic for quick one-shot results*

### Which Mode Should I Start With?

**Start with Interactive mode.** It's the most flexible and helps you learn:
- You can experiment and ask follow-up questions
- Context builds naturally through conversation
- Mistakes are easy to correct with `/clear`

Once you're comfortable, try:
- **Programmatic mode** (`-p`) for quick, one-off questions
- **Plan mode** (`/plan`) when you need to plan things out in more detail before coding

---

## The Three Modes

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

> What's the best way to handle file I/O errors in Python?

[Copilot explains try/except, context managers, and specific exception types]

> Show me an example with reading a JSON file

[Copilot builds on the previous context to show a JSON file example]

> /exit
```

**Key insight**: Interactive mode maintains context. Each message builds on previous ones, just like a real conversation.

#### Interactive Mode Example

```bash
copilot

# In the session:
> Review @samples/book-app-project/utils.py and suggest improvements
> Add type hints to all functions
> Make the error handling more robust
> /exit
```

Notice how each prompt builds on the previous answer. You're having a conversation, not starting over each time.

---

### Mode 2: Plan Mode

**Best for**: Complex tasks where you want to review the approach before execution

Plan mode shows you a step-by-step plan before writing any code. Use the `/plan` command or press **Shift+Tab** to toggle Plan Mode:

> 💡 **Tip**: **Shift+Tab** is a keyboard shortcut that toggles between regular mode and plan mode. Press it anytime during an interactive session to switch modes without typing a command.

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

**Plan mode output:**

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**Key insight**: Plan mode lets you review and modify the approach before any code is written. You see exactly what Copilot will do before it does it.

> 💡 **Want something more complex?** Try: `/plan Add search and filter capabilities to the book app` - Plan mode scales from simple features to full applications.

---

### Mode 3: Programmatic Mode

**Best for**: Automation, scripts, CI/CD, single-shot commands

Use the `-p` flag for one-time commands that don't need interaction:

```bash
# Analyze code
copilot -p "List all functions in @samples/book-app-project/book_app.py"

# Generate code
copilot -p "Write a function that checks if a number is even or odd"

# Get quick help
copilot -p "How do I read a JSON file in Python?"
```

**Key insight**: Programmatic mode gives you a quick answer and exits. No conversation, just input → output.

<details>
<summary>📚 <strong>Going Further: Using Programmatic Mode in Scripts</strong> (click to expand)</summary>

Once you're comfortable, you can use `-p` in shell scripts:

```bash
#!/bin/bash

# Generate commit messages automatically
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Review a file
copilot -p "Review @myfile.py for issues"
```

</details>

---

## Essential Slash Commands

These commands work in interactive mode. **Start with just these four** - they cover 90% of daily use:

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `/help` | Show all available commands | When you forget a command |
| `/clear` | Clear conversation and start fresh | When switching topics |
| `/plan` | Plan your work out before coding | For more complex features |
| `/exit` | End the session | When you're done |

That's it for getting started! As you become comfortable, you can explore additional commands.

> 📚 **Official Documentation**: [CLI command reference](https://docs.github.com/copilot/reference/cli-command-reference) for the complete list of commands and flags.

<details>
<summary>📚 <strong>Additional Commands</strong> (click to expand)</summary>

### Core Commands

| Command | What It Does |
|---------|--------------|
| `/model` | Show or switch AI model |
| `/review` | Run the code-review agent |
| `/delegate` | Hand off task to Copilot coding agent on GitHub (agent in the cloud) |

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
| `/tasks` | View background subagents and detached shell sessions |

### Directory Access

| Command | What It Does |
|---------|--------------|
| `/add-dir <directory>` | Add a directory to allowed list |
| `/list-dirs` | Show all allowed directories |
| `/cwd`, `/cd [directory]` | View or change working directory |

### Configuration

| Command | What It Does |
|---------|--------------|
| `/theme` | View or set terminal theme |
| `/terminal-setup` | Enable multiline input support |
| `/user` | Manage GitHub accounts |
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

> ⚠️ **Use with caution**: These skip confirmation prompts. Great for trusted projects, but be careful with untrusted code.

### Quick Shell Commands

Run shell commands directly without AI by prefixing with `!`:

```bash
copilot

> !git status
# Runs git status directly, bypassing the AI

> !python -m pytest tests/
# Runs pytest directly
```

### The /delegate Command

The `/delegate` command hands off tasks to the [Copilot coding agent on GitHub](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks). This is a powerful way to get work done in the cloud without leaving your terminal.

```bash
copilot

> /delegate Complete the API integration tests and fix any failing edge cases

# Or use the & prefix shortcut:
> & Add error handling to the login function
```

### Switching Models

```bash
copilot
> /model

# Shows available models - these vary by subscription and region
```

</details>

---

## Hands-On Examples

### Example 1: Interactive Exploration

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Let's refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### Example 2: Plan a Feature

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Review the plan
# Approve or modify
# Watch it implement step by step
```

### Example 3: Automate with Programmatic Mode

```bash

# Review all Python files in the book app
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot -p "Quick code quality review of @$file - critical issues only"
done
```

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **Interactive Challenge**: Start `copilot` and explore the book app. Ask about `@samples/book-app-project/books.py` and request improvements 3 times in a row.

2. **Plan Mode Challenge**: Run `/plan Add rating and review features to the book app`. Read the plan carefully - does it make sense?

3. **Programmatic Challenge**: Run `copilot -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. Did it work on the first try?

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

<details>
<summary>💡 Hints (click to expand)</summary>

**Sample prompts to try:**
```bash
> Write a Python function that calculates the factorial of a number
> Add error handling for negative numbers and non-integers
> Add a comprehensive docstring with examples
```

**Common issues:**
- If Copilot asks clarifying questions, just answer them naturally
- Use `/clear` if you want to start over
- The context carries forward, so each prompt builds on the previous

</details>

### Bonus Challenge: Compare the Modes

Try this same task in all three modes:

1. **Interactive**: Build the function through conversation (as above)
2. **Plan**: Use `/plan Write a factorial function` to see the plan first
3. **Programmatic**: `copilot -p "Write a Python factorial function with error handling and docstring"`

**Reflection**: Which mode felt most natural? When would you use each?

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong> (click to expand)</summary>

### Common Mistakes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Typing `exit` instead of `/exit` | Copilot treats "exit" as a prompt, not a command | Slash commands always start with `/` |
| Using `-p` for multi-turn conversations | Each `-p` call is isolated with no memory of previous calls | Use interactive mode (`copilot`) for conversations that build on context |
| Forgetting quotes around prompts with `$` or `!` | Shell interprets special characters before Copilot sees them | Wrap prompts in quotes: `copilot -p "What does $HOME mean?"` |

### Troubleshooting

**"Model not available"** - Your subscription may not include all models. Use `/model` to see what's available.

**"Context too long"** - Your conversation has used the full context window. Use `/clear` to reset, or start a new session.

**"Rate limit exceeded"** - Wait a few minutes and try again. Consider using programmatic mode for batch operations with delays.

</details>

---

## Key Takeaways

1. **Interactive mode** is for exploration and iteration - context carries forward
2. **Plan mode** is for complex tasks - review before implementation
3. **Programmatic mode** is for automation - no interaction needed
4. **Four essential commands** (`/help`, `/clear`, `/plan`, `/exit`) cover most daily use

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
