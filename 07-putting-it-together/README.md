![Chapter 07: Putting It All Together](images/chapter-header.png)

> **Everything you learned combines here. Go from idea to merged PR in a single session.**

In this chapter, you'll bring together everything you've learned into complete workflows. You'll build features using multi-agent collaboration, set up pre-commit hooks that catch security issues before they're committed, integrate Copilot into CI/CD pipelines, and go from feature idea to merged PR in a single terminal session. This is where GitHub Copilot CLI becomes a genuine force multiplier.

> 💡 **Note**: This chapter shows how to combine everything you've learned. **You don't need agents, skills, or MCP to be productive (although they can be very helpful).** If you only completed Chapters 00-03, start with the [Minimal Workflow](#start-here-minimal-workflow-no-custom-setup-required) section - it covers a complete feature workflow using only built-in features.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Combine agents, skills, and MCP in unified workflows
- Build complete features using multi-tool approaches
- Set up basic automation with hooks
- Apply best practices for professional development

> ⏱️ **Estimated Time**: ~60 minutes (20 min reading + 40 min hands-on)

---

## Idea to Merged PR in One Session

This is the culmination of everything you've learned. Traditional development of a feature like "list unread books" takes hours. Watch what happens when you combine all your tools:

```bash
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot creates high-level plan...

# SWITCH TO PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What's the best approach?

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# SWITCH TO PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# IMPLEMENT
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TEST
> Generate comprehensive tests for the new feature

# SHIP
> /review
> Create a pull request titled "Feature: Add list unread books command"
```

---

<details>
<summary>🎬 See it in action!</summary>

![Full Review Demo](images/full-review-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

---

**Traditional approach**: 1-2 days of context-switching between tools

**The key insight**: You directed specialists like an architect. They handled the details. You handled the vision.

---

## Real-World Analogy: The Orchestra

A symphony orchestra has many sections:
- **Strings** provide the foundation (like your core workflows)
- **Brass** adds power (like agents with specialized expertise)
- **Woodwinds** add color (like skills that extend capabilities)
- **Percussion** keeps rhythm (like MCP connecting to external systems)

Individually, each section sounds limited. Together, conducted well, they create something magnificent.

That's what this chapter teaches: conducting your tools into a unified workflow.

<img src="images/orchestra-analogy.png" alt="Orchestra Analogy - Unified Workflow" width="800"/>

*Like a conductor with an orchestra, you orchestrate agents, skills, and MCP into unified workflows*

---

## Start Here: Minimal Workflow (No Custom Setup Required)

**This is the most important section.** The ["Idea to Merged PR"](#idea-to-merged-pr-in-one-session) example above uses agents and MCP for maximum power. But you can achieve the same result using just built-in features from Chapters 01-03:

```
1. Understand   →  Describe requirements, review existing code with @
2. Plan         →  Use /plan to outline the approach
3. Implement    →  Build the feature in interactive mode
4. Test         →  Generate tests with a prompt
5. Review       →  Use /review to check your changes
6. Ship         →  Generate commit message with -p
```

**This uses only:** Interactive mode (Ch 01), `@` syntax (Ch 02), `/plan` and `/review` (Ch 01 & 03), and `-p` mode (Ch 01).

**That's a complete feature workflow!** Everything below shows how to enhance this with agents, skills, and MCP - but you're already productive without them.

<details>
<summary>🎬 See the minimal workflow in action!</summary>

![Minimal Workflow Demo](images/minimal-workflow-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

---

## The Integration Pattern (For Power Users)

Here's the mental model for combining everything:

```
+-------------------------------------------------------------+
|                     YOUR WORKFLOW                            |
+-------------------------------------------------------------+
|                                                              |
|  1. GATHER CONTEXT (MCP)                                     |
|     Get issue details from GitHub                            |
|     Read relevant code files                                 |
|                                                              |
|  2. ANALYZE & PLAN (Agents)                                  |
|     Switch to backend agent for analysis                     |
|     Switch to security agent for review                      |
|                                                              |
|  3. EXECUTE (Skills + Manual)                                |
|     Ask naturally - skills load automatically                |
|     Implement the fix                                        |
|                                                              |
|  4. COMPLETE (MCP)                                           |
|     Create PR via GitHub                                     |
|     Request review                                           |
|                                                              |
+-------------------------------------------------------------+
```

---

## Workflow 1: Complete Feature Development (With Agents)

The ["Idea to Merged PR"](#idea-to-merged-pr-in-one-session) example at the top of this chapter demonstrates the full pattern. Here's a breakdown of the phases it follows - apply this to any feature:

| Phase | What You Do | Tools Used |
|-------|-------------|------------|
| 1. **Understand** | Describe requirements, check existing code | Interactive mode, `@` syntax |
| 2. **Design** | Switch to specialized agents for design and test planning | `/agent` (python-reviewer, pytest-helper) |
| 3. **Implement** | Build the feature with agent guidance | Interactive mode |
| 4. **Test** | Generate comprehensive tests | Skills (auto-triggered) |
| 5. **Ship** | Create PR with descriptive summary | MCP (GitHub) |

Adapt the prompts to your tech stack - the phased approach works whether you're building in Python, JavaScript, Go, or anything else.

---

## Workflow 2: Bug Investigation and Fix

Real-world bug fixing with full tool integration:

```bash
copilot

# PHASE 1: Understand the bug from GitHub (MCP provides this)
> Get the details of issue #1

# Learn: "find_by_author doesn't work with partial names"

# PHASE 2: Find related code
> @samples/book-app-project/books.py Show me the find_by_author method

# PHASE 3: Get expert analysis
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching

# Agent identifies: Method uses exact equality instead of substring matching

# PHASE 4: Research best practice
> What are the best practices for Python case-insensitive string matching?

# PHASE 5: Fix with agent guidance
> Implement the fix using lowercase comparison and 'in' operator

# PHASE 6: Generate tests
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# PHASE 7: Commit and PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## Workflow 3: Code Review Automation (Optional)

> 💡 **This section is optional.** Pre-commit hooks are useful for teams but not required to be productive. Skip this if you're just getting started.
>
> ⚠️ **Performance note**: This hook calls `copilot -p` for each staged file, which takes several seconds per file. For large commits, consider limiting to critical files or running reviews manually with `/review` instead.

Set up automated code review on your commits:

```bash

# Create a pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    REVIEW=$(timeout 60 copilot -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> 📚 **Official Documentation**: [Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) and [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) for the complete hooks API.

Now every commit gets a quick security review:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Output:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## Workflow 4: Multi-Agent Feature Planning

For features that require design and testing, use multiple agents:

```bash
copilot

> I need to add an "export to CSV" feature to the book app

# Get design from python-reviewer agent
> /agent
# Select "python-reviewer"

> Design the export feature:
> - File format and structure
> - Error handling for file I/O
> - Edge cases (empty collection, special characters)

# Python-reviewer agent produces:
# - CSV structure with headers
# - Using csv.DictWriter for safety
# - Exception handling recommendations

# Get test design from pytest-helper agent
> /agent
# Select "pytest-helper"

> Design test cases for the CSV export feature:
> - What should we test?
> - What fixtures do we need?
> - What edge cases should we cover?

# Pytest-helper agent produces:
# - Test cases for successful export
# - Test cases for empty collections
# - Test cases for file write errors

# Synthesize into implementation plan
> Create a step-by-step implementation plan for the export feature
```

---

## Workflow 5: Onboarding to a New Codebase

When joining a new project:

```bash
copilot

# Understand project structure
> Give me an overview of this project structure

# Understand dependencies
> @samples/book-app-project/book_app.py What does this application do?

# Understand architecture
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# Find the entry point
> Where does the application start? Show me the main entry point.

# Understand key flows
> Walk me through how adding a book flows through the code

# Check for issues to work on
> List open issues labeled "good first issue"
```

---

## Best Practices

### 1. Start with Context Before Analysis

Always gather context before asking for analysis:

```bash
# Good
> Get the details of issue #42
> /agent
# Select backend
> Analyze this issue

# Less effective
> /agent
# Select backend
> Fix login bug
# Agent doesn't have issue context
```

### 2. Use Agents for Analysis, Skills for Execution

```bash
# Agent analyzes
> /agent
# Select security
> Review this authentication code

# Skill executes (automatically triggered by your prompt)
> Generate comprehensive tests for this code
```

### 3. Keep Sessions Focused

```bash
# Good: One feature per session
> /rename list-unread-feature
# Work on list unread
> /exit

copilot
> /rename export-csv-feature
# Work on CSV export
> /exit

# Less effective: Everything in one long session
```

### 4. Create Reusable Workflows

Document your workflows so you can repeat them:

```markdown
## Bug Fix Workflow

1. Get issue details from GitHub
2. Search for related code
3. Switch to python-reviewer agent for analysis
4. Implement fix
5. Switch to pytest-helper agent for test design
6. Generate tests
7. Create PR
```

---

## Bonus: Production Patterns

These patterns are optional but valuable for professional environments.

### PR Description Generator

```bash
# Generate comprehensive PR descriptions
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD Integration

For teams with existing CI/CD pipelines, you can automate Copilot reviews on every pull request using GitHub Actions. This includes posting review comments automatically and filtering for critical issues.

> 📖 **Learn more**: See [CI/CD Integration](../appendices/ci-cd-integration.md) for complete GitHub Actions workflows, configuration options, and troubleshooting tips.

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **End-to-End Challenge**: Pick a small feature (e.g., "list unread books" or "export to CSV"). Use the full workflow:
   - Plan with `/plan`
   - Design with agents (python-reviewer, pytest-helper)
   - Implement
   - Generate tests
   - Create PR

2. **Automation Challenge**: Set up the pre-commit hook from the Code Review Automation workflow. Make a commit with an intentional file path vulnerability. Does it get blocked?

3. **Your Production Workflow**: Design your own workflow for a common task you do. Write it down as a checklist. What parts could be automated with skills, agents, or hooks?

**Self-Check**: You've completed the course when you can explain to a colleague how agents, skills, and MCP work together - and when to use each.

---

## Assignment

### Main Challenge: End-to-End Feature

The hands-on examples walked through building a "list unread books" feature. Now practice the full workflow on a different feature — **search books by year range**:

1. Start Copilot and gather context: `@samples/book-app-project/books.py`
2. Plan with `/plan Add a "search by year" command that lets users find books published between two years`
3. Implement a `find_by_year_range(start_year, end_year)` method in `BookCollection`
4. Add a `handle_search_year()` function in `book_app.py` that prompts the user for start and end years
5. Generate tests: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. Review with `/review`
7. Update the README: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. Generate a commit message

Document your workflow as you go.

**Success criteria**: You've completed the feature from idea to commit using Copilot CLI, including planning, implementation, tests, documentation, and review.

> 💡 **Bonus**: If you have agents set up from Chapter 04, try using `/agent` to switch to your error-handler agent for implementation review and your doc-writer agent for the README update.

<details>
<summary>💡 Hints (click to expand)</summary>

**Follow the pattern from the ["Idea to Merged PR"](#idea-to-merged-pr-in-one-session) example** at the top of this chapter. The key steps are:

1. Gather context with `@samples/book-app-project/books.py`
2. Plan with `/plan Add a "search by year" command`
3. Implement the method and command handler
4. Generate tests with edge cases (invalid input, empty results, reversed range)
5. Review with `/review`
6. Update README with `@samples/book-app-project/README.md`
7. Generate commit message with `-p`

**Edge cases to think about:**
- What if the user enters "2000" and "1990" (reversed range)?
- What if no books match the range?
- What if the user enters non-numeric input?

**The key is practicing the full workflow** from idea → context → plan → implement → test → document → commit.

</details>

### Bonus Challenge: Workflow Automation

1. Create a pre-commit hook that runs Copilot review
2. Set up a custom shell function for your most common workflow
3. Document your workflow in a team-shareable format

---

<details>
<summary>🔧 <strong>Common Mistakes</strong> (click to expand)</summary>

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Jumping straight to implementation | Miss design issues that are costly to fix later | Use `/plan` first to think through the approach |
| Using one tool when multiple would help | Slower, less thorough results | Combine: Agent for analysis → Skill for execution → MCP for integration |
| Not reviewing before committing | Security issues or bugs slip through | Always run `/review` or use a [pre-commit hook](#workflow-3-code-review-automation) |
| Forgetting to share workflows with team | Each person reinvents the wheel | Document patterns in shared agents, skills, and instructions |

</details>

---

## Course Complete!

Congratulations! You've learned:

| Chapter | What You Mastered |
|---------|-------------------|
| 00 | Instant value with quick start |
| 01 | Three modes of interaction |
| 02 | Context management with @ syntax |
| 03 | Development workflows |
| 04 | Specialized agents |
| 05 | Extensible skills |
| 06 | External connections with MCP |
| 07 | Unified production workflows |

You're now equipped to use GitHub Copilot CLI as a genuine force multiplier in your development workflow.

---

## What's Next?

Your learning doesn't stop here:

1. **Practice daily**: Use Copilot CLI for real work
2. **Build custom tools**: Create agents and skills for your specific needs
3. **Share knowledge**: Help your team adopt these workflows
4. **Stay updated**: Follow GitHub Copilot updates for new features

### Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Community Skills](https://github.com/topics/copilot-skill)

---

## Key Takeaways

1. **Integration > Isolation**: Combine tools for maximum impact
2. **Context first**: Always gather context before analysis
3. **Agents analyze, Skills execute**: Use the right tool for the job
4. **Automate repetition**: Hooks and scripts multiply your effectiveness
5. **Document workflows**: Shareable patterns benefit the whole team

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

**You did it! Now go build something amazing.**

**[← Back to Chapter 06](../06-mcp-servers/README.md)** | **[Return to Course Home →](../README.md)**
