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

![Capítulo 03: Flujos de trabajo de desarrollo](../../../03-development-workflows/assets/chapter-header.png)

> **¿Qué pasaría si la IA pudiera encontrar errores que ni siquiera sabías que debías preguntar?**

En este capítulo, GitHub Copilot CLI se convierte en tu herramienta diaria. Lo usarás dentro de los flujos de trabajo en los que ya confías cada día: pruebas, refactorización, depuración y Git.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Realizar revisiones de código exhaustivas con Copilot CLI
- Refactorizar código heredado de forma segura
- Depurar problemas con la ayuda de la IA
- Generar pruebas automáticamente
- Integrar Copilot CLI con tu flujo de trabajo de git

> ⏱️ **Tiempo estimado**: ~60 minutos (15 min de lectura + 45 min práctico)

---

## 🧩 Analogía del mundo real: el flujo de trabajo de un carpintero

Un carpintero no solo sabe usar herramientas, tiene *flujos de trabajo* para distintos trabajos:

<img src="../../../03-development-workflows/assets/carpenter-workflow-steps.png" alt="Taller de artesano que muestra tres carriles de flujo de trabajo: Construir muebles (Medir, Cortar, Ensamblar, Acabado), Reparar daños (Evaluar, Retirar, Reparar, Igualar), y Control de calidad (Inspeccionar, Probar uniones, Comprobar alineación)" width="800"/>

De forma similar, los desarrolladores tienen flujos de trabajo para distintas tareas. GitHub Copilot CLI mejora cada uno de estos flujos, haciéndote más eficiente y efectivo en tus tareas de codificación diarias.

---

# Los cinco flujos de trabajo

<img src="../../../03-development-workflows/assets/five-workflows.png" alt="Cinco iconos de neón brillantes que representan los flujos de revisión de código, pruebas, depuración, refactorización e integración con git" width="800"/>

Cada flujo de trabajo a continuación es independiente. Elige los que se ajusten a tus necesidades actuales, o recórrelos todos.

---

## Elige tu propia aventura

Este capítulo cubre cinco flujos de trabajo que los desarrolladores suelen utilizar. **¡Sin embargo, no necesitas leerlos todos de una vez!** Cada flujo de trabajo es independiente y se encuentra en una sección desplegable a continuación. Elige los que coincidan con lo que necesitas y que mejor se adapten a tu proyecto actual. Siempre puedes volver y explorar los demás más tarde.

<img src="../../../03-development-workflows/assets/five-workflows-swimlane.png" alt="Cinco flujos de desarrollo: Revisión de código, Refactorización, Depuración, Generación de pruebas e Integración con Git mostrados como carriles horizontales" width="800"/>

