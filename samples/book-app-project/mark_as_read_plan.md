# Plan: Agregar comando "mark" y "unmark" a book-app

## Problema
El comando para marcar libros como leídos no existe en la CLI, aunque la lógica existe en `BookCollection.mark_as_read()`.

## Solución
Agregar dos nuevos comandos:
- `python book_app.py mark` — Marca un libro como leído (interactivo)
- `python book_app.py unmark` — Marca un libro como no leído (interactivo)

## Decisiones de diseño
- **Comando:** `mark` / `unmark` (no `read` / `unread`)
- **Entrada:** Interactivo (preguntar título, como en `add`)
- **Feedback:** Mostrar si el libro se marcó exitosamente o si no fue encontrado
- **Simetría:** Agregar `mark_as_unread()` para complementar `mark_as_read()`

---

## Tareas por implementar

### 1. `books.py` — Agregar `mark_as_unread()`
Crear método simétrico a `mark_as_read()`:
```python
def mark_as_unread(self, title: str) -> bool:
    """Mark a book as unread."""
    book = self.find_book_by_title(title)
    if book:
        book.read = False
        self.save_books()
        return True
    return False
```

### 2. `book_app.py` — Agregar handlers
Crear dos nuevos handlers (similar a `handle_find()`):
```python
def handle_mark():
    # Pedir título
    # Llamar collection.mark_as_read()
    # Mostrar éxito o error

def handle_unmark():
    # Pedir título
    # Llamar collection.mark_as_unread()
    # Mostrar éxito o error
```

### 3. `book_app.py` — Actualizar `main()` y `show_help()`
- Agregar `elif command == "mark":` en main()
- Agregar `elif command == "unmark":` en main()
- Documentar comandos en `show_help()`

### 4. `test_books.py` — Agregar tests
Nuevos tests para `mark_as_unread()`:
- `test_mark_book_as_unread()` — Marcar un libro existente
- `test_mark_book_as_unread_invalid()` — Intento con libro inexistente

### 5. `README.md` — Actualizar documentación
Agregar comandos `mark` y `unmark` a la sección de "Running the App"

---

## Orden de implementación
1. `books.py` — Agregar método (no depende de nada)
2. `book_app.py` — Agregar handlers + main + help (depende de books.py)
3. `test_books.py` — Tests (depende de books.py)
4. `README.md` — Documentación (depende de todo lo anterior)
