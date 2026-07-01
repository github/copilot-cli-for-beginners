<!--
---
id: CopilotCLI-01
title: !translate First Steps
description: !translate Experience GitHub Copilot CLI through hands-on demos, then learn when to use interactive, plan, and programmatic modes.
audience: Developers / Students / Terminal users
slug: first-steps
weight: 2
---
-->

![Capítulo 01: Primeros pasos](../../../01-setup-and-first-steps/assets/chapter-header.png)

> **Mira cómo la IA encuentra errores al instante, explica código confuso y genera scripts funcionales. Luego aprende tres formas diferentes de usar GitHub Copilot CLI.**

¡Este capítulo es donde empieza la magia! Experimentarás de primera mano por qué los desarrolladores describen GitHub Copilot CLI como tener a un ingeniero senior a un toque de distancia. Verás a la IA encontrar errores de seguridad en segundos, obtener explicaciones de código complejo en un inglés sencillo y generar scripts funcionales al instante. Luego dominarás los tres modos de interacción (Interactive, Plan y Programmatic) para saber exactamente cuál usar en cada tarea.

> ⚠️ **Requisitos previos**: Asegúrate de haber completado **[Capítulo 00: Inicio rápido](../00-quick-start/README.md)** primero. Necesitarás tener GitHub Copilot CLI instalado y autenticado antes de ejecutar los demos a continuación.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, serás capaz de:

- Experimentar el impulso de productividad que GitHub Copilot CLI ofrece mediante demostraciones prácticas
- Elegir el modo correcto (Interactive, Plan o Programmatic) para cualquier tarea
- Usar comandos slash para controlar tus sesiones

> ⏱️ **Tiempo estimado**: ~45 minutos (15 min lectura + 30 min práctica)

---

# Tu primera experiencia con Copilot CLI

<img src="../../../01-setup-and-first-steps/assets/first-copilot-experience.png" alt="Desarrollador sentado en un escritorio con código en el monitor y partículas brillantes que representan la asistencia de IA" width="800"/>

Sumérgete y descubre lo que Copilot CLI puede hacer.

---

## Familiarízate: Tus primeros prompts

Antes de sumergirnos en las demostraciones impresionantes, empecemos con algunas indicaciones simples que puedes probar ahora mismo. **No se necesita un repositorio de código**. Solo abre una terminal y inicia Copilot CLI:

```bash
copilot
```

Prueba estas indicaciones para principiantes:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

¿No usas Python? ¡No hay problema! Simplemente haz preguntas sobre el lenguaje que prefieras.

Fíjate en lo natural que se siente. Haz preguntas como lo harías con un colega. Cuando termines de explorar, escribe `/exit` para salir de la sesión.

**La idea clave**: GitHub Copilot CLI es conversacional. No necesitas sintaxis especial para comenzar. Simplemente haz preguntas en un inglés sencillo.

## Verlo en acción

Ahora veamos por qué los desarrolladores describen esto como "tener a un ingeniero senior en marcación rápida".

> 📖 **Lectura de los ejemplos**: Las líneas que comienzan con `>` son indicaciones que escribes dentro de una sesión interactiva de Copilot CLI. Las líneas sin el prefijo `>` son comandos de shell que ejecutas en tu terminal.

> 💡 **Sobre las salidas de ejemplo**: Las salidas de muestra mostradas a lo largo de este curso son ilustrativas. Debido a que las respuestas de Copilot CLI varían cada vez, tus resultados diferirán en redacción, formato y detalle. Concéntrate en el *tipo* de información devuelta, no en el texto exacto.

### Demo 1: Revisión de código en segundos

El curso incluye archivos de ejemplo con problemas intencionales de calidad de código. Si estás trabajando en tu máquina local y aún no has clonado el repo, ejecuta el comando `git clone` que aparece más abajo, navega a la carpeta `copilot-cli-for-beginners` y luego ejecuta el comando `copilot`.

```bash
# Clona el repositorio del curso si estás trabajando localmente y aún no lo has hecho
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Inicia Copilot
copilot
```

