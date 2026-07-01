<!--
---
id: CopilotCLI-02
title: !translate Context and Conversations
description: !translate Use file and directory context, resume previous sessions, and write effective multi-turn conversations with GitHub Copilot CLI.
audience: Developers / Students / Terminal users
slug: context-and-conversations
weight: 3
---
-->

![Capítulo 02: Contexto y Conversaciones](../../../02-context-conversations/assets/chapter-header.png)

> **¿Y si la IA pudiera ver todo tu código, no solo un archivo a la vez?**

En este capítulo, desbloquearás el verdadero poder de GitHub Copilot CLI: el contexto. Aprenderás a usar la sintaxis `@` para referenciar archivos y directorios, dándole a Copilot CLI una comprensión profunda de tu base de código. Descubrirás cómo mantener conversaciones a través de sesiones, reanudar el trabajo días después exactamente donde lo dejaste, y verás cómo el análisis entre archivos detecta errores que las revisiones de un solo archivo pasarían por alto por completo.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Usar la sintaxis `@` para referenciar archivos, directorios e imágenes
- Reanudar sesiones anteriores con `--resume` y `--continue`
- Entender cómo funcionan las [ventanas de contexto](../GLOSSARY.md#ventana-de-contexto)
- Escribir conversaciones multi-turn efectivas
- Administrar permisos de directorio para flujos de trabajo con múltiples proyectos

> ⏱️ **Tiempo estimado**: ~50 minutos (20 min lectura + 30 min práctica)

---

## 🧩 Analogía del mundo real: Trabajar con un colega

<img src="../../../02-context-conversations/assets/colleague-context-analogy.png" alt="El contexto marca la diferencia - Sin contexto vs Con contexto" width="800"/>

*Al igual que tus colegas, Copilot CLI no es un lector de mentes. Proporcionar más información ayuda tanto a humanos como a Copilot a ofrecer soporte más dirigido.*

Imagina explicar un bug a un colega:

> **Sin contexto**: "La aplicación de libros no funciona."

> **Con contexto**: "Mira `books.py`, especialmente la función `find_book_by_title`. No está haciendo una comparación sin distinguir mayúsculas y minúsculas."

Para proporcionar contexto a Copilot CLI usa *la sintaxis `@`* para apuntar Copilot CLI a archivos específicos.

---

# Esencial: Contexto básico

<img src="../../../02-context-conversations/assets/essential-basic-context.png" alt="Bloques de código brillantes conectados por rastros de luz que representan cómo fluye el contexto en las conversaciones de Copilot CLI" width="800"/>

Esta sección cubre todo lo que necesitas para trabajar eficazmente con el contexto. Domina estos conceptos básicos primero.

---

## La sintaxis @

El símbolo `@` referencia archivos y directorios en tus indicaciones. Es como decirle a Copilot CLI "mira este archivo".

> 💡 **Nota**: Todos los ejemplos en este curso usan la carpeta `samples/` incluida en este repositorio, así que puedes probar cada comando directamente.

### Pruébalo ahora (sin configuración necesaria)

Puedes probar esto con cualquier archivo en tu computadora:

```bash
copilot

# Señala cualquier archivo que tengas
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

### Patrones básicos @

| Patrón | Qué hace | Ejemplo de uso |
|---------|--------------|-------------|
| `@file.py` | Referencia un solo archivo | `Review @samples/book-app-project/books.py` |
| `@folder/` | Referencia todos los archivos en un directorio | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | Referencia múltiples archivos | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### Referenciar un solo archivo

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de contexto de archivo](../../../02-context-conversations/assets/file-context-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

### Referenciar múltiples archivos

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

Aquí es donde el contexto se convierte en una superpotencia. El análisis de un solo archivo es útil. El análisis entre archivos es transformador.

<img src="../../../02-context-conversations/assets/cross-file-intelligence.png" alt="Inteligencia entre archivos - comparando análisis de un solo archivo vs análisis entre archivos mostrando cómo analizar archivos juntos revela errores, flujo de datos y patrones invisibles en aislamiento" width="800"/>

### Demostración: Encontrar errores que abarcan varios archivos

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **Opción avanzada**: Para análisis entre archivos centrado en seguridad, prueba los ejemplos de seguridad en Python:
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración multi-archivo](../../../02-context-conversations/assets/multi-file-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

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

**Por qué esto importa**: Una revisión de un solo archivo perdería la imagen completa. Solo el análisis entre archivos revela:
- **Código duplicado** que debería consolidarse
- **Patrones de flujo de datos** que muestran cómo interactúan los componentes
- **Problemas arquitectónicos** que afectan la mantenibilidad

---

### Demostración: Entender una base de código en 60 segundos

<img src="../../../02-context-conversations/assets/codebase-understanding.png" alt="Comparación en pantalla dividida mostrando revisión manual de código tomando 1 hora frente a análisis asistido por IA tomando 10 segundos" width="800" />

¿Nuevo en un proyecto? Conócelo rápidamente usando Copilot CLI.

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

## Ejemplos prácticos

### Ejemplo 1: Revisión de código con contexto

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI ahora tiene el contenido completo del archivo y puede dar comentarios específicos:
# "Line 49: La comparación sensible a mayúsculas y minúsculas puede omitir libros..."
# "Line 29: Los errores de decodificación JSON se capturan pero la corrupción de datos no se registra..."

> What about @samples/book-app-project/book_app.py?

# Ahora revisando book_app.py, pero aún consciente del contexto de books.py
```

### Ejemplo 2: Entender una base de código

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI lee books.py y comprende la clase BookCollection

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI examina el directorio y resume

> How does the app save and load books?

# Copilot CLI puede rastrear el código que ya ha visto
```

<details>
<summary>🎬 ¡Mira una conversación multi-turno en acción!</summary>

![Demostración multi-turno](../../../02-context-conversations/assets/multi-turn-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

### Ejemplo 3: Refactorización multi-archivo

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI ve ambos archivos y puede sugerir cómo combinar el código duplicado
```

---

## Gestión de sesiones

Las sesiones se guardan automáticamente mientras trabajas. Puedes reanudar sesiones anteriores para continuar donde lo dejaste.

### Guardado automático de sesiones

Cada conversación se guarda automáticamente. Simplemente sal de forma normal:

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... do some work ...]

