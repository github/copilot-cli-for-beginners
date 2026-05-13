![Capítulo 03: Flujos de trabajo de desarrollo](../../../03-development-workflows/images/chapter-header.png)

> **¿Y si la IA pudiera encontrar errores que ni siquiera sabías que tenías que preguntar?**

En este capítulo, GitHub Copilot CLI se convierte en tu compañero diario. Lo usarás dentro de los flujos de trabajo en los que ya confías cada día: pruebas, refactorización, depuración y Git.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Realizar revisiones exhaustivas de código con Copilot CLI
- Refactorizar código heredado de forma segura
- Depurar problemas con asistencia de IA
- Generar tests automáticamente
- Integrar Copilot CLI con tu flujo de trabajo de git

> ⏱️ **Tiempo estimado**: ~60 minutos (15 min de lectura + 45 min de práctica)

---

## 🧩 Analogía del mundo real: el flujo de trabajo de un carpintero

Un carpintero no solo sabe usar herramientas, tiene *flujos de trabajo* para distintas tareas:

<img src="../../../03-development-workflows/images/carpenter-workflow-steps.png" alt="Taller de artesano que muestra tres carriles de flujo de trabajo: Construir muebles (Medir, Cortar, Ensamblar, Acabar), Reparar daños (Evaluar, Quitar, Reparar, Igualar) y Control de calidad (Inspeccionar, Probar uniones, Verificar alineación)" width="800"/>

De forma similar, los desarrolladores tienen flujos de trabajo para distintas tareas. GitHub Copilot CLI mejora cada uno de estos flujos, haciéndote más eficiente y efectivo en tus tareas diarias de programación.

---

# Los cinco flujos de trabajo

<img src="../../../03-development-workflows/images/five-workflows.png" alt="Cinco iconos de neón brillantes que representan los flujos de revisión de código, pruebas, depuración, refactorización e integración con git" width="800"/>

Cada flujo de trabajo a continuación es autocontenido. Elige los que se ajusten a tus necesidades actuales o trabaja con todos.

---

## Elige tu propia aventura

Este capítulo cubre cinco flujos de trabajo que los desarrolladores suelen usar. **¡Sin embargo, no necesitas leerlos todos a la vez!** Cada flujo de trabajo es autocontenido en una sección colapsable a continuación. Elige los que se ajusten a lo que necesitas y que mejor encajen con tu proyecto actual. Siempre puedes volver y explorar los demás más adelante.

<img src="../../../03-development-workflows/images/five-workflows-swimlane.png" alt="Cinco flujos de trabajo de desarrollo: Revisión de código, Refactorización, Depuración, Generación de tests e Integración con Git mostrados como carriles horizontales" width="800"/>

