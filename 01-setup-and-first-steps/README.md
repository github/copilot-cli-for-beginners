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
> Explain what a REST API is in simple terms

> Write a function that reverses a string in Python

> What's the difference between let and const in JavaScript?

> Give me 5 best practices for writing clean code
```

Notice how natural it feels. Just ask questions like you would to a colleague. When you're done exploring, type `/exit` to leave the session.

**The key insight**: GitHub Copilot CLI is conversational. You don't need special syntax to get started. Just ask questions in plain English.

## See It In Action

Now let's see why developers are calling this "having a senior engineer on speed dial."

> 📖 **Reading the Examples**: Lines starting with `>` are prompts you type inside an interactive Copilot session. Lines without a `>` prefix are shell commands you run in your terminal.

### Demo 1: Security Scan in Seconds

The course includes sample files with intentional bugs. Let's scan one:

```bash
# Clone the course repository (if you haven't already)
git clone https://github.com/github/github-copilot-cli-for-beginners
cd github-copilot-cli-for-beginners

# Start Copilot
copilot
```

Once inside the interactive session:

```
> Review @samples/buggy-code/js/userService.js for security vulnerabilities
```

> 💡 **What's the `@`?** The `@` symbol tells Copilot to read a file. You'll learn all about this in Chapter 02 - for now, just copy the command exactly as shown.

<details>
<summary>🎬 See it in action!</summary>

![Security Scan Demo](images/security-scan-demo.gif)

</details>

**What happens**:

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

**The takeaway**: A professional security audit in seconds. Manual review would take...well...more time than that!

---

### Demo 2: Explain Confusing Code

Ever stared at code wondering what it does? Try this in your Copilot session:

```
> Explain this in simple terms: const debounce = (fn, ms) => { let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); }; }
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

Need a script you'd otherwise spend 15 minutes googling? Still in your session:

```
> Write a bash script that finds all files over 100MB and lists them by size
```

<details>
<summary>🎬 See it in action!</summary>

![Generate Script Demo](images/generate-script-demo.gif)

</details>

**What happens**: A complete, working script in seconds that you can copy-paste-run.

When you're done exploring, exit the session:

```
> /exit
```

**The takeaway**: Instant gratification, and you stayed in one continuous session the whole time.

---

You've just seen what Copilot CLI can do. Now let's understand *how* to use these capabilities effectively. The key is knowing which of the three interaction modes to use for different situations.

---

## Real-World Analogy: Learning to Drive

Think of GitHub Copilot CLI like a car with three driving modes:

| Mode | Car Analogy | When to Use |
|------|-------------|-------------|
| **Interactive** | Rally driver with co-driver | Exploring, iterating, real-time guidance as you go |
| **Plan** | GPS navigation | Complex tasks where you want to see the route first |
| **Programmatic** | Self-driving car | Automation, scripts, CI/CD - set the destination and let it run |

Just like driving, you'll naturally learn when each mode feels right.

<img src="images/learning-to-drive-analogy.png" alt="Three Modes of GitHub Copilot CLI" width="800"/>

*Choose your mode based on the task: Interactive for real-time collaboration, Plan for seeing the route first, Programmatic for hands-off automation*

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
> Write a function that greets someone by name
> Now make it return the greeting instead of printing it
> Add a default name of "World" if no name is given
> /exit
```

Notice how each prompt builds on the previous answer. You're having a conversation, not starting over each time.

---

### Mode 2: Plan Mode

**Best for**: Complex tasks where you want to review the approach before execution

Plan mode shows you a step-by-step plan before writing any code. Use the `/plan` command or press **Shift+Tab** to toggle Plan Mode:

> 💡 **Tip**: You can also press **Shift+Tab** at any time to toggle between regular and plan modes.

```bash
copilot

> /plan Create a simple todo list program
```

**Plan mode output:**

```
📋 Implementation Plan

Step 1: Create the data structure
  - Array to store todo items
  - Each item has: id, text, completed status

Step 2: Implement core functions
  - addTodo(text) - Add a new item
  - completeTodo(id) - Mark item as done
  - listTodos() - Show all items

Step 3: Add display formatting
  - Show ✓ for completed items
  - Show numbered list

Proceed with implementation? [Y/n]
```

**Key insight**: Plan mode lets you review and modify the approach before any code is written. You see exactly what Copilot will do before it does it.

> 💡 **Want something more complex?** Try: `/plan Create a REST API for a blog` - Plan mode scales from simple scripts to full applications.

---

### Mode 3: Programmatic Mode

**Best for**: Automation, scripts, CI/CD, single-shot commands

Use the `-p` flag for one-time commands that don't need interaction:

```bash
# Generate code
copilot -p "Write a function that checks if a number is even or odd"

# Explain something
copilot -p "Explain what a for loop does"

# Get quick help
copilot -p "How do I read a file in Python?"
```

<details>
<summary>🎬 See it in action!</summary>

![Programmatic Mode Demo](images/luhn-algorithm-demo.gif)

</details>

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
copilot -p "Review @myfile.js for issues"
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

## Common Mistakes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Typing `exit` instead of `/exit` | Copilot treats "exit" as a prompt, not a command | Slash commands always start with `/` |
| Using `-p` for multi-turn conversations | Each `-p` call is isolated with no memory of previous calls | Use interactive mode (`copilot`) for conversations that build on context |
| Forgetting quotes around prompts with `$` or `!` | Shell interprets special characters before Copilot sees them | Wrap prompts in quotes: `copilot -p "What does $HOME mean?"` |

---

## Troubleshooting

### "Model not available"

Your subscription may not include all models. Use `/model` to see what's available.

### "Context too long"

Your conversation has used the full context window. Use `/clear` to reset, or start a new session.

### "Rate limit exceeded"

Wait a few minutes and try again. Consider using programmatic mode for batch operations with delays.


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