> /exit
```

### Reanudar la sesión más reciente

```bash
# Continúa donde lo dejaste
copilot --continue
```

### Reanudar una sesión específica

```bash
# Elige de una lista de sesiones de forma interactiva
copilot --resume

# -r es un atajo para --resume (¡ahorra algo de tecleo!)
copilot -r

# O reanuda una sesión específica por su ID
copilot --resume=abc123

# O reanuda por el nombre que le diste a la sesión
copilot --resume="my book app review"
```

> 💡 **¿Cómo encuentro un ID de sesión?** No necesitas memorizarlos. Ejecutar `copilot --resume` sin un ID muestra una lista interactiva de tus sesiones anteriores, sus nombres, IDs y cuándo estuvieron activas por última vez. Simplemente elige la que quieras.
>
> **¿Y qué pasa con múltiples terminales?** Cada ventana de terminal es su propia sesión con su propio contexto. Si tienes Copilot CLI abierto en tres terminales, eso son tres sesiones separadas. Ejecutar `--resume` desde cualquier terminal te permite navegar por todas ellas. La bandera `--continue` toma la sesión del directorio de trabajo actual primero; si no existe ninguna allí, elige la sesión que estuvo activa más recientemente.
>
> **¿Puedo cambiar de sesión sin reiniciar?** Sí. Usa el comando con barra `/resume` desde dentro de una sesión activa:
> ```
> > /resume
> # Shows a list of sessions to switch to
> ```

### Organiza tus sesiones

Dale a las sesiones nombres significativos para que puedas encontrarlas después. Puedes nombrar una sesión al iniciarla, o renombrarla en cualquier momento mientras estás dentro de la sesión:

```bash
# Nombra una sesión justo cuando la inicias
copilot --name book-app-review

# O renombra la sesión actual desde dentro
copilot

> /rename book-app-review
# Sesión renombrada para facilitar su identificación
```

Una vez que una sesión tiene nombre, puedes reanudarla directamente por nombre sin navegar por una lista:

```bash
copilot --resume=book-app-review
```

Para limpiar sesiones que ya no necesitas, usa `/session delete` desde dentro de una sesión:

```bash
copilot

> /session delete            # Elimina la sesión actual
> /session delete abc123     # Elimina una sesión específica por su ID
> /session delete-all        # Elimina todas las sesiones (¡úselo con precaución!)
```

### Memoria persistente entre sesiones

Las sesiones guardan el historial de tu conversación, pero la **memoria** va un paso más allá y permite que Copilot CLI recuerde preferencias y hechos *entre todas las sesiones*, no solo dentro de una sola.

```bash
copilot

