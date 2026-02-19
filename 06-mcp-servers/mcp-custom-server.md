# Building a Custom MCP Server

> ⚠️ **This content is completely optional.** You can be highly productive with Copilot CLI using only the pre-built MCP servers (GitHub, filesystem, Context7). This guide is for developers who want to connect Copilot to custom internal APIs. See the [MCP for Beginners course](https://github.com/microsoft/mcp-for-beginners) for more details.
>
> **Prerequisites:**
> - Comfortable with Python
> - Understanding of `async`/`await` patterns
> - `pip` available on your system (included in this dev container)
>
> **[← Back to Chapter 06: MCP Servers](README.md)**

---

Want to connect Copilot to your own APIs? Here's how to build a simple MCP server in Python that looks up book information, tying back to the book app project you've been using throughout this course.

## Project Setup

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **What is the `mcp` package?** It's the official Python SDK for building MCP servers. It handles the protocol details so you can focus on your tools.

## Server Implementation

Create a file called `server.py`:

```python
# server.py
import json
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("book-lookup")

# Sample book database (in a real server, this could query an API or database)
BOOKS_DB = {
    "978-0-547-92822-7": {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "genre": "Fantasy",
    },
    "978-0-451-52493-5": {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian Fiction",
    },
    "978-0-441-17271-9": {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Science Fiction",
    },
}


@mcp.tool()
def lookup_book(isbn: str) -> str:
    """Look up a book by its ISBN and return title, author, year, and genre."""
    book = BOOKS_DB.get(isbn)
    if book:
        return json.dumps(book, indent=2)
    return f"No book found with ISBN: {isbn}"


@mcp.tool()
def search_books(query: str) -> str:
    """Search for books by title or author. Returns all matching results."""
    query_lower = query.lower()
    results = [
        {**book, "isbn": isbn}
        for isbn, book in BOOKS_DB.items()
        if query_lower in book["title"].lower()
        or query_lower in book["author"].lower()
    ]
    if results:
        return json.dumps(results, indent=2)
    return f"No books found matching: {query}"


@mcp.tool()
def list_all_books() -> str:
    """List all books in the database with their ISBNs."""
    books_list = [
        {"isbn": isbn, "title": book["title"], "author": book["author"]}
        for isbn, book in BOOKS_DB.items()
    ]
    return json.dumps(books_list, indent=2)


if __name__ == "__main__":
    mcp.run()
```

**What's happening here:**

| Part | What It Does |
|------|-------------|
| `FastMCP("book-lookup")` | Creates a server named "book-lookup" |
| `@mcp.tool()` | Registers a function as a tool Copilot can call |
| Type hints + docstrings | Tell Copilot what each tool does and what parameters it needs |
| `mcp.run()` | Starts the server and listens for requests |

> 💡 **Why decorators?** The `@mcp.tool()` decorator is all you need. The MCP SDK automatically reads your function's name, type hints, and docstring to generate the tool schema. No manual JSON schema needed!

## Configuration

Add to your `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "book-lookup": {
      "type": "local",
      "command": "python3",
      "args": ["./book-lookup-mcp-server/server.py"],
      "tools": ["*"]
    }
  }
}
```

## Usage

```bash
copilot

> Look up the book with ISBN 978-0-547-92822-7

{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "genre": "Fantasy"
}

> Search for books by Orwell

[
  {
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "genre": "Dystopian Fiction",
    "isbn": "978-0-451-52493-5"
  }
]

> List all available books

[Shows all books in the database with ISBNs]
```

## Next Steps

Once you've built a basic server, you can:

1. **Add more tools** - Each `@mcp.tool()` function becomes a tool Copilot can call
2. **Connect real APIs** - Replace the mock `BOOKS_DB` with actual API calls or database queries
3. **Add authentication** - Handle API keys and tokens securely
4. **Share your server** - Publish to PyPI so others can install it with `pip`

## Resources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners Course](https://github.com/microsoft/mcp-for-beginners)

---

**[← Back to Chapter 06: MCP Servers](README.md)**
