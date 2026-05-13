![Capítulo 02: Contexto y conversaciones](../../../02-context-conversations/images/chapter-header.png)

> **¿Y si la IA pudiera ver toda tu base de código, no solo un archivo a la vez?**

En este capítulo desbloquearás el verdadero poder de GitHub Copilot CLI: el contexto. Aprenderás a usar la sintaxis `@` para referenciar archivos y directorios, dándole a Copilot CLI un conocimiento profundo de tu base de código. Descubrirás cómo mantener conversaciones entre sesiones, retomar el trabajo días después justo donde lo dejaste y verás cómo el análisis entre archivos detecta errores que las revisiones de un solo archivo pasan por alto.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Usar la sintaxis `@` para referenciar archivos, directorios e imágenes
- Reanudar sesiones anteriores con `--resume` y `--continue`
- Comprender cómo funcionan las [ventanas de contexto](../../../GLOSSARY.md#context-window)
- Escribir conversaciones efectivas de varios turnos
- Gestionar permisos de directorios para flujos de trabajo multiproyecto

> ⏱️ **Tiempo estimado**: ~50 minutos (20 min de lectura + 30 min de práctica)

---

## 🧩 Analogía del mundo real: trabajar con un colega

<img src="../../../02-context-conversations/images/colleague-context-analogy.png" alt="El contexto marca la diferencia: sin contexto vs con contexto" width="800"/>

*Igual que tus colegas, Copilot CLI no lee la mente. ¡Proporcionar más información ayuda tanto a las personas como a Copilot a brindar soporte específico!*

Imagina explicarle un error a un colega:

> **Sin contexto**: "La app de libros no funciona."

> **Con contexto**: "Mira `books.py`, especialmente la función `find_book_by_title`. No está haciendo coincidencias sin distinguir entre mayúsculas y minúsculas."

Para proporcionar contexto a Copilot CLI usa *la sintaxis `@`* para apuntar Copilot CLI a archivos específicos.

---

# Esencial: contexto básico

<img src="../../../02-context-conversations/images/essential-basic-context.png" alt="Bloques de código brillantes conectados por estelas de luz que representan cómo fluye el contexto a través de las conversaciones de Copilot CLI" width="800"/>

Esta sección cubre todo lo que necesitas para trabajar de forma efectiva con el contexto. Domina primero estos fundamentos.

---

## La sintaxis @

El símbolo `@` referencia archivos y directorios en tus prompts. Es la forma de decirle a Copilot CLI "mira este archivo".

> 💡 **Nota**: Todos los ejemplos de este curso usan la carpeta `samples/` incluida en este repositorio, así puedes probar cada comando directamente.

### Pruébalo ahora (sin configuración)

Puedes probar esto con cualquier archivo de tu equipo:

```bash
copilot

# Apunta a cualquier archivo que tengas
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **¿No tienes un proyecto a mano?** Crea un archivo de prueba rápido:
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### Patrones básicos de @

| Patrón | Qué hace | Ejemplo de uso |
|---------|--------------|-------------|
| `@file.py` | Referencia un único archivo | `Review @samples/book-app-project/books.py` |
| `@folder/` | Referencia todos los archivos de un directorio | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | Referencia varios archivos | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### Referenciar un único archivo

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de contexto de archivo](../../../02-context-conversations/images/file-context-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

### Referenciar varios archivos

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### Referenciar un directorio completo

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## Inteligencia entre archivos

Aquí es donde el contexto se convierte en un superpoder. El análisis de un solo archivo es útil. El análisis entre archivos es transformador.

<img src="../../../02-context-conversations/images/cross-file-intelligence.png" alt="Inteligencia entre archivos: comparación entre análisis de un solo archivo y análisis entre archivos, mostrando cómo analizar archivos juntos revela errores, flujo de datos y patrones invisibles de forma aislada" width="800"/>

### Demo: encontrar errores que abarcan varios archivos

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **Opción avanzada**: Para análisis entre archivos enfocado en seguridad, prueba los ejemplos de seguridad en Python:
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo multiarchivo](../../../02-context-conversations/images/multi-file-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

---

**Lo que descubre Copilot CLI**:

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**Por qué importa esto**: Una revisión de un solo archivo se perdería el panorama general. Solo el análisis entre archivos revela:
- **Código duplicado** que debería consolidarse
- **Patrones de flujo de datos** que muestran cómo interactúan los componentes
- **Problemas arquitectónicos** que afectan la mantenibilidad

---

### Demo: entender una base de código en 60 segundos

<img src="../../../02-context-conversations/images/codebase-understanding.png" alt="Comparación en pantalla dividida que muestra una revisión manual de código tomando 1 hora frente al análisis asistido por IA tomando 10 segundos" width="800" />

¿Nuevo en un proyecto? Aprende sobre él rápidamente usando Copilot CLI.

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**Lo que obtienes**:
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**Resultado**: Lo que toma una hora de lectura de código se reduce a 10 segundos. Sabes exactamente dónde concentrarte.

---

## Ejemplos prácticos

### Ejemplo 1: revisión de código con contexto

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI now has the full file content and can give specific feedback:
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# Now reviewing book_app.py, but still aware of books.py context
```

### Ejemplo 2: entender una base de código

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI reads books.py and understands the BookCollection class

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI scans the directory and summarizes

> How does the app save and load books?

# Copilot CLI can trace through the code it's already seen
```

<details>
<summary>🎬 ¡Mira una conversación de varios turnos en acción!</summary>

![Demo multiturno](../../../02-context-conversations/images/multi-turn-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

### Ejemplo 3: refactorización entre archivos

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI sees both files and can suggest how to merge the duplicate code
```

---

## Gestión de sesiones

Las sesiones se guardan automáticamente mientras trabajas. Puedes reanudar sesiones anteriores para continuar donde lo dejaste.

### Las sesiones se guardan automáticamente

Cada conversación se guarda automáticamente. Solo sal con normalidad:

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... do some work ...]

