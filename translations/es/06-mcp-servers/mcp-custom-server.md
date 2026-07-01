<!--
---
id: CopilotCLI-06-Custom-MCP-Server
title: !translate Building a Custom MCP Server
description: !translate Build a simple custom MCP server in Python to connect GitHub Copilot CLI to your own APIs.
audience: Developers / Students / Terminal users
slug: building-a-custom-mcp-server
weight: 61
---
-->

# Creación de un servidor MCP personalizado

> ⚠️ **Este contenido es completamente opcional.** Puedes ser muy productivo con Copilot CLI usando solo los servidores MCP preconstruidos (GitHub, filesystem, Context7). Esta guía es para desarrolladores que quieran conectar Copilot a APIs internas personalizadas. Consulta el [curso MCP para principiantes](https://github.com/microsoft/mcp-for-beginners) para más detalles.
>
> **Requisitos previos:**
> - Cómodo con Python
> - Comprensión de los patrones `async`/`await`
> - `pip` disponible en tu sistema (incluido en este contenedor de desarrollo)
>
> **[← Volver al Capítulo 06: Servidores MCP](README.md)**

---

¿Quieres conectar Copilot a tus propias API? Aquí tienes cómo construir un servidor MCP sencillo en Python que busca información de libros, conectando con el proyecto de la aplicación de libros que has estado usando a lo largo de este curso.

## Configuración del proyecto

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **¿Qué es el paquete `mcp`?** Es el SDK oficial de Python para construir servidores MCP. Gestiona los detalles del protocolo para que puedas centrarte en tus herramientas.

## Implementación del servidor

Crea un archivo llamado `server.py`:

```python
# server.py
import json
from mcp.server.fastmcp import FastMCP

# Crear el servidor MCP
mcp = FastMCP("book-lookup")

# Base de datos de libros de ejemplo (en un servidor real, esto podría consultar una API o una base de datos)
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

**Lo que ocurre aquí:**

| Parte | Qué hace |
|------|-------------|
| `FastMCP("book-lookup")` | Crea un servidor llamado "book-lookup" |
| `@mcp.tool()` | Registra una función como una herramienta que Copilot puede invocar |
| Type hints + docstrings | Indican a Copilot qué hace cada herramienta y qué parámetros necesita |
| `mcp.run()` | Inicia el servidor y escucha solicitudes |

> 💡 **¿Por qué los decoradores?** El decorador `@mcp.tool()` es todo lo que necesitas. El SDK de MCP lee automáticamente el nombre de tu función, las anotaciones de tipo y el docstring para generar el esquema de la herramienta. ¡No se necesita un esquema JSON manual!

## Configuración

Añade a tu `~/.copilot/mcp-config.json`:

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

[Muestra todos los libros de la base de datos con sus ISBN]
```

## Próximos pasos

Una vez que hayas construido un servidor básico, puedes:

1. **Agregar más herramientas** - Cada función `@mcp.tool()` se convierte en una herramienta que Copilot puede invocar
2. **Conectar APIs reales** - Reemplaza la base de datos simulada `BOOKS_DB` con llamadas a APIs reales o consultas a bases de datos
3. **Agregar autenticación** - Maneja claves de API y tokens de forma segura
4. **Compartir tu servidor** - Publícalo en PyPI para que otros puedan instalarlo con `pip`

## Recursos

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners Course](https://github.com/microsoft/mcp-for-beginners)

---

**[← Volver al Capítulo 06: Servidores MCP](README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->