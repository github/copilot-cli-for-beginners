![Chapter 03: Development Workflows](../../../03-development-workflows/images/chapter-header.png)

> **¿Y si la IA pudiera encontrar errores sobre los que ni siquiera sabías preguntar?**

En este capítulo, GitHub Copilot CLI se convierte en tu herramienta diaria. Lo usarás dentro de los flujos de trabajo que ya empleas todos los días: pruebas, refactorización, depuración y Git.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Realizar revisiones de código exhaustivas con Copilot CLI
- Refactorizar código heredado de forma segura
- Depurar problemas con asistencia de IA
- Generar pruebas automáticamente
- Integrar Copilot CLI con tu flujo de trabajo git

> ⏱️ **Tiempo estimado**: ~60 minutos (15 min de lectura + 45 min práctico)

---

## 🧩 Analogía del mundo real: El flujo de trabajo de un carpintero

Un carpintero no solo sabe usar herramientas, tiene *flujos de trabajo* para diferentes tareas:

<img src="../../../03-development-workflows/images/carpenter-workflow-steps.png" alt="Taller de artesano que muestra tres carriles de flujo de trabajo: Fabricación de muebles (Medir, Cortar, Ensamblar, Acabar), Reparar daños (Evaluar, Quitar, Reparar, Igualar) y Control de calidad (Inspeccionar, Probar uniones, Comprobar alineación)" width="800"/>

De manera similar, los desarrolladores tienen flujos de trabajo para distintas tareas. GitHub Copilot CLI mejora cada uno de estos flujos, haciéndote más eficiente y eficaz en tus tareas diarias de programación.

---

# Los cinco flujos de trabajo

<img src="../../../03-development-workflows/images/five-workflows.png" alt="Cinco iconos de neón brillantes que representan los flujos de trabajo de revisión de código, pruebas, depuración, refactorización e integración con git" width="800"/>

Cada flujo de trabajo a continuación es autónomo. Elige los que se ajusten a tus necesidades actuales o recórrelos todos.

---

## Elige tu propia aventura

Este capítulo cubre cinco flujos de trabajo que los desarrolladores suelen usar. **¡Sin embargo, no necesitas leerlos todos de una vez!** Cada flujo de trabajo está contenido en una sección plegable abajo. Elige los que coincidan con lo que necesitas y lo que mejor se adapte a tu proyecto actual. Siempre puedes volver y explorar los demás más tarde.

<img src="../../../03-development-workflows/images/five-workflows-swimlane.png" alt="Cinco flujos de trabajo de desarrollo: Revisión de código, Refactorización, Depuración, Generación de pruebas e Integración con Git mostrados como carriles horizontales" width="800"/>