> /exit
```

### Reanudar la sesión más reciente

```bash
# Continue where you left off
copilot --continue
```

### Reanudar una sesión específica

```bash
# Pick from a list of sessions interactively
copilot --resume

# Or resume a specific session by ID
copilot --resume=abc123

# Or resume by the name you gave the session
copilot --resume="my book app review"
```

> 💡 **¿Cómo encuentro un ID de sesión?** No necesitas memorizarlos. Ejecutar `copilot --resume` sin un ID muestra una lista interactiva de tus sesiones anteriores, sus nombres, IDs y cuándo estuvieron activas por última vez. Solo elige la que quieras.
>
> **¿Y con varias terminales?** Cada ventana de terminal es su propia sesión con su propio contexto. Si tienes Copilot CLI abierto en tres terminales, son tres sesiones separadas. Ejecutar `--resume` desde cualquier terminal te permite explorarlas todas. La opción `--continue` toma primero la sesión del directorio de trabajo actual; si no existe ninguna allí, elige la sesión activa más reciente.
>
> **¿Puedo cambiar de sesión sin reiniciar?** Sí. Usa el comando de barra `/resume` desde dentro de una sesión activa:
> ```
> > /resume
> # Shows a list of sessions to switch to
> ```

### Organiza tus sesiones

Dale a las sesiones nombres significativos para que puedas encontrarlas más adelante. Puedes nombrar una sesión al iniciarla, o renombrarla en cualquier momento desde dentro de la sesión:

```bash
# Name a session right when you start it
copilot --name book-app-review

# Or rename the current session from inside
copilot

> /rename book-app-review
# Session renamed for easier identification
```

Una vez nombrada una sesión, puedes reanudarla directamente por nombre sin navegar por una lista:

```bash
copilot --resume=book-app-review
```

Para limpiar las sesiones que ya no necesitas, usa `/session delete` desde dentro de una sesión:

```bash
copilot

> /session delete            # Deletes the current session
> /session delete abc123     # Deletes a specific session by ID
> /session delete-all        # Deletes all sessions (use with care!)
```

### Verifica y gestiona el contexto

A medida que añades archivos y conversación, la [ventana de contexto](../../../GLOSSARY.md#context-window) de Copilot CLI se llena. Hay varios comandos disponibles para ayudarte a mantener el control:

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandons the current session (no history saved) and starts a fresh conversation

> /new
# Ends the current session (saving it to history for search/resume) and starts a fresh conversation

> /rewind
# Opens a timeline picker allowing you to roll back to an earlier point in your conversation
```