Una vez dentro de la sesión interactiva de Copilot CLI, ejecuta lo siguiente:

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **¿Para qué se usa el símbolo `@`?** El símbolo `@` indica a Copilot CLI que lea un archivo. Aprenderás todo sobre esto en el Capítulo 02. Por ahora, simplemente copia el comando exactamente como se muestra.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de revisión de código](../../../01-setup-and-first-steps/assets/code-review-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**La conclusión**: Una revisión de código profesional en segundos. La revisión manual tomaría... bueno... mucho más tiempo que eso!

---

### Demo 2: Explicar código confuso

¿Alguna vez te has quedado mirando código preguntándote qué hace? Prueba esto en tu sesión de Copilot CLI:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de explicación de código](../../../01-setup-and-first-steps/assets/explain-code-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Qué ocurre**: (tu salida diferirá) Copilot CLI lee el archivo, entiende el código y lo explica en un inglés sencillo.

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**La conclusión**: Código complejo explicado como lo haría un mentor paciente.

---

### Demo 3: Generar código funcional

¿Necesitas una función para la que de otro modo perderías 15 minutos buscando en Google? Aún en tu sesión:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de generación de código](../../../01-setup-and-first-steps/assets/generate-code-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Qué ocurre**: Una función completa y funcional en segundos que puedes copiar, pegar y ejecutar.

Cuando termines de explorar, sal de la sesión:

```
> /exit
```

**La conclusión**: Gratificación instantánea, y te mantuviste en una única sesión continua todo el tiempo.

---

# Modos y comandos

<img src="../../../01-setup-and-first-steps/assets/modes-and-commands.png" alt="Panel de control futurista con pantallas brillantes, diales y ecualizadores que representan los modos y comandos de Copilot CLI" width="800"/>

Acabas de ver lo que Copilot CLI puede hacer. Ahora entendamos *cómo* usar estas capacidades de forma efectiva. La clave es saber cuál de los tres modos de interacción usar según la situación.

> 💡 **Nota**: Copilot CLI también tiene un modo **Autopilot** donde trabaja en las tareas sin esperar tu entrada. Es potente pero requiere otorgar permisos completos y usa solicitudes premium de forma autónoma. Este curso se centra en los tres modos que aparecen abajo. Te indicaremos Autopilot una vez que te sientas cómodo con lo básico.

---

## 🧩 Analogía del mundo real: Comer fuera

Piensa en usar GitHub Copilot CLI como salir a comer. Desde planificar el trayecto hasta hacer el pedido, diferentes situaciones requieren enfoques distintos:

| Modo | Analogía | Cuándo usarlo |
|------|----------------|-------------|
| **Plan** | Ruta GPS al restaurante | Tareas complejas: traza la ruta, revisa paradas, acuerda el plan y luego conduce |
| **Interactive** | Hablar con el camarero | Exploración e iteración: haz preguntas, personaliza, obtén retroalimentación en tiempo real |
| **Programmatic** | Pedido en el autoservicio (drive-through) | Tareas rápidas y específicas: permanece en tu entorno, obtén un resultado rápido |

Al igual que al salir a comer, aprenderás de forma natural cuándo cada enfoque es el adecuado.

<img src="../../../01-setup-and-first-steps/assets/ordering-food-analogy.png" alt="Tres formas de usar GitHub Copilot CLI - Plan Mode (ruta GPS al restaurante), Interactive Mode (hablar con el camarero), Programmatic Mode (autoservicio)" width="800"/>

*Elige tu modo según la tarea: Plan para trazarla primero, Interactive para colaboración de ida y vuelta, Programmatic para resultados rápidos de una sola ejecución*

### ¿Con qué modo debería empezar?

**Empieza con Interactive mode.**
- Puedes experimentar y hacer preguntas de seguimiento
- El contexto se construye de forma natural a través de la conversación
- Los errores son fáciles de corregir con `/clear`

Una vez que te sientas cómodo, prueba:
- **Programmatic mode** (`copilot -p "<your prompt>"`) para preguntas rápidas y puntuales
- **Plan mode** (`/plan`) cuando necesites planificar en más detalle antes de codificar

---

## Los tres modos

### Modo 1: Interactive Mode (empieza aquí)

<img src="../../../01-setup-and-first-steps/assets/interactive-mode.png" alt="Interactive Mode - Como hablar con un camarero que puede responder preguntas y ajustar el pedido" width="250"/>

**Mejor para**: Exploración, iteración, conversaciones multi-turn. Como hablar con un camarero que puede responder preguntas, recibir feedback y ajustar el pedido sobre la marcha.

Inicia una sesión interactiva:

```bash
copilot
```

Como has visto hasta este punto, verás un prompt donde puedes escribir de forma natural. Para obtener ayuda sobre los comandos disponibles, simplemente escribe:

```
> /help
```

**Idea clave**: Interactive mode mantiene el contexto. Cada mensaje se construye sobre los anteriores, igual que en una conversación real.

#### Ejemplo de Interactive Mode

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Fíjate en cómo cada indicación se construye sobre la respuesta anterior. Estás teniendo una conversación, no empezando de nuevo cada vez.

---

### Modo 2: Plan Mode

<img src="../../../01-setup-and-first-steps/assets/plan-mode.png" alt="Plan Mode - Como planificar una ruta antes de un viaje usando GPS" width="250"/>

**Mejor para**: Tareas complejas donde quieres revisar el enfoque antes de ejecutarlo. Similar a planificar una ruta antes de un viaje usando GPS.

Plan mode te ayuda a crear un plan paso a paso antes de escribir cualquier código. Usa el comando `/plan`, presiona **Shift+Tab** para cambiar a Plan Mode:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Tip**: **Shift+Tab** alterna entre modos: Interactive → Plan → Autopilot. Púlsalo en cualquier momento durante una sesión interactiva para cambiar de modo sin escribir un comando.

También puedes iniciar Copilot CLI directamente en plan mode usando el flag `--plan`:

```bash
copilot --plan
```

**Salida de Plan mode:** (tu salida puede diferir)

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**Idea clave**: Plan mode te permite revisar y modificar el enfoque antes de que se escriba código. Una vez que un plan está completo, incluso puedes indicar a Copilot CLI que lo guarde en un archivo para referencia posterior. Por ejemplo, "Save this plan to `mark_as_read_plan.md`" crearía un archivo markdown con los detalles del plan.

> 💡 **¿Quieres algo más complejo?** Prueba: `/plan Add search and filter capabilities to the book app`. Plan mode escala desde características simples hasta aplicaciones completas.

> 📚 **Autopilot mode**: Puede que hayas notado que Shift+Tab alterna por un tercer modo llamado **Autopilot**. En autopilot mode, Copilot trabaja todo un plan sin esperar tu entrada después de cada paso — como encargar una tarea a un colega y decir "avísame cuando hayas acabado". El flujo típico es plan → accept → autopilot, lo que significa que necesitas saber escribir buenos planes primero. También puedes iniciar directamente en autopilot con `copilot --autopilot`. Familiarízate con Interactive y Plan modes primero, y luego consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) cuando estés listo.

