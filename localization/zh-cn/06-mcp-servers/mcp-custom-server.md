# 构建自定义 MCP 服务器

> ⚠️ **本内容完全是可选的。** 仅使用预构建的 MCP 服务器（GitHub、filesystem、Context7），你也能高效地使用 Copilot CLI。本指南面向那些希望将 Copilot 连接到自定义内部 API 的开发者。更多详情请参阅 [MCP for Beginners 课程](https://github.com/microsoft/mcp-for-beginners)。
>
> **前置条件：**
> - 熟悉 Python
> - 理解 `async`/`await` 模式
> - 系统中可用 `pip`（本开发容器中已包含）
>
> **[← 返回第 06 章：MCP 服务器](README.md)**

---

想把 Copilot 连接到你自己的 API？下面演示如何用 Python 构建一个简单的 MCP 服务器，用于查询图书信息，并将其与你在本课程中一直使用的 book app 项目联系起来。

## 项目设置

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **`mcp` 包是什么？** 它是用于构建 MCP 服务器的官方 Python SDK。它处理协议细节，让你可以专注于工具本身。

## 服务器实现

创建一个名为 `server.py` 的文件：

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

**这里发生了什么：**

| 部分 | 作用 |
|------|-------------|
| `FastMCP("book-lookup")` | 创建一个名为 "book-lookup" 的服务器 |
| `@mcp.tool()` | 将一个函数注册为 Copilot 可调用的工具 |
| 类型提示 + 文档字符串 | 告诉 Copilot 每个工具的功能以及它需要什么参数 |
| `mcp.run()` | 启动服务器并监听请求 |

> 💡 **为什么用装饰器？** `@mcp.tool()` 装饰器就是你所需的全部。MCP SDK 会自动读取你函数的名称、类型提示和文档字符串，从而生成工具的 schema。无需手写 JSON schema！

## 配置

添加到你的 `~/.copilot/mcp-config.json`：

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

## 使用

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

## 后续步骤

构建好基本服务器后，你可以：

1. **添加更多工具** —— 每个 `@mcp.tool()` 函数都会成为 Copilot 可调用的一个工具
2. **连接真实 API** —— 用实际的 API 调用或数据库查询替换模拟的 `BOOKS_DB`
3. **添加身份验证** —— 安全地处理 API 密钥和令牌
4. **共享你的服务器** —— 发布到 PyPI，让其他人可以用 `pip` 安装

## 资源

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP 服务器示例](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners 课程](https://github.com/microsoft/mcp-for-beginners)

---

**[← 返回第 06 章：MCP 服务器](README.md)**