> 💡 **Cuándo usar `/clear` o `/new`**: Si has estado revisando books.py y quieres cambiar a discutir utils.py, ejecuta /new primero (o /clear si no necesitas el historial de la sesión). De lo contrario, el contexto obsoleto del tema anterior puede confundir las respuestas.

> 💡 **¿Cometiste un error o quieres probar un enfoque diferente?** Usa `/rewind` (o pulsa Esc dos veces) para abrir un **selector de línea de tiempo** que te permite retroceder a cualquier punto anterior de tu conversación, no solo al más reciente. Esto es útil cuando tomaste el camino equivocado y quieres dar marcha atrás sin empezar todo de nuevo.

---

### Continúa donde lo dejaste

<img src="../../../02-context-conversations/images/session-persistence-timeline.png" alt="Línea de tiempo que muestra cómo persisten las sesiones de GitHub Copilot CLI a lo largo de varios días: comenzar el lunes, reanudar el miércoles con todo el contexto restaurado" width="800"/>

*Las sesiones se guardan automáticamente al salir. Reanúdalas días después con todo el contexto: archivos, problemas y progreso, todo recordado.*

Imagina este flujo de trabajo a lo largo de varios días:

```bash
# Monday: Start book app review with a name right from the beginning
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# Work on the fix...

> /exit
```

```bash
# Wednesday: Resume exactly where you left off, by name
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**Lo que hace esto poderoso**: Días después, Copilot CLI recuerda:
- El archivo exacto en el que estabas trabajando
- La lista numerada de problemas
- Cuáles ya has abordado
- El contexto de tu conversación

Sin volver a explicar. Sin volver a leer archivos. Solo continúa trabajando.

---

**🎉 ¡Ahora conoces lo esencial!** La sintaxis `@`, la gestión de sesiones (`--name`/`--continue`/`--resume`/`/rename`) y los comandos de contexto (`/context`/`/clear`) son suficientes para ser muy productivo. Todo lo de abajo es opcional. Vuelve a ello cuando estés listo.

---

# Opcional: profundiza más

<img src="../../../02-context-conversations/images/optional-going-deeper.png" alt="Cueva de cristal abstracta en tonos azules y morados que representa una exploración más profunda de los conceptos de contexto" width="800"/>

Estos temas se construyen sobre los esenciales anteriores. **Elige lo que te interese o salta directamente a [Práctica](#practice).**

| Quiero aprender sobre... | Saltar a |
|---|---|
| Patrones comodín y comandos de sesión avanzados | [Patrones @ adicionales y comandos de sesión](#additional-patterns) |
| Construir contexto a través de varios prompts | [Conversaciones conscientes del contexto](#context-aware-conversations) |
| Límites de tokens y `/compact` | [Entender las ventanas de contexto](#understanding-context-windows) |
| Cómo elegir los archivos correctos para referenciar | [Elegir qué referenciar](#choosing-what-to-reference) |
| Analizar capturas de pantalla y mockups | [Trabajar con imágenes](#working-with-images) |

<details>
<summary><strong>Patrones @ adicionales y comandos de sesión</strong></summary>
<a id="additional-patterns"></a>

### Patrones @ adicionales

Para usuarios avanzados, Copilot CLI admite patrones comodín y referencias a imágenes:

| Patrón | Qué hace |
|---------|--------------|
| `@folder/*.py` | Todos los archivos .py en folder |
| `@**/test_*.py` | Comodín recursivo: encuentra todos los archivos de test en cualquier lugar |
| `@image.png` | Archivo de imagen para revisión de UI |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### Ver información de la sesión

```bash
copilot

> /session
# Shows current session details and workspace summary

> /usage
# Shows session metrics and statistics
```

### Compartir tu sesión

```bash
copilot

> /share file ./my-session.md
# Exports session as a markdown file

> /share gist
# Creates a GitHub gist with the session

