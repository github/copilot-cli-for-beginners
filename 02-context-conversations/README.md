# Chapter 02: Context and Conversations

> **What if AI could see your entire codebase, not just one file at a time?**

In this chapter, you'll unlock the real power of GitHub Copilot CLI: context. You'll learn to use the `@` syntax to reference files and directories, giving Copilot deep understanding of your codebase. You'll discover how to maintain conversations across sessions, resume work days later exactly where you left off, and see how cross-file analysis catches bugs that single-file reviews miss entirely.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Use the `@` syntax to reference files and directories
- Resume previous sessions with `--resume` and `--continue`
- Understand how context windows work
- Write effective multi-turn conversations

---

## Real-World Analogy: Working with a Colleague

Imagine explaining a bug to a colleague:

**Without context**: "The login doesn't work."
**With context**: "Look at `auth/login.js`, especially the `validateToken` function on line 42. It's not handling expired tokens correctly."

The second approach gets better help because your colleague can see exactly what you're talking about.

GitHub Copilot CLI works the same way. The `@` syntax is how you point Copilot at specific files, giving it the context it needs to help effectively.

<img src="images/colleague-context-analogy.png" alt="Context Makes the Difference - Without vs With Context" width="800"/>

*The @ syntax gives Copilot the context it needs to help effectively*

---

## The @ Syntax

The `@` symbol references files and directories in your prompts.

### @ Syntax Quick Reference

| Pattern | What It Does | When to Use |
|---------|--------------|-------------|
| `@file.js` | Single file | Focused review, specific questions |
| `@folder/` | Entire directory | Architecture review, pattern detection |
| `@folder/*.js` | All .js files in folder | Language-specific analysis |
| `@**/*.test.js` | Recursive glob pattern | Find all test files anywhere |
| `@file1.js @file2.js` | Multiple specific files | Cross-file comparison, dependencies |
| `@image.png` | Image file | UI review, visual debugging |

### Reference a Single File

```bash
copilot

> Explain what @src/utils/helpers.js does
```

<details>
<summary>🎬 See it in action!</summary>

![File Context Demo](images/file-context-demo.gif)

</details>

### Reference Multiple Files

```bash
copilot

> Compare @src/auth/login.js and @src/auth/register.js for consistency
```

### Reference an Entire Directory

```bash
copilot

> Review all files in @src/api/ for error handling
```

### Reference with Glob Patterns

```bash
copilot

> Find all TODO comments in @src/**/*.js
```

---

## Cross-File Intelligence

This is where context becomes a superpower. Single-file analysis is useful. Cross-file analysis is transformative.

### Demo: Find Bugs That Span Multiple Files

```bash
copilot

> @samples/buggy-code/js/userService.js @samples/buggy-code/js/paymentProcessor.js
>
> Find security vulnerabilities that span BOTH files. Look for patterns that are dangerous when these two modules work together.
```

<details>
<summary>🎬 See it in action!</summary>

![Multi-File Demo](images/multi-file-demo.gif)

</details>

**What Copilot discovers**:

```
Cross-Module Security Analysis
==============================

1. SYSTEMATIC SQL INJECTION (Both Files)
   Both files construct queries with string concatenation.
   This isn't one bug - it's a codebase-wide pattern.

   userService.js:12    "SELECT * FROM users WHERE id = " + userId
   paymentProcessor.js:28  "SELECT * FROM payments WHERE user = " + id

2. CROSS-MODULE DATA LEAKAGE (Critical)
   userService.js:34 logs the full user object including password hash
   paymentProcessor.js:45 logs transaction details referencing user data

   Impact: When these modules interact, password hashes from userService may be exposed in paymentProcessor's transaction logs!

3. SHARED HARDCODED KEY (Both Files)
   userService.js:8      const API_KEY = "sk_live_abc123"
   paymentProcessor.js:5 const API_KEY = "sk_live_abc123"

   Same production key hardcoded in two places = organizational issue
```

**Why this matters**: A single-file review would find SQL injection. Only cross-file analysis reveals:
- The **systematic nature** of the problem (codebase-wide, not a one-off)
- **Cross-module data flows** that leak sensitive information
- **Organizational patterns** suggesting deeper security culture issues

---

### Demo: Understand a Codebase in 60 Seconds

New to a project? Skip the hour of reading code:

```bash
copilot

> @samples/buggy-code/
>
> In one paragraph, what does this codebase do and what are its biggest architectural problems?
```

