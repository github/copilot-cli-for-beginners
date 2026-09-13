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

![Capítulo 01: Primeros Pasos](../../../01-setup-and-first-steps/assets/chapter-header.png)

> **Mira cómo la IA encuentra errores al instante, explica código confuso y genera scripts funcionales. Luego aprende tres formas diferentes de usar GitHub Copilot CLI.**

¡Este capítulo es donde empieza la magia! Experimentarás de primera mano por qué los desarrolladores describen GitHub Copilot CLI como si tuvieras a un ingeniero sénior al alcance de un botón. Verás a la IA encontrar fallos de seguridad en segundos, obtener explicaciones de código complejo en inglés sencillo y generar scripts que funcionan al instante. Luego dominarás los tres modos de interacción (Interactive, Plan y Programmatic) para saber exactamente cuál usar en cada tarea.

> ⚠️ **Requisitos previos**: Asegúrate de haber completado **[Capítulo 00: Inicio rápido](../00-quick-start/README.md)** primero. Necesitarás tener GitHub Copilot CLI instalado y autenticado antes de ejecutar las demos a continuación.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Experimentar el aumento de productividad que proporciona GitHub Copilot CLI a través de demostraciones prácticas
- Elegir el modo adecuado (Interactive, Plan o Programmatic) para cualquier tarea
- Usar comandos slash para controlar tus sesiones

> ⏱️ **Tiempo estimado**: ~45 minutos (15 min de lectura + 30 min prácticos)

---

# Tu primera experiencia con Copilot CLI

<img src="../../../01-setup-and-first-steps/assets/first-copilot-experience.png" alt="Desarrollador sentado en un escritorio con código en el monitor y partículas brillantes que representan la asistencia de la IA" width="800"/>

Sumérgete y descubre lo que Copilot CLI puede hacer.

---

## Familiarízate: Tus primeros prompts

Antes de sumergirte en las demos impresionantes, comencemos con algunos prompts sencillos que puedes probar ahora mismo. **No se necesita un repositorio de código**. Simplemente abre una terminal y inicia Copilot CLI:

```bash
copilot
```

Prueba estos prompts para principiantes:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

¿No usas Python? ¡No hay problema! Simplemente haz preguntas sobre el lenguaje que prefieras.

Fíjate en lo natural que se siente. Simplemente haz preguntas como lo harías con un colega. Cuando termines de explorar, escribe `/exit` para salir de la sesión.

**La idea clave**: GitHub Copilot CLI es conversacional. No necesitas una sintaxis especial para empezar. Simplemente haz preguntas en inglés sencillo.

## Verlo en acción

Ahora veamos por qué los desarrolladores llaman esto "tener a un ingeniero sénior en marcación rápida."

> 📖 **Cómo leer los ejemplos**: Las líneas que comienzan con `>` son prompts que escribes dentro de una sesión interactiva de Copilot CLI. Las líneas sin prefijo `>` son comandos de shell que ejecutas en tu terminal.

> 💡 **Sobre las salidas de ejemplo**: Los ejemplos de salida que se muestran a lo largo de este curso son ilustrativos. Debido a que las respuestas de Copilot CLI varían cada vez, tus resultados diferirán en redacción, formato y detalle. Concéntrate en el *tipo* de información devuelta, no en el texto exacto.

### Demo 1: Revisión de código en segundos

El curso incluye archivos de ejemplo con problemas de calidad intencionales. Si estás trabajando en tu máquina local y aún no has clonado el repositorio, ejecuta el comando `git clone` que aparece abajo, navega a la carpeta `copilot-cli-for-beginners` y luego ejecuta el comando `copilot`.

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

> 💡 **¿Para qué sirve el símbolo `@`?** El símbolo `@` le indica a Copilot CLI que lea un archivo. Aprenderás todo sobre esto en el Capítulo 02. Por ahora, simplemente copia el comando exactamente como se muestra.

---

<details>
<summary>🎬 ¡Mira cómo funciona!</summary>

