# Aplicación de libros - Versión con errores

Este directorio contiene una versión intencionalmente defectuosa de la aplicación de colección de libros para ejercicios de depuración en el Capítulo 03.

**NO arregles estos errores directamente.** Existen para que los estudiantes practiquen usando GitHub Copilot CLI para identificar y depurar problemas.

---

## Errores intencionales

### books_buggy.py

| # | Error | Síntoma |
|---|-----|---------|
| 1 | `find_book_by_title()` usa coincidencia exacta de mayúsculas y minúsculas | Buscar "the hobbit" no devuelve nada aunque "The Hobbit" exista |
| 2 | `save_books()` no usa un administrador de contexto | Fuga de descriptor de archivo; sin manejo de errores para problemas de permisos |
| 3 | `add_book()` no valida el año | Acepta años negativos, el año 0 y años muy lejanos en el futuro |
| 4 | `remove_book()` usa la comprobación de subcadena `in` | Eliminar "Dune" también coincide y elimina "Dune Messiah" |
| 5 | `mark_as_read()` marca TODOS los libros como leídos | Error en la variable del bucle: itera todos los libros en lugar de solo la coincidencia |
| 6 | `find_by_author()` requiere coincidencia exacta | "Tolkien" no encontrará "J.R.R. Tolkien" (sin coincidencia parcial) |

### book_app_buggy.py

| # | Error | Síntoma |
|---|-----|---------|
| 7 | `show_books()` la numeración empieza en 0 | Los libros se muestran como "0. ...", "1. ..." en lugar de "1. ...", "2. ..." |
| 8 | `handle_add()` acepta título/autor vacío | Se pueden añadir libros con títulos y autores en blanco |
| 9 | `handle_remove()` siempre imprime éxito | Dice "Book removed" incluso cuando no se encontró el libro |

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