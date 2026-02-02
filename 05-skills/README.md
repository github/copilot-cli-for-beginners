![Chapter 05: Skills System](images/chapter-header.png)

> **What if Copilot could automatically apply your team's best practices without you having to explain them every time?**

In this chapter, you'll learn about Agent Skills: folders of instructions that Copilot automatically loads when relevant to your task. While agents change *how* Copilot thinks, skills teach Copilot *specific ways to complete tasks*. You'll create a security audit skill that Copilot applies whenever you ask about security, build team-standard review criteria that ensure consistent code quality, and learn how skills work across Copilot CLI, VS Code, and the Copilot coding agent.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Understand how Agent Skills work (automatic loading, not manual commands)
- Create custom skills with SKILL.md files
- Use community skills from shared repositories
- Know when to use skills vs agents vs MCP

---

## Real-World Analogy: Power Tools

A general-purpose drill is useful, but specialized attachments make it powerful:

| Attachment | Purpose |
|------------|---------|
| Screwdriver bit | Drive screws quickly |
| Hole saw | Cut perfect circles |
| Sanding disc | Smooth surfaces |
| Wire brush | Remove rust |

Skills work the same way. They're specialized tools that extend what Copilot can do.

<img src="images/power-tools-analogy.png" alt="Power Tools - Skills Extend Copilot's Capabilities" width="800"/>

*Skills are specialized attachments that extend what Copilot can do*

---

## Understanding Skills

Agent Skills are folders containing instructions, scripts, and resources that Copilot **automatically loads when relevant** to your task. Copilot reads your prompt, checks if any skills match, and applies the relevant instructions automatically.

```bash
copilot

> Review src/api/users.js for security issues
# Copilot detects this matches your "security-audit" skill
# and automatically applies its OWASP checklist

> Generate tests for the login function
# Copilot loads your "generate-tests" skill
# and applies your preferred test structure

> What are the code quality issues in this file?
# Copilot loads your "code-review" skill
# and checks against your team's standards
```

> 💡 **Key Insight**: Skills are **automatically triggered** based on your prompt matching the skill's description. You don't need to type a special command - just ask naturally, and Copilot applies relevant skills behind the scenes.

### Direct Slash Command Invocation

While auto-triggering is the primary way skills work, you can also **invoke skills directly** using their name as a slash command:

```bash
# Invoke a skill directly by name with your prompt
> /generate-tests Create tests for the user authentication module
> /code-review Check src/utils.js for security issues
> /security-audit Review the API endpoints
```

This gives you explicit control when you want to ensure a specific skill is used.

> 📝 **Skills vs Agents Invocation**: Don't confuse skill invocation with agent invocation:
> - **Skills**: `/skill-name <prompt>` — e.g., `/code-review Check this file`
> - **Agents**: `/agent` (select from list) or `copilot --agent <name>` (command line)
> 
> If you have both a skill and an agent with the same name (e.g., "code-reviewer"), typing `/code-reviewer` invokes the **skill**, not the agent.

### How Do I Know a Skill Was Used?

You can ask Copilot directly:

```bash
> What skills did you use for that response?

# Or before asking:
> What skills do you have available for security reviews?
```

### Skills vs Agents vs MCP

<img src="images/skills-agents-mcp-comparison.png" alt="Comparison diagram showing the differences between Agents, Skills, and MCP Servers and how they combine into your workflow" width="800"/>

*Three ways to extend Copilot CLI: Agents change how it thinks, Skills provide task-specific instructions, MCP connects to external services*

| Feature | What It Does | When to Use |
|---------|--------------|-------------|
| **Agents** | Changes how AI thinks | Need specialized expertise across many tasks |
| **Skills** | Provides task-specific instructions (auto-loaded) | Specific, repeatable tasks with detailed steps |
| **MCP** | Connects external services | Need live data from APIs |

**Quick rule**: Use agents for broad expertise, skills for specific task instructions, and MCP for external data.

> 📚 **Learn More**: See the official [About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) documentation for the complete reference on skill formats and best practices.

---

## Finding and Using Community Skills

### Community Skill Repositories

Pre-made skills are available from community repositories:

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - Official GitHub Copilot resources including skills documentation and examples

### Installing a Community Skill

To use a community skill, copy its folder to your skills directory:

```bash
# Clone the awesome-copilot repository
git clone https://github.com/github/awesome-copilot.git /tmp/awesome-copilot

# Copy a specific skill to your skills directory
cp -r /tmp/awesome-copilot/skills/code-review ~/.copilot/skills/

# Or for project-specific use
cp -r /tmp/awesome-copilot/skills/code-review .github/skills/
```