> /share html
# Exports session as a self-contained interactive HTML file
# Useful for sharing polished session reports with teammates or saving for reference
```

</details>

<details>
<summary><strong>Conversaciones conscientes del contexto</strong></summary>
<a id="context-aware-conversations"></a>

### Conversaciones conscientes del contexto

La magia ocurre cuando tienes conversaciones de varios turnos que se construyen unas sobre otras.

#### Ejemplo: mejora progresiva

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[Shows typed version]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[Adds validation and proper exceptions]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[Generates comprehensive tests]
```

Observa cómo cada prompt se basa en el trabajo anterior. Este es el poder del contexto.

</details>

<details>
<summary><strong>Entender las ventanas de contexto</strong></summary>
<a id="understanding-context-windows"></a>

### Entender las ventanas de contexto

Ya conoces `/context` y `/clear` desde lo esencial. Aquí está la imagen más profunda de cómo funcionan las ventanas de contexto.

Toda IA tiene una "ventana de contexto", que es la cantidad de texto que puede considerar a la vez.

<img src="../../../02-context-conversations/images/context-window-visualization.png" alt="Visualización de la ventana de contexto" width="800"/>

*La ventana de contexto es como un escritorio: solo puede contener cierta cantidad a la vez. Los archivos, el historial de conversación y los prompts del sistema ocupan espacio.*

#### Qué ocurre en el límite

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# As you add more files and conversation, this grows

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Warning: Approaching context limit

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### El comando `/compact`

Cuando tu contexto se está llenando pero no quieres perder la conversación, `/compact` resume tu historial para liberar tokens:

```bash
copilot

> /compact
# Summarizes conversation history, freeing up context space
# Your key findings and decisions are preserved
```

#### Consejos de eficiencia de contexto

| Situación | Acción | Por qué |
|-----------|--------|-----|
| Iniciar nuevo tema | `/clear` | Elimina el contexto irrelevante |
| Tomaste el camino equivocado | `/rewind` | Retrocede a cualquier punto anterior |
| Conversación larga | `/compact` | Resume el historial, libera tokens |
| Necesitas un archivo específico | `@file.py` y no `@folder/` | Carga solo lo que necesitas |
| Llegando a los límites | `/new` o `/clear` | Contexto fresco |
| Varios temas | Usa `/rename` por tema | Es fácil reanudar la sesión correcta |

#### Buenas prácticas para bases de código grandes

1. **Sé específico**: `@samples/book-app-project/books.py` en lugar de `@samples/book-app-project/`
2. **Limpia el contexto entre temas**: Usa `/new` o `/clear` cuando cambies de enfoque
3. **Usa `/compact`**: Resume la conversación para liberar contexto
4. **Usa varias sesiones**: Una sesión por característica o tema

</details>

<details>
<summary><strong>Elegir qué referenciar</strong></summary>
<a id="choosing-what-to-reference"></a>

### Elegir qué referenciar

No todos los archivos son iguales cuando se trata de contexto. Aquí te explicamos cómo elegir sabiamente:

#### Consideraciones sobre el tamaño del archivo