| Quiero... | Ir a |
|---|---|
| Revisar código antes de fusionar | [Flujo de trabajo 1: Revisión de código](#workflow-1-code-review) |
| Limpiar código desordenado o heredado | [Flujo de trabajo 2: Refactorización](#workflow-2-refactoring) |
| Localizar y corregir un error | [Flujo de trabajo 3: Depuración](#workflow-3-debugging) |
| Generar pruebas para mi código | [Flujo de trabajo 4: Generación de pruebas](#workflow-4-test-generation) |
| Escribir mejores commits y pull requests | [Flujo de trabajo 5: Integración con Git](#workflow-5-git-integration) |
| Investigar antes de codificar | [Consejo rápido: Investigar antes de planificar o codificar](#revisar-antes-del-push) |
| Ver un flujo de trabajo completo de corrección de errores de principio a fin | [Poniéndolo todo junto](#usar-delegate-para-tareas-en-segundo-plano) |

**Selecciona un flujo de trabajo abajo para expandirlo** y ver cómo GitHub Copilot CLI puede mejorar tu proceso de desarrollo en esa área. 

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>Workflow 1: Code Review</strong> - Revisa archivos, usa el agente /review, crea listas de verificación por severidad</summary>

<img src="../../../03-development-workflows/images/code-review-swimlane-single.png" alt="Flujo de revisión de código: revisar, identificar problemas, priorizar, generar lista de verificación." width="800"/>

### Revisión básica

Este ejemplo usa el símbolo `@` para referenciar un archivo, otorgando a Copilot CLI acceso directo a su contenido para revisión.

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Code Review Demo](../../../03-development-workflows/images/code-review-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

---

### Revisión de validación de entrada

Pide a Copilot CLI que enfoque su revisión en una preocupación específica (aquí, validación de entrada) enumerando las categorías que te interesan en el prompt.

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### Revisión del proyecto en varios archivos

Referencia todo un directorio con `@` para permitir que Copilot CLI escanee todos los archivos del proyecto a la vez.

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### Revisión de código interactiva

Usa una conversación multi-turno para profundizar. Comienza con una revisión amplia y luego haz preguntas de seguimiento sin reiniciar.

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI proporciona una revisión detallada

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI muestra problemas potenciales con cadenas vacías y caracteres especiales

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI genera elementos de acción priorizados
```

### Plantilla de lista de verificación para revisión

Pide a Copilot CLI que estructure su salida en un formato específico (aquí, una lista de verificación en markdown categorizada por severidad que puedes pegar en un issue).

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Entendiendo los cambios en Git (Importante para /review)

Antes de usar el comando `/review`, necesitas entender dos tipos de cambios en git:

| Change Type | What It Means | How to See |
|-------------|---------------|------------|
| **Staged changes** | Files you've marked for the next commit with `git add` | `git diff --staged` |
| **Unstaged changes** | Files you've modified but haven't added yet | `git diff` |

```bash
# Referencia rápida
git status           # Muestra tanto los cambios preparados como los no preparados
git add file.py      # Preparar un archivo para el commit
git diff             # Muestra cambios no preparados
git diff --staged    # Muestra cambios preparados
```

### Uso del comando /review

El comando `/review` invoca el **agente de revisión de código** incorporado, que está optimizado para analizar cambios staged y unstaged con una salida de alta relación señal/ruido. Usa un comando con slash para activar un agente integrado especializado en lugar de escribir un prompt en lenguaje libre.

```bash
copilot

> /review
# Invoca al agente de revisión de código sobre cambios preparados/no preparados
# Proporciona comentarios enfocados y accionables

> /review Check for security issues in authentication
# Ejecuta la revisión con un área de enfoque específica
```

> 💡 **Consejo**: El agente de revisión de código funciona mejor cuando tienes cambios pendientes. Etapa tus archivos con `git add` para revisiones más enfocadas.

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>Workflow 2: Refactoring</strong> - Reestructura el código, separa responsabilidades, mejora el manejo de errores</summary>

<img src="../../../03-development-workflows/images/refactoring-swimlane-single.png" alt="Flujo de refactorización: evaluar código, planear cambios, implementar, verificar comportamiento." width="800"/>

### Refactorización simple

> **Prueba esto primero:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

Comienza con mejoras sencillas. Pruébalas en la aplicación de libros. Cada prompt usa una referencia de archivo `@` junto con una instrucción de refactorización específica para que Copilot CLI sepa exactamente qué cambiar.

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **¿Nuevo en refactorización?** Comienza con solicitudes simples como agregar type hints o mejorar nombres de variables antes de abordar transformaciones complejas.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Refactor Demo](../../../03-development-workflows/images/refactor-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

---

### Separar responsabilidades

Referencia múltiples archivos con `@` en un solo prompt para que Copilot CLI pueda mover código entre ellos como parte del refactor.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### Mejorar el manejo de errores

Proporciona dos archivos relacionados y describe la preocupación transversal para que Copilot CLI pueda sugerir una corrección coherente en ambos.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### Añadir documentación

Usa una lista de viñetas detallada para especificar exactamente qué debe contener cada docstring.

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### Refactorización segura con pruebas

Encadena dos solicitudes relacionadas en una conversación multi-turno. Primero genera pruebas y luego refactoriza con esas pruebas como red de seguridad.

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Escribe las pruebas primero

> Now refactor the BookCollection class to use a context manager for file operations

# Refactoriza con confianza - las pruebas verifican que el comportamiento se mantiene
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>Workflow 3: Debugging</strong> - Localiza errores, auditorías de seguridad, rastrea problemas a través de archivos</summary>

<img src="../../../03-development-workflows/images/debugging-swimlane-single.png" alt="Flujo de depuración: entender el error, localizar la causa raíz, arreglar, probar." width="800"/>

### Depuración simple

> **Prueba esto primero:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

Comienza describiendo qué está mal. Aquí hay patrones comunes de depuración que puedes probar con la aplicación de libros con errores. Cada prompt combina una referencia de archivo `@` con una descripción clara del síntoma para que Copilot CLI pueda localizar y diagnosticar el error.

```bash
copilot

# Patrón: "Se esperaba X pero se obtuvo Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Patrón: "Comportamiento inesperado"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Patrón: "Resultados incorrectos"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **Consejo de depuración**: Describe el *síntoma* (lo que ves) y la *expectativa* (lo que debería suceder). Copilot CLI se encarga del resto.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Fix Bug Demo](../../../03-development-workflows/images/fix-bug-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

---

### El "Detective de bugs" - La IA encuentra bugs RELACIONADOS

Aquí es donde la depuración con contexto brilla. Prueba este escenario con la aplicación de libros con errores. Proporciona el archivo completo mediante `@` y describe solo el síntoma informado por el usuario. Copilot CLI trazará la causa raíz y puede encontrar errores adicionales cercanos.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Lo que hace Copilot CLI**:
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**Por qué importa**: Copilot CLI lee todo el archivo, comprende el contexto de tu informe de error y te da una solución específica con una explicación clara.

> 💡 **Bonus**: Debido a que Copilot CLI analiza todo el archivo, a menudo descubre *otros* problemas sobre los que no preguntaste. Por ejemplo, al arreglar la búsqueda por autor, Copilot CLI podría notar también el bug de sensibilidad a mayúsculas en `find_book_by_title`!

### Barra lateral de seguridad en el mundo real

Aunque depurar tu propio código es importante, entender las vulnerabilidades de seguridad en aplicaciones en producción es crítico. Prueba este ejemplo: señala a Copilot CLI un archivo desconocido y pídele auditarlo en busca de problemas de seguridad.

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

Este archivo demuestra patrones de seguridad del mundo real que encontrarás en aplicaciones de producción.

> 💡 **Términos comunes de seguridad que encontrarás:**
> - **Inyección SQL**: Cuando la entrada del usuario se pone directamente en una consulta a la base de datos, permitiendo que atacantes ejecuten comandos maliciosos
> - **Consultas parametrizadas**: La alternativa segura: marcadores (`?`) separan los datos del usuario de los comandos SQL
> - **Condición de carrera**: Cuando dos operaciones ocurren al mismo tiempo y se interfieren entre sí
> - **XSS (Cross-Site Scripting)**: Cuando atacantes inyectan scripts maliciosos en páginas web

---

### Entendiendo un error

Pega un stack trace directamente en tu prompt junto con una referencia de archivo `@` para que Copilot CLI pueda mapear el error al código fuente.

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### Depuración con caso de prueba

Describe la entrada exacta y la salida observada para darle a Copilot CLI un caso de prueba concreto y reproducible sobre el que razonar.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### Rastrear un problema a través del código

Referencia múltiples archivos y pide a Copilot CLI que siga el flujo de datos entre ellos para localizar dónde se origina el problema.

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### Entendiendo problemas de datos

Incluye un archivo de datos junto con el código que lo lee para que Copilot CLI entienda el panorama completo al sugerir mejoras en el manejo de errores.

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>Workflow 4: Test Generation</strong> - Genera pruebas y casos límite de forma automática</summary>

<img src="../../../03-development-workflows/images/test-gen-swimlane-single.png" alt="Flujo de generación de pruebas: analizar función, generar pruebas, incluir casos límite, ejecutar." width="800"/>

> **Prueba esto primero:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### La "Explosión de pruebas" - 2 pruebas vs 15+ pruebas

Al escribir pruebas manualmente, los desarrolladores típicamente crean 2-3 pruebas básicas:
- Probar entrada válida
- Probar entrada inválida
- Probar un caso límite

Observa lo que ocurre cuando pides a Copilot CLI generar pruebas exhaustivas. Este prompt usa una lista de viñetas estructurada con una referencia de archivo `@` para guiar a Copilot CLI hacia una cobertura de prueba completa:

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Test Generation Demo](../../../03-development-workflows/images/test-gen-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

---

**Lo que obtienes**: 15+ pruebas exhaustivas incluyendo:

```python
class TestBookCollection:
    # Camino feliz
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # Operaciones de búsqueda
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # Casos límite
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # Persistencia de datos
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # Caracteres especiales
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**Resultado**: En 30 segundos, obtienes pruebas de casos límite que tomarían una hora en pensar y escribir.

---

### Pruebas unitarias

Apunta a una sola función y enumera las categorías de entrada que quieres probar para que Copilot CLI genere pruebas unitarias enfocadas y completas.

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### Ejecutar pruebas

Hazle a Copilot CLI una pregunta en lenguaje natural sobre tu cadena de herramientas. Puede generar el comando shell correcto para ti.

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI responde:
# cd samples/book-app-project && python -m pytest tests/
# O para salida detallada: python -m pytest tests/ -v
# Para ver las sentencias print: python -m pytest tests/ -s
```

### Prueba escenarios específicos

Enumera escenarios avanzados o complicados que quieras cubrir para que Copilot CLI vaya más allá del camino feliz.

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### Agregar pruebas al archivo existente

Ask for *additional* tests for a single function so Copilot CLI generates new cases that complement what you already have.

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>Flujo de trabajo 5: Integración con Git</strong> - Mensajes de commit, descripciones de PR, /pr, /delegate y /diff</summary>

<img src="../../../03-development-workflows/images/git-integration-swimlane-single.png" alt="Flujo de integración con Git: preparar cambios, generar mensaje, commit, crear PR." width="800"/>

> 💡 **Este flujo de trabajo asume familiaridad básica con git** (preparar cambios, commits, ramas). Si git es nuevo para ti, prueba primero los otros cuatro flujos de trabajo.

### Generar mensajes de commit

> **Intenta esto primero:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — prepara algunos cambios, luego ejecuta esto para ver cómo Copilot CLI escribe tu mensaje de commit.

This example uses the `-p` inline prompt flag with shell command substitution to pipe `git diff` output directly into Copilot CLI for a one-shot commit message. The `$(...)` syntax runs the command inside the parentheses and inserts its output into the outer command.

```bash

# Ver qué cambió
git diff --staged

# Generar mensaje de commit usando el formato [Conventional Commit](../GLOSSARY.md#conventional-commit)
# (mensajes estructurados como "feat(books): agregar búsqueda" o "fix(data): manejar entrada vacía")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Salida: "feat(books): agregar búsqueda parcial de nombre de autor
#
# - Actualizar find_by_author para admitir coincidencias parciales
# - Añadir comparación sin distinción entre mayúsculas y minúsculas
# - Mejorar la experiencia del usuario al buscar autores"
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de integración con Git](../../../03-development-workflows/images/git-integration-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

### Explicar cambios

Pasa la salida de `git show` a un prompt `-p` para obtener un resumen en lenguaje natural del último commit.

```bash
# ¿Qué cambió este commit?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### Descripción de PR

Combina la salida de `git log` con una plantilla de prompt estructurada para generar automáticamente una descripción completa del pull request.

```bash
# Generar la descripción del PR a partir de los cambios en la rama
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### Usar /pr en modo interactivo para la rama actual

Si estás trabajando con una rama en el modo interactivo de Copilot CLI, puedes usar el comando `/pr` para trabajar con pull requests. Usa `/pr` para ver un PR, crear uno nuevo, arreglar un PR existente o dejar que Copilot CLI decida automáticamente según el estado de la rama.

```bash
copilot

> /pr [view|create|fix|auto]
```

### Revisar antes del push

Usa `git diff main..HEAD` dentro de un prompt `-p` para una verificación rápida (pre-push) de todos los cambios de la rama.

```bash
# Última revisión antes de hacer push
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### Usar /delegate para tareas en segundo plano

El comando `/delegate` delega trabajo al agente en la nube de GitHub Copilot. Usa el comando slash `/delegate` (o el atajo `&`) para descargar una tarea bien definida a un agente en segundo plano.

```bash
copilot

> /delegate Add input validation to the login form

# O usa el atajo con el prefijo &:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Confirma tus cambios en una nueva rama
# 2. Abre un pull request en borrador
# 3. Funciona en segundo plano en GitHub
# 4. Solicita tu revisión cuando termine
```

This is great for well-defined tasks you want completed while you focus on other work.

### Usar /diff para revisar los cambios de la sesión

El comando `/diff` muestra todos los cambios realizados durante tu sesión actual. Usa este comando slash para ver un diff visual de todo lo que Copilot CLI ha modificado antes de que confirmes los cambios.

```bash
copilot

# Después de hacer algunos cambios...
> /diff

# Muestra una comparación visual de todos los archivos modificados en esta sesión
# Ideal para revisar antes de confirmar los cambios
```

</details>

---

## Consejo rápido: Investigar antes de planear o codificar

When you need to investigate a library, understand best practices, or explore an unfamiliar topic, use `/research` to run a deep research investigation before writing any code:

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot searches GitHub repositories and web sources, then returns a summary with references. This is useful when you're about to start a new feature and want to make informed decisions first. You can share the results using `/share`.

> 💡 **Consejo**: `/research` funciona bien *antes* de `/plan`. Investiga el enfoque, luego planifica la implementación.

---

## Poniéndolo todo junto: flujo de trabajo de corrección de errores

Here's a complete workflow for fixing a reported bug:

```bash

# 1. Comprender el informe de errores
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. Depurar el problema y corregirlo (continuando en la misma sesión)
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. Generar pruebas para la corrección
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# Salir de la sesión interactiva

> /exit

# 4. Ejecutar git add

# Poner los cambios en el área de preparación para que git diff --staged tenga algo con lo que trabajar
git add .

# 5. Generar el mensaje de commit
copilot -p "Generate commit message for: $(git diff --staged)"

# Example Output: "fix(books): soportar búsqueda parcial por nombre de autor"

# 6. Confirmar los cambios (opcional)

git commit -m "<paste generated message>"
```

### Resumen del flujo de corrección de errores

| Paso | Acción | Copilot Command |
|------|--------|-----------------|
| 1 | Comprender el error | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | Análisis y corrección | `> Show me the function and fix the issue` |
| 3 | Generar pruebas | `> Generate tests for [specific scenarios]` |
| 4 | Preparar cambios | `git add .` |
| 5 | Generar mensaje de commit | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | Confirmar cambios| `git commit -m "<paste generated message>"` |

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración de escritorio acogedora con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica." width="800"/>

Ahora es tu turno para aplicar estos flujos de trabajo.

---

## ▶️ Inténtalo tú mismo

After completing the demos, try these variations:

1. **Desafío detective de bugs**: Pídele a Copilot CLI que depure la función `mark_as_read` en `samples/book-app-buggy/books_buggy.py`. ¿Explicó por qué la función marca TODOS los libros como leídos en vez de solo uno?
2. **Desafío de pruebas**: Genera pruebas para la función `add_book` en la aplicación de libros. Cuenta cuántos casos límite incluye Copilot CLI que tú no habrías pensado.
3. **Desafío de mensaje de commit**: Haz cualquier cambio pequeño en un archivo de la aplicación de libros, agrégalo al área de staging (`git add .`), luego ejecuta:
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   ¿Es el mensaje mejor que lo que hubieras escrito rápidamente?

**Autoevaluación**: Entiendes los flujos de trabajo de desarrollo cuando puedas explicar por qué "depurar este bug" es más poderoso que "encontrar bugs" (¡el contexto importa!).

---

## 📝 Tarea

### Desafío principal: Refactorizar, probar y entregar

The hands-on examples focused on `find_book_by_title` and code reviews. Now practice the same workflow skills on different functions in `book-app-project`:

1. **Revisar**: Pide a Copilot CLI que revise `remove_book()` en `books.py` en busca de casos límite y problemas potenciales:
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **Refactorizar**: Pide a Copilot CLI que mejore `remove_book()` para manejar casos límite como coincidencia sin distinguir mayúsculas/minúsculas y devolver retroalimentación útil cuando no se encuentra un libro
3. **Probar**: Genera pruebas con pytest específicamente para la función `remove_book()` mejorada, cubriendo:
   - Eliminar un libro que existe
   - Coincidencia de título sin distinguir mayúsculas/minúsculas
   - Un libro que no existe devuelve retroalimentación apropiada
   - Eliminar de una colección vacía
4. **Revisión**: Pon tus cambios en staging y ejecuta `/review` para comprobar si quedan problemas
5. **Commit**: Genera un mensaje de commit convencional:
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 Sugerencias (haz clic para expandir)</summary>

**Ejemplos de prompts para cada paso:**

```bash
copilot

# Paso 1: Revisar
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# Paso 2: Refactorizar
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# Paso 3: Probar
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# Paso 4: Revisar
> /review

# Paso 5: Confirmar
> Generate a conventional commit message for this refactor
```

**Consejo:** Después de mejorar `remove_book()`, prueba a preguntarle a Copilot CLI: "¿Hay otras funciones en este archivo que podrían beneficiarse de las mismas mejoras?". Puede sugerir cambios similares en `find_book_by_title()` o `find_by_author()`.

</details>

### Bonus Challenge: Create an application with the Copilot CLI

> 💡 **Nota**: Este ejercicio de GitHub Skills usa **Node.js** en lugar de Python. Las técnicas de GitHub Copilot CLI que practicarás - crear issues, generar código y colaborar desde la terminal - aplican a cualquier lenguaje.

The exercise shows developers how to use GitHub Copilot CLI to create issues, generate code, and collaborate from the terminal while building a Node.js calculator app. You'll install the CLI, use templates and agents, and practice iterative, command-line driven development.

##### <img src="../../../images/github-skills-logo.png" width="28" align="center" /> [Iniciar el ejercicio de Skills "Crear aplicaciones con el Copilot CLI"](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 Errores comunes y solución de problemas (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué pasa | Solución |
|---------|--------------|-----|
| Usar prompts vagos como "Revisa este código" | Retroalimentación genérica que omite problemas específicos | Sé específico: "Revisa para inyección SQL, XSS y problemas de autenticación" |
| No usar `/review` para revisiones de código | Pierdes el agente optimizado para revisión de código | Usa `/review`, que está ajustado para una salida con alta relación señal/ruido |
| Pedir "find bugs" sin contexto | Copilot CLI no sabe qué error estás experimentando | Describe el síntoma: "Los usuarios reportan que X sucede cuando Y" |
| Generar pruebas sin especificar el framework | Las pruebas pueden usar sintaxis incorrecta o una biblioteca de aserciones equivocada | Especifica: "Generar pruebas usando Jest" o "usando pytest" |

### Solución de problemas

**La revisión parece incompleta** - Sé más específico sobre qué buscar:

```bash
copilot

# En lugar de:
> Review @samples/book-app-project/book_app.py

# Prueba:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**Las pruebas no coinciden con mi framework** - Especifica el framework:

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**La refactorización cambia el comportamiento** - Pide a Copilot CLI que preserve el comportamiento:

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# Resumen

## 🔑 Conclusiones clave

<img src="../../../03-development-workflows/images/specialized-workflows.png" alt="Flujos de trabajo especializados para cada tarea: revisión de código, refactorización, depuración, pruebas e integración con Git" width="800"/>

1. **La revisión de código se vuelve más completa con prompts específicos**
2. **La refactorización es más segura cuando generas pruebas primero**
3. **La depuración se beneficia de mostrar a Copilot CLI el error Y el código**
4. **La generación de pruebas debe incluir casos límite y escenarios de error**
5. **La integración con Git automatiza mensajes de commit y descripciones de PR**

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ✅ Punto de control: Has dominado lo esencial

**¡Felicidades!** Ahora tienes todas las habilidades básicas para ser productivo con GitHub Copilot CLI:

| Habilidad | Capítulo | Ahora puedes... |
|-------|---------|----------------|
| Comandos básicos | Cap 01 | Usar el modo interactivo, modo plan, modo programático (-p), y comandos slash |
| Contexto | Cap 02 | Referenciar archivos con `@`, gestionar sesiones, entender las ventanas de contexto |
| Flujos de trabajo | Cap 03 | Revisar código, refactorizar, depurar, generar pruebas, integrar con git |

Los capítulos 04-06 cubren características adicionales que añaden aún más potencia y vale la pena aprender.

---

## 🛠️ Construyendo tu flujo de trabajo personal

No hay una única forma "correcta" de usar GitHub Copilot CLI. Aquí tienes algunos consejos mientras desarrollas tus propios patrones:

> 📚 **Documentación oficial**: [Buenas prácticas de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices) para flujos de trabajo recomendados y consejos de GitHub.

- **Empieza con `/plan`** para cualquier cosa no trivial. Refina el plan antes de la ejecución: un buen plan conduce a mejores resultados.
- **Guarda los prompts que funcionen bien.** Cuando Copilot CLI cometa un error, anota qué salió mal. Con el tiempo, esto se convierte en tu manual personal.
- **Experimenta libremente.** Algunos desarrolladores prefieren prompts largos y detallados. Otros prefieren prompts cortos con seguimientos. Prueba diferentes enfoques y observa qué se siente más natural.

> 💡 **Próximo**: En los capítulos 04 y 05 aprenderás cómo codificar tus mejores prácticas en instrucciones personalizadas y habilidades que Copilot CLI carga automáticamente.

---

## ➡️ Qué sigue

| Capítulo | Qué cubre | Cuándo lo necesitarás |
|---------|----------------|---------------------|
| Ch 04: Agents | Crear personajes de IA especializados | Cuando quieras expertos de dominio (frontend, seguridad) |
| Ch 05: Skills | Cargar automáticamente instrucciones para tareas | Cuando repites los mismos prompts con frecuencia |
| Ch 06: MCP | Conectar servicios externos | Cuando necesites datos en vivo desde GitHub, bases de datos |

**Recomendación**: Prueba los flujos de trabajo principales durante una semana, luego vuelve a los capítulos 04-06 cuando tengas necesidades específicas.

---

## Continúa con temas adicionales

En **[Capítulo 04: Agentes e instrucciones personalizadas](../04-agents-custom-instructions/README.md)**, aprenderás:

- Usar agentes integrados (`/plan`, `/review`)
- Crear agentes especializados (experto frontend, auditor de seguridad) con archivos `.agent.md`
- Patrones de colaboración multi-agente
- Archivos de instrucciones personalizadas para estándares del proyecto

---

**[← Volver al Capítulo 02](../02-context-conversations/README.md)** | **[Continuar al Capítulo 04 →](../04-agents-custom-instructions/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->