| Quiero... | Ir a |
|---|---|
| Revisar código antes de fusionar | [Flujo 1: Revisión de código](#workflow-1-code-review) |
| Limpiar código desordenado o legado | [Flujo 2: Refactorización](#workflow-2-refactoring) |
| Rastrear y corregir un error | [Flujo 3: Depuración](#workflow-3-debugging) |
| Generar pruebas para mi código | [Flujo 4: Generación de pruebas](#workflow-4-test-generation) |
| Escribir mejores commits y PRs | [Flujo 5: Integración con Git](#workflow-5-git-integration) |
| Investigar antes de planificar o codificar | [Consejo rápido: Investiga antes de planificar o codificar](#usar-delegate-para-tareas-en-segundo-plano) |
| Ver un flujo completo de corrección de errores de principio a fin | [Poniéndolo todo junto](#usar-diff-para-revisar-cambios-de-la-sesión) |

**Selecciona un flujo de trabajo abajo para expandirlo** y ver cómo GitHub Copilot CLI puede mejorar tu proceso de desarrollo en esa área. 

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>Flujo 1: Revisión de código</strong> - Revisar archivos, usar el agente /review, crear listas de verificación por severidad</summary>

<img src="../../../03-development-workflows/assets/code-review-swimlane-single.png" alt="Flujo de revisión de código: revisar, identificar problemas, priorizar, generar lista de verificación." width="800"/>

### Revisión básica

Este ejemplo usa el símbolo `@` para referenciar un archivo, dando a Copilot CLI acceso directo a su contenido para revisión.

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de revisión de código](../../../03-development-workflows/assets/code-review-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas serán distintos a lo mostrado aquí.*

</details>

---

### Revisión de validación de entrada

Pide a Copilot CLI que enfoque su revisión en una preocupación específica (aquí, validación de entrada) enumerando las categorías que te importan en la solicitud.

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### Revisión de proyecto entre archivos

Referencia un directorio entero con `@` para permitir que Copilot CLI escanee todos los archivos del proyecto a la vez.

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### Revisión de código interactiva

Usa una conversación de múltiples turnos para profundizar. Comienza con una revisión amplia y luego realiza preguntas de seguimiento sin reiniciar.

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI proporciona una revisión detallada

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI muestra posibles problemas con cadenas vacías, caracteres especiales

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

### Comprender los cambios en Git (Importante para /review)

Antes de usar el comando `/review`, necesitas entender dos tipos de cambios en git:

| Tipo de cambio | Qué significa | Cómo verlo |
|-------------|---------------|------------|
| **Cambios preparados (staged)** | Archivos que has marcado para el siguiente commit con `git add` | `git diff --staged` |
| **Cambios no preparados (unstaged)** | Archivos que has modificado pero que aún no has añadido | `git diff` |

```bash
# Referencia rápida
git status           # Muestra tanto los cambios preparados como los no preparados
git add file.py      # Preparar un archivo para la confirmación
git diff             # Muestra los cambios no preparados
git diff --staged    # Muestra los cambios preparados
```

### Uso del comando /review

El comando `/review` invoca el **agente de revisión de código** integrado, que está optimizado para analizar cambios preparados y no preparados con una salida de alta relación señal-ruido. Usa un comando con barra para activar un agente integrado especializado en lugar de escribir un prompt libre.

```bash
copilot

> /review
# Invoca al agente de revisión de código sobre los cambios preparados/no preparados
# Proporciona retroalimentación enfocada y accionable

> /review Check for security issues in authentication
# Ejecutar revisión con un área de enfoque específica
```

> 💡 **Consejo**: El agente de revisión de código funciona mejor cuando tienes cambios pendientes. Prepara tus archivos con `git add` para revisiones más focalizadas.

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>Flujo 2: Refactorización</strong> - Reestructurar código, separar responsabilidades, mejorar el manejo de errores</summary>

<img src="../../../03-development-workflows/assets/refactoring-swimlane-single.png" alt="Flujo de refactorización: evaluar código, planificar cambios, implementar, verificar comportamiento." width="800"/>

### Refactorización simple

> **Prueba esto primero:** `@samples/book-app-project/book_app.py El manejo de comandos usa cadenas de if/elif. Refactorízalo para usar un patrón de despacho por diccionario.`

Comienza con mejoras sencillas. Pruébalas en la aplicación de libros. Cada prompt usa una referencia de archivo `@` emparejada con una instrucción de refactorización específica para que Copilot CLI sepa exactamente qué cambiar.

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **¿Nuevo en la refactorización?** Comienza con peticiones sencillas como agregar anotaciones de tipo o mejorar los nombres de variables antes de abordar transformaciones complejas.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de refactorización](../../../03-development-workflows/assets/refactor-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas serán distintos a lo mostrado aquí.*

</details>

---

### Separar responsabilidades

Referencia múltiples archivos con `@` en una sola solicitud para que Copilot CLI pueda mover código entre ellos como parte de la refactorización.

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

# Consigue las pruebas primero

> Now refactor the BookCollection class to use a context manager for file operations

# Refactoriza con confianza - las pruebas verifican que el comportamiento se mantiene
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>Flujo 3: Depuración</strong> - Rastrear errores, auditorías de seguridad, trazar problemas a través de archivos</summary>

<img src="../../../03-development-workflows/assets/debugging-swimlane-single.png" alt="Flujo de depuración: entender el error, localizar la causa raíz, corregir, probar." width="800"/>

### Depuración simple

> **Prueba esto primero:** `@samples/book-app-buggy/books_buggy.py Los usuarios informan que buscar "The Hobbit" no devuelve resultados aunque está en los datos. Depura por qué.`

Comienza describiendo qué está mal. Aquí hay patrones de depuración comunes que puedes probar con la aplicación de libros con errores. Cada prompt empareja una referencia de archivo `@` con una descripción clara del síntoma para que Copilot CLI pueda localizar y diagnosticar el error.

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
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de corrección de errores](../../../03-development-workflows/assets/fix-bug-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas serán distintos a lo mostrado aquí.*

</details>

---

### El "Detective de errores" - La IA encuentra BUGS RELACIONADOS

Aquí es donde brilla la depuración con conciencia del contexto. Prueba este escenario con la aplicación de libros con errores. Proporciona el archivo completo con `@` y describe únicamente el síntoma reportado por el usuario. Copilot CLI rastreará la causa raíz y puede detectar errores adicionales cercanos.

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Qué hace Copilot CLI**:
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**Por qué esto importa**: Copilot CLI lee todo el archivo, comprende el contexto de tu informe de error y te ofrece una corrección específica con una explicación clara.

> 💡 **Bonus**: Debido a que Copilot CLI analiza todo el archivo, a menudo descubre *otros* problemas que no pediste. Por ejemplo, mientras corrige la búsqueda por autor, Copilot CLI también podría notar el bug de sensibilidad a mayúsculas/minúsculas en `find_book_by_title`!

### Apunte de seguridad en el mundo real

Aunque depurar tu propio código es importante, comprender las vulnerabilidades de seguridad en aplicaciones de producción es crítico. Prueba este ejemplo: apunta Copilot CLI a un archivo desconocido y pídele que audite en busca de problemas de seguridad.

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

Este archivo demuestra patrones de seguridad del mundo real que encontrarás en aplicaciones de producción.

> 💡 **Términos comunes de seguridad que encontrarás:**
> - **Inyección SQL**: Cuando la entrada del usuario se inserta directamente en una consulta de base de datos, permitiendo a atacantes ejecutar comandos maliciosos
> - **Consultas parametrizadas**: La alternativa segura: los marcadores de posición (`?`) separan los datos del usuario de los comandos SQL
> - **Condición de carrera**: Cuando dos operaciones ocurren al mismo tiempo y se interfieren entre sí
> - **XSS (Cross-Site Scripting)**: Cuando atacantes inyectan scripts maliciosos en páginas web

---

### Comprender un error

Pega una traza de pila directamente en tu prompt junto con una referencia de archivo `@` para que Copilot CLI pueda mapear el error al código fuente.

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### Depuración con caso de prueba

Describe la entrada exacta y la salida observada para dar a Copilot CLI un caso de prueba concreto y reproducible sobre el que razonar.

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

### Comprender problemas de datos

Incluye un archivo de datos junto al código que lo lee para que Copilot CLI comprenda el panorama completo al sugerir mejoras en el manejo de errores.

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>Flujo 4: Generación de pruebas</strong> - Generar pruebas exhaustivas y casos límite automáticamente</summary>

<img src="../../../03-development-workflows/assets/test-gen-swimlane-single.png" alt="Flujo de generación de pruebas: analizar función, generar pruebas, incluir casos límite, ejecutar." width="800"/>

> **Prueba esto primero:** `@samples/book-app-project/books.py Genera pruebas pytest para todas las funciones, incluyendo casos límite`

### La "Explosión de pruebas" - 2 pruebas vs 15+ pruebas

Al escribir pruebas manualmente, los desarrolladores típicamente crean 2-3 pruebas básicas:
- Probar entrada válida
- Probar entrada inválida
- Probar un caso límite

Observa lo que sucede cuando le pides a Copilot CLI que genere pruebas exhaustivas. Este prompt usa una lista de viñetas estructurada con una referencia de archivo `@` para guiar a Copilot CLI hacia una cobertura de pruebas completa:

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

![Demostración de generación de pruebas](../../../03-development-workflows/assets/test-gen-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas serán distintos a lo mostrado aquí.*

</details>

---

**Qué obtienes**: 15+ pruebas exhaustivas que incluyen:

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

**Resultado**: En 30 segundos obtienes pruebas de casos límite que tomarían una hora en pensar y escribir.

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

Hazle a Copilot CLI una pregunta en inglés sencillo sobre tu cadena de herramientas. Puede generar el comando de shell correcto para ti.

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI responde:
# cd samples/book-app-project && python -m pytest tests/
# O para salida detallada: python -m pytest tests/ -v
# Para ver las salidas de print: python -m pytest tests/ -s
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

Pide pruebas *adicionales* para una sola función para que Copilot CLI genere nuevos casos que complementen los que ya tienes.

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
<summary><strong>Flujo 5: Integración con Git</strong> - Mensajes de commit, descripciones de PR, /pr, /delegate, /diff y /branch</summary>

<img src="../../../03-development-workflows/assets/git-integration-swimlane-single.png" alt="Flujo de integración con Git: preparar cambios, generar mensaje, confirmar, crear PR." width="800"/>

> 💡 **Este flujo asume familiaridad básica con git** (preparar cambios, confirmar, ramas). Si git es nuevo para ti, prueba los otros cuatro flujos primero.

### Generar mensajes de commit

> **Intenta esto primero:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — stage some changes, then run this to see Copilot CLI write your commit message.

This example uses the `-p` inline prompt flag with shell command substitution to pipe `git diff` output directly into Copilot CLI for a one-shot commit message. The `$(...)` syntax runs the command inside the parentheses and inserts its output into the outer command.

```bash

# Ver qué cambió
git diff --staged

# Generar el mensaje de commit usando el formato [Conventional Commit](../GLOSSARY.md#commit-convencional)
# (mensajes estructurados como "feat(books): añadir búsqueda" o "fix(data): manejar entrada vacía")
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# Salida: "feat(books): añadir búsqueda parcial del nombre del autor
#
# - Actualizar find_by_author para admitir coincidencias parciales
# - Añadir comparación insensible a mayúsculas/minúsculas
# - Mejorar la experiencia del usuario al buscar autores"
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de Integración con Git](../../../03-development-workflows/assets/git-integration-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

---

### Explicar cambios

Deriva la salida de `git show` a un prompt `-p` para obtener un resumen en inglés sencillo del último commit.

```bash
# ¿Qué cambió este commit?
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### Descripción de PR

Combina la salida de `git log` con una plantilla de prompt estructurada para autogenerar una descripción completa de pull request.

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

Si estás trabajando con una rama en el modo interactivo de Copilot CLI, puedes usar el comando `/pr` para trabajar con pull requests. Usa `/pr` para ver un PR, crear uno nuevo, corregir un PR existente, o dejar que Copilot CLI decida automáticamente según el estado de la rama.

```bash
copilot

> /pr [view|create|fix|auto]
```

### Revisar antes del push

Usa `git diff main..HEAD` dentro de un prompt `-p` para una verificación rápida de pre-push de todos los cambios de la rama.

```bash
# Última comprobación antes de subir
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### Usar /delegate para tareas en segundo plano

El comando `/delegate` encarga el trabajo a un agente en la nube de GitHub Copilot. Usa el comando slash `/delegate` (o el atajo `&`) para delegar una tarea bien definida a un agente en segundo plano.

```bash
copilot

> /delegate Add input validation to the login form

# O usa el atajo de prefijo &:
> & Fix the typo in the README header

# Copilot CLI:
# 1. Confirma tus cambios en una nueva rama
# 2. Abre una solicitud de extracción en borrador
# 3. Funciona en segundo plano en GitHub
# 4. Solicita tu revisión cuando termine
```

Esto es ideal para tareas bien definidas que quieres que se completen mientras te concentras en otro trabajo.

### Usar /diff para revisar cambios de la sesión

El comando `/diff` muestra todos los cambios realizados durante tu sesión actual. Usa este comando slash para ver un diff visual de todo lo que Copilot CLI ha modificado antes de que confirmes. También funciona en carpetas que no son repositorios git.

```bash
copilot

# Después de hacer algunos cambios...
> /diff

# Muestra una comparación visual de todos los archivos modificados en esta sesión
# Ideal para revisar antes de confirmar
```

### Crear ramas de tu sesión con /branch o /fork

A veces quieres explorar dos enfoques diferentes para un problema sin perder tu conversación original. El comando `/branch` (también disponible como `/fork`) crea una copia de tu sesión actual para que puedas probar una dirección diferente y luego comparar resultados.

```bash
copilot

> Fix the find_by_author function to support partial matches

# Quieres probar un enfoque diferente — ¡crea primero una rama!
> /branch

# Ahora estás en una nueva copia de la sesión. Prueba tu enfoque alternativo:
> Fix find_by_author using a different regex-based strategy

# Si no te gusta el resultado, vuelve a tu sesión original usando /session
```

> 💡 **`/branch` y `/fork` son lo mismo**: Ambos comandos hacen cosas idénticas. `/branch` se añadió como un nombre más intuitivo. Usa el que tenga más sentido para ti.

> 💡 **Cuándo crear una rama**: Crear una rama es genial cuando no estás seguro de qué enfoque es mejor y quieres mantener ambas opciones abiertas.

</details>

---

## Consejo rápido: Investiga antes de planear o codificar

Cuando necesites investigar una librería, entender las mejores prácticas o explorar un tema desconocido, usa `/research` para realizar una investigación profunda antes de escribir cualquier código:

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot busca en repositorios de GitHub y fuentes web, y luego devuelve un resumen con referencias. Esto es útil cuando estás a punto de comenzar una nueva función y quieres tomar decisiones informadas primero. Puedes compartir los resultados usando `/share`.

> 💡 **Consejo**: `/research` funciona bien *antes* de `/plan`. Investiga el enfoque, luego planifica la implementación.

---

## Poniéndolo todo junto: flujo de trabajo para corregir bugs

Aquí hay un flujo de trabajo completo para corregir un bug reportado:

```bash

# 1. Entender el informe de errores
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

# Agregar los cambios al área de preparación para que git diff --staged tenga algo con lo que trabajar
git add .

# 5. Generar el mensaje de commit
copilot -p "Generate commit message for: $(git diff --staged)"

# Ejemplo de salida: "fix(books): soportar búsqueda parcial por nombre de autor"

# 6. Confirmar los cambios (opcional)

git commit -m "<paste generated message>"
```

### Resumen del flujo para corregir bugs

| Paso | Acción | Comando de Copilot |
|------|--------|--------------------|
| 1 | Entender el bug | `> [describe bug] @relevant-file.py Analyze the likely cause` |
| 2 | Análisis y corrección | `> Show me the function and fix the issue` |
| 3 | Generar pruebas | `> Generate tests for [specific scenarios]` |
| 4 | Preparar cambios | `git add .` |
| 5 | Generar mensaje de commit | `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` |
| 6 | Confirmar cambios| `git commit -m "<paste generated message>"` |

---

# Práctica

<img src="../../../assets/practice.png" alt="Configuración cálida de escritorio con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica práctica" width="800"/>

Ahora es tu turno de aplicar estos flujos de trabajo.

---

## ▶️ Pruébalo tú mismo

Después de completar las demos, prueba estas variantes:

1. **Desafío Detective de bugs**: Pide a Copilot CLI que depure la función `mark_as_read` en `samples/book-app-buggy/books_buggy.py`. ¿Explicó por qué la función marca TODOS los libros como leídos en lugar de solo uno?

2. **Desafío de pruebas**: Genera pruebas para la función `add_book` en la aplicación de libros. Cuenta cuántos casos límite incluye Copilot CLI que tú no habrías pensado.

3. **Desafío de mensajes de commit**: Haz cualquier cambio pequeño en un archivo de la aplicación de libros, prepáralo (`git add .`), luego ejecuta:
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   ¿Es el mensaje mejor que lo que hubieras escrito rápidamente?

**Autoevaluación**: Entiendes los flujos de trabajo de desarrollo cuando puedes explicar por qué "depura este bug" es más poderoso que "encuentra bugs" (¡el contexto importa!).

---

## 📝 Tarea

### Desafío principal: Refactorizar, probar y entregar

Los ejemplos prácticos se centraron en `find_book_by_title` y revisiones de código. Ahora practica las mismas habilidades de flujo de trabajo en diferentes funciones en `book-app-project`:

1. **Revisar**: Pide a Copilot CLI que revise `remove_book()` en `books.py` para casos límite y posibles problemas:
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **Refactorizar**: Pide a Copilot CLI que mejore `remove_book()` para manejar casos límite como coincidencia sin distinguir mayúsculas/minúsculas y devolver retroalimentación útil cuando no se encuentra un libro
3. **Probar**: Genera pruebas pytest específicamente para la función mejorada `remove_book()`, cubriendo:
   - Eliminar un libro que existe
   - Coincidencia de título sin distinguir mayúsculas/minúsculas
   - Un libro que no existe devuelve una retroalimentación apropiada
   - Eliminar de una colección vacía
4. **Revisar**: Prepara tus cambios y ejecuta `/review` para comprobar si quedan problemas
5. **Confirmar**: Genera un mensaje de commit convencional:
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

**Consejo:** Después de mejorar `remove_book()`, intenta preguntarle a Copilot CLI: "¿Hay otras funciones en este archivo que podrían beneficiarse de las mismas mejoras?". Podría sugerir cambios similares a `find_book_by_title()` o `find_by_author()`.

</details>

### Desafío extra: Crea una aplicación con Copilot CLI

> 💡 **Nota**: Este ejercicio de GitHub Skills usa **Node.js** en lugar de Python. Las técnicas de GitHub Copilot CLI que practicarás - crear issues, generar código y colaborar desde la terminal - se aplican a cualquier lenguaje.

El ejercicio muestra a los desarrolladores cómo usar GitHub Copilot CLI para crear issues, generar código y colaborar desde la terminal mientras construyen una calculadora en Node.js. Instalarás el CLI, usarás plantillas y agentes, y practicarás desarrollo iterativo dirigido por la línea de comandos.

##### <img src="../../../assets/github-skills-logo.png" width="28" align="center" /> [Comienza el ejercicio de GitHub Skills "Crear aplicaciones con Copilot CLI"](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué pasa | Solución |
|---------|--------------|-----|
| Usar prompts vagos como "Revisa este código" | Retroalimentación genérica que pasa por alto problemas específicos | Sé específico: "Revisa para inyección SQL, XSS y problemas de autenticación" |
| No usar `/review` para revisiones de código | Falta el agente de revisión de código optimizado | Usa `/review` que está afinado para una salida con alta señal y bajo ruido |
| Pedir "encuentra bugs" sin contexto | Copilot CLI no sabe qué bug estás experimentando | Describe el síntoma: "Los usuarios reportan que X ocurre cuando Y" |
| Generar pruebas sin especificar el framework | Las pruebas pueden usar sintaxis equivocada o una biblioteca de aserciones distinta | Especifica: "Genera pruebas usando Jest" o "usando pytest" |

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

**El refactor cambia el comportamiento** - Pide a Copilot CLI que preserve el comportamiento:

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
2. **La refactorización** es más segura cuando generas pruebas primero
3. **La depuración** se beneficia de mostrar a Copilot CLI el error Y el código
4. **La generación de pruebas** debe incluir casos límite y escenarios de error
5. **La integración con Git** automatiza mensajes de commit y descripciones de PR

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ✅ Punto de control: Has dominado lo esencial

**¡Felicidades!** Ahora tienes todas las habilidades fundamentales para ser productivo con GitHub Copilot CLI:

| Habilidad | Capítulo | Ahora puedes... |
|-------|---------|----------------|
| Comandos básicos | Ch 01 | Usar modo interactivo, modo plan, modo programático (-p), y comandos slash |
| Contexto | Ch 02 | Referenciar archivos con `@`, gestionar sesiones, entender ventanas de contexto |
| Flujos de trabajo | Ch 03 | Revisar código, refactorizar, depurar, generar pruebas, integrar con git |

Los capítulos 04-06 cubren características adicionales que aportan aún más potencia y vale la pena aprenderlas.

---

## 🛠️ Construyendo tu flujo de trabajo personal

No existe una única forma "correcta" de usar GitHub Copilot CLI. Aquí hay algunos consejos mientras desarrollas tus propios patrones:

> 📚 **Documentación oficial**: [Buenas prácticas de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices) para flujos de trabajo recomendados y consejos de GitHub.

- **Comienza con `/plan`** para cualquier cosa no trivial. Refinar el plan antes de ejecutar: un buen plan conduce a mejores resultados.
- **Guarda los prompts que funcionan bien.** Cuando Copilot CLI comete un error, anota qué salió mal. Con el tiempo, esto se vuelve tu libro de jugadas personal.
- **Experimenta libremente.** Algunos desarrolladores prefieren prompts largos y detallados. Otros prefieren prompts cortos con seguimientos. Prueba diferentes enfoques y nota lo que se siente natural.

> 💡 **Próximamente**: En los Capítulos 04 y 05, aprenderás cómo codificar tus mejores prácticas en instrucciones y habilidades personalizadas que Copilot CLI carga automáticamente.

---

## ➡️ Qué sigue

Los capítulos restantes cubren características adicionales que extienden las capacidades de Copilot CLI:

| Capítulo | Qué cubre | Cuándo lo querrás |
|---------|----------------|---------------------|
| Ch 04: Agentes | Crear agentes de IA especializados | Cuando quieras expertos de dominio (frontend, seguridad) |
| Ch 05: Habilidades | Cargar automáticamente instrucciones para tareas | Cuando repitas los mismos prompts con frecuencia |
| Capítulo 06: MCP | Conectar servicios externos | Cuando necesites datos en vivo de GitHub, bases de datos |

**Recomendación**: Prueba los flujos de trabajo principales durante una semana, luego vuelve a los Capítulos 04-06 cuando tengas necesidades específicas.

---

## Continuar con temas adicionales

En **[Capítulo 04: Agentes e Instrucciones Personalizadas](../04-agents-custom-instructions/README.md)**, aprenderás:

- Uso de agentes integrados (`/plan`, `/review`)
- Creación de agentes especializados (experto en frontend, auditor de seguridad) con archivos `.agent.md`
- Patrones de colaboración multiagente
- Archivos de instrucciones personalizadas para estándares del proyecto

---

**[← Volver al Capítulo 02](../02-context-conversations/README.md)** | **[Continuar al Capítulo 04 →](../04-agents-custom-instructions/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->