| Tamaño del archivo | [Tokens](../../../GLOSSARY.md#token) aproximados | Estrategia |
|-----------|-------------------|----------|
| Pequeño (<100 líneas) | ~500-1.500 tokens | Referencia con libertad |
| Mediano (100-500 líneas) | ~1.500-7.500 tokens | Referencia archivos específicos |
| Grande (500+ líneas) | 7.500+ tokens | Sé selectivo, usa archivos específicos |
| Muy grande (1000+ líneas) | 15.000+ tokens | Considera dividir o apuntar a secciones |

**Ejemplos concretos:**
- Los 4 archivos Python de la app de libros combinados ≈ 2.000-3.000 tokens
- Un módulo Python típico (200 líneas) ≈ 3.000 tokens
- Un archivo de API Flask (400 líneas) ≈ 6.000 tokens
- Tu package.json ≈ 200-500 tokens
- Un prompt corto + respuesta ≈ 500-1.500 tokens

> 💡 **Estimación rápida para código:** Multiplica las líneas de código por ~15 para obtener los tokens aproximados. Ten en cuenta que esto es solo una estimación.

#### Qué incluir vs. qué excluir

**Alto valor** (incluye estos):
- Puntos de entrada (`book_app.py`, `main.py`, `app.py`)
- Los archivos específicos sobre los que estás preguntando
- Archivos importados directamente por tu archivo objetivo
- Archivos de configuración (`requirements.txt`, `pyproject.toml`)
- Modelos de datos o dataclasses

**Menor valor** (considera excluirlos):
- Archivos generados (salida compilada, recursos empaquetados)
- Módulos de Node o directorios de proveedores
- Archivos de datos grandes o fixtures
- Archivos no relacionados con tu pregunta

#### El espectro de especificidad

```
Less specific ────────────────────────► More specific
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ Scans everything                     └─ Just what you need
        (uses more context)                      (preserves context)
```

**Cuándo ir amplio** (`@samples/book-app-project/`):
- Exploración inicial de la base de código
- Encontrar patrones a través de muchos archivos
- Revisiones de arquitectura

**Cuándo ir específico** (`@samples/book-app-project/books.py`):
- Depurar un problema concreto
- Revisión de código de un archivo específico
- Preguntar sobre una sola función

#### Ejemplo práctico: carga de contexto por etapas

```bash
copilot

# Step 1: Start with structure
> @package.json What frameworks does this project use?

# Step 2: Narrow based on answer
> @samples/book-app-project/ Show me the project structure

# Step 3: Focus on what matters
> @samples/book-app-project/books.py Review the BookCollection class

# Step 4: Add related files only as needed
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

Este enfoque por etapas mantiene el contexto enfocado y eficiente.

</details>

<details>
<summary><strong>Trabajar con imágenes</strong></summary>
<a id="working-with-images"></a>

### Trabajar con imágenes

Puedes incluir imágenes en tus conversaciones usando la sintaxis `@`, o simplemente **pegar desde el portapapeles** (Cmd+V / Ctrl+V). Copilot CLI puede analizar capturas de pantalla, mockups y diagramas para ayudarte con depuración de UI, implementación de diseños y análisis de errores.

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **Aprende más**: Consulta [Funciones de contexto adicionales](../appendices/additional-context.md#working-with-images) para conocer formatos compatibles, casos de uso prácticos y consejos para combinar imágenes con código.

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración acogedora de escritorio con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Es momento de aplicar tus habilidades de contexto y gestión de sesiones.

---

## ▶️ Pruébalo tú mismo

### Revisión completa del proyecto

El curso incluye archivos de muestra que puedes revisar directamente. Inicia copilot y ejecuta el prompt que se muestra a continuación:

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI will identify issues like:
# - Duplicate display functions
# - Missing input validation
# - Inconsistent error handling
```

> 💡 **¿Quieres probar con tus propios archivos?** Crea un pequeño proyecto Python (`mkdir -p my-project/src`), añade algunos archivos .py y luego usa `@my-project/src/` para revisarlos. ¡Puedes pedirle a copilot que cree código de muestra para ti si lo deseas!

### Flujo de trabajo de sesión

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI suggests validation approach]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# Later - resume where you left off
copilot --continue