### Viewing Your Installed Skills

```bash
# List global skills
ls ~/.copilot/skills/

# List project skills
ls .github/skills/

# View a skill's instructions
cat ~/.copilot/skills/code-review/SKILL.md
```

<details>
<summary>🎬 See it in action!</summary>

![List Skills Demo](images/list-skills-demo.gif)

</details>

### How Copilot Finds Skills

Copilot automatically scans these locations for skills:

| Location | Scope |
|----------|-------|
| `.github/skills/` | Project-specific (shared with team via git) |
| `.claude/skills/` | Project-specific (Claude Code compatible) |
| `~/.copilot/skills/` | Global (your personal skills) |
| `~/.claude/skills/` | Global (Claude Code compatible) |

> 💡 **Cross-Platform**: If you've already set up skills for Claude Code in `.claude/skills/`, Copilot picks them up automatically!

---

## From Manual Prompts to Automatic Expertise

> 💡 **Why show benefits first?** Before diving into how to create skills, let's see *why* they're worth learning. Once you see the consistency gains, the "how" will make more sense.

### Before Skills: Inconsistent Reviews

Every code review, you might forget something:

```bash
copilot

> Review this code for issues
# Generic review - might miss your team's specific concerns
```

Or you write a long prompt every time:

```bash
> Review this code checking for SQL injection, XSS, hardcoded secrets,
> missing error handling, functions over 50 lines, console.log statements,
> and make sure all async operations have try/catch blocks...
```

Time: **30+ seconds** to type. Consistency: **varies by memory**.

### After Skills: Automatic Best Practices

With a `code-review` skill installed, just ask naturally:

```bash
copilot

> Review the authentication code for issues
```

**What happens behind the scenes**:
1. Copilot sees "review" and "issues" in your prompt
2. Checks skill descriptions, finds your `code-review` skill matches
3. Automatically loads your team's 15-point checklist
4. Applies all checks without you listing them

**Output**:
```
Code Review: src/auth/login.js

[CRITICAL] SQL Injection (line 23)
  Query uses string concatenation
  Fix: Use parameterized queries

[HIGH] Missing rate limiting
  Login endpoint has no rate limiting
  Fix: Add express-rate-limit middleware

[MEDIUM] Console.log in production code (line 45)
  Debug statement should be removed

✅ Error handling: All async operations have try/catch
✅ Function length: All functions under 50 lines
```

**The difference**: Your team's standards are applied automatically, every time, without typing them out.

---

## Consistency at Scale: Team PR Review Skill

Imagine your team has a 10-point PR checklist. Without a skill, every developer must remember all 10 points, and someone always forgets #6 or #9.

With a `pr-review` skill, the entire team gets consistent reviews:

```bash
copilot

> Can you review this PR?
```

Copilot automatically loads your team's `pr-review` skill and checks all 10 points:

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- Parameterized queries used

## Code Quality ⚠️
- [WARN] console.log on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**The power**: Every team member applies the same standards automatically. New hires don't need to memorize the checklist because the skill handles it.

---

## How Skills Get Triggered

Skills activate automatically based on your prompt matching the skill's description. You don't invoke them explicitly. Copilot decides when they're relevant.

### Automatic Matching

```bash
copilot

> Check this code for security vulnerabilities
# Copilot matches "security vulnerabilities" to your
# security-audit skill and loads its OWASP checklist

> @src/api/users.js Are there any issues with this file?
# Copilot loads your code-review skill based on
# "issues" matching the skill's description
```

### Writing Good Skill Descriptions

The `description` field in your SKILL.md is crucial because it's how Copilot decides whether to use your skill:

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **Tip**: Include keywords in your description that match how you naturally ask questions. If you say "security review," include "security review" in the description.

### Combining Skills with Agents

Skills and agents work together. The agent provides expertise, the skill provides specific instructions:

```bash
# Start with a backend agent
copilot --agent backend

> Review the API endpoints for issues
# Backend agent's Node.js/Express expertise combines
# with your code-review skill's checklist
```

---

## Skill Locations

Skills are discovered from multiple locations. Project-specific skills take priority over global ones:

| Location | Scope | Use Case |
|----------|-------|----------|
| `.github/skills/` | Project | Team standards, shared via git |
| `.claude/skills/` | Project | Claude Code compatible skills |
| `~/.copilot/skills/` | Global | Personal skills across all projects |
| `~/.claude/skills/` | Global | Claude Code personal skills |

