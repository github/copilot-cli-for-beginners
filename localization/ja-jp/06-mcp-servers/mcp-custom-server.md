# カスタム MCP サーバーを構築する

> ⚠️ **この内容は完全にオプションです。** プリビルドの MCP サーバー（GitHub、filesystem、Context7）だけで Copilot CLI を非常に生産的に使えます。このガイドはカスタムの内部 API に Copilot を接続したい開発者向けです。詳細は [MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners)を参照してください。
>
> **前提条件:**
> - Python に慣れている
> - `async`/`await` パターンを理解している
> - システムで `pip` が利用可能（この開発コンテナに含まれている）
>
> **[← 第 06 章: MCP サーバーに戻る](README.md)**

---

Copilot を独自の API に接続したいですか？このコース全体で使用してきたブックアプリプロジェクトに結び付けて、書籍情報を検索するシンプルな MCP サーバーを Python で構築する方法を説明します。

## プロジェクトのセットアップ

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **`mcp` パッケージとは何ですか？** MCP サーバーを構築するための公式 Python SDK です。プロトコルの詳細を処理するので、ツールに集中できます。

## サーバーの実装

`server.py` というファイルを作成します:

```python
# server.py
import json
from mcp.server.fastmcp import FastMCP

# MCP サーバーを作成する
mcp = FastMCP("book-lookup")

# サンプル書籍データベース（実際のサーバーでは API やデータベースを照会できる）
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

**ここで何が行われているか:**

| 部分 | 機能 |
|------|-------------|
| `FastMCP("book-lookup")` | "book-lookup" という名前のサーバーを作成する |
| `@mcp.tool()` | 関数を Copilot が呼び出せるツールとして登録する |
| 型ヒント + ドキュメント文字列 | 各ツールが何をするか、どのパラメータが必要かを Copilot に伝える |
| `mcp.run()` | サーバーを起動してリクエストを待機する |

> 💡 **なぜデコレーターを使うのですか？** `@mcp.tool()` デコレーターだけで十分です。MCP SDK は関数の名前、型ヒント、ドキュメント文字列を自動的に読み込んでツールスキーマを生成します。手動の JSON スキーマは不要です！

## 設定

`~/.copilot/mcp-config.json` に追加します:

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

## 使用方法

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

[データベース内のすべての本を ISBN とともに表示する]
```

## 次のステップ

基本的なサーバーを構築したら、以下ができます。

1. **ツールを追加する** - 各 `@mcp.tool()` 関数が Copilot の呼び出せるツールになる
2. **実際の API に接続する** - モックの `BOOKS_DB` を実際の API 呼び出しやデータベースクエリに置き換える
3. **認証を追加する** - API キーとトークンを安全に処理する
4. **サーバーを共有する** - PyPI に公開して他の人が `pip` でインストールできるようにする

## リソース

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP サーバーの例](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners)

---

**[← 第 06 章: MCP サーバーに戻る](README.md)**