---

### Modo 3: Programmatic Mode

<img src="../../../01-setup-and-first-steps/assets/programmatic-mode.png" alt="Programmatic Mode - Como usar un drive-through para un pedido rápido" width="250"/>

**Mejor para**: Automatización, scripts, CI/CD, comandos de una sola ejecución. Como usar un drive-through para un pedido rápido sin necesidad de hablar con un camarero.

Usa el flag `-p` para comandos puntuales que no requieren interacción:

```bash
# Generar código
copilot -p "Write a function that checks if a number is even or odd"

# Obtener ayuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Idea clave**: Programmatic mode te da una respuesta rápida y sale. No hay conversación, solo entrada → salida.

<details>
<summary>📚 <strong>Ir más allá: Uso de Programmatic Mode en scripts</strong> (haz clic para expandir)</summary>

Una vez que te sientas cómodo, puedes usar `-p` en scripts de shell:

```bash
#!/bin/bash

# Generar mensajes de commit automáticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar un archivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Acerca de `--allow-all`**: Esta opción omite todas las solicitudes de permisos, permitiendo que Copilot CLI lea archivos, ejecute comandos y acceda a URLs sin preguntar primero. Esto es necesario para el modo programmatic (`-p`) ya que no hay una sesión interactiva para aprobar acciones. Usa `--allow-all` solo con prompts que hayas escrito tú y en directorios de confianza. Nunca lo uses con entradas no confiables o en directorios sensibles.

</details>

---

## Comandos slash esenciales

Estos comandos son buenos para aprender inicialmente mientras empiezas con Copilot CLI:

| Comando | Qué hace | Cuándo usarlo |
|---------|--------------|-------------|
| `/ask` | Haz una pregunta rápida sin que afecte el historial de la conversación | Cuando quieres una respuesta rápida sin desviar tu tarea actual |
| `/clear` | Borra la conversación y empieza de nuevo | Al cambiar de tema |
| `/help` | Muestra todos los comandos disponibles | Cuando olvides un comando |
| `/model` | Mostrar o cambiar el modelo de IA | Cuando quieras cambiar el modelo de IA |
| `/plan` | Planifica tu trabajo antes de codificar | Para funciones más complejas |
| `/research` | Investigación profunda usando GitHub y fuentes web | Cuando necesites investigar un tema antes de codificar |
| `/exit` | Finalizar la sesión | Cuando hayas terminado |

