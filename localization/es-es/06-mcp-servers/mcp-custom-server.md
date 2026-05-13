# Construir un servidor MCP personalizado

> ⚠️ **Este contenido es totalmente opcional.** Puedes ser muy productivo con Copilot CLI usando únicamente los servidores MCP preconstruidos (GitHub, filesystem, Context7). Esta guía es para personas desarrolladoras que quieran conectar Copilot con APIs internas personalizadas. Consulta el [curso MCP for Beginners](https://github.com/microsoft/mcp-for-beginners) para más detalles.
>
> **Requisitos previos:**
> - Sentirte cómodo con Python
> - Comprender los patrones `async`/`await`
> - Tener `pip` disponible en tu sistema (incluido en este dev container)
>
> **[← Volver al Capítulo 06: Servidores MCP](README.md)**

---

¿Quieres conectar Copilot con tus propias APIs? Aquí tienes cómo construir un servidor MCP sencillo en Python que busca información de libros, vinculándolo con el proyecto book app que has estado usando a lo largo de este curso.

## Configuración del proyecto

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **¿Qué es el paquete `mcp`?** Es el SDK oficial de Python para construir servidores MCP. Se encarga de los detalles del protocolo para que tú puedas centrarte en tus herramientas.

## Implementación del servidor

Crea un archivo llamado `server.py`:

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

**Qué está pasando aquí:**

| Parte | Qué hace |
|------|-------------|
| `FastMCP("book-lookup")` | Crea un servidor llamado "book-lookup" |
| `@mcp.tool()` | Registra una función como herramienta que Copilot puede invocar |
| Type hints + docstrings | Indican a Copilot lo que hace cada herramienta y los parámetros que necesita |
| `mcp.run()` | Inicia el servidor y se queda escuchando peticiones |

> 💡 **¿Por qué decoradores?** El decorador `@mcp.tool()` es todo lo que necesitas. El SDK de MCP lee automáticamente el nombre de tu función, sus type hints y su docstring para generar el esquema de la herramienta. ¡No hace falta escribir un esquema JSON a mano!

## Configuración

Añade esto a tu `~/.copilot/mcp-config.json`:

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

## Uso

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

## Próximos pasos

Una vez que hayas construido un servidor básico, puedes:

1. **Añadir más herramientas** - Cada función `@mcp.tool()` se convierte en una herramienta que Copilot puede invocar
2. **Conectar APIs reales** - Sustituye el `BOOKS_DB` simulado por llamadas reales a una API o consultas a una base de datos
3. **Añadir autenticación** - Maneja claves de API y tokens de forma segura
4. **Compartir tu servidor** - Publícalo en PyPI para que otras personas puedan instalarlo con `pip`

## Recursos

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Servidores MCP de ejemplo](https://github.com/modelcontextprotocol/servers)
- [Curso MCP for Beginners](https://github.com/microsoft/mcp-for-beginners)

---

**[← Volver al Capítulo 06: Servidores MCP](README.md)**
