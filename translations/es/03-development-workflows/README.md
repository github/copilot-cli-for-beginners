<!--
---
id: CopilotCLI-03
title: !translate Development Workflows
description: !translate Apply GitHub Copilot CLI to everyday development workflows including code review, refactoring, debugging, test generation, and Git.
audience: Developers / Students / Terminal users
slug: development-workflows
weight: 4
---
-->

![Chapter 03: Development Workflows](../../../03-development-workflows/assets/chapter-header.png)

> **¿Y si la IA pudiera encontrar errores sobre los que ni siquiera sabías preguntar?**

En este capítulo, GitHub Copilot CLI se convierte en tu herramienta diaria. Lo usarás dentro de los flujos de trabajo que ya utilizas cada día: pruebas, refactorización, depuración y Git.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, serás capaz de:

- Ejecutar revisiones de código completas con Copilot CLI
- Refactorizar código antiguo de forma segura
- Depurar problemas con asistencia de IA
- Generar pruebas automáticamente
- Integrar Copilot CLI con tu flujo de trabajo de git

> ⏱️ **Tiempo estimado**: ~60 minutos (15 min lectura + 45 min práctica)

---

## 🧩 Analogía del mundo real: El flujo de trabajo de un carpintero

Un carpintero no solo sabe usar herramientas, tiene *flujos de trabajo* para distintos trabajos:

<img src="../../../03-development-workflows/assets/carpenter-workflow-steps.png" alt="Taller de artesano mostrando tres carriles de flujo de trabajo: Construir muebles (Medir, Cortar, Ensamblar, Acabado), Reparar daños (Evaluar, Retirar, Reparar, Igualar), y Control de calidad (Inspeccionar, Probar uniones, Comprobar alineación)" width="800"/>

De forma similar, los desarrolladores tienen flujos de trabajo para distintas tareas. GitHub Copilot CLI mejora cada uno de estos flujos, haciéndote más eficiente y eficaz en tus tareas diarias de programación.

---

# Los cinco flujos de trabajo

<img src="../../../03-development-workflows/assets/five-workflows.png" alt="Cinco iconos de neón brillantes que representan revisión de código, pruebas, depuración, refactorización e integración con git" width="800"/>

Cada flujo de trabajo que aparece a continuación es independiente. Elige los que coincidan con tus necesidades actuales, o trabaja con todos ellos.

---

## Elige tu propia aventura

Este capítulo cubre cinco flujos de trabajo que los desarrolladores usan típicamente. **¡Sin embargo, no necesitas leerlos todos de una vez!** Cada flujo de trabajo está contenido en una sección plegable abajo. Elige los que coincidan con lo que necesitas y con lo que mejor encaje con tu proyecto actual. Siempre puedes volver y explorar los demás más tarde.

<img src="../../../03-development-workflows/assets/five-workflows-swimlane.png" alt="Cinco flujos de desarrollo: Revisión de código, Refactorización, Depuración, Generación de pruebas e Integración con Git mostrados como carriles horizontales" width="800"/>