**Pro tip**: Create project-specific skills in `.github/skills/` to share them with your team via git. They'll be version-controlled and available to everyone who clones the repo.

---

## Managing Skills with the `/skills` Command

Use the `/skills` command to manage your installed skills:

| Command | What It Does |
|---------|--------------|
| `/skills list` | Show all installed skills |
| `/skills info <name>` | Get details about a specific skill |
| `/skills add <name>` | Enable a skill (from a repository or marketplace) |
| `/skills remove <name>` | Disable or uninstall a skill |
| `/skills reload` | Reload skills after editing SKILL.md files |

> 💡 **Remember**: You don't need to "activate" skills for each prompt. Once installed, skills are **automatically triggered** when your prompt matches their description. These commands are for managing which skills are available, not for using them.

### Example: View Your Skills

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-review: Team-standard code review checklist
...

> /skills info security-audit

Name: security-audit
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
Location: ~/.copilot/skills/security-audit/
```

### When to Use /skills reload

After creating or editing a skill's SKILL.md file, run `/skills reload` to pick up the changes without restarting Copilot:

```bash
# Edit your skill file
# Then in Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **Good to know**: Skills remain effective even after using `/compact` to summarize your conversation history. No need to reload after compacting.

---

## Creating Custom Skills

Skills are stored in `~/.copilot/skills/` (global) or `.github/skills/` (project-specific).

### Skill Structure

Each skill lives in its own folder with a `SKILL.md` file. You can optionally include scripts, examples, or other resources:

```
~/.copilot/skills/
└── my-skill/
    ├── SKILL.md           # Required: Skill definition and instructions
    ├── examples/          # Optional: Example files Copilot can reference
    │   └── sample.ts
    └── scripts/           # Optional: Scripts the skill can use
        └── validate.sh
```

> 💡 **Tip**: The directory name should match the `name` in your SKILL.md frontmatter (lowercase with hyphens).

### SKILL.md Format

Skills use a simple markdown format with YAML frontmatter:

```markdown
---
name: my-code-review
description: Comprehensive code review with security, performance, and maintainability checks
license: MIT
---

# Code Review

When reviewing code, check for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML Properties:**

| Property | Required | Description |
|----------|----------|-------------|
| `name` | **Yes** | Unique identifier (lowercase, hyphens for spaces) |
| `description` | **Yes** | What the skill does and when Copilot should use it |
| `license` | No | License that applies to this skill |

> 📖 **Official docs**: [About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

### Creating Your First Skill

```bash
# Create skill directory
mkdir -p ~/.copilot/skills/security-audit

# Create the SKILL.md file
cat > ~/.copilot/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Test your skill (skills load automatically based on your prompt)
copilot

> @src/api/ Check this code for security vulnerabilities
# Copilot detects "security vulnerabilities" matches your skill
# and automatically applies its OWASP checklist
```

---

## Hands-On Examples

### Example 1: Test Generation Skill

```bash
# Create skill
mkdir -p ~/.copilot/skills/generate-tests

cat > ~/.copilot/skills/generate-tests/SKILL.md << 'EOF'
---
name: generate-tests
description: Generate comprehensive unit tests with edge cases
---

# Test Generation

Generate unit tests that include:

## Test Structure
- Use describe/it blocks (Jest style)
- One assertion per test when possible
- Clear test names describing expected behavior

## Coverage
- Happy path scenarios
- Edge cases: null, undefined, empty strings
- Boundary values
- Error scenarios

## Mocking
- Mock external dependencies
- Mock API calls with realistic responses
- Mock database operations

## Output
Provide complete, runnable test file.
EOF
```

### Example 2: Documentation Skill

```bash
mkdir -p ~/.copilot/skills/document-api

cat > ~/.copilot/skills/document-api/SKILL.md << 'EOF'
---
name: document-api
description: Generate API documentation in OpenAPI format
---

# API Documentation

Generate documentation including:

## For Each Endpoint
- HTTP method and path
- Description of what it does
- Request parameters (query, path, body)
- Request body schema with examples
- Response schemas for all status codes
- Example requests and responses

## Format
Output as OpenAPI 3.0 YAML.
EOF
```

### Example 3: Commit Message Skill

```bash
mkdir -p ~/.copilot/skills/commit-msg

cat > ~/.copilot/skills/commit-msg/SKILL.md << 'EOF'
---
name: commit-msg
description: Generate conventional commit messages
---

