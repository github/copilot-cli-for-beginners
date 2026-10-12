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

> **Observa cómo la IA encuentra errores al instante, explica código confuso y genera scripts funcionales. Luego aprende tres formas diferentes de usar GitHub Copilot CLI.**

¡Este capítulo es donde empieza la magia! Experimentarás de primera mano por qué los desarrolladores describen GitHub Copilot CLI como tener a un ingeniero senior en marcación rápida. Verás a la IA encontrar fallos de seguridad en segundos, obtener explicaciones de código complejo en lenguaje claro y generar scripts funcionales al instante. Luego dominarás los tres modos de interacción (Interactive, Plan, and Programmatic) para saber exactamente cuál usar para cada tarea.

> ⚠️ **Requisitos previos**: Asegúrate de haber completado primero **[Chapter 00: Quick Start](../00-quick-start/README.md)**. Necesitarás tener GitHub Copilot CLI instalado y autenticado antes de ejecutar las demostraciones a continuación.

## 🎯 Objetivos de aprendizaje

Al finalizar este capítulo, podrás:

- Experimentar el impulso de productividad que GitHub Copilot CLI ofrece mediante demostraciones prácticas
- Elegir el modo adecuado (Interactive, Plan o Programmatic) para cualquier tarea
- Usar comandos con barra (slash commands) para controlar tus sesiones

> ⏱️ **Tiempo estimado**: ~45 minutos (15 min lectura + 30 min práctica)

---

# Tu primera experiencia con Copilot CLI

<img src="../../../01-setup-and-first-steps/assets/first-copilot-experience.png" alt="Desarrollador sentado en un escritorio con código en el monitor y partículas brillantes que representan la asistencia de la IA" width="800"/>

Sumérgete y descubre lo que Copilot CLI puede hacer.

---

## Familiarízate: Tus primeros prompts

Antes de sumergirte en las demostraciones impresionantes, empecemos con algunos prompts sencillos que puedes probar ahora mismo. ¡**No se necesita un repositorio de código**! Solo abre una terminal y ejecuta Copilot CLI:

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

Fíjate en lo natural que se siente. Haz preguntas como se las harías a un colega. Cuando termines de explorar, escribe `/exit` para salir de la sesión.

**La idea clave**: GitHub Copilot CLI es conversacional. No necesitas una sintaxis especial para comenzar. Simplemente haz preguntas en lenguaje sencillo.

## Verlo en acción

Ahora veamos por qué los desarrolladores describen esto como "tener a un ingeniero senior en marcación rápida."

> 📖 **Cómo leer los ejemplos**: Las líneas que comienzan con `>` son prompts que escribes dentro de una sesión interactiva de Copilot CLI. Las líneas sin prefijo `>` son comandos de shell que ejecutas en tu terminal.

> 💡 **Sobre los resultados de ejemplo**: Las salidas de ejemplo que se muestran a lo largo de este curso son ilustrativas. Debido a que las respuestas de Copilot CLI varían cada vez, tus resultados diferirán en redacción, formato y detalle. Concéntrate en el *tipo* de información devuelta, no en el texto exacto.

### Demostración 1: Revisión de código en segundos

El curso incluye archivos de ejemplo con problemas intencionales de calidad de código. Si estás trabajando en tu máquina local y aún no has clonado el repositorio, ejecuta el comando `git clone` a continuación, navega hasta la carpeta `copilot-cli-for-beginners` y luego ejecuta el comando `copilot`.

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