> Generate tests for the changes we made
```

---

Tras completar los demos, prueba estas variaciones:

1. **Reto entre archivos**: Analiza cómo book_app.py y books.py trabajan juntos:
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **Reto de sesión**: Inicia una sesión, nómbrala con `/rename my-first-session`, trabaja en algo, sal con `/exit`, luego ejecuta `copilot --continue`. ¿Recuerda lo que estabas haciendo?

3. **Reto de contexto**: Ejecuta `/context` a mitad de la sesión. ¿Cuántos tokens estás usando? Prueba `/compact` y vuelve a verificar. (Consulta [Entender las ventanas de contexto](#understanding-context-windows) en Profundiza más para más información sobre `/compact`.)

**Autocomprobación**: Entiendes el contexto cuando puedes explicar por qué `@folder/` es más potente que abrir cada archivo individualmente.

---

## 📝 Tarea

### Reto principal: traza el flujo de datos

Los ejemplos prácticos se centraron en revisiones de calidad del código y validación de entrada. Ahora practica las mismas habilidades de contexto en una tarea diferente, trazando cómo se mueven los datos a través de la app:

1. Inicia una sesión interactiva: `copilot`
2. Referencia `books.py` y `book_app.py` juntos:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. Trae el archivo de datos para contexto adicional:
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. Pide una mejora entre archivos:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. Renombra la sesión: `/rename data-flow-analysis`
6. Sal con `/exit`, luego reanuda con `copilot --continue` y haz una pregunta de seguimiento sobre el flujo de datos

**Criterios de éxito**: Puedes trazar datos a través de varios archivos, reanudar una sesión nombrada y obtener sugerencias entre archivos.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Para empezar:**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

Luego reanuda con: `copilot --continue`

**Comandos útiles:**
- `@file.py` - Referencia un único archivo
- `@folder/` - Referencia todos los archivos de una carpeta (nota la `/` final)
- `/context` - Comprueba cuánto contexto estás usando
- `/rename <name>` - Nombra tu sesión para reanudarla fácilmente

</details>

### Reto extra: límites de contexto

1. Referencia todos los archivos de la app de libros a la vez con `@samples/book-app-project/`
2. Haz varias preguntas detalladas sobre diferentes archivos (`books.py`, `utils.py`, `book_app.py`, `data.json`)
3. Ejecuta `/context` para ver el uso. ¿Qué tan rápido se llena?
4. Practica usando `/compact` para recuperar espacio, luego continúa la conversación
5. Prueba a ser más específico con las referencias a archivos (por ejemplo, `@samples/book-app-project/books.py` en lugar de toda la carpeta) y observa cómo afecta al uso de contexto

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Olvidar el `@` antes de los nombres de archivo | Copilot CLI trata "books.py" como texto plano | Usa `@samples/book-app-project/books.py` para referenciar archivos |
| Esperar que las sesiones persistan automáticamente | Iniciar `copilot` desde cero pierde todo el contexto anterior | Usa `--continue` (última sesión) o `--resume` (elegir una sesión) |
| Referenciar archivos fuera del directorio actual | Errores "Permission denied" o "File not found" | Usa `/add-dir /path/to/directory` para conceder acceso |
| No usar `/clear` al cambiar de tema | El contexto antiguo confunde las respuestas sobre el nuevo tema | Ejecuta `/clear` antes de empezar una tarea diferente |

### Solución de problemas

**Errores "File not found"** - Asegúrate de estar en el directorio correcto:

```bash
pwd  # Check current directory
ls   # List files

# Then start copilot and use relative paths
copilot

> Review @samples/book-app-project/books.py
```

**"Permission denied"** - Añade el directorio a tu lista permitida:

```bash
copilot --add-dir /path/to/directory

# Or in a session:
> /add-dir /path/to/directory
```

**El contexto se llena demasiado rápido**:
- Sé más específico con las referencias a archivos
- Usa `/clear` entre temas diferentes
- Divide el trabajo entre varias sesiones

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **La sintaxis `@`** le da a Copilot CLI contexto sobre archivos, directorios e imágenes
2. **Las conversaciones de varios turnos** se construyen unas sobre otras conforme se acumula el contexto
3. **Las sesiones se guardan automáticamente**: nómbralas al inicio con `--name`, reanúdalas por nombre con `--resume=<name>`, o usa `--continue` para retomar la sesión más reciente
4. **Las ventanas de contexto** tienen límites: gestiónalas con `/clear`, `/compact`, `/context`, `/new` y `/rewind`
5. **Las opciones de permisos** (`--add-dir`, `--allow-all`) controlan el acceso multidirectorio. ¡Úsalas con cuidado!
6. **Las referencias a imágenes** (`@screenshot.png`) ayudan a depurar visualmente problemas de UI

> 📚 **Documentación oficial**: [Use Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) para la referencia completa sobre contexto, sesiones y trabajo con archivos.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ahora que puedes darle contexto a Copilot CLI, vamos a ponerlo a trabajar en tareas reales de desarrollo. Las técnicas de contexto que acabas de aprender (referencias a archivos, análisis entre archivos y gestión de sesiones) son la base de los potentes flujos de trabajo del próximo capítulo.

En el **[Capítulo 03: Flujos de trabajo de desarrollo](../03-development-workflows/README.md)** aprenderás:

- Flujos de trabajo de revisión de código
- Patrones de refactorización
- Asistencia para depuración
- Generación de tests
- Integración con git

---

**[← Volver al Capítulo 01](../01-setup-and-first-steps/README.md)** | **[Continuar al Capítulo 03 →](../03-development-workflows/README.md)**