# Commit Message Generation

Generate commit messages following Conventional Commits:

## Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Types
- feat: New feature
- fix: Bug fix
- docs: Documentation only
- style: Formatting, no code change
- refactor: Code change that neither fixes nor adds
- perf: Performance improvement
- test: Adding tests
- chore: Maintenance

## Rules
- Subject line max 72 characters
- Use imperative mood ("add" not "added")
- Body explains what and why, not how
EOF
```

### Example 4: Team PR Review Skill

```bash
mkdir -p ~/.copilot/skills/pr-review

cat > ~/.copilot/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] SQL queries use parameterized statements
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No console.log/print statements
- [ ] Error handling for all async operations
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **Skill Creation Challenge**: Create a `quick-review` skill that does a 3-point checklist:
   - Security issues
   - Missing error handling
   - Unclear variable names

   Test it by asking: "Do a quick review of userService.js"

2. **Skill Comparison**: Time yourself writing a detailed security review prompt manually. Then just ask "Check for security issues in this file" and let your security-audit skill load automatically. How much time did the skill save?

3. **Team Skill Challenge**: Think about your team's code review checklist. Could you encode it as a skill? Write down 3 things the skill should always check.

**Self-Check**: You understand skills when you can explain why the `description` field matters (it's how Copilot decides whether to load your skill).

---

## Assignment

### Main Challenge: Create Your Own Skill

1. List your current skills: `ls ~/.copilot/skills/`
2. Create a skill that solves a repetitive task you do
3. Your skill should have:
   - Clear name and description (description is crucial for matching!)
   - Specific instructions for the task
   - Expected output format
4. Test the skill by asking Copilot a question that should trigger it

**Success criteria**: You have a working custom skill that Copilot automatically applies when relevant.

### Bonus Challenge: Share Your Skill

1. Document your skill with examples
2. Create a GitHub repo with the `copilot-skill` or `agent-skill` topic
3. Include a README explaining what prompts trigger the skill

---

## Troubleshooting

### Skill not being used

If Copilot isn't using your skill when expected:

1. **Check the description**: Does it match how you're asking?
   ```markdown
   # Bad: Too vague
   description: Reviews code

   # Good: Includes trigger words
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **Verify the file location**:
   ```bash
   # Global skills
   ls ~/.copilot/skills/

   # Project skills
   ls .github/skills/
   ```

3. **Check SKILL.md format**: Frontmatter is required:
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

### Skill not appearing

Verify the folder structure:
```
~/.copilot/skills/
└── my-skill/           # Folder name
    └── SKILL.md        # Must be exactly SKILL.md (case-sensitive)
```

### Testing if a skill loads

Ask Copilot directly:
```bash
> What skills do you have available for code review?
# Copilot will describe relevant skills it found
```

### How do I know my skill is actually working?

1. **Check the output format**: If your skill specifies an output format (like `[CRITICAL]` tags), look for that in the response
2. **Ask directly**: After getting a response, ask "Did you use any skills for that?"
3. **Compare with/without**: Try the same prompt with `--no-custom-instructions` to see the difference:
   ```bash
   # With skills
   copilot -p "Review @file.js for security issues"

   # Without skills (baseline comparison)
   copilot -p "Review @file.js for security issues" --no-custom-instructions
   ```
4. **Check for specific checks**: If your skill includes specific checks (like "functions over 50 lines"), see if those appear in the output

---

## Key Takeaways

1. **Skills are automatic**: Copilot loads them when your prompt matches the skill's description
2. **Direct invocation**: You can also invoke skills directly with `/skill-name` as a slash command
3. **SKILL.md format**: YAML frontmatter (name, description, optional license) plus markdown instructions
4. **Locations matter**: `.github/skills/` for team sharing, `~/.copilot/skills/` for personal use
5. **Cross-platform**: Same skill format works in Copilot CLI, VS Code, and Claude Code
6. **Description is key**: Write descriptions that match how you naturally ask questions

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

## What's Next

Skills extend what Copilot can do with auto-loaded instructions. But what about connecting to external services? That's where MCP comes in.

In **[Chapter 06: MCP Servers](../06-mcp-servers/README.md)**, you'll learn:

- What MCP (Model Context Protocol) is
- Connecting to GitHub, databases, and APIs
- Configuring MCP servers
- Multi-server workflows

---

**[← Back to Chapter 04](../04-agents-custom-instructions/README.md)** | **[Continue to Chapter 06 →](../06-mcp-servers/README.md)**