**What you get**:
```
This is a simple e-commerce backend with user authentication and payment
processing. The biggest architectural problems are:

1. No separation of concerns - database queries mixed with business logic
2. No input validation layer - each function validates (or doesn't) independently
3. No error handling strategy - some functions throw, some return null, some crash
4. Security as afterthought - authentication logic duplicated rather than centralized

Priority fix: Add a validation middleware and centralized auth before any new features.
```

**Result**: What takes an hour of code reading compressed into 10 seconds. You know exactly where to focus.

---

## Practical Examples

### Example 1: Code Review with Context

```bash
copilot

> @src/api/users.js Review this file for security issues

# Copilot now has the full file content and can give specific feedback:
# "Line 23: SQL query is vulnerable to injection..."
# "Line 45: Password is stored in plain text..."

> What about @src/api/auth.js?

# Now reviewing auth.js, but still aware of users.js context
```

### Example 2: Understanding a Codebase

```bash
copilot

> @package.json What does this project do?

# Copilot reads package.json and understands dependencies

> @src/ Give me an overview of the code structure

# Copilot scans the directory and summarizes

> How does the authentication flow work?

# Copilot can trace through the code it's already seen
```

### Example 3: Multi-File Refactoring

```bash
copilot

> @src/services/userService.js @src/services/productService.js
> These services have duplicated error handling. Extract a common pattern.

# Copilot sees both files and can suggest a shared abstraction
```

---

## Session Management

Sessions are automatically saved as you work. You can resume previous sessions to continue where you left off.

### Sessions Auto-Save

Every conversation is automatically saved. Just exit normally:

```bash
copilot

> @src/services/ Let's refactor these services to use async/await

[... do some work ...]

> /exit
```

### Resume the Most Recent Session

```bash
# Continue where you left off
copilot --continue
```

### Resume a Specific Session

```bash
# Pick from a list of sessions interactively
copilot --resume

# Or resume a specific session by ID
copilot --resume abc123
```

### Pick Up Where You Left Off

Imagine this workflow across multiple days:

```bash
# Monday: Start security audit
copilot

> /rename security-audit
> @samples/buggy-code/js/userService.js
> Review and number all security issues

Security Issues Found:
1. SQL Injection (line 12) - CRITICAL
2. XSS vulnerability (line 34) - HIGH
3. Hardcoded API key (line 8) - HIGH
4. Weak password comparison (line 56) - MEDIUM
5. Missing rate limiting - MEDIUM

> Fix issue #1 (SQL injection)
# Work on the fix...

> /exit
```

```bash
# Wednesday: Resume exactly where you left off
copilot --continue

> What issues remain unfixed from our security audit?

Remaining issues from our security-audit session:
2. XSS vulnerability (line 34) - HIGH
3. Hardcoded API key (line 8) - HIGH
4. Weak password comparison (line 56) - MEDIUM
5. Missing rate limiting - MEDIUM

Issue #1 (SQL injection) was fixed on Monday.

> Let's tackle issue #2 next
```

**What makes this powerful**: Days later, Copilot remembers:
- The exact file you were working on
- The numbered list of issues
- Which ones you've already addressed
- The context of your conversation

No re-explaining. No re-reading files. Just continue working.

---

### Switch Sessions While Working

Inside an interactive session, use the `/resume` command:

```bash
copilot

> /resume
# Shows a list of sessions to switch to
```

### Rename Your Session

```bash
copilot

> /rename backend-refactor
# Session renamed for easier identification
```

### View Session Info

```bash
copilot

> /session
# Shows current session details and workspace summary

> /usage
# Shows session metrics and statistics
```

### Share Your Session

```bash
copilot

> /share file ./my-session.md
# Exports session as a markdown file

> /share gist
# Creates a GitHub gist with the session
```

---

## Context-Aware Conversations

The magic happens when you have multi-turn conversations that build on each other.

### Example: Progressive Enhancement

```bash
copilot

> @src/components/Button.jsx Review this React component

Copilot: "The component looks good, but I notice:
1. No PropTypes or TypeScript types
2. No accessibility attributes
3. Could benefit from CSS-in-JS or CSS modules"

> Add TypeScript types

Copilot: "Here's the component with TypeScript..."
[Shows typed version]

> Now add accessibility attributes

Copilot: "Building on the typed version, here's accessibility..."
[Adds aria-label, role, keyboard handlers]

> Generate tests for this final version

Copilot: "Based on the component with types and accessibility..."
[Generates comprehensive tests]
```

Notice how each prompt builds on the previous work - this is the power of context.

---

## Understanding Context Windows

Every AI has a "context window" - the amount of text it can consider at once.