> 💡 **¿Para qué se usa el símbolo `@`?** El símbolo `@` le indica a Copilot CLI que lea un archivo. Aprenderás todo sobre esto en el Capítulo 02. Por ahora, simplemente copia el comando exactamente como se muestra.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de revisión de código](../../../01-setup-and-first-steps/assets/code-review-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Conclusión**: Una revisión de código profesional en segundos. La revisión manual tomaría... bueno... mucho más tiempo que eso.

---

### Demostración 2: Explicar código confuso

¿Alguna vez te has quedado mirando código preguntándote qué hace? Prueba esto en tu sesión de Copilot CLI:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de explicación de código](../../../01-setup-and-first-steps/assets/explain-code-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Qué sucede**: (tu salida será diferente) Copilot CLI lee el archivo, comprende el código y lo explica en lenguaje claro.

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

### Demostración 3: Generar código funcional

¿Necesitas una función por la que de otro modo pasarías 15 minutos buscando en Google? Aún en tu sesión:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de generación de código](../../../01-setup-and-first-steps/assets/generate-code-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Qué sucede**: Una función completa y funcional en segundos que puedes copiar, pegar y ejecutar.

Cuando termines de explorar, sal de la sesión:

```
> /exit
```

**Conclusión**: Gratificación instantánea y permaneciste en una sola sesión continua todo el tiempo.

---

# Modos y comandos

<img src="../../../01-setup-and-first-steps/assets/modes-and-commands.png" alt="Panel de control futurista con pantallas brillantes, diales y ecualizadores que representan los modos y comandos de Copilot CLI" width="800"/>

Acabas de ver lo que Copilot CLI puede hacer. Ahora entendamos *cómo* usar estas capacidades de manera efectiva. La clave es saber cuál de los tres modos de interacción utilizar en diferentes situaciones.

> 💡 **Nota**: Copilot CLI también tiene un modo **Autopilot** donde trabaja en las tareas sin esperar tu entrada. Es potente pero requiere otorgar permisos completos y utiliza solicitudes premium de forma autónoma. Este curso se centra en los tres modos que aparecen a continuación. Te señalaremos Autopilot una vez que te sientas cómodo con lo básico.

---

## 🧩 Analogía del mundo real: Salir a comer

Piensa en usar GitHub Copilot CLI como salir a comer. Desde planear el viaje hasta hacer el pedido, diferentes situaciones requieren diferentes enfoques:

| Modo | Analogía gastronómica | Cuándo usar |
|------|----------------|-------------|
| **Plan** | Ruta GPS al restaurante | Tareas complejas: traza la ruta, revisa paradas, acuerda el plan y luego conduce |
| **Interactive** | Hablar con el camarero | Exploración e iteración: haz preguntas, personaliza, obtén retroalimentación en tiempo real |
| **Programmatic** | Pedido en el autoservicio | Tareas rápidas y específicas: permanece en tu entorno y obtén un resultado rápido |

Al igual que al salir a comer, aprenderás de forma natural cuándo cada enfoque es el adecuado.

<img src="../../../01-setup-and-first-steps/assets/ordering-food-analogy.png" alt="Tres formas de usar GitHub Copilot CLI - Modo Plan (ruta GPS al restaurante), Modo Interactive (hablar con el camarero), Modo Programmatic (autoservicio)" width="800"/>

*Elige tu modo según la tarea: Plan para planificar primero, Interactive para colaboración de ida y vuelta, Programmatic para resultados rápidos de una sola vez*

### ¿Con qué modo debo empezar?

**Comienza con el modo Interactive.** 
- Puedes experimentar y hacer preguntas de seguimiento
- El contexto se construye de forma natural mediante la conversación
- Los errores son fáciles de corregir con `/clear`

Una vez que te sientas cómodo, prueba:
- **Programmatic mode** (`copilot -p "<your prompt>"`) para preguntas rápidas y puntuales
- **Plan mode** (`/plan`) cuando necesites planificar las cosas con más detalle antes de codificar

---

## Los tres modos

### Modo 1: Interactive Mode (comienza aquí)

<img src="../../../01-setup-and-first-steps/assets/interactive-mode.png" alt="Modo Interactive - Como hablar con un camarero que puede responder preguntas y ajustar el pedido" width="250"/>

**Ideal para**: Exploración, iteración, conversaciones de múltiples intercambios. Como hablar con un camarero que puede responder preguntas, recibir comentarios y ajustar el pedido al instante.

Inicia una sesión interactiva:

```bash
copilot
```

Como has visto hasta ahora, verás un prompt donde puedes escribir de forma natural. Para obtener ayuda sobre los comandos disponibles, simplemente escribe:

```
> /help
```

**Idea clave**: El modo Interactive mantiene el contexto. Cada mensaje se basa en los anteriores, igual que en una conversación real.

#### Ejemplo del modo Interactive

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Fíjate cómo cada prompt se basa en la respuesta anterior. Estás manteniendo una conversación, no empezando de cero cada vez.

---

### Modo 2: Plan Mode

<img src="../../../01-setup-and-first-steps/assets/plan-mode.png" alt="Modo Plan - Como planear una ruta antes de un viaje usando GPS" width="250"/>

**Ideal para**: Tareas complejas donde quieres revisar el enfoque antes de la ejecución. Similar a planear una ruta antes de un viaje usando GPS.

El modo Plan te ayuda a crear un plan paso a paso antes de escribir código. Usa el comando `/plan`, presiona **Shift+Tab** para cambiar al modo Plan:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Consejo**: **Shift+Tab** cambia entre modos: Interactive → Plan → Autopilot. Púlsalo en cualquier momento durante una sesión interactiva para cambiar de modo sin escribir un comando.

También puedes iniciar Copilot CLI directamente en modo plan usando el indicador `--plan`:

```bash
copilot --plan
```

**Salida del modo Plan:** (tu salida puede variar)

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

**Idea clave**: El modo Plan te permite revisar y modificar el enfoque antes de que se escriba código. Mientras estás en modo Plan, Copilot CLI es de **solo lectura** y no editará ningún archivo ni ejecutará comandos que cambien tu espacio de trabajo hasta que apruebes y pases a la implementación. Esto te mantiene de forma segura en la etapa de 'pensamiento' hasta que estés listo. Una vez que un plan esté completo, incluso puedes decirle a Copilot CLI que lo guarde en un archivo para referencia posterior. Por ejemplo, "Save this plan to `mark_as_read_plan.md`" crearía un archivo markdown con los detalles del plan.

> 💡 **¿Quieres algo más complejo?** Prueba: `/plan Add search and filter capabilities to the book app`. El modo Plan escala desde características simples hasta aplicaciones completas.

> 📚 **Autopilot mode**: Puede que hayas notado que Shift+Tab recorre un tercer modo llamado **Autopilot**. En el modo autopilot, Copilot ejecuta todo un plan sin esperar tu entrada después de cada paso — como encargar una tarea a un colega y decirle "avísame cuando termines". El flujo de trabajo típico es plan → aceptar → autopilot, lo que significa que necesitas saber redactar buenos planes primero. También puedes iniciar directamente en autopilot con `copilot --autopilot`, o establecer un objetivo en línea con `/autopilot <objective>` (por ejemplo, `/autopilot Add a search command to the book app`). También puedes combinar la planificación y autopilot ejecutando `copilot --plan --mode autopilot`. Copilot creará un plan primero y luego lo implementará automáticamente sin pausar para aprobación. Familiarízate primero con los modos Interactive y Plan, luego consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) cuando estés listo.

