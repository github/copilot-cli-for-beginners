# Aplicación de Libros - Versión con Errores

Este directorio contiene una versión intencionalmente con errores de la aplicación de colección de libros para ejercicios de depuración en el Capítulo 03.

**NO arregles estos errores directamente.** Existen para que los estudiantes puedan practicar usando GitHub Copilot CLI para identificar y depurar problemas.

---

## Errores intencionales

### books_buggy.py

| # | Error | Síntoma |
|---|-----|---------|
| 1 | `find_book_by_title()` uses exact case match | Buscar "the hobbit" no devuelve nada aunque "The Hobbit" exista |
| 2 | `save_books()` doesn't use context manager | Fuga de descriptores de archivo; sin manejo de errores para problemas de permisos |
| 3 | `add_book()` has no year validation | Acepta años negativos, año 0 y años muy lejanos en el futuro |
| 4 | `remove_book()` uses `in` substring check | Eliminar "Dune" también coincide y elimina "Dune Messiah" |
| 5 | `mark_as_read()` marks ALL books as read | Error en la variable del bucle - itera sobre todos los libros en lugar de solo la coincidencia |
| 6 | `find_by_author()` requires exact match | "Tolkien" no encontrará "J.R.R. Tolkien" (sin coincidencia parcial) |

### book_app_buggy.py

| # | Error | Síntoma |
|---|-----|---------|
| 7 | `show_books()` numbering starts at 0 | Los libros se muestran como "0. ...", "1. ..." en lugar de "1. ...", "2. ..." |
| 8 | `handle_add()` accepts empty title/author | Se pueden agregar libros con títulos y autores en blanco |
| 9 | `handle_remove()` always prints success | Muestra "Libro eliminado" incluso cuando no se encontró el libro |

---

## Cómo usar en el Capítulo 03

```bash
copilot

> @samples/book-app-buggy/books_buggy.py Users report that searching for
> "The Hobbit" returns no results even though it's in the data. Debug why.

> @samples/book-app-buggy/book_app_buggy.py When I remove a book that
> doesn't exist, the app says it was removed. Help me find why.
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->