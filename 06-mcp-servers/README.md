![Chapter 06: MCP Servers](images/chapter-header.png)

> **What if Copilot could read your GitHub issues, check your database, and create PRs... all from the terminal?**

In this chapter, you'll connect Copilot to the outside world using MCP (Model Context Protocol). You'll configure servers for GitHub, filesystem access, and documentation, then experience the magic of going from "Get issue #42" to "Create a PR with the fix" - all without leaving your terminal. You'll also learn to build your own MCP servers to connect any API you need.

## Learning Objectives

By the end of this chapter, you'll be able to:

- Understand what MCP is and why it matters
- Manage MCP servers using `/mcp` commands
- Configure MCP servers for GitHub, filesystem, and documentation
- Use MCP in your daily workflows
- Build a basic custom MCP server

> ⏱️ **Estimated Time**: ~45 minutes (20 min reading + 25 min hands-on)

---

## 🚀 Start Here: MCP in 30 Seconds

**What is MCP?** It connects Copilot to external services (GitHub, databases, APIs) so it can read real data instead of just analyzing files.

**Quickest way to see it work:** The GitHub MCP is included by default. Try this:

```bash
copilot
> List my recent pull requests
```

If it works, MCP is already set up! If not, this chapter shows you how.

**Time estimate:** Basic setup takes ~10-15 minutes. Most time is spent getting a GitHub token.

---

## Real-World Analogy: Browser Extensions

Think of MCP servers like browser extensions:

| Extension | What It Does |
|-----------|--------------|
| Password manager | Connects browser to your vault |
| GitHub | Adds GitHub features to any page |
| Grammarly | Connects to writing analysis service |

MCP servers do the same thing for Copilot. They connect it to external services so it can read GitHub issues, query databases, fetch documentation, and more.

<img src="images/browser-extensions-analogy.png" alt="MCP Servers are like Browser Extensions" width="800"/>

*MCP servers connect Copilot to the outside world: GitHub, databases, documentation, and more*

---

## What is MCP?

MCP (Model Context Protocol) is a standard for connecting AI assistants to external data sources.

**Without MCP:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**With MCP:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP makes Copilot aware of your actual development environment.

> 📚 **Official Documentation**: [About MCP](https://docs.github.com/copilot/concepts/context/mcp) for a deeper look at how MCP works with GitHub Copilot.

---

## Managing MCP Servers

Use the `/mcp` command to manage MCP servers:

| Command | What It Does |
|---------|--------------|
| `/mcp show` | Show all configured MCP servers and their status |
| `/mcp add` | Interactive setup for adding a new server |
| `/mcp edit <server-name>` | Edit an existing server configuration |
| `/mcp enable <server-name>` | Enable a disabled server |
| `/mcp disable <server-name>` | Temporarily disable a server |
| `/mcp delete <server-name>` | Remove a server permanently |

### Example: Check Your MCP Servers

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
✗ postgres (disabled) - PostgreSQL database

> /mcp enable postgres
Server 'postgres' enabled.
```

---

<details>
<summary>🎬 See it in action!</summary>

![MCP Status Demo](images/mcp-status-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

---

## MCP Configuration File

MCP servers are configured in `~/.copilot/mcp-config.json` (global) or `.copilot/mcp-config.json` (project).

### Understanding the JSON Format

> 💡 **New to JSON?** JSON is just a way to write configuration data. Here's what each part means:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

| Field | What It Means |
|-------|---------------|
| `"mcpServers"` | Container for all your MCP server configurations |
| `"server-name"` | A name you choose (e.g., "github", "filesystem") |
| `"type": "local"` | The server runs on your machine |
| `"command": "npx"` | The program to run (npx runs npm packages) |
| `"args": [...]` | Arguments passed to the command |
| `"tools": ["*"]` | Allow all tools from this server |

**Important JSON rules:**
- Use double quotes `"` for strings (not single quotes)
- No trailing commas after the last item
- File must be valid JSON (use a [JSON validator](https://jsonlint.com/) if unsure)

---

## MCP Server 1: Filesystem

Access files with additional capabilities beyond basic `@` syntax.

### Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"],
      "tools": ["*"]
    }
  }
}
```

### Usage

Once configured, the filesystem MCP provides tools that Copilot can use automatically:

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

---

## MCP Server 2: GitHub

The GitHub MCP server is **built-in** - if you logged into Copilot (which you did during initial setup), it already works. No configuration needed!

> 💡 **Not working?** Run `/login` to re-authenticate with GitHub.

### Authentication in Dev Containers

If you're using this course in a Codespace or dev container, here's how authentication works:

- **GitHub Codespaces** (recommended): Authentication is automatic. The `gh` CLI inherits your Codespace token. No action needed.
- **Local dev container (Docker)**: Run `gh auth login` after the container starts, then restart Copilot.

**Troubleshooting authentication:**
```bash
# Check if you're authenticated
gh auth status