<img src="images/context-window-visualization.png" alt="Context Window Visualization" width="800"/>

*The context window is like a desk - it can only hold so much at once. Files, conversation history, and system prompts all take space.*

### What Happens at the Limit

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# As you add more files and conversation, this grows

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Warning: Approaching context limit

> @another-large-file.js

Context limit reached. Older context will be summarized.
```

### Managing Context

```bash
# Check current usage
> /context

# Clear and start fresh
> /clear

# Start new topic in same session
> /clear
> Let's switch to talking about the database...
```

### Context Efficiency Tips

| Situation | Action | Why |
|-----------|--------|-----|
| Starting new topic | `/clear` | Removes irrelevant context |
| Long conversation | `/compact` | Summarizes history, frees tokens |
| Need specific file | `@file.js` not `@folder/` | Loads only what you need |
| Hitting limits | Start new session | Fresh 128K context |
| Multiple topics | Use `/rename` per topic | Easy to resume right session |

### Best Practices for Large Codebases

1. **Be specific**: `@src/auth/login.js` instead of `@src/`
2. **Clear between topics**: Use `/clear` when switching focus
3. **Use `/compact`**: Summarize conversation to free up context
4. **Use multiple sessions**: One session per feature or topic

---

## Choosing What to Reference

Not all files are equal when it comes to context. Here's how to choose wisely:

### File Size Considerations

| File Size | Approximate Tokens | Strategy |
|-----------|-------------------|----------|
| Small (<100 lines) | ~500-1,500 tokens | Reference freely |
| Medium (100-500 lines) | ~1,500-7,500 tokens | Reference specific files |
| Large (500+ lines) | 7,500+ tokens | Be selective, use specific files |
| Very Large (1000+ lines) | 15,000+ tokens | Consider splitting or targeting sections |

**Rule of thumb**: A typical 128K token context window can hold approximately:
- ~30-50 medium files, OR
- ~10-15 large files, OR
- A mix of files plus substantial conversation

### What to Include vs. Exclude

**High value** (include these):
- Entry points (`index.js`, `main.py`, `app.ts`)
- The specific files you're asking about
- Files directly imported by your target file
- Configuration files (`package.json`, `tsconfig.json`)
- Type definitions or interfaces

**Lower value** (consider excluding):
- Generated files (`*.min.js`, bundled output)
- Node modules or vendor directories
- Large data files or fixtures
- Files unrelated to your question

### The Specificity Spectrum

```
Less specific ────────────────────────► More specific
@src/                                   @src/auth/login.js:23-45
     │                                       │
     └─ Scans everything                     └─ Just what you need
        (uses more context)                      (preserves context)
```

**When to go broad** (`@src/`):
- Initial codebase exploration
- Finding patterns across many files
- Architecture reviews

**When to go specific** (`@src/auth/login.js`):
- Debugging a particular issue
- Code review of a specific file
- Asking about a single function

### Practical Example: Staged Context Loading

```bash
copilot

# Step 1: Start with structure
> @package.json What frameworks does this project use?

# Step 2: Narrow based on answer
> @src/api/ Show me the API structure

# Step 3: Focus on what matters
> @src/api/users.js Review this specific endpoint

# Step 4: Add related files only as needed
> @src/api/users.js @src/models/User.js How does this endpoint use the User model?
```

This staged approach keeps context focused and efficient.

---

## Permission Patterns

By default, Copilot can access files in your current directory. For files elsewhere, you need to grant access.

### Add Directories

```bash
# Add a directory to the allowed list
copilot --add-dir /path/to/other/project

# Add multiple directories
copilot --add-dir ~/workspace --add-dir /tmp
```

### Allow All Paths

```bash
# Disable path restrictions entirely (use with caution)
copilot --allow-all-paths
```

### Inside a Session

```bash
copilot

> /add-dir /path/to/other/project
# Now you can reference files from that directory

> /list-dirs
# See all allowed directories
```

### For Automation

```bash
# Allow all permissions for non-interactive scripts
copilot -p "Review @src/" --allow-all

# Or use the memorable alias
copilot -p "Review @src/" --yolo
```

---

## Working with Images

You can include images in your conversations using the `@` syntax. Copilot can analyze screenshots, mockups, diagrams, and other visual content.

### Basic Image Reference

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analyzes the image and responds

> @mockup.png @current-design.png Compare these two designs

# You can also drag and drop images or paste from clipboard
```

### Supported Image Formats