> /memory show
# Muestra lo que Copilot CLI recuerda actualmente sobre ti y tu proyecto

> /memory on
# Activa la memoria (habilitada por defecto si tu cuenta la admite)

> /memory off
# Desactiva la memoria (útil si prefieres empezar de cero cada vez)
```

Por ejemplo, si le dices a Copilot CLI "Siempre prefiero pytest para pruebas en Python", puede recordar esa preferencia y aplicarla automáticamente en sesiones futuras. Todo sin que tengas que repetirlo.

> 💡 **Memoria vs. Sesiones**: Las sesiones guardan el historial de la conversación para que puedas reanudar una tarea específica. La memoria guarda hechos reutilizables del repositorio y preferencias del usuario que Copilot puede aplicar en trabajos futuros. Piensa en las sesiones como cuadernos de tareas, y en la memoria como contexto reutilizable que Copilot puede llevar adelante.

### Verificar y gestionar el contexto

A medida que agregas archivos y conversación, la [ventana de contexto](../GLOSSARY.md#ventana-de-contexto) de Copilot CLI se va llenando. Hay varios comandos disponibles para ayudarte a mantener el control:

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandona la sesión actual (no se guarda el historial) y comienza una conversación nueva

> /new
# Finaliza la sesión actual (guardándola en el historial para búsqueda o reanudación) y comienza una conversación nueva

> /rewind
# Abre un selector de línea de tiempo que te permite retroceder a un punto anterior de la conversación
```

> 💡 **Cuándo usar `/clear` o `/new`**: Si has estado revisando books.py y quieres cambiar a discutir utils.py, ejecuta /new primero (o /clear si no necesitas el historial de la sesión). De lo contrario, el contexto obsoleto del tema anterior puede confundir las respuestas.
>
> 💡 **¿Cometiste un error o quieres probar un enfoque diferente?** Usa `/rewind` (o presiona Esc dos veces) para abrir un **selector de línea de tiempo** que te permite volver a cualquier punto anterior en tu conversación, no solo al más reciente. Esto es útil cuando te equivocaste de camino y quieres retroceder sin empezar de nuevo por completo.

---

### Retoma donde lo dejaste

<img src="../../../02-context-conversations/assets/session-persistence-timeline.png" alt="Línea de tiempo que muestra cómo las sesiones de GitHub Copilot CLI persisten a lo largo de días - comenzar el lunes, reanudar el miércoles con el contexto completo restablecido" width="800"/>

*Las sesiones se guardan automáticamente cuando sales. Reanuda días después con el contexto completo: archivos, issues y progreso, todo recordado.*

Imagina este flujo de trabajo a lo largo de varios días:

```bash
# Lunes: Empezar la revisión de la aplicación de libros con un nombre desde el principio
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
# Miércoles: Reanuda exactamente donde te quedaste, por nombre
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (funciones duplicadas) se solucionó el lunes.

> Let's tackle issue #2 next
```

**Por qué esto es poderoso**: Días después, Copilot CLI recuerda:
- El archivo exacto en el que estabas trabajando
- La lista numerada de problemas
- Cuáles ya has abordado
- El contexto de tu conversación

No volver a explicar. No volver a leer archivos. Simplemente continúa trabajando.

---

**🎉 ¡Ahora conoces lo esencial!** La sintaxis `@`, la gestión de sesiones (`--name`/`--continue`/`--resume`/`/rename`), y los comandos de contexto (`/context`/`/clear`) son suficientes para ser muy productivo. Todo lo que sigue es opcional. Vuelve a ello cuando estés listo.

---

# Opcional: Profundizar

<img src="../../../02-context-conversations/assets/optional-going-deeper.png" alt="Cueva de cristal abstracta en tonos azules y morados que representa una exploración más profunda de los conceptos de contexto" width="800"/>

