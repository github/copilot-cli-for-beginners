# 커스텀 MCP 서버 만들기

> ⚠️ **이 콘텐츠는 완전히 선택 사항입니다.** 미리 만들어진 MCP 서버(GitHub, filesystem, Context7)만 사용해도 Copilot CLI로 매우 생산적으로 작업할 수 있습니다. 이 가이드는 Copilot을 사내 커스텀 API에 연결하고 싶은 개발자를 위한 것입니다. 더 자세한 내용은 [MCP for Beginners 코스](https://github.com/microsoft/mcp-for-beginners)를 참고해 보세요.
>
> **사전 준비:**
> - Python에 익숙할 것
> - `async`/`await` 패턴 이해
> - 시스템에 `pip` 설치 (이 dev container에는 포함되어 있습니다)
>
> **[← 6장으로 돌아가기: MCP 서버](README.md)**

---

Copilot을 여러분의 API에 연결하고 싶으신가요? 이 코스 전반에서 사용해 온 book app 프로젝트와 연결되는, 책 정보를 조회하는 간단한 MCP 서버를 Python으로 만드는 방법을 소개합니다.

## 프로젝트 설정

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **`mcp` 패키지란?** MCP 서버를 만들기 위한 공식 Python SDK입니다. 프로토콜 세부 사항을 처리해 주므로, 여러분은 도구 자체에만 집중할 수 있습니다.

## 서버 구현

`server.py`라는 파일을 만듭니다.

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

**여기서 일어나는 일:**

| 부분 | 하는 일 |
|------|-------------|
| `FastMCP("book-lookup")` | "book-lookup"이라는 이름의 서버를 만듭니다 |
| `@mcp.tool()` | 함수를 Copilot이 호출할 수 있는 도구로 등록합니다 |
| 타입 힌트 + docstring | 각 도구가 무엇을 하고 어떤 매개변수가 필요한지 Copilot에게 알려 줍니다 |
| `mcp.run()` | 서버를 시작하고 요청을 수신 대기합니다 |

> 💡 **왜 데코레이터를 쓰나요?** `@mcp.tool()` 데코레이터 하나면 충분합니다. MCP SDK가 함수 이름, 타입 힌트, docstring을 자동으로 읽어 도구 스키마를 생성해 줍니다. 직접 JSON 스키마를 작성할 필요가 없습니다!

## 설정

`~/.copilot/mcp-config.json`에 다음 내용을 추가합니다.

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

## 사용 방법

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

## 다음 단계

기본 서버를 만든 다음에는 이런 일들을 해 볼 수 있습니다.

1. **도구 더 추가하기** - 각 `@mcp.tool()` 함수가 Copilot이 호출할 수 있는 도구가 됩니다
2. **실제 API 연결하기** - 모의 데이터인 `BOOKS_DB`를 실제 API 호출이나 데이터베이스 쿼리로 교체합니다
3. **인증 추가하기** - API 키와 토큰을 안전하게 처리합니다
4. **서버 공유하기** - PyPI에 게시해서 다른 사람들이 `pip`으로 설치할 수 있게 합니다

## 참고 자료

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP 서버 예제](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners 코스](https://github.com/microsoft/mcp-for-beginners)

---

**[← 6장으로 돌아가기: MCP 서버](README.md)**