| Quiero... | Saltar a |
|---|---|
| Revisar código antes de fusionar | [Flujo 1: Revisión de código](#workflow-1-code-review) |
| Limpiar código desordenado o heredado | [Flujo 2: Refactorización](#workflow-2-refactoring) |
| Localizar y corregir un error | [Flujo 3: Depuración](#workflow-3-debugging) |
| Generar tests para mi código | [Flujo 4: Generación de tests](#workflow-4-test-generation) |
| Escribir mejores commits y PRs | [Flujo 5: Integración con Git](#workflow-5-git-integration) |
| Investigar antes de codificar | [Consejo rápido: investiga antes de planificar o codificar](#consejo-rápido-investiga-antes-de-planificar-o-codificar) |
| Ver un flujo completo de corrección de errores de principio a fin | [Poniéndolo todo junto](#poniéndolo-todo-junto-flujo-de-corrección-de-errores) |

**Selecciona un flujo de trabajo a continuación para expandirlo** y ver cómo GitHub Copilot CLI puede mejorar tu proceso de desarrollo en esa área.

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>Flujo 1: Revisión de código</strong> - Revisar archivos, usar el agente /review, crear listas de verificación por severidad</summary>

<img src="../../../03-development-workflows/images/code-review-swimlane-single.png" alt="Flujo de revisión de código: revisar, identificar problemas, priorizar, generar lista de verificación." width="800"/>

### Revisión básica

Este ejemplo usa el símbolo `@` para referenciar un archivo, dándole a Copilot CLI acceso directo a su contenido para su revisión.

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de revisión de código](../../../03-development-workflows/images/code-review-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

### Revisión de validación de entrada

Pídele a Copilot CLI que enfoque su revisión en una preocupación específica (aquí, validación de entrada) listando las categorías que te importan en el prompt.

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### Revisión de proyecto entre archivos

Referencia un directorio completo con `@` para que Copilot CLI escanee todos los archivos del proyecto a la vez.

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### Revisión de código interactiva

Usa una conversación de varios turnos para profundizar. Empieza con una revisión amplia, luego haz preguntas de seguimiento sin reiniciar.

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI provides detailed review

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI shows potential issues with empty strings, special characters

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI generates prioritized action items
```

### Plantilla de lista de verificación de revisión

Pídele a Copilot CLI que estructure su salida en un formato específico (aquí, una lista de verificación markdown categorizada por severidad que puedes pegar en un issue).

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Entender los cambios de Git (importante para /review)

Antes de usar el comando `/review`, necesitas entender dos tipos de cambios en git:

| Tipo de cambio | Qué significa | Cómo verlo |
|-------------|---------------|------------|
| **Cambios en stage** | Archivos que has marcado para el próximo commit con `git add` | `git diff --staged` |
| **Cambios fuera de stage** | Archivos que has modificado pero aún no has añadido | `git diff` |

```bash
# Quick reference
git status           # Shows both staged and unstaged
git add file.py      # Stage a file for commit
git diff             # Shows unstaged changes
git diff --staged    # Shows staged changes
```

### Usando el comando /review

El comando `/review` invoca el **agente code-review** integrado, que está optimizado para analizar cambios en stage y fuera de stage con una salida de alta relación señal-ruido. Usa un comando de barra para activar un agente integrado especializado en lugar de escribir un prompt libre.

```bash
copilot

> /review
# Invokes the code-review agent on staged/unstaged changes
# Provides focused, actionable feedback

> /review Check for security issues in authentication
# Run review with specific focus area
```

> 💡 **Consejo**: El agente code-review funciona mejor cuando tienes cambios pendientes. Pasa tus archivos a stage con `git add` para revisiones más enfocadas.

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>Flujo 2: Refactorización</strong> - Reestructurar código, separar responsabilidades, mejorar el manejo de errores</summary>

<img src="../../../03-development-workflows/images/refactoring-swimlane-single.png" alt="Flujo de refactorización: evaluar el código, planificar cambios, implementar, verificar el comportamiento." width="800"/>

### Refactorización simple

> **Prueba esto primero:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

Empieza con mejoras sencillas. Pruébalas en la app de libros. Cada prompt usa una referencia de archivo `@` junto con una instrucción específica de refactorización para que Copilot CLI sepa exactamente qué cambiar.

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **¿Nuevo en la refactorización?** Empieza con peticiones sencillas como añadir type hints o mejorar nombres de variables antes de abordar transformaciones complejas.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de refactorización](../../../03-development-workflows/images/refactor-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

### Separar responsabilidades

Referencia varios archivos con `@` en un solo prompt para que Copilot CLI pueda mover código entre ellos como parte de la refactorización.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### Mejorar el manejo de errores

Proporciona dos archivos relacionados y describe la preocupación transversal para que Copilot CLI pueda sugerir una solución consistente en ambos.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### Añadir documentación

Usa una lista detallada de viñetas para especificar exactamente qué debe contener cada docstring.

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### Refactorización segura con tests

Encadena dos peticiones relacionadas en una conversación de varios turnos. Primero genera tests, luego refactoriza con esos tests como red de seguridad.

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Get tests first

> Now refactor the BookCollection class to use a context manager for file operations

# Refactor with confidence - tests verify behavior is preserved
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>Flujo 3: Depuración</strong> - Localizar errores, auditorías de seguridad, rastrear problemas entre archivos</summary>

<img src="../../../03-development-workflows/images/debugging-swimlane-single.png" alt="Flujo de depuración: entender el error, localizar la causa raíz, corregir, probar." width="800"/>

### Depuración simple

> **Prueba esto primero:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

Empieza describiendo qué falla. Aquí tienes patrones comunes de depuración que puedes probar con la app de libros con errores. Cada prompt empareja una referencia de archivo `@` con una descripción clara del síntoma para que Copilot CLI pueda localizar y diagnosticar el error.

```bash
copilot

# Pattern: "Expected X but got Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Pattern: "Unexpected behavior"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Pattern: "Wrong results"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **Consejo de depuración**: Describe el *síntoma* (lo que ves) y la *expectativa* (lo que debería ocurrir). Copilot CLI averigua el resto.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de corrección de error](../../../03-development-workflows/images/fix-bug-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

### El "Detective de errores" - La IA encuentra errores RELACIONADOS

Aquí es donde brilla la depuración consciente del contexto. Prueba este escenario con la app de libros con errores. Proporciona el archivo completo mediante `@` y describe solo el síntoma reportado por el usuario. Copilot CLI rastreará la causa raíz y puede detectar errores adicionales cercanos.

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

**Por qué importa esto**: Copilot CLI lee el archivo completo, entiende el contexto de tu reporte de error y te da una corrección específica con una explicación clara.

> 💡 **Bonus**: Como Copilot CLI analiza todo el archivo, a menudo descubre *otros* problemas que no preguntaste. Por ejemplo, mientras corrige la búsqueda por autor, ¡Copilot CLI también podría notar el error de sensibilidad a mayúsculas en `find_book_by_title`!

### Apartado de seguridad del mundo real

Si bien depurar tu propio código es importante, entender vulnerabilidades de seguridad en aplicaciones de producción es crítico. Prueba este ejemplo: Apunta Copilot CLI a un archivo desconocido y pídele que audite problemas de seguridad.

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

Este archivo demuestra patrones de seguridad reales que encontrarás en apps de producción.

> 💡 **Términos comunes de seguridad que encontrarás:**
> - **Inyección SQL**: Cuando la entrada del usuario se inserta directamente en una consulta de base de datos, permitiendo a atacantes ejecutar comandos maliciosos
> - **Consultas parametrizadas**: La alternativa segura - los marcadores de posición (`?`) separan los datos del usuario de los comandos SQL
> - **Condición de carrera**: Cuando dos operaciones ocurren al mismo tiempo e interfieren entre sí
> - **XSS (Cross-Site Scripting)**: Cuando los atacantes inyectan scripts maliciosos en páginas web

---

### Entender un error

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

Referencia varios archivos y pídele a Copilot CLI que siga el flujo de datos a través de ellos para localizar dónde se origina el problema.

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### Entender problemas de datos

Incluye un archivo de datos junto al código que lo lee para que Copilot CLI entienda el panorama completo al sugerir mejoras en el manejo de errores.

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>Flujo 4: Generación de tests</strong> - Generar tests exhaustivos y casos límite automáticamente</summary>

<img src="../../../03-development-workflows/images/test-gen-swimlane-single.png" alt="Flujo de generación de tests: analizar función, generar tests, incluir casos límite, ejecutar." width="800"/>

> **Prueba esto primero:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### La "Explosión de tests" - 2 tests vs 15+ tests

Al escribir tests manualmente, los desarrolladores normalmente crean 2-3 tests básicos:
- Probar entrada válida
- Probar entrada inválida
- Probar un caso límite

¡Mira lo que ocurre cuando le pides a Copilot CLI que genere tests exhaustivos! Este prompt usa una lista de viñetas estructurada con una referencia de archivo `@` para guiar a Copilot CLI hacia una cobertura de tests completa:

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

![Demo de generación de tests](../../../03-development-workflows/images/test-gen-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

**Lo que obtienes**: 15+ tests exhaustivos incluyendo:

```python
class TestBookCollection:
    # Happy path
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # Find operations
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # Edge cases
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # Data persistence
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # Special characters
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**Resultado**: En 30 segundos, obtienes tests de casos límite que tomaría una hora pensar y escribir.

---

### Tests unitarios

Apunta a una sola función y enumera las categorías de entrada que quieres probar para que Copilot CLI genere tests unitarios enfocados y exhaustivos.

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### Ejecutar tests

Hazle a Copilot CLI una pregunta en lenguaje natural sobre tu cadena de herramientas. Puede generar el comando de shell adecuado por ti.

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI responds:
# cd samples/book-app-project && python -m pytest tests/
# Or for verbose output: python -m pytest tests/ -v
# To see print statements: python -m pytest tests/ -s
```

### Tests para escenarios específicos

Lista escenarios avanzados o complicados que quieres cubrir para que Copilot CLI vaya más allá del happy path.

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### Añadir tests a un archivo existente

Pide tests *adicionales* para una sola función para que Copilot CLI genere casos nuevos que complementen los que ya tienes.

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
<summary><strong>Flujo 5: Integración con Git</strong> - Mensajes de commit, descripciones de PR, /pr, /delegate y /diff</summary>

<img src="../../../03-development-workflows/images/git-integration-swimlane-single.png" alt="Flujo de integración con Git: pasar cambios a stage, generar mensaje, hacer commit, crear PR." width="800"/>

> 💡 **Este flujo de trabajo asume familiaridad básica con git** (stage, commit, ramas). Si git es nuevo para ti, prueba primero los otros cuatro flujos.

### Generar mensajes de commit

> **Prueba esto primero:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — pasa algunos cambios a stage, luego ejecuta esto para ver a Copilot CLI escribir tu mensaje de commit.

Este ejemplo usa la opción de prompt en línea `-p` con sustitución de comandos de shell para canalizar la salida de `git diff` directamente a Copilot CLI para un mensaje de commit de un solo disparo. La sintaxis `$(...)` ejecuta el comando dentro de los paréntesis e inserta su salida en el comando exterior.

```bash

# See what changed
git diff --staged

# Generate commit message using [Conventional Commit](../../../GLOSSARY.md#conventional-commit) format
# (structured messages like "feat(books): add search" or "fix(data): handle empty input")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Output: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de integración con Git](../../../03-development-workflows/images/git-integration-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

### Explicar cambios

Canaliza la salida de `git show` a un prompt `-p` para obtener un resumen en lenguaje natural del último commit.

```bash
# What did this commit change?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### Descripción de PR

Combina la salida de `git log` con una plantilla de prompt estructurado para autogenerar una descripción completa de pull request.

```bash
# Generate PR description from branch changes
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### Usando /pr en modo interactivo para la rama actual

Si estás trabajando con una rama en el modo interactivo de Copilot CLI, puedes usar el comando `/pr` para trabajar con pull requests. Usa `/pr` para ver un PR, crear un nuevo PR, corregir un PR existente o dejar que Copilot CLI decida automáticamente según el estado de la rama.

```bash
copilot

> /pr [view|create|fix|auto]
```

### Revisar antes de hacer push

Usa `git diff main..HEAD` dentro de un prompt `-p` para una rápida verificación antes del push entre todos los cambios de la rama.

```bash
# Last check before pushing
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### Usando /delegate para tareas en segundo plano

El comando `/delegate` delega trabajo al agente en la nube de GitHub Copilot. Usa el comando de barra `/delegate` (o el atajo `&`) para delegar una tarea bien definida a un agente en segundo plano.

```bash
copilot

> /delegate Add input validation to the login form

# Or use the & prefix shortcut:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Commits your changes to a new branch
# 2. Opens a draft pull request
# 3. Works in the background on GitHub
# 4. Requests your review when done
```

Esto es excelente para tareas bien definidas que quieres completar mientras te enfocas en otro trabajo.

### Usando /diff para revisar cambios de la sesión

El comando `/diff` muestra todos los cambios realizados durante tu sesión actual. Usa este comando de barra para ver un diff visual de todo lo que Copilot CLI ha modificado antes de hacer commit.

```bash
copilot

# After making some changes...
> /diff

# Shows a visual diff of all files modified in this session
# Great for reviewing before committing
```

</details>

---

## Consejo rápido: investiga antes de planificar o codificar

Cuando necesitas investigar una librería, entender buenas prácticas o explorar un tema desconocido, usa `/research` para realizar una investigación profunda antes de escribir cualquier código:

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot busca en repositorios de GitHub y fuentes web, luego devuelve un resumen con referencias. Esto es útil cuando estás a punto de empezar una nueva característica y quieres tomar decisiones informadas primero. Puedes compartir los resultados usando `/share`.

> 💡 **Consejo**: `/research` funciona bien *antes* de `/plan`. Investiga el enfoque, luego planifica la implementación.

---

## Poniéndolo todo junto: flujo de corrección de errores

Aquí tienes un flujo completo para corregir un error reportado:

```bash

# 1. Understand the bug report
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. Debug the issue and fix (continuing in same session)
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. Generate tests for the fix
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# Exit the interactive session

> /exit

# 4. Run git add

# Stage the changes so git diff --staged has something to work with
git add .

# 5. Generate commit message
copilot -p "Generate commit message for: $(git diff --staged)"

# Example Output: "fix(books): support partial author name search"

# 6. Commit changes (optional)

git commit -m "<paste generated message>"
```

### Resumen del flujo de corrección de errores

| Paso | Acción | Comando de Copilot |
|------|--------|-----------------|
| 1 | Entender el error | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | Análisis y corrección | `> Show me the function and fix the issue` |
| 3 | Generar tests | `> Generate tests for [specific scenarios]` |
| 4 | Pasar cambios a stage | `git add .` |
| 5 | Generar mensaje de commit | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | Hacer commit | `git commit -m "<paste generated message>"` |

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración acogedora de escritorio con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Ahora es tu turno de aplicar estos flujos de trabajo.

---

## ▶️ Pruébalo tú mismo

Tras completar los demos, prueba estas variaciones:

1. **Reto del Detective de errores**: Pídele a Copilot CLI que depure la función `mark_as_read` en `samples/book-app-buggy/books_buggy.py`. ¿Explicó por qué la función marca TODOS los libros como leídos en lugar de solo uno?

2. **Reto de tests**: Genera tests para la función `add_book` en la app de libros. Cuenta cuántos casos límite incluye Copilot CLI que no se te habrían ocurrido.

3. **Reto de mensaje de commit**: Haz cualquier cambio pequeño en un archivo de la app de libros, pásalo a stage (`git add .`) y luego ejecuta:
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   ¿Es el mensaje mejor de lo que habrías escrito rápidamente?

**Autocomprobación**: Entiendes los flujos de trabajo de desarrollo cuando puedes explicar por qué "depura este error" es más potente que "encuentra errores" (¡el contexto importa!).

---

## 📝 Tarea

### Reto principal: refactoriza, prueba y entrega

Los ejemplos prácticos se centraron en `find_book_by_title` y revisiones de código. Ahora practica las mismas habilidades de flujo de trabajo en diferentes funciones en `book-app-project`:

1. **Revisar**: Pídele a Copilot CLI que revise `remove_book()` en `books.py` para casos límite y problemas potenciales:
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **Refactorizar**: Pídele a Copilot CLI que mejore `remove_book()` para manejar casos límite como coincidencia sin distinguir mayúsculas y minúsculas y devolver retroalimentación útil cuando no se encuentre un libro
3. **Probar**: Genera tests pytest específicamente para la función `remove_book()` mejorada, cubriendo:
   - Eliminar un libro que existe
   - Coincidencia de título sin distinguir mayúsculas y minúsculas
   - Un libro que no existe devuelve retroalimentación apropiada
   - Eliminar de una colección vacía
4. **Revisar**: Pasa tus cambios a stage y ejecuta `/review` para comprobar si quedan problemas
5. **Commit**: Genera un mensaje de commit convencional:
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Prompts de muestra para cada paso:**

```bash
copilot

# Step 1: Review
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# Step 2: Refactor
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# Step 3: Test
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# Step 4: Review
> /review

# Step 5: Commit
> Generate a conventional commit message for this refactor
```

**Consejo:** Tras mejorar `remove_book()`, prueba a preguntarle a Copilot CLI: "¿Hay otras funciones en este archivo que podrían beneficiarse de las mismas mejoras?". Puede sugerir cambios similares para `find_book_by_title()` o `find_by_author()`.

</details>

### Reto extra: crear una aplicación con Copilot CLI

> 💡 **Nota**: Este ejercicio de GitHub Skills usa **Node.js** en lugar de Python. Las técnicas de GitHub Copilot CLI que practicarás (crear issues, generar código y colaborar desde la terminal) se aplican a cualquier lenguaje.

El ejercicio muestra a los desarrolladores cómo usar GitHub Copilot CLI para crear issues, generar código y colaborar desde la terminal mientras construyen una app calculadora en Node.js. Instalarás la CLI, usarás plantillas y agentes, y practicarás desarrollo iterativo dirigido por línea de comandos.

##### <img src="../../../images/github-skills-logo.png" width="28" align="center" /> [Comienza el ejercicio de Skills "Create applications with the Copilot CLI"](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Usar prompts vagos como "Review this code" | Retroalimentación genérica que pasa por alto problemas específicos | Sé específico: "Review for SQL injection, XSS, and auth issues" |
| No usar `/review` para revisiones de código | Te pierdes el agente code-review optimizado | Usa `/review` que está afinado para una salida con alta relación señal-ruido |
| Pedir "encontrar errores" sin contexto | Copilot CLI no sabe qué error estás experimentando | Describe el síntoma: "Users report X happens when Y" |
| Generar tests sin especificar el framework | Los tests pueden usar la sintaxis o la librería de aserciones equivocada | Especifica: "Generate tests using Jest" o "using pytest" |

### Solución de problemas

**La revisión parece incompleta** - Sé más específico sobre qué buscar:

```bash
copilot

# Instead of:
> Review @samples/book-app-project/book_app.py

# Try:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**Los tests no coinciden con mi framework** - Especifica el framework:

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**La refactorización cambia el comportamiento** - Pídele a Copilot CLI que preserve el comportamiento:

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# Resumen

## 🔑 Conclusiones clave

<img src="../../../03-development-workflows/images/specialized-workflows.png" alt="Flujos de trabajo especializados para cada tarea: revisión de código, refactorización, depuración, pruebas e integración con Git" width="800"/>

1. **La revisión de código** se vuelve exhaustiva con prompts específicos
2. **La refactorización** es más segura cuando generas tests primero
3. **La depuración** se beneficia de mostrar a Copilot CLI el error Y el código
4. **La generación de tests** debe incluir casos límite y escenarios de error
5. **La integración con Git** automatiza mensajes de commit y descripciones de PR

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver una lista completa de comandos y atajos.

---

## ✅ Punto de control: has dominado lo esencial

**¡Felicidades!** Ahora tienes todas las habilidades fundamentales para ser productivo con GitHub Copilot CLI:

| Habilidad | Capítulo | Ahora puedes... |
|-------|---------|----------------|
| Comandos básicos | Cap 01 | Usar el modo interactivo, modo de planificación, modo programático (-p) y comandos de barra |
| Contexto | Cap 02 | Referenciar archivos con `@`, gestionar sesiones, entender ventanas de contexto |
| Flujos de trabajo | Cap 03 | Revisar código, refactorizar, depurar, generar tests, integrar con git |

Los Capítulos 04-06 cubren características adicionales que añaden aún más potencia y vale la pena aprender.

---

## 🛠️ Construyendo tu flujo de trabajo personal

No hay una única manera "correcta" de usar GitHub Copilot CLI. Aquí tienes algunos consejos mientras desarrollas tus propios patrones:

> 📚 **Documentación oficial**: [Copilot CLI best practices](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices) para flujos de trabajo y consejos recomendados de GitHub.

- **Empieza con `/plan`** para cualquier cosa no trivial. Refina el plan antes de la ejecución: un buen plan lleva a mejores resultados.
- **Guarda los prompts que funcionan bien.** Cuando Copilot CLI cometa un error, anota qué salió mal. Con el tiempo, esto se convierte en tu manual personal.
- **Experimenta libremente.** Algunos desarrolladores prefieren prompts largos y detallados. Otros prefieren prompts cortos con seguimientos. Prueba diferentes enfoques y observa cuál se siente natural.

> 💡 **Próximamente**: En los Capítulos 04 y 05, aprenderás cómo codificar tus mejores prácticas en instrucciones personalizadas y skills que Copilot CLI carga automáticamente.

---

## ➡️ Qué sigue

Los capítulos restantes cubren características adicionales que extienden las capacidades de Copilot CLI:

| Capítulo | Qué cubre | Cuándo lo querrás |
|---------|----------------|---------------------|
| Cap 04: Agentes | Crear personas IA especializadas | Cuando quieras expertos de dominio (frontend, seguridad) |
| Cap 05: Skills | Cargar instrucciones automáticamente para tareas | Cuando repitas los mismos prompts a menudo |
| Cap 06: MCP | Conectar servicios externos | Cuando necesites datos en vivo de GitHub, bases de datos |

**Recomendación**: Prueba los flujos de trabajo principales durante una semana, luego vuelve a los Capítulos 04-06 cuando tengas necesidades específicas.

---

## Continúa con temas adicionales

En el [**Capítulo 04: Agentes e instrucciones personalizadas**](../04-agents-custom-instructions/README.md) aprenderás:

- Usar agentes integrados (`/plan`, `/review`)
- Crear agentes especializados (experto frontend, auditor de seguridad) con archivos `.agent.md`
- Patrones de colaboración multiagente
- Archivos de instrucciones personalizadas para estándares del proyecto

---

[**← Volver al Capítulo 02**](../02-context-conversations/README.md) | [**Continuar al Capítulo 04 →**](../04-agents-custom-instructions/README.md)