> 💡 **`/ask` vs chat normal**: Normalmente cada mensaje que envías forma parte de la conversación en curso y afecta las respuestas futuras. `/ask` es un atajo "off the record" — perfecto para preguntas puntuales como `/ask What does YAML mean?` sin contaminar el contexto de tu sesión.
> 💡 **Autocompletado con Tab**: Al escribir un comando con barra, presiona **Tab** para autocompletar el nombre del comando o para recorrer los subcomandos y argumentos disponibles. Esto es especialmente útil cuando no recuerdas el nombre exacto de un comando.

¡Eso es todo para empezar! A medida que te sientas más cómodo, puedes explorar comandos adicionales.

> 📚 **Documentación oficial**: [Referencia de comandos de la CLI](https://docs.github.com/copilot/reference/cli-command-reference) para la lista completa de comandos y opciones.

<details>
<summary>📚 <strong>Comandos adicionales</strong> (haz clic para expandir)</summary>

> 💡 Los comandos esenciales anteriores cubren gran parte de lo que harás en el uso diario. Esta referencia está aquí para cuando estés listo para explorar más.

### Entorno del agente

| Command | What It Does |
|---------|--------------|
| `/agent` | Browse and select from available agents |
| `/env` | Show loaded environment details — what instructions, MCP servers, skills, agents, and plugins are active |
| `/init` | Initialize Copilot instructions for your repository |
| `/mcp` | Manage MCP server configuration |
| `/settings` | Open an interactive dialog to browse and edit all user settings in one place |
| `/skills` | Manage skills for enhanced capabilities |

> 💡 Los agentes se tratan en [Capítulo 04](../04-agents-custom-instructions/README.md), las skills se tratan en [Capítulo 05](../05-skills/README.md), y los servidores MCP se tratan en [Capítulo 06](../06-mcp-servers/README.md).

### Modelos y subagentes

| Command | What It Does |
|---------|--------------|
| `/delegate` | Hand off task to GitHub Copilot cloud agent |
| `/fleet` | Split a complex task into parallel subtasks for faster completion |
| `/model` | Show or switch AI model |
| `/tasks` | View background subagents and detached shell sessions |

### Código

| Command | What It Does |
|---------|--------------|
| `/diff` | Review the changes made in the current directory |
| `/pr` | Operate on pull requests for the current branch |
| `/research` | Run deep research investigation using GitHub and web sources |
| `/review` | Run the code-review agent to analyze changes |
| `/terminal-setup` | Enable multiline input support (shift+enter and ctrl+enter) |

### Permisos

| Command | What It Does |
|---------|--------------|
| `/add-dir <directory>` | Add a directory to allowed list |
| `/allow-all [on\|off\|show]` | Auto-approve all permission prompts; use `on` to enable, `off` to disable, `show` to check current status |
| `/yolo` | Quick alias for `/allow-all on` — auto-approves all permission prompts. |
| `/cwd`, `/cd [directory]` | View or change working directory |
| `/list-dirs` | Show all allowed directories |

> ⚠️ **Usar con precaución**: `/allow-all` y `/yolo` omiten las solicitudes de confirmación. Genial para proyectos de confianza, pero ten cuidado con código no confiable.

### Sesión

| Command | What It Does |
|---------|--------------|
| `/clear` | Abandons the current session (no history saved) and starts a fresh conversation |
| `/compact` | Summarize conversation to reduce context usage (optionally add focus instructions, e.g. `/compact focus on the bug list`) |
| `/context` | Show context window token usage and visualization |
| `/keep-alive` | Prevent your system from sleeping while Copilot CLI is active — handy for long-running tasks on a laptop |
| `/memory [on\|off\|show]` | Enable, disable, or view persistent memory — facts and preferences remembered across all sessions |
| `/new` | Ends the current session (saving it to history for search/resume) and starts a fresh conversation. |
| `/resume` | Switch to a different session (optionally specify session ID or name) |
| `/rename` | Rename the current session (omit the name to auto-generate one) |
| `/rewind` | Open a timeline picker to roll back to any earlier point in the conversation |
| `/usage` | Display session usage metrics and statistics, including quota progress bars |
| `/session` | Show session info and workspace summary; use `/session delete`, `/session delete <id>`, or `/session delete-all` to remove sessions |
| `/share` | Export session as a markdown file, GitHub gist, or self-contained HTML file |
| `/every <interval> <prompt>` | Schedule a prompt to run on a recurring interval (e.g., `/every 1h summarize new commits`). Use natural language for the interval. `/loop` is an alias for `/every`. |
| `/after <time> <prompt>` | Schedule a prompt to run once after a delay (e.g., `/after 30m run tests`). Use natural language for the time. |

### Visualización

| Command | What It Does |
|---------|--------------|
| `/statusline` (or `/footer`) | Customize which items appear in the status bar at the bottom of the session (directory, branch, effort, context window, quota) |
| `/theme` | View or set terminal theme |
| `/voice` | Dictate your prompt using local speech-to-text — speak naturally instead of typing |

### Ayuda y comentarios

| Command | What It Does |
|---------|--------------|
| `/app` | Open the GitHub app (or browser fallback) directly from the CLI |
| `/changelog` | Display changelog for CLI versions |
| `/feedback` | Submit feedback to GitHub |
| `/help` | Show all available commands |

### Comandos rápidos de shell

Run shell commands directly without AI by prefixing with `!`:

```bash
copilot

> !git status
# Ejecuta git status directamente, evitando la IA

> !python -m pytest tests/
# Ejecuta pytest directamente
```

### Cambio de modelos

Copilot CLI admite múltiples modelos de IA de OpenAI, Anthropic, Google y otros. Los modelos disponibles para ti dependen de tu nivel de suscripción y región. Usa `/model` para ver tus opciones y cambiar entre ellos:

```bash
copilot
> /model

# Muestra los modelos disponibles y te permite elegir uno. Selecciona Sonnet 4.5.
```

> 💡 **Consejo**: Algunos modelos consumen más "solicitudes premium" que otros. Los modelos marcados **1x** (como Claude Sonnet 4.5) son una gran opción por defecto. Son capaces y eficientes. Los modelos con multiplicadores más altos usan tu cuota de solicitudes premium más rápido, así que guárdalos para cuando realmente los necesites.

> 💡 **¿No sabes qué modelo elegir?** Selecciona **`Auto`** desde el selector de modelos para dejar que Copilot elija automáticamente el mejor modelo disponible para cada sesión. Es una excelente opción por defecto si recién empiezas y no quieres preocuparte por la selección de modelos.

> 💡 **Atajos por familia de modelos**: También puedes escribir un alias corto de familia —como `opus`, `sonnet`, `haiku`, `gpt`, o `gemini`— directamente en el selector de `/model` en lugar de desplazarte por la lista completa. Copilot escogerá el mejor modelo disponible de esa familia para ti.

</details>

---

# Practice

<img src="../../../assets/practice.png" alt="Configuración cálida de escritorio con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica práctica" width="800"/>

Es hora de poner en práctica lo que has aprendido.

---

## ▶️ Pruébalo tú mismo

### Exploración interactiva

Inicia Copilot y usa indicaciones de seguimiento para mejorar iterativamente la aplicación de libros:

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### Planifica una función

Usa `/plan` para que Copilot CLI trace una implementación antes de escribir cualquier código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revisar el plan
# Aprobar o modificar
# Vigilar su implementación paso a paso
```

### Automatiza con el modo programático

El indicador `-p` te permite ejecutar Copilot CLI directamente desde tu terminal sin entrar en modo interactivo. Copia y pega el siguiente script en tu terminal (no dentro de Copilot) desde la raíz del repositorio para revisar todos los archivos Python en la app de libros.

```bash
# Revisar todos los archivos Python en la aplicación book
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# Revisar todos los archivos Python en la aplicación del libro
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

Después de completar las demostraciones, prueba estas variaciones:

1. **Desafío interactivo**: Inicia `copilot` y explora la app de libros. Pregunta por `@samples/book-app-project/books.py` y solicita mejoras 3 veces seguidas.

2. **Desafío en modo Plan**: Ejecuta `/plan Add rating and review features to the book app`. Lee el plan con detenimiento. ¿Tiene sentido?

3. **Desafío programático**: Ejecuta `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. ¿Funcionó en el primer intento?

---

## 💡 Consejo: Controla tu sesión CLI desde la web o el móvil

GitHub Copilot CLI admite **sesiones remotas**, lo que te permite monitorear e interactuar con una sesión CLI en ejecución desde un navegador web (en escritorio o móvil) o la app GitHub Mobile sin estar físicamente en tu terminal.

Inicia una sesión remota con la bandera `--remote`:

```bash
copilot --remote
```

Copilot CLI mostrará un enlace y proporcionará acceso a un código QR. Abre el enlace en tu teléfono o en una pestaña del navegador del escritorio para ver la sesión en tiempo real, enviar indicaciones de seguimiento, revisar planes y dirigir al agente de forma remota. Las sesiones son específicas del usuario, por lo que solo puedes acceder a tus propias sesiones de Copilot CLI.

También puedes habilitar el acceso remoto desde dentro de una sesión activa en cualquier momento:

```
> /remote
```

Detalles adicionales sobre sesiones remotas se pueden encontrar en la [documentación de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Tarea

### Reto principal: Mejora las utilidades de la app de libros

Los ejemplos prácticos se centraron en revisar y refactorizar `book_app.py`. Ahora practica las mismas habilidades en un archivo diferente, `utils.py`:

1. Inicia una sesión interactiva: `copilot`
2. Pide a Copilot CLI que resuma el archivo: "Summarize @samples/book-app-project/utils.py and explain what each function in this file does"
3. Pídele que añada validación de entrada: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. Pídele que mejore el manejo de errores: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. Pídele una docstring: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. Observa cómo el contexto se conserva entre las indicaciones. Cada mejora se basa en la anterior
7. Sal con `/exit`

Criterios de éxito: Debes tener un `utils.py` mejorado con validación de entrada, manejo de errores y una docstring, todo construido a través de una conversación de varios turnos.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Indicaciones de ejemplo para probar:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**Problemas comunes:**
- Si Copilot CLI hace preguntas aclaratorias, respóndelas de manera natural
- El contexto se lleva hacia adelante, así que cada indicación se basa en la anterior
- Usa `/clear` si quieres empezar de nuevo

</details>

### Reto extra: Compara los modos

Los ejemplos usaron `/plan` para una función de búsqueda y `-p` para revisiones por lotes. Ahora prueba los tres modos en una sola nueva tarea: añadir un método `list_by_year()` a la clase `BookCollection`:

1. **Interactivo**: `copilot` → pídele que diseñe y construya el método paso a paso
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programático**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**Reflexión**: ¿Qué modo te resultó más natural? ¿Cuándo usarías cada uno?

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Typing `exit` instead of `/exit` | Copilot CLI treats "exit" as a prompt, not a command | Slash commands always start with `/` |
| Using `-p` for multi-turn conversations | Each `-p` call is isolated with no memory of previous calls | Use interactive mode (`copilot`) for conversations that build on context |
| Forgetting quotes around prompts with `$` or `!` | Shell interprets special characters before Copilot CLI sees them | Wrap prompts in quotes: `copilot -p "What does $HOME mean?"` |
| Pressing Esc once to cancel a running task | A single Esc no longer cancels in-flight work (to prevent accidents) | Press **Esc twice** to cancel while Copilot CLI is processing |

### Solución de problemas

**"Model not available"** - Your subscription may not include all models. Use `/model` to see what's available.

**"Context too long"** - Your conversation has used the full context window. Use `/clear` to reset, or start a new session.

**"Rate limit exceeded"** - Wait a few minutes and try again. Consider using programmatic mode for batch operations with delays.

</details>

---

# Summary

## 🔑 Conclusiones clave
1. **Modo interactivo** es para la exploración y la iteración - el contexto se mantiene. Es como mantener una conversación con alguien que recuerda lo que has dicho hasta ese momento.
2. **Modo de planificación** está pensado normalmente para tareas más complejas. Revísalo antes de implementarlo.
3. **Modo programático** es para automatización. No requiere interacción.
4. **Comandos esenciales** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`) cubren la mayor parte del uso diario.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para obtener una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ahora que entiendes los tres modos, aprendamos cómo darle contexto a Copilot CLI sobre tu código.

En **[Capítulo 02: Contexto y Conversaciones](../02-context-conversations/README.md)**, aprenderás:

- La sintaxis `@` para referenciar archivos y directorios
- Gestión de sesiones con `--resume` y `--continue`
- Cómo la gestión del contexto hace que Copilot CLI sea realmente potente

---

**[← Volver al inicio del curso](../README.md)** | **[Continuar al Capítulo 02 →](../02-context-conversations/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->