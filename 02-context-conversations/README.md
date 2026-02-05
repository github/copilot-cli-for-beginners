![Chapter 02: Context and Conversations](images/chapter-header.png)

> **What if AI could see your entire codebase, not just one file at a time?**

In this chapter, you'll unlock the real power of GitHub Copilot CLI: context. You'll learn to use the `@` syntax to reference files and directories, giving Copilot deep understanding of your codebase. You'll discover how to maintain conversations across sessions, resume work days later exactly where you left off, and see how cross-file analysis catches bugs that single-file reviews miss entirely.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Use the `@` syntax to reference files, directories, and images
- Resume previous sessions with `--resume` and `--continue`
- Understand how [context windows](../GLOSSARY.md#context-window) work
- Write effective multi-turn conversations
- Manage directory permissions for multi-project workflows

> ⏱️ **Estimated Time**: ~50 minutes (20 min reading + 30 min hands-on)

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

# Essential: Basic Context

This section covers everything you need to work effectively with context. Master these basics first.

---

## The @ Syntax

The `@` symbol references files and directories in your prompts. It's how you tell Copilot "look at this file."

> 💡 **Note**: All examples in this course use the `samples/` folder included in this repository, so you can try every command directly.

### Try It Now (No Setup Required)

You can try this with any file on your computer:

```bash
copilot

# Point at any file you have
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **Don't have a project handy?** Create a quick test file:
> ```bash
> echo "function greet(name) { return 'Hello ' + name; }" > test.js
> copilot
> > What does @test.js do?
> ```

### Basic @ Patterns

| Pattern | What It Does | Example Use |
|---------|--------------|-------------|
| `@file.js` | Reference a single file | `Review @samples/src/index.js` |
| `@folder/` | Reference all files in a directory | `Review @samples/src/api/` |
| `@file1.js @file2.js` | Reference multiple files | `Compare @samples/src/auth/login.js @samples/src/auth/register.js` |

### Reference a Single File

```bash
copilot

> Explain what @samples/src/utils/helpers.js does
```

<details>
<summary>🎬 See it in action!</summary>

![File Context Demo](images/file-context-demo.gif)

</details>

### Reference Multiple Files

```bash
copilot

> Compare @samples/src/auth/login.js and @samples/src/auth/register.js for consistency
```

### Reference an Entire Directory

```bash
copilot

> Review all files in @samples/src/api/ for error handling
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

> @samples/src/api/users.js Review this file for security issues

# Copilot now has the full file content and can give specific feedback:
# "Line 23: SQL query is vulnerable to injection..."
# "Line 45: Password is stored in plain text..."

> What about @samples/src/api/auth.js?

# Now reviewing auth.js, but still aware of users.js context
```

### Example 2: Understanding a Codebase

```bash
copilot

> @package.json What does this project do?

# Copilot reads package.json and understands dependencies

> @samples/src/ Give me an overview of the code structure

# Copilot scans the directory and summarizes

> How does the authentication flow work?

# Copilot can trace through the code it's already seen
```

### Example 3: Multi-File Refactoring

```bash
copilot

> @samples/src/services/userService.js @samples/src/services/productService.js
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

> @samples/src/services/ Let's refactor these services to use async/await

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

**🎉 You now know the essentials!** The `@` syntax for referencing files, and `--continue`/`--resume` for session management, are enough to be highly productive. Everything below is optional - return to it when you're ready.

---

# Optional: Going Deeper

> 💡 **For beginners**: The sections below are optional. Return to these once you're comfortable with the basics above. You can be very productive with just the basic @ syntax and session management covered earlier.

---

## Additional @ Patterns

For power users, Copilot supports glob patterns and image references:

| Pattern | What It Does |
|---------|--------------|
| `@folder/*.js` | All .js files in folder |
| `@**/*.test.js` | Recursive glob - find all test files anywhere |
| `@image.png` | Image file for UI review |

```bash
copilot

> Find all TODO comments in @samples/src/**/*.js
```

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

> @samples/src/components/Button.jsx Review this React component

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

1. **Be specific**: `@samples/src/auth/login.js` instead of `@samples/src/`
2. **Clear between topics**: Use `/clear` when switching focus
3. **Use `/compact`**: Summarize conversation to free up context
4. **Use multiple sessions**: One session per feature or topic

---

## Choosing What to Reference

Not all files are equal when it comes to context. Here's how to choose wisely:

### File Size Considerations

| File Size | Approximate [Tokens](../GLOSSARY.md#token) | Strategy |
|-----------|-------------------|----------|
| Small (<100 lines) | ~500-1,500 tokens | Reference freely |
| Medium (100-500 lines) | ~1,500-7,500 tokens | Reference specific files |
| Large (500+ lines) | 7,500+ tokens | Be selective, use specific files |
| Very Large (1000+ lines) | 15,000+ tokens | Consider splitting or targeting sections |

**Concrete examples:**
- A typical React component (200 lines) ≈ 3,000 tokens
- A Node.js API file (400 lines) ≈ 6,000 tokens
- Your package.json ≈ 200-500 tokens
- A short prompt + response ≈ 500-1,500 tokens

> 💡 **Quick estimate for code:** Multiply lines of code by ~15 to get approximate tokens. Keep in mind this is only an estimate.

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
@samples/src/                                   @samples/src/auth/login.js:23-45
     │                                       │
     └─ Scans everything                     └─ Just what you need
        (uses more context)                      (preserves context)
```

**When to go broad** (`@samples/src/`):
- Initial codebase exploration
- Finding patterns across many files
- Architecture reviews

**When to go specific** (`@samples/src/auth/login.js`):
- Debugging a particular issue
- Code review of a specific file
- Asking about a single function

### Practical Example: Staged Context Loading

```bash
copilot

# Step 1: Start with structure
> @package.json What frameworks does this project use?

# Step 2: Narrow based on answer
> @samples/src/api/ Show me the API structure

# Step 3: Focus on what matters
> @samples/src/api/users.js Review this specific endpoint

# Step 4: Add related files only as needed
> @samples/src/api/users.js @samples/src/models/User.js How does this endpoint use the User model?
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
copilot -p "Review @samples/src/" --allow-all

# Or use the memorable alias
copilot -p "Review @samples/src/" --yolo
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

> @screenshot-of-bug.png @samples/src/components/Header.jsx
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

> @samples/src/ Give me a security and code quality review of this project

# Copilot will identify:
# - SQL injection in index.js
# - Weak email validation in utils.js
# - Missing error handling
```

### Example 2: Session Workflow

```bash
copilot

> /rename project-review
> @samples/src/index.js Let's fix the SQL injection vulnerability

[Copilot suggests parameterized queries]

> Implement that fix
> Now update @samples/src/utils.js to have proper email validation
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
4. Ask Copilot to find patterns across all files: "What patterns are repeated across @samples/src/?"
5. Ask for a refactoring suggestion that affects multiple files
6. Rename the session: `/rename review-session`
7. Exit, then resume with `copilot --continue` and continue where you left off

**Success criteria**: You should be able to resume a session with context spanning multiple files.

<details>
<summary>💡 Hints (click to expand)</summary>

**Don't have a project?** Use this course repo! Try:
```bash
cd /path/to/github-copilot-cli-for-beginners
copilot
> @samples/buggy-code/js/ Review these files for common issues
> What patterns do you see across these files?
> /rename buggy-code-review
> /exit
```

Then resume with: `copilot --continue`

**Useful commands:**
- `@file.js` - Reference a single file
- `@folder/` - Reference all files in a folder (note the trailing `/`)
- `/context` - Check how much context you're using
- `/rename <name>` - Name your session for easy resuming

</details>

### Bonus Challenge: Context Limits

1. Find (or create) a large codebase
2. Start a session and reference multiple large files
3. Run `/context` to see usage
4. Approach the limit and observe how Copilot handles it
5. Practice clearing context and being more specific with file references

---

## Common Mistakes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Forgetting `@` before filenames | Copilot treats "src/index.js" as plain text | Use `@samples/src/index.js` to reference files |
| Expecting sessions to persist automatically | Starting `copilot` fresh loses all previous context | Use `--continue` (last session) or `--resume` (pick a session) |
| Referencing files outside current directory | "Permission denied" or "File not found" errors | Use `/add-dir /path/to/directory` to grant access |
| Not using `/clear` when switching topics | Old context confuses responses about the new topic | Run `/clear` before starting a different task |

---

## Troubleshooting

### "File not found" errors

Make sure you're in the correct directory:

```bash
pwd  # Check current directory
ls   # List files

# Then start copilot and use relative paths
copilot

> Review @samples/src/index.js
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

1. **`@` syntax** gives Copilot context about files, directories, and images
2. **Multi-turn conversations** build on each other as context accumulates
3. **Sessions auto-save**: use `--continue` or `--resume` to pick up where you left off
4. **Context windows** have limits: manage them with `/context`, `/clear`, and `/compact`
5. **Permission flags** (`--add-dir`, `--allow-all-paths`) control multi-directory access
6. **Image references** (`@screenshot.png`) help debug UI issues visually

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

## What's Next

Now that you can give Copilot context, let's put it to work on real development tasks. The context techniques you just learned (file references, cross-file analysis, and session management) are the foundation for the powerful workflows in the next chapter.

In **[Chapter 03: Development Workflows](../03-development-workflows/README.md)**, you'll learn:

- Code review workflows
- Refactoring patterns
- Debugging assistance
- Test generation
- Git integration

---

**[← Back to Chapter 01](../01-setup-and-first-steps/README.md)** | **[Continue to Chapter 03 →](../03-development-workflows/README.md)**