![Demostración de revisión de código](../../../01-setup-and-first-steps/assets/code-review-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes de lo que se muestra aquí.*

</details>

---

**Conclusión**: Una revisión de código profesional en segundos. La revisión manual tomaría... bueno... mucho más tiempo que eso.

---

### Demo 2: Explicar código confuso

¿Alguna vez te has quedado mirando código preguntándote qué hace? Prueba esto en tu sesión de Copilot CLI:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 ¡Mira cómo funciona!</summary>

![Demostración de explicación de código](../../../01-setup-and-first-steps/assets/explain-code-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes de lo que se muestra aquí.*

</details>

---

**Qué ocurre**: (tu salida será diferente) Copilot CLI lee el archivo, entiende el código y lo explica en inglés sencillo.

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

**Conclusión**: Código complejo explicado como lo haría un mentor paciente.

---

### Demo 3: Generar código funcional

¿Necesitas una función para la que de otro modo pasarías 15 minutos buscando en Google? Sigue en tu sesión:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 ¡Mira cómo funciona!</summary>

![Demostración de generación de código](../../../01-setup-and-first-steps/assets/generate-code-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes de lo que se muestra aquí.*

</details>

---

**Qué ocurre**: Una función completa y funcional en segundos que puedes copiar, pegar y ejecutar.

Cuando termines de explorar, sal de la sesión:

```
> /exit
```

**Conclusión**: Gratificación instantánea, y te mantuviste en una sesión continua todo el tiempo.

---

# Modos y comandos

<img src="../../../01-setup-and-first-steps/assets/modes-and-commands.png" alt="Panel de control futurista con pantallas brillantes, diales y ecualizadores que representan los modos y comandos de Copilot CLI" width="800"/>

Acabas de ver lo que Copilot CLI puede hacer. Ahora entendamos *cómo* usar estas capacidades de forma efectiva. La clave es saber cuál de los tres modos de interacción usar para diferentes situaciones.

> 💡 **Nota**: Copilot CLI también tiene un modo **Autopilot** en el que ejecuta tareas sin esperar tu entrada. Es potente pero requiere otorgar permisos completos y usa solicitudes premium de forma autónoma. Este curso se centra en los tres modos que aparecen más abajo. Te mostraremos Autopilot una vez que te sientas cómodo con lo básico.

---

## 🧩 Analogía del mundo real: salir a comer

Piensa en usar GitHub Copilot CLI como si fueras a salir a comer. Desde planear el viaje hasta hacer tu pedido, diferentes situaciones piden distintos enfoques:

| Modo | Analogía al salir a comer | Cuándo usar |
|------|----------------|-------------|
| **Plan** | Ruta GPS al restaurante | Tareas complejas - traza la ruta, revisa las paradas, acuerda el plan y luego conduce |
| **Interactive** | Hablar con el camarero | Exploración e iteración - haz preguntas, personaliza, recibe retroalimentación en tiempo real |
| **Programmatic** | Pedido en el drive-through | Tareas rápidas y específicas - permanece en tu entorno y obtén un resultado rápido |

Al igual que al salir a comer, aprenderás de forma natural cuándo cada enfoque es el adecuado.

<img src="../../../01-setup-and-first-steps/assets/ordering-food-analogy.png" alt="Tres formas de usar GitHub Copilot CLI - Modo Plan (ruta GPS al restaurante), Modo Interactive (hablar con el camarero), Modo Programmatic (pedido en drive-through)" width="800"/>

*Elige tu modo según la tarea: Plan para mapear primero, Interactive para colaboración de ida y vuelta, Programmatic para resultados rápidos de una sola vez*

### ¿Con qué modo debo empezar?

**Comienza con el modo Interactive.** 
- Puedes experimentar y hacer preguntas de seguimiento
- El contexto se construye de forma natural mediante la conversación
- Los errores son fáciles de corregir con `/clear`

Una vez que te sientas cómodo, prueba:
- **Modo Programmatic** (`copilot -p "<your prompt>"`) para preguntas rápidas y puntuales
- **Modo Plan** (`/plan`) cuando necesitas planear las cosas con más detalle antes de programar

---

## Los tres modos

### Modo 1: Modo Interactive (comienza aquí)

<img src="../../../01-setup-and-first-steps/assets/interactive-mode.png" alt="Modo Interactive - Como hablar con un camarero que puede responder preguntas y ajustar el pedido" width="250"/>

**Ideal para**: Exploración, iteración y conversaciones de varias vueltas. Como hablar con un camarero que puede responder preguntas, aceptar retroalimentación y ajustar el pedido al instante.

Inicia una sesión interactiva:

```bash
copilot
```

Como has visto hasta ahora, verás un prompt donde puedes escribir de forma natural. Para obtener ayuda sobre los comandos disponibles, simplemente escribe:

```
> /help
```

**Idea clave**: El modo Interactive mantiene el contexto. Cada mensaje se construye sobre los anteriores, como en una conversación real.

#### Ejemplo del modo Interactive

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Fíjate cómo cada prompt se construye sobre la respuesta anterior. Estás manteniendo una conversación, no empezando de nuevo cada vez.

---

### Modo 2: Modo Plan

<img src="../../../01-setup-and-first-steps/assets/plan-mode.png" alt="Modo Plan - Como planear una ruta antes de un viaje usando GPS" width="250"/>

**Ideal para**: Tareas complejas donde quieres revisar el enfoque antes de ejecutarlo. Similar a planear una ruta antes de un viaje usando GPS.

El modo Plan te ayuda a crear un plan paso a paso antes de escribir código. Usa el comando `/plan`, presiona **Shift+Tab** para cambiar al modo Plan:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Consejo**: **Shift+Tab** cicla entre modos: Interactive → Plan → Autopilot. Púlsalo en cualquier momento durante una sesión interactiva para cambiar de modo sin escribir un comando.

También puedes iniciar Copilot CLI directamente en modo plan usando la opción `--plan`:

```bash
copilot --plan
```

**Salida del modo Plan:** (tu salida puede diferir)

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

**Idea clave**: El modo Plan te permite revisar y modificar el enfoque antes de que se escriba código. Mientras estás en modo Plan, Copilot CLI es **solo lectura** y no editará archivos ni ejecutará comandos que cambien tu espacio de trabajo hasta que apruebes y pases a la implementación. Esto te mantiene de forma segura en la fase de "pensar" hasta que estés listo. Una vez que un plan esté completo, incluso puedes decirle a Copilot CLI que lo guarde en un archivo para referencia posterior. Por ejemplo, "Guarda este plan en `mark_as_read_plan.md`" crearía un archivo markdown con los detalles del plan.

> 💡 **¿Quieres algo más complejo?** Prueba: `/plan Add search and filter capabilities to the book app`. El modo Plan escala desde funciones simples hasta aplicaciones completas.

> 📚 **Modo Autopilot**: Puede que hayas notado que Shift+Tab cicla por un tercer modo llamado **Autopilot**. En el modo autopilot, Copilot ejecuta todo un plan sin esperar tu entrada después de cada paso — como entregar una tarea a un colega y decir 'avísame cuando termines'. El flujo de trabajo típico es plan → aceptar → autopilot, lo que significa que necesitas ser bueno escribiendo planes primero. También puedes iniciar directamente en autopilot con `copilot --autopilot`, o establecer un objetivo en línea con `/autopilot <objective>` (por ejemplo, `/autopilot Add a search command to the book app`). También puedes combinar planificación y autopilot ejecutando `copilot --plan --mode autopilot`. Copilot creará primero un plan y luego lo implementará automáticamente sin pausar para aprobación. Familiarízate primero con los modos Interactive y Plan, y luego consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) cuando estés listo.

---

### Modo 3: Modo Programmatic

<img src="../../../01-setup-and-first-steps/assets/programmatic-mode.png" alt="Modo Programmatic - Como usar un drive-through para un pedido rápido" width="250"/>

**Ideal para**: Automatización, scripts, CI/CD y comandos de una sola ejecución. Como usar un drive-through para un pedido rápido sin necesidad de hablar con un camarero.

Usa la opción `-p` para comandos puntuales que no necesitan interacción:

```bash
# Generar código
copilot -p "Write a function that checks if a number is even or odd"

# Obtener ayuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Idea clave**: El modo Programmatic te da una respuesta rápida y sale. No hay conversación, solo entrada → salida.

<details>
<summary>📚 <strong>Ir más allá: Usar el modo Programmatic en scripts</strong> (haz clic para expandir)</summary>

Una vez que te sientas cómodo, puedes usar `-p` en scripts de shell:

```bash
#!/bin/bash

# Generar mensajes de commit automáticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar un archivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Acerca de `--allow-all`**: Esta opción omite todas las solicitudes de permiso, permitiendo que Copilot CLI lea archivos, ejecute comandos y acceda a URLs sin preguntar primero. Esto es necesario para el modo programmatic (`-p`) ya que no hay una sesión interactiva para aprobar acciones. Usa `--allow-all` solo con prompts que hayas escrito tú mismo y en directorios de confianza. Nunca lo uses con entradas no confiables o en directorios sensibles.

</details>

---

## Comandos slash esenciales

Estos comandos son geniales para aprender al principio mientras comienzas con Copilot CLI:

| Comando | Qué hace | Cuándo usar |
|---------|--------------|-------------|
| `/ask` | Haz una pregunta rápida sin que afecte el historial de la conversación | Cuando quieres una respuesta rápida sin desviar tu tarea actual |
| `/clear` | Borra la conversación y comienza de nuevo | Al cambiar de tema |
| `/config` | Ver o establecer valores predeterminados persistentes (p. ej., modelo por defecto) | Cuando quieres que una configuración se aplique a todas las futuras sesiones |
| `/help` | Mostrar todos los comandos disponibles | Cuando olvidas un comando |
| `/model` | Mostrar o cambiar el modelo de IA para la sesión actual | Cuando quieres cambiar el modelo de IA |
| `/plan` | Planifica tu trabajo antes de codificar | Para características más complejas |
| `/refine` | Reescribe un prompt desordenado y en flujo de conciencia en uno claro y enfocado | Cuando tu prompt se siente desordenado y quieres mejores resultados |
| `/research` | Investigación profunda usando GitHub y fuentes web | Cuando necesitas investigar un tema antes de codificar |
| `/exit` | Terminar la sesión | Cuando has terminado |

> 💡 **`/ask` vs regular chat**: Normalmente cada mensaje que envías forma parte de la conversación en curso y afecta respuestas futuras. `/ask` es un atajo "fuera de registro". Es perfecto para preguntas rápidas y puntuales como `/ask What does YAML mean?` sin contaminar el contexto de tu sesión.

> 💡 **`/refine` for better prompts**: ¿No estás seguro de que tu prompt sea lo suficientemente claro? Escríbelo tal como te viene a la mente y luego ejecuta `/refine` para que Copilot lo reescriba en un prompt preciso y bien estructurado antes de enviarlo. Esto es especialmente útil cuando eres nuevo en herramientas de IA y aún aprendes a redactar prompts efectivos.

> 💡 **Tab-completion**: Al escribir un comando con barra, presiona **Tab** para autocompletar el nombre del comando o para recorrer los subcomandos y argumentos disponibles. Esto es especialmente útil cuando no recuerdas el nombre exacto de un comando.

> 💡 **Queue prompts while Copilot is busy**: Si Copilot está en medio de una tarea y se te ocurre lo siguiente que quieres pedirle, simplemente escríbelo y presiona **Enter**. Copilot lo ejecutará automáticamente cuando termine la tarea actual, así no tienes que esperar.

¡Eso es todo para comenzar! A medida que te sientas cómodo, puedes explorar comandos adicionales.

> 📚 **Official Documentation**: [CLI command reference](https://docs.github.com/copilot/reference/cli-command-reference) para la lista completa de comandos y banderas.

<details>
<summary>📚 <strong>Comandos adicionales</strong> (haz clic para expandir)</summary>

> 💡 Los comandos esenciales anteriores cubren gran parte de lo que harás en el uso diario. Esta referencia está aquí para cuando estés listo para explorar más.

### Entorno de agentes

| Command | What It Does |
|---------|--------------|
| `/agent` | Navegar y seleccionar entre agentes disponibles |
| `/env` | Mostrar detalles del entorno cargado — qué instrucciones, servidores MCP, skills, agentes y plugins están activos |
| `/init` | Inicializar las instrucciones de Copilot para tu repositorio |
| `/instructions` | Ver y gestionar todos los archivos de instrucciones cargados para la sesión actual |
| `/mcp` | Abrir el panel de control de plugins (enfocado en servidores MCP); usa `/mcp config` para el asistente de configuración dedicado de MCP |
| `/plugin` | Abrir el panel de control de plugins para explorar, instalar, habilitar y actualizar plugins |
| `/settings` | Abrir un diálogo interactivo para explorar y editar todos los ajustes de usuario en un solo lugar |
| `/skills` | Abrir el panel de control de plugins (enfocado en skills) para descubrir y gestionar skills |
| `/subagents` | Ver y gestionar subagentes ejecutándose en la sesión actual |

> 💡 Agents are covered in [Chapter 04](../04-agents-custom-instructions/README.md), skills are covered in [Chapter 05](../05-skills/README.md), and MCP servers are covered in [Chapter 06](../06-mcp-servers/README.md).

### Modelos y subagentes

| Command | What It Does |
|---------|--------------|
| `/config` | Ver o establecer valores predeterminados persistentes (por ejemplo, `/config model` para establecer tu modelo predeterminado para todas las sesiones futuras) |
| `/delegate` | Delegar una tarea al agente en la nube de GitHub Copilot |
| `/fleet` | Dividir una tarea compleja en subtareas paralelas para completarla más rápido |
| `/model` | Mostrar o cambiar el modelo de IA solo para la sesión actual |
| `/tasks` | Ver subagentes en segundo plano y sesiones de shell desacopladas |

### Código

| Command | What It Does |
|---------|--------------|
| `/diff` | Revisar los cambios realizados en el directorio actual |
| `/pr` | Operar sobre pull requests para la rama actual |
| `/research` | Realizar una investigación profunda usando GitHub y fuentes web |
| `/review` | Ejecutar el agente de revisión de código para analizar cambios |
| `/terminal-setup` | Habilitar soporte de entrada multilínea (shift+enter y ctrl+enter) |

### Permisos

| Command | What It Does |
|---------|--------------|
| `/add-dir <directory>` | Añadir un directorio a la lista permitida |
| `/allow-all [on\|off\|show]` | Aprobar automáticamente todos los avisos de permisos; usa `on` para habilitar, `off` para deshabilitar, `show` para comprobar el estado actual |
| `/permissions` | Cambiar entre modos de aprobación (interactivo, plan, piloto automático) para controlar cuánto puede hacer Copilot sin preguntar |
| `/yolo` | Alias rápido para `/allow-all on` — aprueba automáticamente todos los avisos de permisos. |
| `/cwd`, `/cd [directory]` | Ver o cambiar el directorio de trabajo |
| `/list-dirs` | Mostrar todos los directorios permitidos |

> ⚠️ **Use with caution**: `/allow-all` and `/yolo` skip confirmation prompts. Great for trusted projects, but be careful with untrusted code.

### Sesión

| Command | What It Does |
|---------|--------------|
| `/clear` | Abandona la sesión actual (no se guarda historial) y comienza una conversación nueva |
| `/compact` | Resumir la conversación para reducir el uso de contexto (opcionalmente añadir instrucciones de enfoque, p. ej. `/compact focus on the bug list`) |
| `/context` | Mostrar el uso y visualización de tokens de la ventana de contexto |
| `/keep-alive` | Evitar que tu sistema entre en suspensión mientras Copilot CLI está activo — útil para tareas de larga duración en un portátil |
| `/memory [on\|off\|show]` | Habilitar, deshabilitar o ver la memoria persistente — hechos y preferencias recordados en todas las sesiones |
| `/new` | Finaliza la sesión actual (guardándola en el historial para búsqueda/reanudación) y comienza una conversación nueva. |
| `/resume` | Cambiar a una sesión diferente (opcionalmente especifica el ID o nombre de la sesión) |
| `/rename` | Renombrar la sesión actual (omitir el nombre para autogenerarlo) |
| `/rewind` | Abrir un selector de línea de tiempo para retroceder a cualquier punto anterior en la conversación; opcionalmente restaura los archivos que Copilot cambió (funciona sin git) |
| `/usage` | Mostrar métricas y estadísticas de uso de la sesión, incluidas barras de progreso de cuota |
| `/session` | Mostrar información de la sesión y resumen del espacio de trabajo; usa `/session delete`, `/session delete <id>`, o `/session delete-all` para eliminar sesiones |
| `/share` | Exportar la sesión como un archivo markdown, un gist de GitHub o un archivo HTML autocontenido |
| `/every <interval> <prompt>` | Programar un prompt para ejecutarse en un intervalo recurrente (p. ej., `/every 1h summarize new commits`). Usa lenguaje natural para el intervalo. `/loop` es un alias de `/every`. |
| `/after <time> <prompt>` | Programar un prompt para ejecutarse una vez después de un retraso (p. ej., `/after 30m run tests`). Usa lenguaje natural para el tiempo. |

> 💡 **Sessions tab**: La interfaz interactiva de Copilot CLI incluye una **pestaña Sessions** en la parte superior de la ventana. Puedes usarla para ver y cambiar entre múltiples sesiones que se ejecutan al mismo tiempo. Presiona `n` en la pestaña Sessions para iniciar una nueva sesión sin cerrar la que estás usando.

### Visualización

| Command | What It Does |
|---------|--------------|
| `/statusline` (or `/footer`) | Personalizar qué elementos aparecen en la barra de estado en la parte inferior de la sesión (directorio, rama, esfuerzo, ventana de contexto, cuota) |
| `/theme` | Ver o establecer el tema del terminal |
| `/voice` | Dictar tu prompt usando reconocimiento de voz local — habla de forma natural en lugar de escribir |

### Ayuda y comentarios

| Command | What It Does |
|---------|--------------|
| `/app` | Abrir la app de GitHub (o fallback en el navegador) directamente desde la CLI |
| `/changelog` | Mostrar el changelog de las versiones de la CLI |
| `/feedback` | Enviar comentarios a GitHub |
| `/help` | Mostrar todos los comandos disponibles |

### Comandos rápidos de shell

Ejecuta comandos de shell directamente sin IA anteponiendo `!`:

```bash
copilot

> !git status
# Ejecuta git status directamente, omitiendo la IA

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

> 💡 **Session vs. persistent model**: El comando `/model` cambia el modelo solo para la **sesión actual**. Cuando inicies una nueva sesión, Copilot usará el predeterminado nuevamente. Para establecer un modelo predeterminado permanente para todas las sesiones futuras, usa `/config model` en su lugar.

> 💡 **Tip**: Algunos modelos consumen más "premium requests" que otros. Los modelos marcados **1x** (como Claude Sonnet 4.5) son un excelente predeterminado. Son capaces y eficientes. Los modelos con multiplicadores más altos usan tu cuota de solicitudes premium más rápido, así que guárdalos para cuando realmente los necesites.

> 💡 **Not sure which model to pick?** Selecciona **`Auto`** en el selector de modelos para que Copilot elija automáticamente el mejor modelo disponible para cada sesión. Este es un buen predeterminado si recién comienzas y no quieres preocuparte por la selección de modelos.

> 💡 **Model family shortcuts**: También puedes escribir un alias corto de familia — como `opus`, `sonnet`, `haiku`, `gpt`, o `gemini` — directamente en el selector `/model` en lugar de desplazarte por la lista completa. Copilot elegirá el mejor modelo disponible en esa familia por ti.

> 💡 **Model picker navigation**: El selector de modelos ahora agrupa modelos en secciones — **Recientes**, **Recomendados**, y **Nuevos** — para que puedas encontrar rápidamente el modelo que usaste por última vez o probar lo que está recién disponible. Usa **Shift+Tab** dentro del selector para cambiar entre vistas de agrupación.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Configuración cálida de escritorio con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica práctica" width="800"/>

Es hora de poner en práctica lo que has aprendido.

---

## ▶️ Pruébalo tú mismo

### Exploración interactiva

Inicia Copilot y usa prompts de seguimiento para mejorar iterativamente la app de libros:

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### Planificar una funcionalidad

Usa `/plan` para que Copilot CLI trace una implementación antes de escribir código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revisar el plan
# Aprobar o modificar
# Observar su implementación paso a paso
```

### Automatizar con el modo programático

El flag `-p` te permite ejecutar Copilot CLI directamente desde tu terminal sin entrar en modo interactivo. Copia y pega el siguiente script en tu terminal (no dentro de Copilot) desde la raíz del repositorio para revisar todos los archivos Python en la app de libros.

```bash
# Revisa todos los archivos Python en la aplicación book
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# Revisar todos los archivos de Python en la aplicación de libros
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

Después de completar las demostraciones, prueba estas variaciones:

1. **Desafío interactivo**: Inicia `copilot` y explora la app de libros. Pregunta sobre `@samples/book-app-project/books.py` y solicita mejoras 3 veces seguidas.

2. **Desafío en modo Plan**: Ejecuta `/plan Add rating and review features to the book app`. Lee el plan cuidadosamente. ¿Tiene sentido?

3. **Desafío programático**: Ejecuta `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. ¿Funcionó a la primera?

---

## 💡 Consejo: Controla tu sesión CLI desde la web o el móvil

GitHub Copilot CLI admite **sesiones remotas**, lo que te permite monitorear e interactuar con una sesión CLI en ejecución desde un navegador web (en escritorio o móvil) o la app GitHub Mobile sin estar físicamente en tu terminal.

Inicia una sesión remota con el flag `--remote`:

```bash
copilot --remote
```

Copilot CLI mostrará un enlace y proporcionará acceso a un código QR. Abre el enlace en tu teléfono o en una pestaña del navegador de escritorio para ver la sesión en tiempo real, enviar prompts de seguimiento, revisar planes y dirigir el agente de forma remota. Las sesiones son específicas del usuario, por lo que solo puedes acceder a tus propias sesiones de Copilot CLI.

También puedes habilitar el acceso remoto desde dentro de una sesión activa en cualquier momento:

```
> /remote
```

Más detalles sobre sesiones remotas se pueden encontrar en la [documentación de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Tarea

### Desafío principal: Mejora las utilidades de la app de libros

Los ejemplos prácticos se centraron en revisar y refactorizar `book_app.py`. Ahora practica las mismas habilidades en un archivo diferente, `utils.py`:

1. Inicia una sesión interactiva: `copilot`
2. Pídele a Copilot CLI que resuma el archivo: "Resume @samples/book-app-project/utils.py y explica qué hace cada función en este archivo"
3. Pídele que añada validación de entrada: "Añade validación a `get_user_choice()` para que maneje entradas vacías y entradas no numéricas"
4. Pídele que mejore el manejo de errores: "¿Qué ocurre si `get_book_details()` recibe una cadena vacía para el título? Agrega comprobaciones para eso."
5. Pide un docstring: "Agrega un docstring completo a `get_book_details()` con descripciones de los parámetros y los valores de retorno"
6. Observa cómo el contexto se mantiene entre las peticiones. Cada mejora se basa en la anterior
7. Sal con `/exit`

**Criterios de éxito**: Deberías tener un `utils.py` mejorado con validación de entrada, manejo de errores y un docstring, todo construido a través de una conversación de múltiples turnos.

<details>
<summary>💡 Consejos (haz clic para expandir)</summary>

**Ejemplos de peticiones para probar:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**Problemas comunes:**
- Si Copilot CLI hace preguntas de aclaración, respóndelas con naturalidad
- El contexto se mantiene, por lo que cada petición se basa en la anterior
- Usa `/clear` si quieres empezar de nuevo

</details>

### Desafío adicional: Compara los modos

Los ejemplos usaron `/plan` para una función de búsqueda y `-p` para revisiones por lotes. Ahora prueba los tres modos en una sola nueva tarea: añadir un método `list_by_year()` a la clase `BookCollection`:

1. **Interactivo**: `copilot` → pídele que diseñe y construya el método paso a paso
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programático**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**Reflexión**: ¿Qué modo te resultó más natural? ¿Cuándo usarías cada uno?

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Escribir `exit` en lugar de `/exit` | Copilot CLI trata "exit" como una petición, no como un comando | Los comandos con slash siempre comienzan con `/` |
| Usar `-p` para conversaciones de múltiples turnos | Cada llamada con `-p` es aislada y no tiene memoria de llamadas previas | Usa el modo interactivo (`copilot`) para conversaciones que construyen contexto |
| Olvidar las comillas alrededor de peticiones con `$` o `!` | El shell interpreta caracteres especiales antes de que Copilot CLI los vea | Encierra las peticiones entre comillas simples: `copilot -p 'What does $HOME mean?'` |
| Presionar Esc una vez para cancelar una tarea en ejecución | Una sola pulsación de Esc ya no cancela el trabajo en curso (para evitar accidentes) | Presiona **Esc dos veces** para cancelar mientras Copilot CLI está procesando |

### Solución de problemas

**"Model not available"** - Es posible que tu suscripción no incluya todos los modelos. Usa `/model` para ver cuáles están disponibles.

**"Context too long"** - Tu conversación ha usado toda la ventana de contexto. Usa `/new` para iniciar una nueva sesión.

**"Rate limit exceeded"** - Espera unos minutos e inténtalo de nuevo. Considera usar el modo programático para operaciones por lotes con retrasos.

</details>

---

# Resumen

## 🔑 Puntos clave

1. **El modo interactivo** es para la exploración y la iteración: el contexto se mantiene. Es como tener una conversación con alguien que recuerda lo que dijiste hasta ese momento.
2. **El modo Plan** suele usarse para tareas más complejas. Revisa antes de implementar.
3. **El modo programático** es para automatización. No se necesita interacción.
4. **Comandos esenciales** (`/ask`, `/help`, `/clear`, `/new`, `/plan`, `/research`, `/model`, `/exit`) cubren la mayoría de los usos diarios.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Ahora que entiendes los tres modos, aprendamos cómo darle contexto a Copilot CLI sobre tu código.

En **[Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md)**, aprenderás:

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