| Format | Best For |
|--------|----------|
| PNG | Screenshots, UI mockups, diagrams |
| JPG/JPEG | Photos, complex images |
| GIF | Simple diagrams (first frame only) |
| WebP | Web screenshots |

### Practical Image Use Cases

**1. UI Debugging**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. Design Implementation**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. Error Analysis**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. Architecture Review**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. Before/After Comparison**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### Combining Images with Code

Images become even more powerful when combined with code context:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### Image Tips

- **Crop screenshots** to show only relevant portions (saves context tokens)
- **Use high contrast** for UI elements you want analyzed
- **Annotate if needed** - circle or highlight problem areas before uploading
- **One image per concept** - multiple images work, but be focused

---

## Hands-On Examples

### Example 1: Full Project Review

Create a small project structure:

```bash
mkdir -p sample-project/src sample-project/tests
```

```javascript
// sample-project/src/index.js
const express = require('express');
const app = express();

app.get('/users', (req, res) => {
  const users = db.query('SELECT * FROM users WHERE active = ' + req.query.active);
  res.json(users);
});

app.listen(3000);
```

```javascript
// sample-project/src/utils.js
function formatDate(date) {
  return date.toISOString();
}

function validateEmail(email) {
  return email.includes('@');
}

module.exports = { formatDate, validateEmail };
```

Now review it:

```bash
cd sample-project
copilot

> @src/ Give me a security and code quality review of this project

# Copilot will identify:
# - SQL injection in index.js
# - Weak email validation in utils.js
# - Missing error handling
```

### Example 2: Session Workflow

```bash
copilot

> /rename project-review
> @src/index.js Let's fix the SQL injection vulnerability

[Copilot suggests parameterized queries]

> Implement that fix
> Now update @src/utils.js to have proper email validation
> /exit

# Later - resume where you left off
copilot --continue

> Generate tests for the fixes we made
```

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **Cross-File Challenge**: Run the same security analysis but with Python files:
   ```bash
   copilot
   > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
   > Find issues that appear in BOTH files
   ```

2. **Session Challenge**: Start a session, name it with `/rename my-first-session`, work on something, exit with `/exit`, then run `copilot --continue`. Does it remember what you were doing?

3. **Context Challenge**: Run `/context` mid-session. How many tokens are you using? Try `/compact` and check again.

**Self-Check**: You understand context when you can explain why `@folder/` is more powerful than opening each file individually.

---

## Assignment

### Main Challenge: Multi-File Review

1. Clone or create a project with at least 3 source files
2. Start an interactive session
3. Use `@` to review each file individually
4. Ask Copilot to find patterns across all files: "What patterns are repeated across @src/?"
5. Ask for a refactoring suggestion that affects multiple files
6. Rename the session: `/rename review-session`
7. Exit, then resume with `copilot --continue` and continue where you left off

**Success criteria**: You should be able to resume a session with context spanning multiple files.

### Bonus Challenge: Context Limits

1. Find (or create) a large codebase
2. Start a session and reference multiple large files
3. Run `/context` to see usage
4. Approach the limit and observe how Copilot handles it
5. Practice clearing context and being more specific with file references

---

## Troubleshooting

### "File not found" errors

Make sure you're in the correct directory:

```bash
pwd  # Check current directory
ls   # List files

# Then start copilot and use relative paths
copilot

> Review @./src/index.js
```

### "Permission denied"

Add the directory to your allowed list:

```bash
copilot --add-dir /path/to/directory

# Or in a session:
> /add-dir /path/to/directory
```

### Context fills up too quickly

- Be more specific with file references
- Use `/clear` between different topics
- Split work across multiple sessions

---

## Key Takeaways

1. **`@` syntax** gives Copilot context about your specific code
2. **Multi-turn conversations** build on each other - context accumulates
3. **Sessions auto-save** - use `--continue` or `--resume` to pick up where you left off
4. **Context windows** have limits - manage them with `/context`, `/clear`, and `/compact`
5. **Permission flags** (`--add-dir`, `--allow-all-paths`) control what files Copilot can access

---

## What's Next

Now that you can give Copilot context, let's put it to work on real development tasks. The context techniques you just learned—file references, cross-file analysis, and session management—are the foundation for the powerful workflows in the next chapter.

In **[Chapter 03: Development Workflows](../03-development-workflows/README.md)**, you'll learn:

- Code review workflows
- Refactoring patterns
- Debugging assistance
- Test generation
- Git integration

---

**[← Back to Chapter 01](../01-setup-and-first-steps/README.md)** | **[Continue to Chapter 03 →](../03-development-workflows/README.md)**
