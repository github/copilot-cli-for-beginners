# Colección de Libros

*(Este README es intencionalmente básico para que puedas mejorarlo con GitHub Copilot CLI)*

Una aplicación en Python para gestionar libros que tienes o quieres leer.
Puede agregar, eliminar y listar libros. También marcarlos como leídos.

---

## Características actuales

* Lee libros desde un archivo JSON (nuestra base de datos)
* La comprobación de entradas es débil en algunas áreas
* Existen algunas pruebas pero probablemente no son suficientes

---

## Archivos

* `book_app.py` - Punto de entrada principal de la CLI
* `books.py` - Clase BookCollection con la lógica de datos
* `utils.py` - Funciones auxiliares para la interfaz de usuario y la entrada
* `data.json` - Datos de libros de ejemplo
* `tests/test_books.py` - Pruebas iniciales de pytest

---

## Ejecutar la aplicación

```bash
python book_app.py list
python book_app.py add
python book_app.py find
python book_app.py remove
python book_app.py help
```

## Ejecutar pruebas

```bash
python -m pytest tests/
```

---

## Notas

* No apto para producción (obviamente)
* Algún código podría mejorarse
* Se podrían añadir más comandos más adelante

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->