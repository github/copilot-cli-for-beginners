# Aplicación de colección de libros

*(Este README es intencionalmente básico para que puedas mejorarlo con GitHub Copilot CLI)*

Una aplicación JavaScript para gestionar libros que tienes o quieres leer.
Puede añadir, eliminar y listar libros. También marcarlos como leídos.

---

## Características actuales

* Lee libros desde un archivo JSON (nuestra base de datos)
* La validación de entrada es débil en algunas áreas
* Existen algunas pruebas pero probablemente no son suficientes

---

## Archivos

* `book_app.js` - Punto de entrada principal de la CLI
* `books.js` - Clase BookCollection con lógica de datos
* `utils.js` - Funciones auxiliares para la UI y la entrada
* `data.json` - Datos de ejemplo de libros
* `tests/test_books.js` - Pruebas iniciales usando el ejecutor de pruebas integrado de Node

---

## Ejecutar la aplicación

```bash
node book_app.js list
node book_app.js add
node book_app.js find
node book_app.js remove
node book_app.js help
```

## Ejecutar pruebas

```bash
npm test
```

---

## Notas

* No apto para producción (obviamente)
* Parte del código podría mejorarse
* Se podrían añadir más comandos más adelante

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->