---

### Modo 3: Programmatic Mode

<img src="../../../01-setup-and-first-steps/assets/programmatic-mode.png" alt="Modo Programmatic - Como usar un autoservicio para un pedido rápido" width="250"/>

**Ideal para**: Automatización, scripts, CI/CD, comandos de una sola ejecución. Como usar un autoservicio para un pedido rápido sin necesitar hablar con un camarero.

Usa la bandera `-p` para comandos puntuales que no necesitan interacción:

```bash
# Generar código
copilot -p "Write a function that checks if a number is even or odd"

# Obtener ayuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Idea clave**: El modo Programmatic te da una respuesta rápida y sale. No hay conversación, solo entrada → salida.

<details>
<summary>📚 <strong>Ir más allá: Usar el modo Programmatic en scripts</strong> (clic para expandir)</summary>

Una vez que te sientas cómodo, puedes usar `-p` en scripts de shell:

```bash
#!/bin/bash

# Generar mensajes de commit automáticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar un archivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Acerca de `--allow-all`**: Esta bandera omite todas las solicitudes de permiso, permitiendo que Copilot CLI lea archivos, ejecute comandos y acceda a URLs sin preguntar primero. Esto es necesario para el modo programmatic (`-p`) ya que no hay una sesión interactiva para aprobar acciones. Usa `--allow-all` solo con prompts que hayas escrito tú mismo y en directorios en los que confíes. Nunca lo uses con entradas no confiables o en directorios sensibles.

</details>

---

## Comandos esenciales (slash commands)

Estos comandos son buenos para aprender al principio cuando comienzas con Copilot CLI:

| Comando | Qué hace | Cuándo usar |
|---------|--------------|-------------|
| `/ask` | Haz una pregunta rápida sin que afecte el historial de tu conversación | Cuando quieres una respuesta rápida sin desviar tu tarea actual |
| `/clear` | Borra la conversación y empieza de nuevo | Al cambiar de tema |
| `/config` | Ver o establecer valores predeterminados persistentes (p. ej., modelo predeterminado) | Cuando quieres que una configuración se aplique a todas las sesiones futuras |
| `/help` | Mostrar todos los comandos disponibles | Cuando olvidas un comando |
| `/model` | Mostrar o cambiar el modelo de IA para la sesión actual | Cuando quieres cambiar el modelo de IA |
| `/plan` | Planifica tu trabajo antes de programar | Para características más complejas |
| `/refine` | Reescribe un prompt aproximado y de flujo de conciencia en uno claro y enfocado | Cuando tu prompt se siente desordenado y quieres mejores resultados |
| `/research` | Investigación profunda usando GitHub y fuentes web | Cuando necesitas investigar un tema antes de programar |
| `/exit` | Terminar la sesión | Cuando hayas terminado |

> 💡 **`/ask` vs chat normal**: Normalmente cada mensaje que envías pasa a formar parte de la conversación en curso y afecta las respuestas futuras. `/ask` es un atajo "off the record". Es perfecto para preguntas rápidas y puntuales como `/ask What does YAML mean?` sin contaminar el contexto de tu sesión.

> 💡 **`/refine` para mejores prompts**: ¿No estás seguro de que tu prompt sea lo suficientemente claro? Escríbelo tal como te viene a la mente, luego ejecuta `/refine` para que Copilot lo reescriba en un prompt preciso y bien estructurado antes de enviarlo. Esto es especialmente útil cuando eres nuevo en herramientas de IA y todavía estás aprendiendo a escribir prompts efectivos.

> 💡 **Autocompletado con Tab**: Al escribir un comando con barra, presiona **Tab** para autocompletar el nombre del comando o recorrer los subcomandos y argumentos disponibles. Esto es especialmente útil cuando no recuerdas el nombre exacto de un comando.

> 💡 **Encolar prompts mientras Copilot está ocupado**: Si Copilot está en medio de una tarea y se te ocurre lo siguiente que quieres que haga, simplemente escríbelo y presiona **Enter**. Copilot lo ejecutará automáticamente cuando la tarea actual termine, así que no tienes que esperar.

¡Eso es todo para comenzar! A medida que te familiarices, puedes explorar comandos adicionales.