Estos temas se basan en lo esencial anterior. **Elige lo que te interese, o salta adelante a [Práctica](#el-espectro-de-especificidad).**

| Quiero aprender sobre... | Ir a |
|---|---|
| Patrones comodín y comandos de sesión avanzados | [Patrones @ adicionales y comandos de sesión](#verificar-y-gestionar-el-contexto) |
| Construir sobre el contexto a través de múltiples indicaciones | [Conversaciones con contexto](#patrones-adicionales) |
| Límites de tokens y `/compact` | [Comprender las ventanas de contexto](#compartir-tu-sesión) |
| Cómo elegir los archivos correctos para referenciar | [Cómo elegir qué referenciar](#el-comando-compact) |
| Analizar capturas de pantalla y maquetas | [Trabajar con imágenes](#qué-incluir-vs-excluir) |

<details>
<summary><strong>Patrones @ adicionales y comandos de sesión</strong></summary>
<a id="additional-patterns"></a>

### Patrones @ adicionales

Para usuarios avanzados, Copilot CLI admite patrones comodín y referencias a imágenes:

| Patrón | Qué hace |
|---------|--------------|
| `@folder/*.py` | Todos los archivos .py en la carpeta |
| `@**/test_*.py` | Comodín recursivo: encuentra todos los archivos de prueba en cualquier lugar |
| `@image.png` | Archivo de imagen para revisión de UI |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### Ver información de la sesión

```bash
copilot

> /session
# Muestra los detalles de la sesión actual y un resumen del espacio de trabajo

> /usage
# Muestra métricas y estadísticas de la sesión
```

### Compartir tu sesión

```bash
copilot

> /share file ./my-session.md
# Exporta la sesión como un archivo markdown

> /share gist
# Crea un gist de GitHub con la sesión

> /share html
# Exporta la sesión como un archivo HTML interactivo autónomo
# Útil para compartir informes de sesión pulidos con compañeros de equipo o guardar como referencia
```

</details>

<details>
<summary><strong>Conversaciones con contexto</strong></summary>
<a id="context-aware-conversations"></a>

### Conversaciones con contexto

La magia ocurre cuando tienes conversaciones de múltiples turnos que se construyen unas sobre otras.

#### Ejemplo: Mejora progresiva

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

Fíjate cómo cada indicación se basa en el trabajo previo. Este es el poder del contexto.

</details>

<details>
<summary><strong>Comprender las ventanas de contexto</strong></summary>
<a id="understanding-context-windows"></a>

### Comprender las ventanas de contexto

Ya conoces `/context` y `/clear` de lo esencial. Aquí tienes una visión más profunda de cómo funcionan las ventanas de contexto.

Every AI has a "context window," which is the amount of text it can consider at once.

<img src="../../../02-context-conversations/assets/context-window-visualization.png" alt="Visualización de la ventana de contexto" width="800"/>

*La ventana de contexto es como un escritorio: solo puede contener cierta cantidad a la vez. Los archivos, el historial de la conversación y los prompts del sistema ocupan espacio.*

#### Qué sucede al llegar al límite

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# A medida que agregas más archivos y conversaciones, esto crece

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Advertencia: Se está acercando al límite de contexto

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### El comando `/compact`
When your context is getting full but you don't want to lose the conversation, `/compact` summarizes your history to free up tokens:

```bash
copilot

> /compact
# Resume el historial de la conversación, liberando espacio de contexto
# Se preservan sus hallazgos y decisiones clave
```

You can also give `/compact` optional focus instructions to shape what gets prioritized in the summary:

```bash
copilot

> /compact focus on the list of bugs we found and decisions made
# Resume el historial, manteniendo la lista de errores y las decisiones en primer plano
```

> 💡 **Cuándo usar instrucciones de enfoque**: Si tu conversación abarcó muchos temas, las instrucciones de enfoque ayudan a que `/compact` conserve las partes más relevantes para tus próximos pasos, para que no pierdas el hilo.

#### Consejos de eficiencia del contexto

| Situation | Action | Why |
|-----------|--------|-----|
| Starting new topic | `/clear` | Removes irrelevant context |
| Went down wrong path | `/rewind` | Roll back to any earlier point |
| Long conversation | `/compact` | Summarizes history, frees tokens |
| Need specific file | `@file.py` not `@folder/` | Loads only what you need |
| Hitting limits | `/new` or `/clear` | Fresh context |
| Multiple topics | Use `/rename` per topic | Easy to resume right session |

#### Mejores prácticas para codebases grandes

1. **Be specific**: `@samples/book-app-project/books.py` instead of `@samples/book-app-project/`
2. **Clear context between topics**: Use `/new` or `/clear` when switching focus
3. **Use `/compact`**: Summarize conversation to free up context
4. **Use multiple sessions**: One session per feature or topic

</details>

<details>
<summary><strong>Eligiendo qué referenciar</strong></summary>
<a id="choosing-what-to-reference"></a>

### Eligiendo qué referenciar

No todos los archivos son iguales cuando se trata de contexto. Aquí tienes cómo elegir sabiamente:

#### Consideraciones sobre el tamaño de los archivos

| File Size | Approximate [Tokens](../GLOSSARY.md#token) | Strategy |
|-----------|-------------------|----------|
| Small (<100 lines) | ~500-1,500 tokens | Reference freely |
| Medium (100-500 lines) | ~1,500-7,500 tokens | Reference specific files |
| Large (500+ lines) | 7,500+ tokens | Be selective, use specific files |
| Very Large (1000+ lines) | 15,000+ tokens | Consider splitting or targeting sections |

**Ejemplos concretos:**
- The book app's 4 Python files combined ≈ 2,000-3,000 tokens
- A typical Python module (200 lines) ≈ 3,000 tokens
- A Flask API file (400 lines) ≈ 6,000 tokens
- Your package.json ≈ 200-500 tokens
- A short prompt + response ≈ 500-1,500 tokens

> 💡 **Estimación rápida para código:** Multiplica las líneas de código por ~15 para obtener una aproximación de tokens. Ten en cuenta que esto es solo una estimación.

#### Qué incluir vs. excluir

**Alto valor** (incluye estos):
- Entry points (`book_app.py`, `main.py`, `app.py`)
- The specific files you're asking about
- Files directly imported by your target file
- Configuration files (`requirements.txt`, `pyproject.toml`)
- Data models or dataclasses

**Menor valor** (considera excluir):
- Generated files (compiled output, bundled assets)
- Node modules or vendor directories
- Large data files or fixtures
- Files unrelated to your question

#### El espectro de especificidad

```
Less specific ────────────────────────► More specific
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ Scans everything                     └─ Just what you need
        (uses more context)                      (preserves context)
```

**Cuando ir amplio** (`@samples/book-app-project/`):
- Initial codebase exploration
- Finding patterns across many files
- Architecture reviews

**Cuando ser específico** (`@samples/book-app-project/books.py`):
- Debugging a particular issue
- Code review of a specific file
- Asking about a single function

#### Ejemplo práctico: Carga de contexto por etapas

```bash
copilot

# Paso 1: Comience con la estructura
> @package.json What frameworks does this project use?

# Paso 2: Reduzca según la respuesta
> @samples/book-app-project/ Show me the project structure

# Paso 3: Concéntrese en lo que importa
> @samples/book-app-project/books.py Review the BookCollection class

# Paso 4: Añada archivos relacionados solo cuando sea necesario
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

This staged approach keeps context focused and efficient.

</details>

<details>
<summary><strong>Trabajando con imágenes</strong></summary>
<a id="working-with-images"></a>

### Trabajando con imágenes

You can include images in your conversations using the `@` syntax, or simply **paste from your clipboard** (Cmd+V / Ctrl+V). Copilot CLI can analyze screenshots, mockups, and diagrams to help with UI debugging, design implementation, and error analysis.

```bash
copilot

> @assets/screenshot.png What is happening in this image?

> @assets/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **Más información**: See [Additional Context Features](../appendices/additional-context.md#trabajar-con-imágenes) for supported formats, practical use cases, and tips for combining images with code.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Configuración cálida de escritorio con monitor que muestra código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Es hora de aplicar tus habilidades de gestión de contexto y sesiones.

---

## ▶️ Pruébalo tú mismo

### Revisión completa del proyecto

The course includes sample files you can review directly. Start copilot and run the prompt shown next:

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI identificará problemas como:
# - Funciones de visualización duplicadas
# - Falta validación de entradas
# - Manejo inconsistente de errores
```

> 💡 **¿Quieres probar con tus propios archivos?** Create a small Python project (`mkdir -p my-project/src`), add some .py files, then use `@my-project/src/` to review them. You can ask copilot to create sample code for you if you'd like!

### Flujo de trabajo de sesión

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI suggests validation approach]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# Más tarde - retoma donde lo dejaste
copilot --continue

> Generate tests for the changes we made
```

---

After completing the demos, try these variations:

1. **Desafío entre archivos**: Analyze how book_app.py and books.py work together:
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **Desafío de sesión**: Start a session, name it with `/rename my-first-session`, work on something, exit with `/exit`, then run `copilot --continue`. Does it remember what you were doing?

3. **Desafío de contexto**: Run `/context` mid-session. How many tokens are you using? Try `/compact` and check again. (See [Understanding Context Windows](#compartir-tu-sesión) in Going Deeper for more on `/compact`.)

**Autoevaluación**: Entiendes el contexto cuando puedas explicar por qué `@folder/` es más poderoso que abrir cada archivo individualmente.

---

## 📝 Tarea

### Desafío principal: Rastrear el flujo de datos

Los ejemplos prácticos se centraron en revisiones de calidad de código y validación de entrada. Ahora practica las mismas habilidades de contexto con una tarea diferente: rastrear cómo se mueve la información a través de la app:

1. Start an interactive session: `copilot`
2. Reference `books.py` and `book_app.py` together:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. Bring in the data file for additional context:
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. Ask for a cross-file improvement:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. Rename the session: `/rename data-flow-analysis`
6. Exit with `/exit`, then resume with `copilot --continue` and ask a follow-up question about the data flow

**Criterios de éxito**: Puedes rastrear datos a través de múltiples archivos, reanudar una sesión nombrada y obtener sugerencias que abarquen varios archivos.

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

Then resume with: `copilot --continue`

**Comandos útiles:**
- `@file.py` - Reference a single file
- `@folder/` - Reference all files in a folder (note the trailing `/`)
- `/context` - Check how much context you're using
- `/rename <name>` - Name your session for easy resuming

</details>

### Desafío adicional: Límites de contexto

1. Reference all the book app files at once with `@samples/book-app-project/`
2. Ask several detailed questions about different files (`books.py`, `utils.py`, `book_app.py`, `data.json`)
3. Run `/context` to see usage. How quickly does it fill up?
4. Practice using `/compact` to reclaim space, then continue the conversation
5. Try being more specific with file references (e.g., `@samples/book-app-project/books.py` instead of the whole folder) and see how it affects context usage

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Forgetting `@` before filenames | Copilot CLI treats "books.py" as plain text | Use `@samples/book-app-project/books.py` to reference files |
| Expecting sessions to persist automatically | Starting `copilot` fresh loses all previous context | Use `--continue` (last session) or `--resume` (pick a session) |
| Referencing files outside current directory | "Permission denied" or "File not found" errors | Use `/add-dir /path/to/directory` to grant access |
| Not using `/clear` when switching topics | Old context confuses responses about the new topic | Run `/clear` before starting a different task |

### Solución de problemas

**"File not found" errors** - Make sure you're in the correct directory:

```bash
pwd  # Comprobar el directorio actual
ls   # Listar archivos

# Luego inicia Copilot y usa rutas relativas
copilot

> Review @samples/book-app-project/books.py
```

**"Permission denied"** - Add the directory to your allowed list:

```bash
copilot --add-dir /path/to/directory

# O en una sesión:
> /add-dir /path/to/directory
```

**Context fills up too quickly**:
- Be more specific with file references
- Use `/clear` between different topics
- Split work across multiple sessions

</details>

---

# Resumen

## 🔑 Puntos clave

1. **`@` syntax** gives Copilot CLI context about files, directories, and images
2. **Multi-turn conversations** build on each other as context accumulates
3. **Sessions auto-save**: name them at startup with `--name`, resume by name with `--resume=<name>`, or use `--continue` to pick up the most recent session
4. **Context windows** have limits: manage them with `/clear`, `/compact`, `/context`, `/new`, and `/rewind`. Use `/compact focus on <topic>` to shape what gets kept in the summary
5. **Persistent memory** (`/memory`) lets Copilot CLI remember preferences and facts across *all* sessions — not just the current one
6. **Permission flags** (`--add-dir`, `--allow-all`) control multi-directory access. Use them wisely!
7. **Image references** (`@screenshot.png`) help debug UI issues visually

> 📚 **Documentación oficial**: [Usar Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) for the complete reference on context, sessions, and working with files.

> 📋 **Referencia rápida**: See the [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) for a complete list of commands and shortcuts.

---

## ➡️ ¿Qué sigue?

Ahora que puedes proporcionar contexto a Copilot CLI, vamos a ponerlo a trabajar en tareas de desarrollo reales. Las técnicas de contexto que acabas de aprender (referencias de archivos, análisis entre archivos y gestión de sesiones) son la base para los flujos de trabajo potentes del próximo capítulo.

En **[Capítulo 03: Flujos de trabajo de desarrollo](../03-development-workflows/README.md)**, aprenderás:

- Code review workflows
- Refactoring patterns
- Debugging assistance
- Test generation
- Git integration

---

**[← Volver al Capítulo 01](../01-setup-and-first-steps/README.md)** | **[Continuar al Capítulo 03 →](../03-development-workflows/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->