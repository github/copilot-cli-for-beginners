<!--
---
id: CopilotCLI-02
title: !translate Contexto y conversaciones
description: !translate Usa el contexto de archivos y directorios, reanuda sesiones previas y escribe conversaciones multi-turno efectivas con GitHub Copilot CLI.
audience: Desarrolladores / Estudiantes / Usuarios de terminal
slug: context-and-conversations
weight: 3
---
-->

![Capítulo 02: Contexto y conversaciones](../../../02-context-conversations/assets/chapter-header.png)

> **¿Y si la IA pudiera ver todo tu código, no solo un archivo a la vez?**

En este capítulo, desbloquearás el verdadero poder de GitHub Copilot CLI: el contexto. Aprenderás a usar la sintaxis `@` para referenciar archivos y directorios, dando a Copilot CLI una comprensión profunda de tu base de código. Descubrirás cómo mantener conversaciones a través de sesiones, reanudar el trabajo días después exactamente donde lo dejaste, y verás cómo el análisis entre archivos detecta errores que las revisiones de un solo archivo pasan por alto por completo.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Usar la sintaxis `@` para referenciar archivos, directorios e imágenes
- Reanudar sesiones previas con `--resume` y `--continue`
- Entender cómo funcionan las [ventanas de contexto](../GLOSSARY.md#ventana-de-contexto)
- Escribir conversaciones multi-turno efectivas
- Gestionar permisos de directorio para flujos de trabajo multi-proyecto

> ⏱️ **Tiempo estimado**: ~50 minutos (20 min lectura + 30 min práctica)

---

## 🧩 Analogía del mundo real: Trabajar con un colega

<img src="../../../02-context-conversations/assets/colleague-context-analogy.png" alt="El contexto marca la diferencia: sin contexto vs con contexto" width="800"/>

*Al igual que tus colegas, Copilot CLI no es un lector de mentes. Proporcionar más información ayuda tanto a las personas como a Copilot a ofrecer un soporte más preciso.*

Imagina explicarle un error a un colega:

> **Sin contexto**: "La aplicación de libros no funciona."

> **Con contexto**: "Mira `books.py`, especialmente la función `find_book_by_title`. No está haciendo una comparación sin distinguir mayúsculas/minúsculas."

Para proporcionar contexto a Copilot CLI usa *la sintaxis `@`* para indicar a Copilot CLI archivos específicos.

---

# Esencial: Contexto básico

<img src="../../../02-context-conversations/assets/essential-basic-context.png" alt="Bloques de código brillantes conectados por rastros de luz que representan cómo fluye el contexto a través de las conversaciones de Copilot CLI" width="800"/>

Esta sección cubre todo lo que necesitas para trabajar eficazmente con el contexto. Domina estas bases primero.

---

## La sintaxis @

El símbolo `@` referencia archivos y directorios en tus indicaciones. Es la forma de decirle a Copilot CLI "mira este archivo".

> 💡 **Nota**: Todos los ejemplos en este curso usan la carpeta `samples/` incluida en este repositorio, así que puedes probar cada comando directamente.

### Pruébalo ahora (No se requiere configuración)

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

### Patrones básicos de @

| Patrón | Qué hace | Ejemplo |
|---------|--------------|-------------|
| `@file.py` | Referenciar un solo archivo | `Revisar @samples/book-app-project/books.py` |
| `@folder/` | Referenciar todos los archivos en un directorio | `Revisar @samples/book-app-project/` |
| `@file1.py @file2.py` | Referenciar múltiples archivos | `Comparar @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### Referenciar un solo archivo

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de contexto de archivo](../../../02-context-conversations/assets/file-context-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

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

Aquí es donde el contexto se convierte en un superpoder. El análisis de un solo archivo es útil. El análisis entre archivos es transformador.

<img src="../../../02-context-conversations/assets/cross-file-intelligence.png" alt="Inteligencia entre archivos: comparar análisis de un solo archivo frente a análisis entre archivos, mostrando cómo analizar archivos juntos revela errores, flujo de datos y patrones invisibles en aislamiento" width="800"/>

### Demostración: Encontrar errores que abarcan múltiples archivos

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

![Demostración multi-archivo](../../../02-context-conversations/assets/multi-file-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

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

**Por qué importa esto**: Una revisión de un solo archivo perdería la imagen completa. Solo el análisis entre archivos revela:
- **Código duplicado** que debería consolidarse
- **Patrones de flujo de datos** que muestran cómo interactúan los componentes
- **Problemas arquitectónicos** que afectan la mantenibilidad

---

### Demostración: Entender una base de código en 60 segundos

<img src="../../../02-context-conversations/assets/codebase-understanding.png" alt="Comparación en pantalla dividida mostrando revisión manual de código que toma 1 hora frente a análisis asistido por IA que toma 10 segundos" width="800" />

¿Nuevo en un proyecto? Aprende sobre él rápidamente usando Copilot CLI.

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**Qué obtienes**:
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

# Copilot CLI ahora tiene el contenido completo del archivo y puede dar retroalimentación específica:
# "Línea 49: La comparación con distinción de mayúsculas/minúsculas puede omitir libros..."
# "Línea 29: Se capturan errores de decodificación JSON, pero no se registra la corrupción de datos..."

> What about @samples/book-app-project/book_app.py?

# Ahora revisando book_app.py, pero aún consciente del contexto de books.py
```

### Ejemplo 2: Entender una base de código

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI lee books.py y comprende la clase BookCollection

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI escanea el directorio y hace un resumen

> How does the app save and load books?

# Copilot CLI puede rastrear el código que ya ha visto
```

<details>
<summary>🎬 ¡Mira una conversación de varios turnos en acción!</summary>

![Demostración multiturno](../../../02-context-conversations/assets/multi-turn-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

### Ejemplo 3: Refactorización en múltiples archivos

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI ve ambos archivos y puede sugerir cómo fusionar el código duplicado
```

---

## Gestión de sesiones

Las sesiones se guardan automáticamente mientras trabajas. Puedes reanudar sesiones previas para continuar donde las dejaste.

### Guardado automático de sesiones

Cada conversación se guarda automáticamente. Simplemente sal normalmente:

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
# Selecciona de una lista de sesiones de forma interactiva
copilot --resume

# -r es una abreviatura de --resume (¡ahorra algo de escritura!)
copilot -r

# O reanuda una sesión específica por su ID
copilot --resume=abc123

# O reanuda usando el nombre que le diste a la sesión
copilot --resume="my book app review"
```

> 💡 **¿Cómo encuentro un ID de sesión?** No necesitas memorizarlos. Ejecutar `copilot --resume` sin un ID muestra una lista interactiva de tus sesiones previas, sus nombres, IDs y cuándo estuvieron activas por última vez. Solo elige la que quieras.
>
> **¿Y qué pasa con múltiples terminales?** Cada ventana de terminal es su propia sesión con su propio contexto. Si tienes Copilot CLI abierto en tres terminales, son tres sesiones separadas. Ejecutar `--resume` desde cualquier terminal te permite explorar todas ellas. La opción `--continue` toma la sesión del directorio de trabajo actual primero; si no existe allí, elige la sesión más recientemente activa.
>
> **¿Puedo cambiar de sesión sin reiniciar?** Sí. Usa el comando con barra `/resume` desde dentro de una sesión activa:
> ```
> > /resume
> # Shows a list of sessions to switch to
> ```

### Organiza tus sesiones

Dale nombres significativos a las sesiones para que puedas encontrarlas después. Puedes nombrar una sesión al iniciarla, o renombrarla en cualquier momento mientras estés dentro de la sesión:

```bash
# Nombra una sesión justo cuando la inicias
copilot --name book-app-review

# O renombra la sesión actual desde dentro
copilot

> /rename book-app-review
# Sesión renombrada para facilitar la identificación
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
> /session delete-all        # Elimina todas las sesiones (¡úselo con precaución!)
```

### Memoria persistente entre sesiones

Las sesiones guardan el historial de conversación, pero la **memoria** va un paso más allá y permite que Copilot CLI recuerde preferencias y hechos *a través de todas las sesiones*, no solo dentro de una sola.

```bash
copilot

> /memory show
# Muestra lo que Copilot CLI recuerda actualmente sobre ti y tu proyecto

> /memory on
# Activa la memoria (activada por defecto si tu cuenta la admite)

> /memory off
# Desactiva la memoria (útil si prefieres empezar de cero cada vez)
```

Por ejemplo, si le dices a Copilot CLI "Siempre prefiero pytest para pruebas en Python", puede recordar esa preferencia y aplicarla automáticamente en sesiones futuras. Todo sin que tengas que repetirlo.

> 💡 **Memoria vs. sesiones**: Las sesiones guardan el historial de conversación para que puedas reanudar una tarea específica. La memoria guarda hechos reutilizables del repositorio y preferencias de usuario que Copilot puede aplicar en trabajos futuros. Piensa en las sesiones como cuadernos de tareas, y en la memoria como contexto reutilizable que Copilot puede llevar adelante.

### Verificar y administrar el contexto

A medida que agregas archivos y conversación, la [ventana de contexto](../GLOSSARY.md#ventana-de-contexto) de Copilot CLI se llena. Hay varios comandos disponibles para ayudarte a mantener el control:

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandona la sesión actual (no se guarda el historial) y comienza una conversación nueva

> /new
# Finaliza la sesión actual (guardándola en el historial para búsqueda y reanudación) y comienza una conversación nueva

> /rewind
# Abre un selector de línea de tiempo que te permite retroceder a un punto anterior de tu conversación
```

> 💡 **Cuándo usar `/clear` o `/new`**: Si has estado revisando books.py y quieres cambiar a discutir utils.py, ejecuta /new primero (o /clear si no necesitas el historial de la sesión). De lo contrario, el contexto antiguo del tema puede confundir las respuestas.

> 💡 **¿Cometiste un error o quieres probar un enfoque diferente?** Usa `/rewind` (o presiona Esc dos veces) para abrir un **selector de línea de tiempo** que te permite retroceder a cualquier punto anterior en tu conversación, no solo al más reciente. Esto es útil cuando tomaste el camino equivocado y quieres retroceder sin empezar completamente de nuevo.

---

### Retoma donde lo dejaste

<img src="../../../02-context-conversations/assets/session-persistence-timeline.png" alt="Cronología que muestra cómo las sesiones de GitHub Copilot CLI persisten a lo largo de los días: comienza el lunes, reanuda el miércoles con todo el contexto restaurado" width="800"/>

*Las sesiones se guardan automáticamente al salir. Reanuda días después con todo el contexto: archivos, problemas y progreso recordados.*

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
# Trabajar en la solución...

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

Issue #1 (funciones duplicadas) se solucionó el lunes.

> Let's tackle issue #2 next
```

**Lo que hace esto poderoso**: Días después, Copilot CLI recuerda:
- El archivo exacto en el que estabas trabajando
- La lista numerada de problemas
- Cuáles ya has resuelto
- El contexto de tu conversación

Sin reexplicaciones. Sin volver a leer archivos. Simplemente continúa trabajando.

---

**🎉 ¡Ahora conoces lo esencial!** La sintaxis `@`, la gestión de sesiones (`--name`/`--continue`/`--resume`/`/rename`) y los comandos de contexto (`/context`/`/clear`) son suficientes para ser muy productivo. Todo lo que sigue es opcional. Vuelve a ello cuando estés listo.

---

# Opcional: Profundizar

<img src="../../../02-context-conversations/assets/optional-going-deeper.png" alt="Cueva de cristal abstracta en tonos azules y morados que representa una exploración más profunda de conceptos de contexto" width="800"/>

Estos temas se basan en lo esencial anterior. **Elige lo que te interese, o salta a [Práctica](#el-espectro-de-especificidad).**

| Quiero aprender sobre... | Ir a |
|---|---|
| Patrones comodín y comandos avanzados de sesión | [Patrones @ adicionales y comandos de sesión](#verificar-y-administrar-el-contexto) |
| Construir sobre el contexto a través de múltiples indicaciones | [Conversaciones conscientes del contexto](#patrones-adicionales) |
| Límites de tokens y `/compact` | [Entendiendo las ventanas de contexto](#compartir-tu-sesión) |
| Cómo elegir los archivos correctos para referenciar | [Elegir qué referenciar](#el-comando-compact) |
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
# Exporta la sesión como un archivo HTML interactivo autónomo
# Útil para compartir informes de sesión pulidos con compañeros de equipo o guardarlos como referencia
```

</details>

<details>
<summary><strong>Conversaciones conscientes del contexto</strong></summary>
<a id="context-aware-conversations"></a>

### Conversaciones conscientes del contexto

La magia ocurre cuando tienes conversaciones de varios turnos que se construyen unas sobre otras.

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

Fíjate en cómo cada indicación se basa en el trabajo previo. Este es el poder del contexto.

</details>

<details>
<summary><strong>Entendiendo las ventanas de contexto</strong></summary>
<a id="understanding-context-windows"></a>

### Entendiendo las ventanas de contexto

Ya conoces `/context` y `/clear` de lo esencial. Aquí tienes una imagen más profunda de cómo funcionan las ventanas de contexto.

Cada IA tiene una "ventana de contexto", que es la cantidad de texto que puede considerar a la vez.

<img src="../../../02-context-conversations/assets/context-window-visualization.png" alt="Visualización de la ventana de contexto" width="800"/>

*La ventana de contexto es como un escritorio: solo puede sostener cierta cantidad a la vez. Los archivos, el historial de conversación y las indicaciones del sistema ocupan espacio.*

#### Qué sucede al llegar al límite

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# A medida que añades más archivos y conversaciones, esto crece

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Advertencia: Se está acercando al límite de contexto

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### El comando `/compact`


Cuando tu contexto se está llenando pero no quieres perder la conversación, `/compact` resume tu historial para liberar tokens:

```bash
copilot

> /compact
# Resume el historial de la conversación, liberando espacio de contexto
# Sus hallazgos y decisiones clave se preservan
```

También puedes darle a `/compact` instrucciones de enfoque opcionales para moldear qué se prioriza en el resumen:

```bash
copilot

> /compact focus on the list of bugs we found and decisions made
# Resume el historial, manteniendo la lista de errores y las decisiones en primer plano
```

> 💡 **Cuándo usar instrucciones de enfoque**: Si tu conversación abarcó muchos temas, las instrucciones de enfoque ayudan a `/compact` a conservar las partes más relevantes para tus próximos pasos para que no pierdas el hilo.

#### Consejos para la eficiencia del contexto

| Situación | Acción | Por qué |
|-----------|--------|-----|
| Comenzar un nuevo tema | `/clear` | Elimina el contexto irrelevante |
| Seguir por un camino equivocado | `/rewind` | Retrocede a cualquier punto anterior |
| Conversación larga | `/compact` | Resume el historial, libera tokens |
| Necesitas un archivo específico | `@file.py` no `@folder/` | Carga solo lo que necesitas |
| Alcanzando límites | `/new` o `/clear` | Contexto nuevo |
| Varios temas | Usa `/rename` por tema | Fácil reanudar la sesión correcta |

#### Mejores prácticas para grandes bases de código

1. **Sé específico**: `@samples/book-app-project/books.py` en lugar de `@samples/book-app-project/`
2. **Limpia el contexto entre temas**: Usa `/new` o `/clear` al cambiar de enfoque
3. **Usa `/compact`**: Resume la conversación para liberar contexto
4. **Usa múltiples sesiones**: Una sesión por característica o tema

</details>

<details>
<summary><strong>Elegir qué referenciar</strong></summary>
<a id="choosing-what-to-reference"></a>

### Elegir qué referenciar

No todos los archivos son iguales cuando se trata de contexto. Aquí tienes cómo elegir sabiamente:

#### Consideraciones sobre el tamaño de archivo

| Tamaño de archivo | Aproximado [Tokens](../GLOSSARY.md#token) | Estrategia |
|-----------|-------------------|----------|
| Pequeño (<100 líneas) | ~500-1,500 tokens | Referéncialos libremente |
| Mediano (100-500 líneas) | ~1,500-7,500 tokens | Referencia archivos específicos |
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

**Alto valor** (incluye estos):
- Puntos de entrada (`book_app.py`, `main.py`, `app.py`)
- Los archivos específicos sobre los que preguntas
- Archivos importados directamente por tu archivo objetivo
- Archivos de configuración (`requirements.txt`, `pyproject.toml`)
- Modelos de datos o dataclasses

**Menor valor** (considera excluir):
- Archivos generados (salida compilada, assets empaquetados)
- Node modules o directorios vendor
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

**Cuándo optar por un enfoque amplio** (`@samples/book-app-project/`):
- Exploración inicial del código
- Encontrar patrones en muchos archivos
- Revisiones de arquitectura

**Cuándo optar por un enfoque específico** (`@samples/book-app-project/books.py`):
- Depurar un problema en particular
- Revisión de código de un archivo específico
- Preguntar sobre una sola función

#### Ejemplo práctico: Carga de contexto por etapas

```bash
copilot

# Paso 1: Comience con la estructura
> @package.json What frameworks does this project use?

# Paso 2: Reduzca en función de la respuesta
> @samples/book-app-project/ Show me the project structure

# Paso 3: Concéntrese en lo que importa
> @samples/book-app-project/books.py Review the BookCollection class

# Paso 4: Agregue archivos relacionados solo cuando sea necesario
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

Este enfoque por etapas mantiene el contexto enfocado y eficiente.

</details>

<details>
<summary><strong>Trabajar con imágenes</strong></summary>
<a id="working-with-images"></a>

### Trabajar con imágenes

Puedes incluir imágenes en tus conversaciones usando la sintaxis `@`, o simplemente **pegar desde el portapapeles** (Cmd+V / Ctrl+V). Copilot CLI puede analizar capturas de pantalla, maquetas y diagramas para ayudar con la depuración de UI, la implementación de diseño y el análisis de errores.

```bash
copilot

> @assets/screenshot.png What is happening in this image?

> @assets/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **Saber más**: Consulta [Funciones de contexto adicionales](../appendices/additional-context.md#trabajar-con-imágenes) para formatos compatibles, casos de uso prácticos y consejos para combinar imágenes con código.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Es hora de aplicar tus habilidades de gestión de contexto y sesiones.

---

## ▶️ Pruébalo tú mismo

### Revisión completa del proyecto

El curso incluye archivos de ejemplo que puedes revisar directamente. Inicia copilot y ejecuta el prompt que se muestra a continuación:

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI identificará problemas como:
# - Funciones de visualización duplicadas
# - Falta de validación de entradas
# - Manejo de errores inconsistente
```

> 💡 **¿Quieres probar con tus propios archivos?** Crea un pequeño proyecto Python (`mkdir -p my-project/src`), agrega algunos archivos .py y luego usa `@my-project/src/` para revisarlos. ¡Puedes pedirle a copilot que cree código de ejemplo si quieres!

### Flujo de trabajo de la sesión

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI suggests validation approach]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# Más tarde - continúa donde lo dejaste
copilot --continue

> Generate tests for the changes we made
```

---

Después de completar las demostraciones, prueba estas variaciones:

1. **Desafío entre archivos**: Analiza cómo funcionan book_app.py y books.py juntos:
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **Desafío de sesión**: Inicia una sesión, nómbrala con `/rename my-first-session`, trabaja en algo, sal con `/exit`, luego ejecuta `copilot --continue`. ¿Recuerda qué estabas haciendo?

3. **Desafío de contexto**: Ejecuta `/context` a mitad de sesión. ¿Cuántos tokens estás usando? Prueba `/compact` y verifica de nuevo. (Consulta [Comprender las ventanas de contexto](#compartir-tu-sesión) en Going Deeper para más información sobre `/compact`.)

**Autoevaluación**: Entiendes el contexto cuando puedes explicar por qué `@folder/` es más potente que abrir cada archivo individualmente.

---

## 📝 Tarea

### Desafío principal: Trazar el flujo de datos

Los ejemplos prácticos se centraron en revisiones de calidad de código y validación de entradas. Ahora practica las mismas habilidades de contexto en una tarea diferente, trazando cómo se mueve la información a través de la app:

1. Inicia una sesión interactiva: `copilot`
2. Referencia `books.py` y `book_app.py` juntos:
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Traza cómo un libro pasa de la entrada del usuario a guardarse en data.json. ¿Qué funciones participan en cada paso?`
3. Trae el archivo de datos para contexto adicional:
   `@samples/book-app-project/data.json ¿Qué sucede si este archivo JSON falta o está corrupto? ¿Qué funciones fallarían?`
4. Solicita una mejora entre archivos:
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Sugiere una estrategia coherente de manejo de errores que funcione en ambos archivos.`
5. Renombra la sesión: `/rename data-flow-analysis`
6. Sal con `/exit`, luego reanuda con `copilot --continue` y haz una pregunta de seguimiento sobre el flujo de datos

**Criterios de éxito**: Puedes trazar datos a través de múltiples archivos, reanudar una sesión con nombre y obtener sugerencias entre archivos.

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
- `@file.py` - Referencia un solo archivo
- `@folder/` - Referencia todos los archivos en una carpeta (nota la barra final `/`)
- `/context` - Comprueba cuánto contexto estás usando
- `/rename <name>` - Nombra tu sesión para reanudarla fácilmente

</details>

### Desafío extra: Límites de contexto

1. Referencia todos los archivos de la app de libros a la vez con `@samples/book-app-project/`
2. Haz varias preguntas detalladas sobre diferentes archivos (`books.py`, `utils.py`, `book_app.py`, `data.json`)
3. Ejecuta `/context` para ver el uso. ¿Qué tan rápido se llena?
4. Practica usar `/compact` para recuperar espacio, luego continúa la conversación
5. Intenta ser más específico con las referencias de archivos (p. ej., `@samples/book-app-project/books.py` en lugar de toda la carpeta) y observa cómo afecta el uso del contexto

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué sucede | Solución |
|---------|--------------|-----|
| Olvidar `@` antes de los nombres de archivo | Copilot CLI trata "books.py" como texto sin formato | Usa `@samples/book-app-project/books.py` para referenciar archivos |
| Esperar que las sesiones persistan automáticamente | Iniciar `copilot` desde cero pierde todo el contexto anterior | Usa `--continue` (última sesión) o `--resume` (elegir una sesión) |
| Referenciar archivos fuera del directorio actual | Errores de "Permission denied" o "File not found" | Usa `/add-dir /path/to/directory` para conceder acceso |
| No usar `/clear` al cambiar de tema | El contexto antiguo confunde las respuestas sobre el nuevo tema | Ejecuta `/clear` antes de comenzar una tarea diferente |

### Solución de problemas

**"File not found" errors** - Asegúrate de que estás en el directorio correcto:

```bash
pwd  # Comprobar el directorio actual
ls   # Listar archivos

# Luego inicia copilot y usa rutas relativas
copilot

> Review @samples/book-app-project/books.py
```

**"Permission denied"** - Añade el directorio a tu lista permitida:

```bash
copilot --add-dir /path/to/directory

# O en una sesión:
> /add-dir /path/to/directory
```

**El contexto se llena demasiado rápido**:
- Sé más específico con las referencias de archivos
- Usa `/clear` entre diferentes temas
- Divide el trabajo entre múltiples sesiones

</details>

---

# Resumen

## 🔑 Puntos clave

1. **La sintaxis `@`** le da a Copilot CLI contexto sobre archivos, directorios e imágenes
2. **Las conversaciones de múltiples turnos** se construyen unas sobre otras a medida que el contexto se acumula
3. **Las sesiones se guardan automáticamente**: nómbralas al iniciar con `--name`, reanúdalas por nombre con `--resume=<name>`, o usa `--continue` para retomar la sesión más reciente
4. **Las ventanas de contexto** tienen límites: adminístralas con `/clear`, `/compact`, `/context`, `/new` y `/rewind`. Usa `/compact focus on <topic>` para orientar lo que se mantiene en el resumen
5. **Memoria persistente** (`/memory`) permite que Copilot CLI recuerde preferencias y hechos a través de *todas* las sesiones — no solo la actual
6. **Banderas de permiso** (`--add-dir`, `--allow-all`) controlan el acceso a múltiples directorios. ¡Úsalas con prudencia!
7. **Referencias de imágenes** (`@screenshot.png`) ayudan a depurar problemas de UI visualmente

> 📚 **Documentación oficial**: [Usa Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) para la referencia completa sobre contexto, sesiones y trabajo con archivos.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para la lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Ahora que puedes darle contexto a Copilot CLI, pongámoslo a trabajar en tareas de desarrollo reales. Las técnicas de contexto que acabas de aprender (referencias de archivos, análisis entre archivos y gestión de sesiones) son la base para los poderosos flujos de trabajo del siguiente capítulo.

En **[Capítulo 03: Flujos de trabajo de desarrollo](../03-development-workflows/README.md)**, aprenderás:

- Flujos de trabajo de revisión de código
- Patrones de refactorización
- Asistencia para depuración
- Generación de tests
- Integración con Git

---

**[← Volver al Capítulo 01](../01-setup-and-first-steps/README.md)** | **[Continuar al Capítulo 03 →](../03-development-workflows/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->