# 构建自定义 MCP 服务器

> ⚠️ **本内容完全可选。** 仅使用预构建的 MCP 服务器（GitHub、文件系统、Context7），你已经可以高效地使用 Copilot CLI。本指南适用于希望将 Copilot 连接到自定义内部 API 的开发者。更多详情请参阅 [MCP 初学者课程](https://github.com/microsoft/mcp-for-beginners)。
>
> **前置条件：**
> - 熟悉 Python
> - 理解 `async`/`await` 模式
> - 系统上已安装 `pip`（包含在此开发容器中）
>
> **[← 返回第 06 章：MCP 服务器](README.zh-CN.md)**

---

想将 Copilot 连接到你自己的 API？这里介绍如何用 Python 构建一个简单的 MCP 服务器，查找书籍信息——与你在本课程中一直使用的书籍应用项目相呼应。

## 项目设置

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **什么是 `mcp` 包？** 这是用于构建 MCP 服务器的官方 Python SDK。它处理协议细节，让你专注于你的工具逻辑。

## 服务器实现

创建名为 `server.py` 的文件：

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

**代码说明：**

| 部分 | 作用 |
|------|------|
| `FastMCP("book-lookup")` | 创建名为"book-lookup"的服务器 |
| `@mcp.tool()` | 将函数注册为 Copilot 可调用的工具 |
| 类型注解 + docstring | 告诉 Copilot 每个工具的功能和所需参数 |
| `mcp.run()` | 启动服务器并监听请求 |

> 💡 **为何使用装饰器？** `@mcp.tool()` 装饰器就是你所需要的全部。MCP SDK 会自动读取函数的名称、类型注解和 docstring 来生成工具模式，无需手动编写 JSON Schema！

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

## 使用方式

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

## 下一步

构建基础服务器后，你可以：

1. **添加更多工具**——每个 `@mcp.tool()` 函数都成为 Copilot 可调用的工具
2. **连接真实 API**——将模拟的 `BOOKS_DB` 替换为实际的 API 调用或数据库查询
3. **添加身份验证**——安全地处理 API 密钥和令牌
4. **分享你的服务器**——发布到 PyPI，让其他人可以用 `pip` 安装

## 资源

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP 服务器示例](https://github.com/modelcontextprotocol/servers)
- [MCP 初学者课程](https://github.com/microsoft/mcp-for-beginners)

---

**[← 返回第 06 章：MCP 服务器](README.zh-CN.md)**