> 📚 **Documentación oficial**: [Referencia de comandos CLI](https://docs.github.com/copilot/reference/cli-command-reference) para la lista completa de comandos y banderas.

<details>
<summary>📚 <strong>Comandos adicionales</strong> (haz clic para expandir)</summary>

> 💡 Los comandos esenciales anteriores cubren gran parte de lo que harás en el uso diario. Esta referencia está aquí para cuando estés listo para explorar más.

### Entorno de agentes

| Comando | Qué hace |
|---------|--------------|
| `/agent` | Examinar y seleccionar entre los agentes disponibles |
| `/env` | Mostrar detalles del entorno cargado — qué instrucciones, servidores MCP, skills, agentes y plugins están activos |
| `/init` | Inicializar las instrucciones de Copilot para tu repositorio |
| `/instructions` | Ver y gestionar todos los archivos de instrucciones cargados para la sesión actual |
| `/mcp` | Abrir el panel de plugins (centrado en servidores MCP); usa `/mcp config` para el asistente de configuración dedicado de MCP |
| `/plugin` | Abrir el panel de plugins para explorar, instalar, habilitar y actualizar plugins |
| `/settings` | Abrir un diálogo interactivo para explorar y editar todos los ajustes de usuario en un solo lugar |
| `/skills` | Abrir el panel de plugins (centrado en skills) para descubrir y gestionar skills |
| `/subagents` | Ver y gestionar subagentes en ejecución en la sesión actual |

> 💡 Los agentes se tratan en [Capítulo 04](../04-agents-custom-instructions/README.md), los skills se tratan en [Capítulo 05](../05-skills/README.md), y los servidores MCP se tratan en [Capítulo 06](../06-mcp-servers/README.md).

### Modelos y subagentes

| Comando | Qué hace |
|---------|--------------|
| `/config` | Ver o establecer valores predeterminados persistentes (por ejemplo, `/config model` para establecer tu modelo predeterminado para todas las sesiones futuras) |
| `/delegate` | Delegar una tarea al agente en la nube de GitHub Copilot |
| `/fleet` | Dividir una tarea compleja en subtareas paralelas para una finalización más rápida |
| `/model` | Mostrar o cambiar el modelo de IA solo para la sesión actual |
| `/tasks` | Ver subagentes en segundo plano y sesiones de shell desacopladas |

### Código

| Comando | Qué hace |
|---------|--------------|
| `/diff` | Revisar los cambios realizados en el directorio actual |
| `/pr` | Operar sobre pull requests para la rama actual |
| `/research` | Realizar investigación profunda usando GitHub y fuentes web |
| `/review` | Ejecutar el agente de revisión de código para analizar cambios |
| `/terminal-setup` | Habilitar soporte de entrada multilínea (shift+enter y ctrl+enter) |

### Permisos

| Comando | Qué hace |
|---------|--------------|
| `/add-dir <directory>` | Agregar un directorio a la lista permitida |
| `/allow-all [on\|off\|show]` | Aprobar automáticamente todas las solicitudes de permisos; usa `on` para activar, `off` para desactivar, `show` para comprobar el estado actual |
| `/permissions` | Cambiar entre modos de aprobación (interactive, plan, autopilot) para controlar cuánto puede hacer Copilot sin preguntar |
| `/yolo` | Alias rápido para `/allow-all on` — aprueba automáticamente todas las solicitudes de permisos. |
| `/cwd`, `/cd [directory]` | Ver o cambiar el directorio de trabajo |
| `/list-dirs` | Mostrar todos los directorios permitidos |

> ⚠️ **Usa con precaución**: `/allow-all` y `/yolo` omiten las solicitudes de confirmación. Genial para proyectos de confianza, pero ten cuidado con código no confiable.

### Sesión

| Comando | Qué hace |
|---------|--------------|
| `/clear` | Abandonar la sesión actual (no se guarda historial) y comenzar una conversación nueva |
| `/compact` | Resumir la conversación para reducir el uso de contexto (opcionalmente añadir instrucciones de enfoque, p.ej. `/compact focus on the bug list`) |
| `/context` | Mostrar uso de tokens de la ventana de contexto y su visualización |
| `/keep-alive` | Evitar que tu sistema entre en reposo mientras Copilot CLI está activo — útil para tareas de larga duración en un portátil |
| `/memory [on\|off\|show]` | Activar, desactivar o ver la memoria persistente — hechos y preferencias recordados entre todas las sesiones |
| `/new` | Termina la sesión actual (guardándola en el historial para búsqueda/continuación) y comienza una conversación nueva. |
| `/resume` | Cambiar a otra sesión (opcionalmente especifica el ID o nombre de la sesión) |
| `/rename` | Renombrar la sesión actual (omite el nombre para que se genere uno automáticamente) |
| `/rewind` | Abrir un selector de línea de tiempo para retroceder a cualquier punto anterior de la conversación; opcionalmente restaura los archivos que Copilot cambió (funciona sin git) |
| `/usage` | Mostrar métricas y estadísticas de uso de la sesión, incluyendo barras de progreso de cuota |
| `/session` | Mostrar información de la sesión y resumen del espacio de trabajo; usa `/session delete`, `/session delete <id>`, o `/session delete-all` para eliminar sesiones |
| `/share` | Exportar la sesión como un archivo markdown, un gist de GitHub o un archivo HTML autónomo |
| `/every <interval> <prompt>` | Programar un prompt para ejecutarse en un intervalo recurrente (p.ej., `/every 1h summarize new commits`). Usa lenguaje natural para el intervalo. `/loop` es un alias de `/every`. |
| `/after <time> <prompt>` | Programar un prompt para ejecutarse una vez después de un retraso (p.ej., `/after 30m run tests`). Usa lenguaje natural para el tiempo. |

> 💡 **Pestaña Sesiones**: La interfaz interactiva de Copilot CLI incluye una **pestaña Sesiones** en la parte superior de la ventana. Puedes usarla para ver y cambiar entre múltiples sesiones que se ejecutan al mismo tiempo. Presiona `n` en la pestaña Sesiones para iniciar una nueva sesión sin cerrar la que tienes abierta.

### Visualización

| Comando | Qué hace |
|---------|--------------|
| `/statusline` (or `/footer`) | Personalizar qué elementos aparecen en la barra de estado en la parte inferior de la sesión (directorio, rama, esfuerzo, ventana de contexto, cuota) |
| `/theme` | Ver o establecer el tema del terminal |
| `/vim` | Activar o desactivar el modo Vim para edición modal en el composer. Escribe de forma natural con atajos de Vim como `hjkl` para navegación e `i`, `a`, `o` para el modo insertar |
| `/voice` | Dicta tu prompt usando reconocimiento de voz local — habla de forma natural en lugar de escribir |

### Ayuda y comentarios

| Comando | Qué hace |
|---------|--------------|
| `/app` | Abrir la app de GitHub (o la versión web como alternativa) directamente desde la CLI |
| `/changelog` | Mostrar el changelog de las versiones de la CLI |
| `/feedback` | Enviar comentarios a GitHub |
| `/help` | Mostrar todos los comandos disponibles |

### Comandos de shell rápidos

Ejecuta comandos de shell directamente sin IA anteponiendo `!`:

```bash
copilot

> !git status
# Ejecuta git status directamente, omitiendo la IA

> !python -m pytest tests/
# Ejecuta pytest directamente
```

### Cambiar modelos

Copilot CLI es compatible con múltiples modelos de IA de OpenAI, Anthropic, Google y otros. Los modelos disponibles dependen de tu nivel de suscripción y de la región. Usa `/model` para ver tus opciones y cambiar entre ellas:

```bash
copilot
> /model

# Muestra los modelos disponibles y te permite elegir uno. Selecciona Sonnet 4.5.
```

> 💡 **Modelo de sesión vs persistente**: El comando `/model` cambia el modelo solo para la **sesión actual**. Cuando inicias una nueva sesión, Copilot volverá a usar el predeterminado. Para establecer un modelo predeterminado permanente para todas las sesiones futuras, usa `/config model`.

> 💡 **Consejo**: Algunos modelos consumen más "premium requests" que otros. Los modelos marcados **1x** (como Claude Sonnet 4.5) son un gran predeterminado. Son capaces y eficientes. Los modelos con multiplicadores más altos usan tu cuota de premium requests más rápido, así que guárdalos para cuando realmente los necesites.

> 💡 **¿No estás seguro de qué modelo elegir?** Selecciona **`Auto`** en el selector de modelos para permitir que Copilot elija automáticamente el mejor modelo disponible para cada sesión. Es un gran valor predeterminado si estás comenzando y no quieres preocuparte por la selección del modelo.

> 💡 **Atajos de familia de modelos**: También puedes escribir un alias corto de familia — como `opus`, `sonnet`, `haiku`, `gpt`, o `gemini` — directamente en el selector `/model` en lugar de desplazarte por la lista completa. Copilot elegirá el mejor modelo disponible de esa familia para ti.

> 💡 **Navegación del selector de modelos**: El selector de modelos ahora agrupa los modelos en secciones — **Recientes**, **Recomendados** y **Nuevos** — para que puedas encontrar rápidamente el modelo que usaste por última vez o probar lo que hay de nuevo. Usa **Shift+Tab** dentro del selector para cambiar entre vistas de agrupación.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

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

### Planificar una función

Usa `/plan` para que Copilot CLI diseñe una implementación antes de escribir código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revisar el plan
# Aprobar o modificar
# Vigilar su implementación paso a paso
```

### Automatizar con el modo programático

La opción `-p` te permite ejecutar Copilot CLI directamente desde tu terminal sin entrar en modo interactivo. Copia y pega el siguiente script en tu terminal (no dentro de Copilot) desde la raíz del repositorio para revisar todos los archivos Python de la app de libros.

```bash
# Revisar todos los archivos Python en la aplicación del libro.
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# Revisar todos los archivos Python en la aplicación de libros
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

## 💡 Consejo: Controla tu sesión de CLI desde la web o el móvil

GitHub Copilot CLI admite **sesiones remotas**, permitiéndote monitorizar e interactuar con una sesión CLI en ejecución desde un navegador web (en escritorio o móvil) o la app GitHub Mobile sin estar físicamente en tu terminal.

Inicia una sesión remota con la opción `--remote`:

```bash
copilot --remote
```

Copilot CLI mostrará un enlace y proporcionará acceso a un código QR. Abre el enlace en tu teléfono o en una pestaña del navegador de escritorio para ver la sesión en tiempo real, enviar prompts de seguimiento, revisar planes y dirigir el agente de forma remota. Las sesiones son específicas por usuario, por lo que solo puedes acceder a tus propias sesiones de Copilot CLI.

También puedes habilitar el acceso remoto desde dentro de una sesión activa en cualquier momento:

```
> /remote
```

Detalles adicionales sobre las sesiones remotas se pueden encontrar en la [documentación de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Tarea

### Desafío principal: Mejorar las utilidades de la app de libros

Los ejemplos prácticos se centraron en revisar y refactorizar `book_app.py`. Ahora practica las mismas habilidades en un archivo diferente, `utils.py`:

1. Inicia una sesión interactiva: `copilot`
2. Pide a Copilot CLI que resuma el archivo: "Resume @samples/book-app-project/utils.py y explica qué hace cada función en este archivo"
3. Pídele que añada validación de entrada: "Agrega validación a `get_user_choice()` para que maneje entradas vacías y entradas no numéricas"
4. Pídele que mejore el manejo de errores: "¿Qué sucede si `get_book_details()` recibe una cadena vacía para el título? Añade comprobaciones para ello."
5. Pídele un docstring: "Agrega un docstring completo a `get_book_details()` con descripciones de los parámetros y valores de retorno"
6. Observa cómo el contexto se transmite entre las indicaciones. Cada mejora se basa en la anterior
7. Sal con `/exit`

**Criterios de éxito**: Deberías tener un `utils.py` mejorado con validación de entrada, manejo de errores y un docstring, todo construido mediante una conversación de múltiples turnos.

<details>
<summary>💡 Sugerencias (haz clic para expandir)</summary>

**Ejemplos de indicaciones para probar:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**Problemas comunes:**
- Si Copilot CLI hace preguntas aclaratorias, respóndelas naturalmente
- El contexto se mantiene, por lo que cada indicación se basa en la anterior
- Usa `/clear` si quieres empezar de nuevo

</details>

### Desafío adicional: Compara los modos

Los ejemplos usaron `/plan` para una función de búsqueda y `-p` para revisiones por lotes. Ahora prueba los tres modos en una nueva tarea única: agregar un método `list_by_year()` a la clase `BookCollection`:

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
| Escribir `exit` en lugar de `/exit` | Copilot CLI trata "exit" como una indicación, no como un comando | Los comandos con barra siempre comienzan con `/` |
| Usar `-p` para conversaciones de varios turnos | Cada llamada con `-p` está aislada y no tiene memoria de llamadas anteriores | Usa el modo interactivo (`copilot`) para conversaciones que se construyen con contexto |
| Olvidar las comillas alrededor de las indicaciones con `$` o `!` | La shell interpreta los caracteres especiales antes de que Copilot CLI los vea | Encierra las indicaciones entre comillas simples: `copilot -p 'What does $HOME mean?'` |
| Presionar Esc una vez para cancelar una tarea en ejecución | Una sola pulsación de Esc ya no cancela trabajos en curso (para prevenir accidentes) | Pulsa **Esc** dos veces para cancelar mientras Copilot CLI está procesando |

### Solución de problemas

**"Model not available"** - Tu suscripción puede no incluir todos los modelos. Usa `/model` para ver qué está disponible.

**"Context too long"** - Tu conversación ha usado toda la ventana de contexto. Usa `/new` para iniciar una nueva sesión.

**"Rate limit exceeded"** - Espera unos minutos e inténtalo de nuevo. Considera usar el modo programático para operaciones por lotes con retardos.

</details>

---

# Resumen

## 🔑 Puntos clave

1. **El modo interactivo** es para exploración e iteración: el contexto se mantiene. Es como tener una conversación con alguien que recuerda lo que has dicho hasta ese momento.
2. **El modo Plan** se usa normalmente para tareas más complejas. Revísalo antes de implementarlo.
3. **El modo programático** es para automatización. No se necesita interacción.
4. **Comandos esenciales** (`/ask`, `/help`, `/clear`, `/new`, `/plan`, `/research`, `/model`, `/exit`) cubren la mayor parte del uso diario.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ahora que entiendes los tres modos, aprendamos cómo proporcionar contexto sobre tu código a Copilot CLI.

En **[Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md)**, aprenderás:

- La sintaxis `@` para referenciar archivos y directorios
- Gestión de sesiones con `--resume` y `--continue`
- Cómo la gestión de contexto hace a Copilot CLI realmente potente

---

**[← Volver al inicio del curso](../README.md)** | **[Continuar al Capítulo 02 →](../02-context-conversations/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->