import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("book-lookup")

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
    book = BOOKS_DB.get(isbn)
    if book:
        return json.dumps(book, indent=2)
    return f"No book found with ISBN {isbn}"


@mcp.tool()
def search_book(query: str) -> str:
    query_lower = query.lower()
    results = [
        {**books, "isbn": isbn}
        for isbn, books in BOOKS_DB.items()
        if query_lower in books["title"].lower()
        or query_lower in books["author"].lower()
    ]

    if results:
        return json.dumps(results, indent=2)
    return "No books found with matching"

@mcp.tool()
def list_all_books() -> str:
    all_books = [
        {"isbn": isbn, "title": books["title"], "author": books["author"]}
        for isbn, books in BOOKS_DB.items()
    ]
    return json.dumps(all_books, indent=2)

if __name__ == "__main__":
    print("Starting book-lookup MCP")
    mcp.run()