| I want to... | Jump to |
|---|---|
| Review code before merging | [Workflow 1: Code Review](#workflow-1-code-review) |
| Clean up messy or legacy code | [Workflow 2: Refactoring](#workflow-2-refactoring) |
| Track down and fix a bug | [Workflow 3: Debugging](#workflow-3-debugging) |
| Generate tests for my code | [Workflow 4: Test Generation](#workflow-4-test-generation) |
| Write better commits and PRs | [Workflow 5: Git Integration](#workflow-5-git-integration) |
| Research before coding | [Quick Tip: Research Before You Plan or Code](#revisar-antes-de-hacer-push) |
| See a full bug-fix workflow end to end | [Putting It All Together](#usar-delegate-para-tareas-en-segundo-plano) |

**Selecciona un flujo de trabajo abajo para expandirlo** y ver cómo GitHub Copilot CLI puede mejorar tu proceso de desarrollo en esa área. 

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>Flujo de trabajo 1: Revisión de código</strong> - Revisar archivos, usar el agente /review, crear listas de verificación por severidad</summary>

<img src="../../../03-development-workflows/assets/code-review-swimlane-single.png" alt="Flujo de revisión de código: revisar, identificar problemas, priorizar, generar lista de verificación." width="800"/>

### Revisión básica

Este ejemplo usa el símbolo `@` para referenciar un archivo, dando a Copilot CLI acceso directo a su contenido para revisión.

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 ¡Véalo en acción!</summary>

![Code Review Demo](../../../03-development-workflows/assets/code-review-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

### Revisión de validación de entrada

Pide a Copilot CLI que centre su revisión en una preocupación específica (aquí, la validación de entrada) enumerando las categorías que te importan en el prompt.

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### Revisión del proyecto entre archivos

Referencia todo un directorio con `@` para permitir que Copilot CLI escanee cada archivo del proyecto de una vez.

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### Revisión interactiva de código

Usa una conversación de múltiples turnos para profundizar. Comienza con una revisión amplia y luego haz preguntas de seguimiento sin reiniciar.

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

### Plantilla de lista de verificación de revisión

Pide a Copilot CLI que estructure su salida en un formato específico (aquí, una lista de verificación en markdown categorizada por severidad que puedes pegar en un issue).

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Entender los cambios en Git (Importante para /review)

Antes de usar el comando `/review`, necesitas entender dos tipos de cambios en git:

| Change Type | What It Means | How to See |
|-------------|---------------|------------|
| **Staged changes** | Files you've marked for the next commit with `git add` | `git diff --staged` |
| **Unstaged changes** | Files you've modified but haven't added yet | `git diff` |

```bash
# Referencia rápida
git status           # Muestra tanto los cambios preparados como los no preparados
git add file.py      # Preparar un archivo para el commit
git diff             # Muestra los cambios no preparados
git diff --staged    # Muestra los cambios preparados
```

### Usar el comando /review

El comando `/review` invoca el **agente de revisión de código** integrado, que está optimizado para analizar cambios staged y unstaged con una salida de alta señal y bajo ruido. Usa un comando con barra para activar un agente integrado especializado en lugar de escribir un prompt de forma libre.

```bash
copilot

> /review
# Invoca al agente de revisión de código en cambios preparados/no preparados
# Proporciona retroalimentación enfocada y accionable

> /review Check for security issues in authentication
# Ejecuta la revisión con un área de enfoque específica
```

> 💡 **Consejo**: El agente de revisión de código funciona mejor cuando tienes cambios pendientes. Prepara tus archivos con `git add` para revisiones más centradas.

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>Flujo de trabajo 2: Refactorización</strong> - Reestructurar código, separar responsabilidades, mejorar el manejo de errores</summary>

<img src="../../../03-development-workflows/assets/refactoring-swimlane-single.png" alt="Flujo de refactorización: evaluar código, planificar cambios, implementar, verificar comportamiento." width="800"/>

### Refactorización simple

> **Prueba esto primero:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

Comienza con mejoras sencillas. Pruébalas en la app de libros. Cada prompt usa una referencia de archivo `@` emparejada con una instrucción de refactorización específica para que Copilot CLI sepa exactamente qué cambiar.

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **¿Nuevo en la refactorización?** Empieza con solicitudes simples como añadir hints de tipos o mejorar nombres de variables antes de abordar transformaciones complejas.

---

<details>
<summary>🎬 ¡Véalo en acción!</summary>

![Refactor Demo](../../../03-development-workflows/assets/refactor-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

### Separar responsabilidades

Referencia múltiples archivos con `@` en un mismo prompt para que Copilot CLI pueda mover código entre ellos como parte del refactor.

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### Mejorar el manejo de errores

Proporciona dos archivos relacionados y describe la preocupación transversal para que Copilot CLI pueda sugerir una corrección consistente en ambos.

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

Encadena dos solicitudes relacionadas en una conversación de múltiples turnos. Primero genera pruebas, luego refactoriza con esas pruebas como red de seguridad.

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# Escribe las pruebas primero

> Now refactor the BookCollection class to use a context manager for file operations

# Refactoriza con confianza: las pruebas verifican que el comportamiento se mantiene
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>Flujo de trabajo 3: Depuración</strong> - Localizar errores, auditorías de seguridad, rastrear problemas a través de archivos</summary>

<img src="../../../03-development-workflows/assets/debugging-swimlane-single.png" alt="Flujo de depuración: entender el error, localizar la causa raíz, corregir, probar." width="800"/>

### Depuración simple

> **Prueba esto primero:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

Empieza describiendo qué está mal. Aquí hay patrones comunes de depuración que puedes probar con la app de libros con errores. Cada prompt empareja una referencia de archivo `@` con una descripción clara del síntoma para que Copilot CLI pueda localizar y diagnosticar el error.

```bash
copilot

# Patrón: "Se esperaba X pero se obtuvo Y"
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# Patrón: "Comportamiento inesperado"
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# Patrón: "Resultados incorrectos"
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **Consejo de depuración**: Describe el *síntoma* (lo que ves) y la *expectativa* (lo que debería pasar). Copilot CLI se encarga del resto.

---

<details>
<summary>🎬 ¡Véalo en acción!</summary>

![Fix Bug Demo](../../../03-development-workflows/assets/fix-bug-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

### El "Detective de bugs" - La IA encuentra bugs RELACIONADOS

Aquí es donde la depuración consciente del contexto brilla. Prueba este escenario con la app de libros con errores. Proporciona el archivo completo mediante `@` y describe solo el síntoma reportado por el usuario. Copilot CLI rastreará la causa raíz y puede detectar errores adicionales cercanos.

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

**Por qué esto importa**: Copilot CLI lee el archivo completo, entiende el contexto de tu informe de error y te da una corrección específica con una explicación clara.

> 💡 **Bonus**: Como Copilot CLI analiza el archivo entero, a menudo descubre *otros* problemas que no pediste. Por ejemplo, al arreglar la búsqueda por autor, Copilot CLI podría también notar el bug de sensibilidad a mayúsculas en `find_book_by_title`!

### Sidebar de seguridad en el mundo real

Aunque depurar tu propio código es importante, entender vulnerabilidades de seguridad en aplicaciones en producción es crítico. Prueba este ejemplo: Apunta Copilot CLI a un archivo desconocido y pídele que audite problemas de seguridad.

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

Este archivo demuestra patrones de seguridad del mundo real que encontrarás en aplicaciones de producción.

> 💡 **Términos de seguridad comunes que encontrarás:**
> - **SQL Injection**: Cuando la entrada del usuario se inserta directamente en una consulta de base de datos, permitiendo a atacantes ejecutar comandos maliciosos
> - **Consultas parametrizadas**: La alternativa segura - los placeholders (`?`) separan los datos del usuario de los comandos SQL
> - **Condición de carrera**: Cuando dos operaciones ocurren al mismo tiempo e interfieren entre sí
> - **XSS (Cross-Site Scripting)**: Cuando atacantes inyectan scripts maliciosos en páginas web

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

Referencia múltiples archivos y pide a Copilot CLI que siga el flujo de datos a través de ellos para localizar dónde se origina el problema.

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### Entender problemas de datos

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
<summary><strong>Flujo de trabajo 4: Generación de pruebas</strong> - Generar pruebas exhaustivas y casos límite automáticamente</summary>

<img src="../../../03-development-workflows/assets/test-gen-swimlane-single.png" alt="Flujo de generación de pruebas: analizar función, generar pruebas, incluir casos límite, ejecutar." width="800"/>

> **Prueba esto primero:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### La "Explosión de pruebas" - 2 pruebas vs 15+ pruebas

Al escribir pruebas manualmente, los desarrolladores típicamente crean 2-3 pruebas básicas:
- Probar entrada válida
- Probar entrada inválida
- Probar un caso límite

Observa lo que pasa cuando pides a Copilot CLI que genere pruebas exhaustivas. Este prompt usa una lista de viñetas estructurada con una referencia de archivo `@` para guiar a Copilot CLI hacia una cobertura de pruebas completa:

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
<summary>🎬 ¡Véalo en acción!</summary>

![Test Generation Demo](../../../03-development-workflows/assets/test-gen-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Lo que obtienes**: 15+ pruebas exhaustivas que incluyen:

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

**Resultado**: En 30 segundos, obtienes pruebas de casos límite que te llevarían una hora pensar y escribir.

---

### Pruebas unitarias

Apunta a una única función y enumera las categorías de entrada que quieres probar para que Copilot CLI genere pruebas unitarias enfocadas y exhaustivas.

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

Hazle a Copilot CLI una pregunta en inglés sencillo sobre tu cadena de herramientas. Puede generar el comando de shell correcto para ti.

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI responde:
# cd samples/book-app-project && python -m pytest tests/
# O para salida detallada: python -m pytest tests/ -v
# Para ver las declaraciones print: python -m pytest tests/ -s
```

### Prueba para escenarios específicos

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

### Agregar pruebas a un archivo existente

Pide pruebas *adicionales* para una única función para que Copilot CLI genere nuevos casos que complementen lo que ya tienes.

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

<img src="../../../03-development-workflows/assets/git-integration-swimlane-single.png" alt="Flujo de trabajo de integración con Git: preparar cambios, generar mensaje, commit, crear PR." width="800"/>

> 💡 **Este flujo de trabajo asume familiaridad básica con git** (preparación de cambios (staging), commits y ramas). Si git te es nuevo, prueba los otros cuatro flujos de trabajo primero.

### Generar mensajes de commit

> **Prueba esto primero:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — prepara algunos cambios (stage), luego ejecuta esto para ver a Copilot CLI escribir tu mensaje de commit.

Este ejemplo usa la opción `-p` (bandera de prompt en línea) con sustitución de comandos de shell para canalizar la salida de `git diff` directamente a Copilot CLI y generar un mensaje de commit de una sola vez. La sintaxis `$(...)` ejecuta el comando dentro de los paréntesis e inserta su salida en el comando exterior.

```bash

# Ver qué cambió
git diff --staged

# Generar un mensaje de commit utilizando el formato [Conventional Commit](../GLOSSARY.md#commit-convencional)
# (mensajes estructurados como "feat(books): add search" o "fix(data): handle empty input")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Salida: "feat(books): add partial author name search
#
# - Actualizar find_by_author para admitir coincidencias parciales
# - Añadir comparación que no distingue entre mayúsculas y minúsculas
# - Mejorar la experiencia de usuario al buscar autores"
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de integración con Git](../../../03-development-workflows/assets/git-integration-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

### Explicar cambios

Canaliza la salida de `git show` en un prompt `-p` para obtener un resumen en inglés sencillo del último commit.

```bash
# ¿Qué cambió este commit?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### Descripción de PR

Combina la salida de `git log` con una plantilla de prompt estructurada para generar automáticamente una descripción completa de la pull request.

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

Si estás trabajando con una rama en el modo interactivo de Copilot CLI, puedes usar el comando `/pr` para trabajar con pull requests. Usa `/pr` para ver una PR, crear una nueva PR, arreglar una PR existente o dejar que Copilot CLI decida automáticamente según el estado de la rama.

```bash
copilot

> /pr [view|create|fix|auto]
```

### Revisar antes de hacer push

Usa `git diff main..HEAD` dentro de un prompt `-p` para una comprobación rápida de coherencia (pre-push) de todos los cambios de la rama.

```bash
# Última comprobación antes de hacer push
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### Usar /delegate para tareas en segundo plano

El comando `/delegate` delega trabajo al agente en la nube de GitHub Copilot. Usa el comando slash `/delegate` (o el atajo `&`) para descargar una tarea bien definida a un agente en segundo plano.

```bash
copilot

> /delegate Add input validation to the login form

# O usa el atajo de prefijo &:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Confirma tus cambios en una nueva rama
# 2. Abre una solicitud de extracción en borrador
# 3. Trabaja en segundo plano en GitHub
# 4. Solicita tu revisión cuando termine
```

Esto es ideal para tareas bien definidas que deseas completar mientras te concentras en otro trabajo.

### Usar /diff para revisar los cambios de la sesión

El comando `/diff` muestra todos los cambios realizados durante tu sesión actual. Usa este comando slash para ver un diff visual de todo lo que Copilot CLI ha modificado antes de que hagas commit.

```bash
copilot

# Después de hacer algunos cambios...
> /diff

# Muestra una comparación visual de todos los archivos modificados en esta sesión
# Ideal para revisar antes de confirmar
```

</details>

---

## Consejo rápido: Investiga antes de planear o codificar

Cuando necesites investigar una librería, comprender las mejores prácticas o explorar un tema desconocido, usa `/research` para realizar una investigación a fondo antes de escribir código:

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot busca en repositorios de GitHub y fuentes web, y luego devuelve un resumen con referencias. Esto es útil cuando estás a punto de comenzar una nueva característica y quieres tomar decisiones informadas primero. Puedes compartir los resultados usando `/share`.

> 💡 **Consejo**: `/research` funciona bien *antes* de `/plan`. Investiga el enfoque y luego planifica la implementación.

---

## Integrándolo todo: flujo de trabajo de corrección de errores

Aquí tienes un flujo de trabajo completo para corregir un error reportado:

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

# Preparar los cambios para que git diff --staged tenga algo con lo que trabajar
git add .

# 5. Generar el mensaje de commit
copilot -p "Generate commit message for: $(git diff --staged)"

# Ejemplo de salida: "fix(books): soportar búsqueda parcial por nombre de autor"

# 6. Confirmar los cambios (opcional)

git commit -m "<paste generated message>"
```

### Resumen del flujo de trabajo para corrección de errores

| Paso | Acción | Comando de Copilot |
|------|--------|--------------------|
| 1 | Entender el error | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | Análisis y corrección | `> Show me the function and fix the issue` |
| 3 | Generar pruebas | `> Generate tests for [specific scenarios]` |
| 4 | Preparar cambios | `git add .` |
| 5 | Generar mensaje de commit | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | Confirmar cambios| `git commit -m "<paste generated message>"` |

---

# Práctica

<img src="../../../assets/practice.png" alt="Escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica práctica" width="800"/>

Ahora es tu turno de aplicar estos flujos de trabajo.

---

## ▶️ Pruébalo tú mismo

Después de completar las demostraciones, prueba estas variaciones:

1. **Desafío Detective de Bugs**: Pide a Copilot CLI que depure la función `mark_as_read` en `samples/book-app-buggy/books_buggy.py`. ¿Explicó por qué la función marca TODOS los libros como leídos en lugar de solo uno?

2. **Desafío de pruebas**: Genera pruebas para la función `add_book` en la aplicación de libros. Cuenta cuántos casos límite incluye Copilot CLI que tú no habrías pensado.

3. **Desafío de mensaje de commit**: Haz cualquier pequeño cambio en un archivo de la aplicación de libros, prepáralo (`git add .`), luego ejecuta:
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   ¿Es el mensaje mejor de lo que habrías escrito rápidamente?

**Autoevaluación**: Entiendes los flujos de trabajo de desarrollo cuando puedas explicar por qué "depurar este bug" es más poderoso que "encontrar bugs" (¡el contexto importa!).

---

## 📝 Tarea

### Desafío principal: refactorizar, probar y publicar

Los ejemplos prácticos se centraron en `find_book_by_title` y revisiones de código. Ahora practica las mismas habilidades de flujo de trabajo en diferentes funciones en `book-app-project`:

1. **Revisión**: Pide a Copilot CLI que revise `remove_book()` en `books.py` para casos límite y problemas potenciales:
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **Refactoriza**: Pide a Copilot CLI que mejore `remove_book()` para manejar casos límite como coincidencia sin distinguir mayúsculas/minúsculas y devolver retroalimentación útil cuando no se encuentra un libro
3. **Prueba**: Genera pruebas con pytest específicamente para la función `remove_book()` mejorada, cubriendo:
   - Eliminar un libro que existe
   - Coincidencia del título sin distinguir mayúsculas/minúsculas
   - Un libro que no existe devuelve retroalimentación apropiada
   - Eliminar desde una colección vacía
4. **Revisión**: Prepara tus cambios y ejecuta `/review` para comprobar si quedan problemas
5. **Commit**: Genera un mensaje de commit convencional:
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Prompts de ejemplo para cada paso:**

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

**Consejo:** Después de mejorar `remove_book()`, intenta pedirle a Copilot CLI: "¿Hay otras funciones en este archivo que podrían beneficiarse de las mismas mejoras?". Puede sugerir cambios similares en `find_book_by_title()` o `find_by_author()`.

</details>

### Desafío adicional: Crea una aplicación con Copilot CLI

> 💡 **Nota**: Este ejercicio de GitHub Skills usa **Node.js** en lugar de Python. Las técnicas de GitHub Copilot CLI que practicarás - crear issues, generar código y colaborar desde la terminal - se aplican a cualquier lenguaje.

El ejercicio muestra a los desarrolladores cómo usar GitHub Copilot CLI para crear issues, generar código y colaborar desde la terminal mientras construyen una aplicación calculadora en Node.js. Instalarás la CLI, usarás plantillas y agentes, y practicarás un desarrollo iterativo guiado por la línea de comandos.

##### <img src="../../../assets/github-skills-logo.png" width="28" align="center" /> [Inicia el ejercicio de Skills "Crear aplicaciones con Copilot CLI"](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|-------|-----------|---------|
| Usar prompts vagos como "Review this code" | Retroalimentación genérica que pasa por alto problemas específicos | Sé específico: "Revisa por SQL injection, XSS y problemas de autenticación" |
| No usar `/review` para revisiones de código | Falta el agente de revisión de código optimizado | Usa `/review` que está afinado para una alta relación señal/ruido |
| Pedir "find bugs" sin contexto | Copilot CLI no sabe qué error estás experimentando | Describe el síntoma: "Los usuarios informan que X ocurre cuando Y" |
| Generar pruebas sin especificar el framework | Las pruebas pueden usar sintaxis incorrecta o una biblioteca de aserciones equivocada | Especifica: "Genera pruebas usando Jest" o "usando pytest" |

### Solución de problemas

**La revisión parece incompleta** - Sé más específico sobre qué buscar:

```bash
copilot

# En lugar de:
> Review @samples/book-app-project/book_app.py

# Intenta:
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

## 🔑 Puntos clave

<img src="../../../03-development-workflows/assets/specialized-workflows.png" alt="Flujos de trabajo especializados para cada tarea: revisión de código, refactorización, depuración, pruebas e integración con Git" width="800"/>

1. **La revisión de código** se vuelve más completa con prompts específicos
2. **La refactorización** es más segura cuando primero generas pruebas
3. **La depuración** se beneficia de mostrar a Copilot CLI el error Y el código
4. **La generación de pruebas** debe incluir casos límite y escenarios de error
5. **La integración con Git** automatiza mensajes de commit y descripciones de PR

> 📋 **Referencia rápida**: Consulta la [Referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ✅ Punto de control: Has dominado lo esencial

**¡Felicidades!** Ahora tienes todas las habilidades básicas para ser productivo con GitHub Copilot CLI:

| Habilidad | Capítulo | Ahora puedes... |
|----------|----------|-----------------|
| Comandos básicos | Ch 01 | Usar el modo interactivo, el modo plan, el modo programático (-p) y comandos slash |
| Contexto | Ch 02 | Referenciar archivos con `@`, gestionar sesiones, entender ventanas de contexto |
| Flujos de trabajo | Ch 03 | Revisar código, refactorizar, depurar, generar pruebas, integrar con git |

Los capítulos 04-06 cubren funciones adicionales que aportan aún más capacidades y vale la pena aprenderlos.

---

## 🛠️ Construyendo tu flujo de trabajo personal

No existe una única forma "correcta" de usar GitHub Copilot CLI. Aquí tienes algunos consejos mientras desarrollas tus propios patrones:

> 📚 **Documentación oficial**: [Mejores prácticas de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices) para flujos de trabajo recomendados y consejos de GitHub.

- **Empieza con `/plan`** para cualquier cosa no trivial. Refina el plan antes de la ejecución: un buen plan conduce a mejores resultados.
- **Guarda prompts que funcionen bien.** Cuando Copilot CLI cometa un error, nota qué salió mal. Con el tiempo, esto se convierte en tu manual personal.
- **Experimenta libremente.** Algunos desarrolladores prefieren prompts largos y detallados. Otros prefieren prompts cortos con seguimientos. Prueba diferentes enfoques y observa qué te resulta natural.

> 💡 **Próximo**: En los Capítulos 04 y 05, aprenderás a codificar tus mejores prácticas en instrucciones y skills personalizadas que Copilot CLI cargará automáticamente.

---

## ➡️ Qué sigue

| Chapter | What It Covers | When You'll Want It |
|---------|----------------|---------------------|
| Ch 04: Agents | Create specialized AI personas | When you want domain experts (frontend, security) |
| Ch 05: Skills | Auto-load instructions for tasks | When you repeat the same prompts often |
| Ch 06: MCP | Connect external services | When you need live data from GitHub, databases |

**Recomendación**: Prueba los flujos de trabajo principales durante una semana y luego vuelve a los Capítulos 04-06 cuando tengas necesidades específicas.

---

## Continuar con temas adicionales

En **[Capítulo 04: Agentes e instrucciones personalizadas](../04-agents-custom-instructions/README.md)**, aprenderás:

- Usar agentes integrados (`/plan`, `/review`)
- Crear agentes especializados (experto en frontend, auditor de seguridad) con archivos `.agent.md`
- Patrones de colaboración multiagente
- Archivos de instrucciones personalizadas para estándares de proyecto
**[← Volver al Capítulo 02](../02-context-conversations/README.md)** | **[Continuar al Capítulo 04 →](../04-agents-custom-instructions/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->