# If not, log in
gh auth login

# Verify GitHub MCP is connected
copilot
> /mcp show
```

### What You Can Do

| Feature | Examples |
|---------|----------|
| **Issues** | List, create, search, and comment on issues |
| **Pull requests** | View PRs, diffs, create PRs, check status |
| **Code search** | Search across repositories |
| **Actions** | Query workflow runs and status |
| **Copilot Spaces** | Access collaborative workspaces |

### Usage

```bash
copilot

# Create an issue for book app improvement
> Create a GitHub issue titled "Add year range search to book app" with
> description "Users should be able to search for books published in a
> specific year range"

Created issue #5: Add year range search to book app
URL: https://github.com/org/repo/issues/5

# Full issue-to-PR workflow
> What's in issue #1?

Issue #1: Search by author doesn't work for partial names
Status: Open
Labels: bug, enhancement
Description: Users should be able to search for "King" and find
"Stephen King". Currently requires exact match.

> @samples/book-app-project/books.py Implement the feature described in issue #1

[Shows implementation with fuzzy search logic]

> Create a pull request for these changes

Created PR #6: Add fuzzy author search to book collection
Base: main
Head: feature/fuzzy-author-search
References: #1
Status: Ready for review
```

---

## MCP Server 3: Context7 (Documentation)

Context7 gives Copilot access to up-to-date documentation for popular frameworks and libraries. Instead of relying on training data that might be outdated, Copilot fetches the actual current documentation.

**Supported documentation sources include:**
- Django, Flask, FastAPI, SQLAlchemy
- PostgreSQL, MongoDB, Redis
- React, Vue, Angular, Node.js
- TypeScript, JavaScript, Go, Rust
- And many more...

### Configuration

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

### Setup Requirements

✅ **No API key required** - Context7 works out of the box
✅ **No account needed** - Just add the configuration
✅ **Automatic updates** - Documentation is fetched in real-time
✅ **Your code stays local** - Context7 fetches public library documentation; your project files are not sent to their servers

**That's it!** Once configured, Copilot automatically uses Context7 when you ask about frameworks or libraries.

### Usage

```bash
copilot

> What's the best practice for database connection management in Python?

From SQLAlchemy Documentation:

## Connection Management

Use context managers to ensure connections are properly closed:

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///books.db")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM books"))
    for row in result:
        print(row)
# Connection automatically closed when exiting the 'with' block
```

Best practices:
- Use context managers for automatic cleanup
- Use connection pooling for production
- Handle connection errors gracefully
- Close connections in finally blocks

> How do I apply this to the book app's data persistence?

# Copilot now knows the official SQLAlchemy patterns
# and can apply them to your specific code
```

---

## Complete Configuration File

Here's a full `mcp-config.json` with filesystem and Context7 servers:

> 💡 **Note:** GitHub MCP is built-in - you don't need to add it to your config file. It uses your `/login` authentication automatically.

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

Save this as `~/.copilot/mcp-config.json` for global access or `.copilot/mcp-config.json` for project-specific configuration.

---

## Putting MCP to Work: Real Workflows

Now that you have MCP configured, let's see what it can do. These workflows demonstrate why developers say "I never want to work without this again."

### Issue to Fix to PR: Without Leaving Terminal

This is the moment developers say "I never want to work without this again."

<img src="images/issue-to-pr-workflow.png" alt="Issue to PR Workflow using MCP - Shows the complete flow from getting a GitHub issue through creating a pull request" width="800"/>

*Complete Issue-to-PR workflow: GitHub MCP retrieves issues and creates PRs, Filesystem MCP finds code, Context7 MCP provides best practices, and Copilot handles analysis and fixes*

### The Complete Workflow (No Copy-Paste, No Context Switching)

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Search by author doesn't work for partial names
Status: Open
Priority: Medium
Reporter: user123 (2 days ago)

Description:
Users should be able to search for "King" and find books by
"Stephen King". Currently the search requires exact match of
the full author name.

Steps to reproduce:
1. Run the book app
2. Search for "King"
3. No results returned (should find "Stephen King" books)

Comments:
- @reviewer: Good enhancement. Should use fuzzy matching.
- @contributor: Could use difflib or fuzzywuzzy for this.

> Find the code that handles author search

Found: samples/book-app-project/books.py

[Shows the BookCollection.search_by_author() method]

> Based on the issue and the code, what's causing this limitation?

Analysis:
Line 52 uses exact string comparison (author == search_term).
This requires users to type the full author name exactly.

Fix: Implement fuzzy matching using difflib or case-insensitive
substring matching.

> Fix the bug and create a pull request that references issue #1

