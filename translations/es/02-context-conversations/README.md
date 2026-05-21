![Chapter 02: Context and Conversations](../../../02-context-conversations/images/chapter-header.png)

> **¿Y si la IA pudiera ver todo tu código, no solo un archivo a la vez?**

En este capítulo desbloquearás el verdadero poder de GitHub Copilot CLI: el contexto. Aprenderás a usar la sintaxis `@` para referenciar archivos y directorios, dando a Copilot CLI un entendimiento profundo de tu base de código. Descubrirás cómo mantener conversaciones a través de sesiones, reanudar el trabajo días después exactamente donde lo dejaste, y verás cómo el análisis entre archivos detecta errores que las revisiones de un solo archivo no alcanzan a ver.

## 🎯 Learning Objectives

Al final de este capítulo, podrás:

- Usar la sintaxis `@` para referenciar archivos, directorios e imágenes
- Reanudar sesiones previas con `--resume` y `--continue`
- Comprender cómo funcionan las [ventanas de contexto](../GLOSSARY.md#context-window)
- Escribir conversaciones de varios turnos efectivas
- Gestionar permisos de directorio para flujos de trabajo de múltiples proyectos

> ⏱️ **Estimated Time**: ~50 minutes (20 min reading + 30 min hands-on)

---

## 🧩 Real-World Analogy: Working with a Colleague

<img src="../../../02-context-conversations/images/colleague-context-analogy.png" alt="El contexto marca la diferencia - Sin contexto vs Con contexto" width="800"/>

*Al igual que tus colegas, Copilot CLI no es un lector de mentes. Proporcionar más información ayuda tanto a las personas como a Copilot a ofrecer soporte más específico!*

Imagina que le explicas un error a un colega:

> **Sin contexto**: "La aplicación de libros no funciona."

> **Con contexto**: "Mira `books.py`, especialmente la función `find_book_by_title`. No está haciendo una comparación insensible a mayúsculas."

Para proporcionar contexto a Copilot CLI usa *la sintaxis `@`* para indicarle archivos específicos a Copilot CLI.

---

# Essential: Basic Context

<img src="../../../02-context-conversations/images/essential-basic-context.png" alt="Bloques de código brillantes conectados por rastros de luz que representan cómo fluye el contexto a través de las conversaciones de Copilot CLI" width="800"/>

Esta sección cubre todo lo que necesitas para trabajar de forma efectiva con el contexto. Domina estos conceptos básicos primero.

---

## The @ Syntax

El símbolo `@` referencia archivos y directorios en tus mensajes. Es la forma de decirle a Copilot CLI "mira este archivo."

> 💡 **Nota**: Todos los ejemplos de este curso usan la carpeta `samples/` incluida en este repositorio, así que puedes probar cada comando directamente.

### Try It Now (No Setup Required)

Puedes probar esto con cualquier archivo en tu computadora:

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

### Basic @ Patterns

| Pattern | Qué hace | Ejemplo de uso |
|---------|--------------|-------------|
| `@file.py` | Referencia un único archivo | `Review @samples/book-app-project/books.py` |
| `@folder/` | Referencia todos los archivos en un directorio | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | Referencia múltiples archivos | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### Reference a Single File

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![File Context Demo](../../../02-context-conversations/images/file-context-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

---

### Reference Multiple Files

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### Reference an Entire Directory

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## Cross-File Intelligence

Aquí es donde el contexto se convierte en una superpotencia. El análisis de un solo archivo es útil. El análisis entre archivos es transformador.

<img src="../../../02-context-conversations/images/cross-file-intelligence.png" alt="Inteligencia entre archivos - comparando análisis de un solo archivo vs análisis entre archivos mostrando cómo analizar archivos juntos revela errores, flujo de datos y patrones invisibles en aislamiento" width="800"/>

### Demo: Find Bugs That Span Multiple Files

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **Opción avanzada**: Para análisis entre archivos centrados en seguridad, prueba los ejemplos de seguridad en Python:
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Multi-File Demo](../../../02-context-conversations/images/multi-file-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

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

**Por qué esto importa**: Una revisión de un solo archivo perdería el panorama completo. Solo el análisis entre archivos revela:
- **Código duplicado** que debería consolidarse
- **Patrones de flujo de datos** que muestran cómo interactúan los componentes
- **Problemas arquitectónicos** que afectan la mantenibilidad

---

### Demo: Understand a Codebase in 60 Seconds

<img src="../../../02-context-conversations/images/codebase-understanding.png" alt="Comparación en pantalla dividida mostrando la revisión manual de código que toma 1 hora frente a análisis asistido por IA que toma 10 segundos" width="800" />

¿Nuevo en un proyecto? Conócela rápidamente usando Copilot CLI.

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

**Resultado**: Lo que toma una hora de lectura de código comprimido en 10 segundos. Sabes exactamente dónde enfocarte.

---

## Practical Examples

### Example 1: Code Review with Context

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI ahora tiene el contenido completo del archivo y puede dar retroalimentación específica:
# "Line 49: La comparación que distingue entre mayúsculas y minúsculas puede omitir libros..."
# "Line 29: Los errores de decodificación JSON se capturan pero la corrupción de datos no se registra..."

> What about @samples/book-app-project/book_app.py?

# Ahora revisando book_app.py, pero aún consciente del contexto de books.py
```

### Example 2: Understanding a Codebase

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI lee books.py y comprende la clase BookCollection

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI escanea el directorio y resume

> How does the app save and load books?

# Copilot CLI puede rastrear el código que ya ha visto
```

<details>
<summary>🎬 Observa una conversación de varios turnos en acción!</summary>

![Multi-Turn Demo](../../../02-context-conversations/images/multi-turn-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

### Example 3: Multi-File Refactoring

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI ve ambos archivos y puede sugerir cómo fusionar el código duplicado
```

---

## Session Management

Las sesiones se guardan automáticamente mientras trabajas. Puedes reanudar sesiones previas para continuar donde lo dejaste.

### Sessions Auto-Save

Cada conversación se guarda automáticamente. Simplemente sal normalmente:

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... do some work ...]

> /exit
```

### Resume the Most Recent Session

```bash
# Continúa donde lo dejaste
copilot --continue
```

### Resume a Specific Session

```bash
# Selecciona de una lista de sesiones de forma interactiva
copilot --resume

# O reanuda una sesión específica por su ID
copilot --resume=abc123

# O reanuda por el nombre que le diste a la sesión
copilot --resume="my book app review"
```

> 💡 **¿Cómo encuentro un ID de sesión?** No necesitas memorizarlos. Ejecutar `copilot --resume` sin un ID muestra una lista interactiva de tus sesiones previas, sus nombres, IDs y cuándo estuvieron activas por última vez. Simplemente elige la que quieras.
>
> **¿Y si tengo múltiples terminales?** Cada ventana de terminal es su propia sesión con su propio contexto. Si tienes Copilot CLI abierto en tres terminales, eso son tres sesiones separadas. Ejecutar `--resume` desde cualquier terminal te permite explorar todas ellas. La bandera `--continue` toma la sesión del directorio de trabajo actual primero; si no existe allí, elige la sesión más recientemente activa.
>
> **¿Puedo cambiar de sesión sin reiniciar?** Sí. Usa el comando con barra `/resume` desde dentro de una sesión activa:
> ```
> > /resume
> # Shows a list of sessions to switch to
> ```

### Organize Your Sessions

Da a las sesiones nombres significativos para que las puedas encontrar después. Puedes nombrar una sesión cuando la inicias, o renombrarla en cualquier momento mientras estás dentro de la sesión:

```bash
# Nombra una sesión justo cuando la inicias
copilot --name book-app-review

# O renombra la sesión actual desde dentro
copilot

> /rename book-app-review
# Sesión renombrada para facilitar su identificación
```

Una vez que una sesión tiene nombre, puedes reanudarla directamente por nombre sin navegar por la lista:

```bash
copilot --resume=book-app-review
```

Para limpiar sesiones que ya no necesitas, usa `/session delete` desde dentro de una sesión:

```bash
copilot

> /session delete            # Elimina la sesión actual
> /session delete abc123     # Elimina una sesión específica por ID
> /session delete-all        # Elimina todas las sesiones (¡usar con precaución!)
```

### Check and Manage Context

A medida que añades archivos y conversación, la [ventana de contexto](../GLOSSARY.md#context-window) de Copilot CLI se llena. Hay varios comandos disponibles para ayudarte a mantener el control:

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandona la sesión actual (no se guarda el historial) y comienza una conversación nueva

> /new
# Finaliza la sesión actual (guardándola en el historial para búsqueda/reanudación) y comienza una conversación nueva

> /rewind
# Abre un selector de línea de tiempo que te permite retroceder a un punto anterior de tu conversación
```

> 💡 **¿Cuándo usar `/clear` o `/new`?** Si has estado revisando books.py y quieres cambiar a discutir utils.py, ejecuta /new primero (o /clear si no necesitas el historial de la sesión). De lo contrario, el contexto obsoleto del tema anterior puede confundir las respuestas.

> 💡 **¿Cometiste un error o quieres probar un enfoque distinto?** Usa `/rewind` (o presiona Esc dos veces) para abrir un **selector de línea de tiempo** que te permite retroceder a cualquier punto anterior en tu conversación, no solo al más reciente. Esto es útil cuando te desviastes por un camino equivocado y quieres retroceder sin empezar de nuevo por completo.

---

### Pick Up Where You Left Off

<img src="../../../02-context-conversations/images/session-persistence-timeline.png" alt="Línea de tiempo que muestra cómo las sesiones de GitHub Copilot CLI persisten a través de los días - empieza el lunes, reanuda el miércoles con todo el contexto restaurado" width="800"/>

*Las sesiones se guardan automáticamente cuando sales. Reanuda días después con todo el contexto: archivos, problemas y progreso, todo recordado.*

Imagina este flujo de trabajo a lo largo de varios días:

```bash
# Lunes: Comenzar la revisión de la aplicación de libros con un nombre desde el principio
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (funciones duplicadas)
# Trabajar en la corrección...

> /exit
```

```bash
# Miércoles: Reanuda exactamente donde lo dejaste, por nombre
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (funciones duplicadas) se corrigió el lunes.

> Let's tackle issue #2 next
```

**Qué lo hace poderoso**: Días después, Copilot CLI recuerda:
- El archivo exacto en el que estabas trabajando
- La lista numerada de problemas
- Cuáles ya has solucionado
- El contexto de tu conversación

Sin volver a explicar. Sin volver a leer archivos. Simplemente continúa trabajando.

---

**🎉 ¡Ahora conoces lo esencial!** La sintaxis `@`, la gestión de sesiones (`--name`/`--continue`/`--resume`/`/rename`) y los comandos de contexto (`/context`/`/clear`) son suficientes para ser muy productivo. Todo lo que sigue abajo es opcional. Vuelve a ello cuando estés listo.

---

# Optional: Going Deeper

<img src="../../../02-context-conversations/images/optional-going-deeper.png" alt="Cueva cristalina abstracta en tonos azul y púrpura que representa una exploración más profunda de conceptos de contexto" width="800"/>

Estos temas se basan en lo esencial anterior. **Elige lo que te interese, o salta a [Práctica](#el-espectro-de-especificidad).**

| I want to learn about... | Jump to |
|---|---|
| Wildcard patterns and advanced session commands | [Additional @ Patterns & Session Commands](#check-and-manage-context) |
| Building on context across multiple prompts | [Context-Aware Conversations](#patrones-adicionales) |
| Token limits and `/compact` | [Understanding Context Windows](#compartir-tu-sesión) |
| How to pick the right files to reference | [Choosing What to Reference](#el-comando-compact) |
| Analyzing screenshots and mockups | [Working with Images](#qué-incluir-vs-excluir) |

<details>
<summary><strong>Patrones @ adicionales y comandos de sesión</strong></summary>
<a id="additional-patterns"></a>

### Patrones @ adicionales

Para usuarios avanzados, Copilot CLI soporta patrones comodín y referencias a imágenes:

| Pattern | Qué hace |
|---------|--------------|
| `@folder/*.py` | Todos los archivos .py en la carpeta |
| `@**/test_*.py` | Comodín recursivo: encuentra todos los archivos de prueba en cualquier lugar |
| `@image.png` | Archivo de imagen para revisión de la UI |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### Ver información de la sesión

```bash
copilot

> /session
# Muestra los detalles de la sesión actual y el resumen del espacio de trabajo

> /usage
# Muestra métricas y estadísticas de la sesión
```

### Compartir tu sesión

```bash
copilot

> /share file ./my-session.md
# Exporta la sesión como un archivo Markdown

> /share gist
# Crea un gist de GitHub con la sesión

> /share html
# Exporta la sesión como un archivo HTML interactivo autocontenido
# Útil para compartir informes de sesión pulidos con compañeros de equipo o guardarlos para referencia
```

</details>

<details>
<summary><strong>Conversaciones conscientes del contexto</strong></summary>
<a id="context-aware-conversations"></a>

### Conversaciones conscientes del contexto

La magia ocurre cuando tienes conversaciones de varios turnos que se construyen unas sobre otras.

#### Example: Progressive Enhancement

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

Fíjate cómo cada instrucción se basa en el trabajo anterior. Este es el poder del contexto.

</details>

<details>
<summary><strong>Comprender las ventanas de contexto</strong></summary>
<a id="understanding-context-windows"></a>

### Comprender las ventanas de contexto

Ya conoces `/context` y `/clear` de lo esencial. Aquí está la imagen más profunda de cómo funcionan las ventanas de contexto.

Cada modelo de IA tiene una "ventana de contexto", que es la cantidad de texto que puede considerar a la vez.

<img src="../../../02-context-conversations/images/context-window-visualization.png" alt="Visualización de la ventana de contexto" width="800"/>

*La ventana de contexto es como un escritorio: solo puede contener cierta cantidad a la vez. Archivos, historial de conversación y prompts del sistema consumen espacio.*

#### Qué sucede cuando se alcanza el límite

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# A medida que agregas más archivos y conversaciones, esto crece

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Advertencia: Acercándose al límite de contexto

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### El comando `/compact`

Cuando tu contexto se está llenando pero no quieres perder la conversación, `/compact` resume tu historial para liberar tokens:

```bash
copilot

> /compact
# Resume el historial de la conversación, liberando espacio de contexto
# Se preservan tus hallazgos y decisiones clave
```

#### Consejos de eficiencia del contexto

| Situación | Acción | Por qué |
|-----------|--------|-----|
| Iniciar un nuevo tema | `/clear` | Elimina contexto irrelevante |
| Tomaste el camino equivocado | `/rewind` | Retrocede a cualquier punto anterior |
| Conversación larga | `/compact` | Resume el historial, libera tokens |
| Necesitas archivo específico | `@file.py` no `@folder/` | Carga solo lo que necesitas |
| Alcanzando límites | `/new` o `/clear` | Contexto fresco |
| Múltiples temas | Usa `/rename` por tema | Fácil reanudar la sesión correcta |

#### Buenas prácticas para bases de código grandes

1. **Sé específico**: `@samples/book-app-project/books.py` en lugar de `@samples/book-app-project/`
2. **Limpia el contexto entre temas**: Usa `/new` o `/clear` cuando cambies de enfoque
3. **Usa `/compact`**: Resume la conversación para liberar contexto
4. **Usa varias sesiones**: Una sesión por característica o tema

</details>

<details>
<summary><strong>Eligiendo qué referenciar</strong></summary>
<a id="choosing-what-to-reference"></a>

### Eligiendo qué referenciar

No todos los archivos son iguales cuando se trata de contexto. Aquí tienes cómo elegir sabiamente:

#### Consideraciones sobre el tamaño de archivo

| Tamaño del archivo | Aproximados [Tokens](../GLOSSARY.md#token) | Estrategia |
|-----------|-------------------|----------|
| Pequeño (<100 líneas) | ~500-1,500 tokens | Referenciar libremente |
| Mediano (100-500 líneas) | ~1,500-7,500 tokens | Referenciar archivos específicos |
| Grande (500+ líneas) | 7,500+ tokens | Sé selectivo, usa archivos específicos |
| Muy grande (1000+ líneas) | 15,000+ tokens | Considera dividir o apuntar a secciones |

**Ejemplos concretos:**
- Los 4 archivos Python de la app de libros combinados ≈ 2,000-3,000 tokens
- Un módulo Python típico (200 líneas) ≈ 3,000 tokens
- Un archivo de API Flask (400 líneas) ≈ 6,000 tokens
- Tu package.json ≈ 200-500 tokens
- Un prompt corto + respuesta ≈ 500-1,500 tokens

> 💡 **Estimación rápida para código:** Multiplica las líneas de código por ~15 para obtener los tokens aproximados. Ten en cuenta que esto es solo una estimación.

#### Qué incluir vs. excluir

**Alto valor** (incluir estos):
- Puntos de entrada (`book_app.py`, `main.py`, `app.py`)
- Los archivos específicos que estás consultando
- Archivos importados directamente por tu archivo objetivo
- Archivos de configuración (`requirements.txt`, `pyproject.toml`)
- Modelos de datos o dataclasses

**Menor valor** (considera excluir):
- Archivos generados (salida compilada, assets empaquetados)
- node_modules o directorios vendor
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

**Cuando ir amplio** (`@samples/book-app-project/`):
- Exploración inicial del código base
- Encontrar patrones a través de muchos archivos
- Revisiones de arquitectura

**Cuando ir específico** (`@samples/book-app-project/books.py`):
- Depurar un problema en particular
- Revisión de código de un archivo específico
- Preguntar sobre una única función

#### Ejemplo práctico: Carga de contexto por etapas

```bash
copilot

# Paso 1: Comienza con la estructura
> @package.json What frameworks does this project use?

# Paso 2: Acota según la respuesta
> @samples/book-app-project/ Show me the project structure

# Paso 3: Enfócate en lo que importa
> @samples/book-app-project/books.py Review the BookCollection class

# Paso 4: Añade solo los archivos relacionados cuando sea necesario
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

Este enfoque por etapas mantiene el contexto enfocado y eficiente.

</details>

<details>
<summary><strong>Trabajar con imágenes</strong></summary>
<a id="working-with-images"></a>

### Trabajar con imágenes

Puedes incluir imágenes en tus conversaciones usando la sintaxis `@`, o simplemente **pegar desde tu portapapeles** (Cmd+V / Ctrl+V). Copilot CLI puede analizar capturas de pantalla, maquetas y diagramas para ayudar con la depuración de UI, la implementación de diseño y el análisis de errores.

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **Aprende más**: Consulta [Funciones adicionales de contexto](../appendices/additional-context.md#trabajar-con-imágenes) para formatos soportados, casos de uso prácticos y consejos para combinar imágenes con código.

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración cálida de escritorio con un monitor que muestra código, una lámpara, una taza de café y auriculares listos para la práctica" width="800"/>

Es hora de aplicar tus habilidades de manejo de contexto y sesiones.

---

## ▶️ Inténtalo tú mismo

### Revisión completa del proyecto

El curso incluye archivos de muestra que puedes revisar directamente. Inicia copilot y ejecuta el prompt mostrado a continuación:

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI identificará problemas como:
# - Funciones de visualización duplicadas
# - Falta de validación de entradas
# - Manejo inconsistente de errores
```

> 💡 **¿Quieres probar con tus propios archivos?** Crea un pequeño proyecto Python (`mkdir -p my-project/src`), añade algunos archivos .py, luego usa `@my-project/src/` para revisarlos. ¡Puedes pedirle a copilot que cree código de ejemplo si quieres!

### Flujo de trabajo de la sesión

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI suggests validation approach]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# Más tarde - reanuda donde lo dejaste
copilot --continue

> Generate tests for the changes we made
```

---

Después de completar las demos, prueba estas variaciones:

1. **Desafío entre archivos**: Analiza cómo trabajan book_app.py y books.py juntos:
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **Desafío de sesión**: Inicia una sesión, asígnale nombre con `/rename my-first-session`, trabaja en algo, sal con `/exit`, luego ejecuta `copilot --continue`. ¿Recuerda lo que estabas haciendo?

3. **Desafío de contexto**: Ejecuta `/context` a mitad de la sesión. ¿Cuántos tokens estás usando? Prueba `/compact` y verifica de nuevo. (Consulta [Comprender las ventanas de contexto](#compartir-tu-sesión) en Going Deeper para más sobre `/compact`.)

**Autoevaluación**: Entiendes el contexto cuando puedes explicar por qué `@folder/` es más poderoso que abrir cada archivo individualmente.

---

## 📝 Tarea

### Desafío principal: Rastrear el flujo de datos

Los ejemplos prácticos se centraron en revisiones de calidad de código y validación de entradas. Ahora practica las mismas habilidades de contexto en una tarea diferente, rastreando cómo se mueven los datos a través de la aplicación:

1. Inicia una sesión interactiva: `copilot`
2. Referencia `books.py` y `book_app.py` juntos:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. Trae el archivo de datos para contexto adicional:
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. Pide una mejora entre archivos:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. Renombra la sesión: `/rename data-flow-analysis`
6. Sal con `/exit`, luego reanuda con `copilot --continue` y haz una pregunta de seguimiento sobre el flujo de datos

**Criterios de éxito**: Puedes rastrear datos a través de múltiples archivos, reanudar una sesión nombrada y obtener sugerencias entre archivos.

<details>
<summary>💡 Sugerencias (haz clic para expandir)</summary>

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
- `@file.py` - Referencia un solo archivo
- `@folder/` - Referencia todos los archivos en una carpeta (fíjate en la `/` final)
- `/context` - Verifica cuánto contexto estás usando
- `/rename <name>` - Nombra tu sesión para reanudarla fácilmente

</details>

### Desafío extra: Límites de contexto

1. Referencia todos los archivos de la app de libros a la vez con `@samples/book-app-project/`
2. Haz varias preguntas detalladas sobre diferentes archivos (`books.py`, `utils.py`, `book_app.py`, `data.json`)
3. Ejecuta `/context` para ver el uso. ¿Qué tan rápido se llena?
4. Practica usando `/compact` para recuperar espacio, luego continúa la conversación
5. Intenta ser más específico con las referencias de archivos (por ejemplo, `@samples/book-app-project/books.py` en lugar de toda la carpeta) y observa cómo afecta el uso del contexto

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué sucede | Solución |
|---------|--------------|-----|
| Olvidar `@` antes de los nombres de archivo | Copilot CLI trata "books.py" como texto plano | Usa `@samples/book-app-project/books.py` para referenciar archivos |
| Esperar que las sesiones persistan automáticamente | Iniciar `copilot` de nuevo pierde todo el contexto previo | Usa `--continue` (última sesión) o `--resume` (elige una sesión) |
| Referenciar archivos fuera del directorio actual | "Permission denied" or "File not found" errors | Usa `/add-dir /path/to/directory` para otorgar acceso |
| No usar `/clear` al cambiar de tema | El contexto antiguo confunde las respuestas sobre el nuevo tema | Ejecuta `/clear` antes de empezar una tarea diferente |

### Solución de problemas

**"File not found" errors** - Asegúrate de estar en el directorio correcto:

```bash
pwd  # Comprobar el directorio actual
ls   # Listar archivos

# Luego inicia copilot y usa rutas relativas
copilot

> Review @samples/book-app-project/books.py
```

**"Permission denied"** - Agrega el directorio a tu lista de permitidos:

```bash
copilot --add-dir /path/to/directory

# O en una sesión:
> /add-dir /path/to/directory
```

**El contexto se llena demasiado rápido**:
- Sé más específico con las referencias a archivos
- Usa `/clear` entre diferentes temas
- Divide el trabajo en varias sesiones

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Sintaxis `@`** proporciona a Copilot CLI contexto sobre archivos, directorios e imágenes
2. **Conversaciones de múltiples turnos** se construyen unas sobre otras a medida que el contexto se acumula
3. **Las sesiones se guardan automáticamente**: nómbralas al inicio con `--name`, reanuda por nombre con `--resume=<name>`, o usa `--continue` para retomar la sesión más reciente
4. **Las ventanas de contexto** tienen límites: adminístralas con `/clear`, `/compact`, `/context`, `/new`, y `/rewind`
5. **Flags de permiso** (`--add-dir`, `--allow-all`) controlan el acceso a múltiples directorios. ¡Úsalos con prudencia!
6. **Referencias de imágenes** (`@screenshot.png`) ayudan a depurar visualmente problemas de UI

> 📚 **Documentación oficial**: [Usar Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) para la referencia completa sobre contexto, sesiones y trabajo con archivos.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ahora que sabes cómo dar contexto a Copilot CLI, pongámoslo a trabajar en tareas reales de desarrollo. Las técnicas de contexto que acabas de aprender (referencias de archivos, análisis entre archivos y gestión de sesiones) son la base para los flujos de trabajo potentes del próximo capítulo.

En **[Capítulo 03: Flujos de trabajo de desarrollo](../03-development-workflows/README.md)**, aprenderás:

- Flujos de revisión de código
- Patrones de refactorización
- Asistencia para depuración
- Generación de pruebas
- Integración con Git

---

**[← Volver al Capítulo 01](../01-setup-and-first-steps/README.md)** | **[Continuar al Capítulo 03 →](../03-development-workflows/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->