✓ Created branch: fix/issue-1-fuzzy-author-search
✓ Modified: samples/book-app-project/books.py (added fuzzy matching)
✓ Modified: samples/book-app-project/test_books.py (added test cases)
✓ Created PR #7: Add fuzzy author search to book collection

PR URL: https://github.com/org/repo/pull/7
```

<details>
<summary>🎬 See the MCP workflow in action!</summary>

![MCP Workflow Demo](images/mcp-workflow-demo.gif)

*Demo output varies — your model, tools, and responses will differ from what's shown here.*

</details>

**The result**: Issue investigation → root cause analysis → fix implementation → PR creation. **Zero copy-paste. Zero context switching. One terminal session.**

---

### The Repository Health Dashboard

Get a complete picture of your codebase health in 30 seconds:

```bash
copilot

> Give me a health report for this repository:
> 1. Count all TODO and FIXME comments
> 2. List open GitHub issues by priority
> 3. Find any issues labeled "security"
> 4. Show me which files have the most lines of code

Repository Health Report
========================

📝 Technical Debt:
- TODO comments: 3 (samples/book-app-project/books.py: 2, utils.py: 1)
- FIXME comments: 1 (in data validation)

🐛 Open Issues: 4
- High: 1 (#1 fuzzy author search)
- Medium: 2
- Low: 1

🧪 Test Coverage:
- Test files: 0
- Functions tested: 0/12 (0%)
- Missing tests: all public functions need coverage

📊 Largest Files:
1. samples/book-app-project/book_app.py (99 lines)
2. samples/book-app-project/books.py (89 lines)
3. samples/book-app-project/utils.py (37 lines)

Recommendations:
- Address issue #1 for better user experience
- Add test coverage for BookCollection methods
- All files well-sized (<100 lines) - good structure!
```

**The result**: Multiple data sources aggregated in 30 seconds. Manual process: 1+ hour of clicking around GitHub, running grep, counting lines.

---

## Multi-Server Workflows

The real power comes from combining servers:

<img src="images/multi-server-workflow.png" alt="Multi-Server MCP Workflow" width="800"/>

*Combine GitHub, Filesystem, and Documentation servers for powerful integrated workflows*

```bash
copilot

# Step 1: Understand the issue from GitHub
> Tell me about issue #1

# Step 2: Find related code
> @samples/book-app-project/books.py Show me the BookCollection class

# Step 3: Get best practices
> What are the Python best practices for input validation?

# Step 4: Synthesize a solution
> Based on the issue, the code, and best practices, suggest a fix

# Step 5: Create the PR
> Create a pull request with this fix
```

### Example: Complete Bug Investigation

```bash
copilot

> Get the details of issue #1
# Learn about the enhancement request

> Show me samples/book-app-project/books.py
# See the relevant code

> What are the best practices for fuzzy string matching in Python?
# Understand the right approach

> Analyze the current implementation and suggest a fix based on what we found

# Copilot synthesizes information from all three sources

> Implement the fix

> Create a pull request titled "Add fuzzy author search to book collection"
```

---

## Web Access with web_fetch

GitHub Copilot CLI includes a built-in `web_fetch` tool that can retrieve content from URLs. You can control which URLs are accessible via your configuration.

> 💡 **Note**: This uses `~/.copilot/config.json` (general Copilot settings), which is separate from `~/.copilot/mcp-config.json` (MCP server definitions).

In `~/.copilot/config.json`:

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**Usage:**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

---

## Building a Custom MCP Server (Optional)

> 📖 **Want to connect Copilot to your own APIs?** See the [Custom MCP Server Guide](mcp-custom-server.md) for a complete walkthrough on building your own server with TypeScript. Additional details can be found in the [MCP for Beginners course](https://github.com/microsoft/mcp-for-beginners).
>
> This is completely optional - the pre-built servers (GitHub, filesystem, Context7) cover most use cases.

---

## 🎯 Try It Yourself

After completing the demos, try these variations:

1. **MCP Status Check**: Run `/mcp show` to see what servers are configured. If GitHub isn't set up, try adding it with your token.

2. **Documentation Challenge**: If Context7 MCP is configured, ask for official documentation on a framework you use:
   ```bash
   copilot
   > Show me the React documentation for useEffect cleanup patterns
   ```

3. **Workflow Challenge**: Try the complete issue-to-PR workflow on a real (or test) repository. Even if you don't have issues, you can create one and immediately work through it.

**Self-Check**: You understand MCP when you can explain why "Get GitHub issue #42" is better than copying and pasting issue content into the prompt.

---

## Assignment

### Main Challenge: Explore the Book App with MCP

The hands-on examples focused on listing PRs and working through an issue. Now practice MCP on different operations:

1. Verify GitHub MCP works (it's built-in): run `copilot` then `List my open PRs`
2. Set up `mcp-config.json` with the filesystem server (if not already done)
3. Use MCP to explore the book app:
   - Use the filesystem server to read the contents of `samples/book-app-project/data.json` and describe what books are in the collection
   - Use GitHub MCP to list recent commits that modified any file in `samples/book-app-project/`
   - Combine both: ask Copilot to use the filesystem server to check what test coverage exists, then use GitHub MCP to create an issue titled "Improve test coverage for BookCollection" with a description listing the missing test cases

**Success criteria**: You can seamlessly combine filesystem and GitHub MCP data in a single Copilot session.

<details>
<summary>💡 Hints (click to expand)</summary>

**Step 1: Verify GitHub MCP**
```bash
copilot
> List my open pull requests
# If this works, GitHub MCP is already set up!
# If not, run: /login
```

**Step 2: Create the config file**

Create `~/.copilot/mcp-config.json` (or use `/mcp add`):

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

**Important JSON tips:**
- Use double quotes `"` (not single quotes)
- No trailing commas after the last item
- Validate at [jsonlint.com](https://jsonlint.com/) if you get errors

**Step 3: Test the combined workflow**
```bash
copilot
> /mcp show
# Should show filesystem as enabled

> Read samples/book-app-project/data.json and describe the books
# Uses filesystem MCP

> List recent commits that modified files in samples/book-app-project/
# Uses GitHub MCP

> Check what tests exist in samples/book-app-project/tests/ and create an issue for missing test coverage
# Combines both servers
```

**If MCP isn't working:** Restart Copilot after editing the config file.

</details>

### Bonus Challenge: Build a Custom MCP Server

Ready to go deeper? Follow the [Custom MCP Server Guide](mcp-custom-server.md) to build your own server that connects to any API.

---

<details>
<summary>🔧 <strong>Common Mistakes & Troubleshooting</strong> (click to expand)</summary>

### Common Mistakes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Not knowing GitHub MCP is built-in | Trying to install/configure it manually | GitHub MCP is included by default. Just use it: "List my open PRs" |
| Looking for config in wrong location | Can't find or edit MCP settings | Config is in `~/.copilot/mcp-config.json` |
| Invalid JSON in config file | MCP servers fail to load | Use `/mcp show` to check configuration; validate JSON syntax |
| Forgetting to authenticate MCP servers | "Authentication failed" errors | Some MCPs need separate auth. Check each server's requirements |

### Troubleshooting

**"MCP server not found"** - Check that:
1. The npm package exists: `npm view @modelcontextprotocol/server-github`
2. Your configuration is valid JSON
3. The server name matches your config

Use `/mcp show` to see the current configuration.

**"GitHub authentication failed"** - The built-in GitHub MCP uses your `/login` credentials. Try:

```bash
copilot
> /login
```

This will re-authenticate you with GitHub. If issues persist, check that your GitHub account has the necessary permissions for the repository you're accessing.

**"MCP server failed to start"** - Check the server logs:
```bash
# Run the server command manually to see errors
npx -y @modelcontextprotocol/server-github
```

**MCP tools not available** - Make sure the server is enabled:
```bash
copilot

> /mcp show
# Check if server is listed and enabled

> /mcp enable server-name
# Enable if disabled
```

</details>

---

## 🔮 Also Available: Plugins

GitHub Copilot CLI also supports a **plugin system** for installing community extensions:

| Command | Purpose |
|---------|---------|
| `/plugin list` | See installed plugins |
| `/plugin marketplace` | Browse available plugins |
| `/plugin install <name>` | Install a plugin |
| `/plugin uninstall <name>` | Remove a plugin |
| `/plugin update` | Update installed plugins |

As the plugin ecosystem grows, this will become another way to extend Copilot's capabilities. For now, MCP servers cover most extensibility needs.

---

## Key Takeaways

1. **MCP** connects Copilot to external services
2. **Common servers** include filesystem, GitHub, and documentation
3. **Configuration** lives in `~/.copilot/mcp-config.json`
4. **Multi-server workflows** combine data from multiple sources
5. **Custom servers** let you connect any API
6. **Manage servers** with the `/mcp` command
7. **Plugins** provide another way to extend Copilot (emerging feature)

> 📋 **Quick Reference**: See the [Command Cheat Sheet](../QUICK-REFERENCE.md) for a complete list of commands and shortcuts.

---

## What's Next

You now have all the building blocks: modes, context, workflows, agents, skills, and MCP. Time to put them all together.

In **[Chapter 07: Putting It All Together](../07-putting-it-together/README.md)**, you'll learn:

- Combining agents, skills, and MCP
- Complete feature development workflows
- Automation with hooks
- Best practices for team environments

---

**[← Back to Chapter 05](../05-skills/README.md)** | **[Continue to Chapter 07 →](../07-putting-it-together/README.md)**
