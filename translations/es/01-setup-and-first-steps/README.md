<!--
---
id: CopilotCLI-01
title: !translate Primeros pasos
description: !translate Experimenta GitHub Copilot CLI mediante demostraciones prácticas, y aprende cuándo usar los modos interactivo, plan y programmatic.
audience: Desarrolladores / Estudiantes / Usuarios de terminal
slug: first-steps
weight: 2
---
-->

![Capítulo 01: Primeros pasos](../../../01-setup-and-first-steps/assets/chapter-header.png)

> **Mira cómo la IA encuentra errores al instante, explica código confuso y genera scripts funcionales. Luego aprende tres formas diferentes de usar GitHub Copilot CLI.**

¡En este capítulo comienza la magia! Experimentarás de primera mano por qué los desarrolladores describen GitHub Copilot CLI como tener a un ingeniero sénior al alcance de la mano. Verás a la IA encontrar fallos de seguridad en segundos, obtendrás explicaciones de código complejo en inglés claro y generarás scripts funcionales al instante. Después dominarás los tres modos de interacción (Interactive, Plan y Programmatic) para que sepas exactamente cuál usar para cada tarea.

> ⚠️ **Requisitos previos**: Asegúrate de haber completado primero **[Capítulo 00: Inicio rápido](../00-quick-start/README.md)**. Necesitarás tener GitHub Copilot CLI instalado y autenticado antes de ejecutar las demostraciones a continuación.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Experimentar el aumento de productividad que GitHub Copilot CLI ofrece mediante demostraciones prácticas
- Elegir el modo correcto (Interactive, Plan o Programmatic) para cualquier tarea
- Usar comandos con barra (slash) para controlar tus sesiones

> ⏱️ **Tiempo estimado**: ~45 minutos (15 min lectura + 30 min práctico)

---

# Tu primera experiencia con Copilot CLI

<img src="../../../01-setup-and-first-steps/assets/first-copilot-experience.png" alt="Desarrollador sentado en un escritorio con código en el monitor y partículas brillantes que representan la asistencia de la IA" width="800"/>

Sumérgete y ve lo que Copilot CLI puede hacer.

---

## Familiarízate: tus primeros prompts

Antes de sumergirte en las demostraciones impresionantes, comencemos con algunos prompts simples que puedes probar ahora mismo. ¡**No se necesita un repositorio de código**! Simplemente abre una terminal y inicia Copilot CLI:

```bash
copilot
```

Prueba estos prompts amigables para principiantes:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

¿No usas Python? ¡No hay problema! Simplemente haz preguntas sobre el lenguaje que prefieras.

Fíjate lo natural que se siente. Solo haz preguntas como lo harías con un colega. Cuando termines de explorar, escribe `/exit` para salir de la sesión.

**La idea clave**: GitHub Copilot CLI es conversacional. No necesitas una sintaxis especial para empezar. Simplemente haz preguntas en inglés simple.

## Verlo en acción

Ahora veamos por qué los desarrolladores llaman a esto “tener a un ingeniero sénior al alcance de la mano.”

> 📖 **Cómo leer los ejemplos**: Las líneas que empiezan con `>` son prompts que escribes dentro de una sesión interactiva de Copilot CLI. Las líneas sin el prefijo `>` son comandos de shell que ejecutas en tu terminal.

> 💡 **Sobre los ejemplos de salida**: Las salidas de ejemplo mostradas a lo largo de este curso son ilustrativas. Dado que las respuestas de Copilot CLI varían cada vez, tus resultados diferirán en redacción, formato y nivel de detalle. Enfócate en el *tipo* de información devuelta, no en el texto exacto.

### Demo 1: Revisión de código en segundos

El curso incluye archivos de ejemplo con problemas intencionales de calidad de código. Si estás trabajando en tu máquina local y aún no has clonado el repositorio, ejecuta el comando `git clone` abajo, navega a la carpeta `copilot-cli-for-beginners` y luego ejecuta el comando `copilot`.

```bash
# Clona el repositorio del curso si trabajas localmente y aún no lo has hecho
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Inicia Copilot
copilot
```

Una vez dentro de la sesión interactiva de Copilot CLI, ejecuta lo siguiente:

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **¿Para qué sirve el símbolo `@`?** El símbolo `@` indica a Copilot CLI que lea un archivo. Aprenderás todo sobre esto en el Capítulo 02. Por ahora, simplemente copia el comando exactamente como se muestra.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de revisión de código](../../../01-setup-and-first-steps/assets/code-review-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

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
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de explicación de código](../../../01-setup-and-first-steps/assets/explain-code-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

---

**Qué sucede**: (tu salida será diferente) Copilot CLI lee el archivo, entiende el código y lo explica en inglés claro.

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

¿Necesitas una función para la que de otro modo pasarías 15 minutos buscando en Google? Aún dentro de tu sesión:

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

**Conclusión**: Gratificación instantánea, y permaneciste en una sesión continua todo el tiempo.

---

# Modos y comandos

<img src="../../../01-setup-and-first-steps/assets/modes-and-commands.png" alt="Panel de control futurista con pantallas brillantes, diales y ecualizadores que representan los modos y comandos de Copilot CLI" width="800"/>

Acabas de ver lo que Copilot CLI puede hacer. Ahora entendamos *cómo* usar estas capacidades de manera efectiva. La clave es saber cuál de los tres modos de interacción usar para distintas situaciones.

> 💡 **Nota**: Copilot CLI también tiene un modo **Autopilot** en el que realiza tareas sin esperar tu entrada. Es potente pero requiere otorgar permisos completos y usa solicitudes premium de forma autónoma. Este curso se centra en los tres modos que aparecen a continuación. Te indicaremos Autopilot una vez que te sientas cómodo con lo básico.

---

## 🧩 Analogía del mundo real: salir a comer

Piensa en usar GitHub Copilot CLI como salir a comer. Desde planear el trayecto hasta hacer el pedido, diferentes situaciones requieren enfoques distintos:

| Modo | Analogía gastronómica | Cuándo usarlo |
|------|----------------|-------------|
| **Plan** | Ruta GPS hasta el restaurante | Tareas complejas - traza la ruta, revisa las paradas, acuerda el plan y luego conduce |
| **Interactive** | Hablar con el camarero | Exploración e iteración - haz preguntas, personaliza, recibe retroalimentación en tiempo real |
| **Programmatic** | Pedido en un autoservicio (drive-through) | Tareas rápidas y específicas - mantente en tu entorno, obtén un resultado rápido |

Al igual que al salir a comer, aprenderás de forma natural cuándo cada enfoque es el adecuado.

<img src="../../../01-setup-and-first-steps/assets/ordering-food-analogy.png" alt="Tres maneras de usar GitHub Copilot CLI - Modo Plan (ruta GPS al restaurante), Modo Interactive (hablar con el camarero), Modo Programmatic (autoservicio)" width="800"/>

*Elige tu modo según la tarea: Plan para trazarla primero, Interactive para colaboración de ida y vuelta, Programmatic para resultados rápidos de una sola ejecución*

### ¿Con cuál modo debo empezar?

**Comienza con el modo Interactive.**
- Puedes experimentar y hacer preguntas de seguimiento
- El contexto se construye de forma natural mediante la conversación
- Los errores son fáciles de corregir con `/clear`

Una vez que te sientas cómodo, prueba:
- **Programmatic mode** (`copilot -p "<your prompt>"`) para preguntas rápidas y puntuales
- **Plan mode** (`/plan`) cuando necesites planificar con más detalle antes de codificar

---

## Los tres modos

### Modo 1: Interactive Mode (comienza aquí)

<img src="../../../01-setup-and-first-steps/assets/interactive-mode.png" alt="Modo Interactive - Como hablar con un camarero que puede responder preguntas y ajustar el pedido" width="250"/>

**Ideal para**: Exploración, iteración y conversaciones de varios turnos. Como hablar con un camarero que puede responder preguntas, recibir comentarios y ajustar el pedido al instante.

Inicia una sesión interactiva:

```bash
copilot
```

Como has visto hasta ahora, verás un indicador donde puedes escribir de forma natural. Para obtener ayuda sobre los comandos disponibles, simplemente escribe:

```
> /help
```

**Idea clave**: Interactive mode mantiene el contexto. Cada mensaje se construye sobre los anteriores, como en una conversación real.

#### Ejemplo de Interactive Mode

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Fíjate cómo cada prompt se basa en la respuesta anterior. Estás manteniendo una conversación, no empezando desde cero cada vez.

---

### Modo 2: Plan Mode

<img src="../../../01-setup-and-first-steps/assets/plan-mode.png" alt="Modo Plan - Como planear una ruta antes de un viaje usando GPS" width="250"/>

**Ideal para**: Tareas complejas donde quieres revisar el enfoque antes de ejecutarlo. Similar a planear una ruta antes de un viaje usando GPS.

El modo Plan te ayuda a crear un plan paso a paso antes de escribir código. Usa el comando `/plan`, presiona **Shift+Tab** para cambiar al modo Plan:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Consejo**: **Shift+Tab** alterna entre modos: Interactive → Plan → Autopilot. Púlsalo en cualquier momento durante una sesión interactiva para cambiar de modo sin escribir un comando.

También puedes iniciar Copilot CLI directamente en modo plan usando la opción `--plan`:

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

**Idea clave**: El modo Plan te permite revisar y modificar el enfoque antes de escribir código. Una vez que un plan está completo, incluso puedes pedirle a Copilot CLI que lo guarde en un archivo para referencia posterior. Por ejemplo, "Save this plan to `mark_as_read_plan.md`" crearía un archivo markdown con los detalles del plan.

> 💡 **¿Quieres algo más complejo?** Prueba: `/plan Add search and filter capabilities to the book app`. El modo Plan escala desde funciones simples hasta aplicaciones completas.

> 📚 **Modo Autopilot**: Puede que hayas notado que Shift+Tab alterna hasta un tercer modo llamado **Autopilot**. En el modo autopilot, Copilot ejecuta un plan completo sin esperar tu entrada después de cada paso — como encargarle una tarea a un colega y decir "avísame cuando termines". El flujo típico es plan → aceptar → autopilot, lo que significa que debes ser bueno escribiendo planes primero. También puedes iniciar directamente en autopilot con `copilot --autopilot`. Familiarízate primero con los modos Interactive y Plan, luego consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) cuando estés listo.

---

### Modo 3: Programmatic Mode

<img src="../../../01-setup-and-first-steps/assets/programmatic-mode.png" alt="Modo Programmatic - Como usar un autoservicio para un pedido rápido" width="250"/>

**Ideal para**: Automatización, scripts, CI/CD, comandos de una sola ejecución. Como usar un autoservicio para un pedido rápido sin tener que hablar con un camarero.

Usa la opción `-p` para comandos puntuales que no necesitan interacción:

```bash
# Generar código
copilot -p "Write a function that checks if a number is even or odd"

# Obtener ayuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Idea clave**: Programmatic mode te da una respuesta rápida y sale. Sin conversación, solo entrada → salida.

<details>
<summary>📚 <strong>Ir más lejos: Usar el modo Programmatic en scripts</strong> (haz clic para expandir)</summary>

Una vez que te sientas cómodo, puedes usar `-p` en scripts de shell:

```bash
#!/bin/bash

# Generar mensajes de commit automáticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar un archivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Sobre `--allow-all`**: Esta opción omite todas las solicitudes de permiso, permitiendo que Copilot CLI lea archivos, ejecute comandos y acceda a URLs sin preguntar primero. Esto es necesario para el modo programmatic (`-p`) ya que no hay una sesión interactiva para aprobar acciones. Usa `--allow-all` solo con prompts que hayas escrito tú mismo y en directorios de confianza. Nunca lo uses con entrada no confiable ni en directorios sensibles.

</details>

---

## Comandos slash esenciales

Estos comandos son geniales para aprender inicialmente mientras comienzas con Copilot CLI:

| Comando | Qué hace | Cuándo usarlo |
|---------|--------------|-------------|
| `/ask` | Haz una pregunta rápida sin que afecte el historial de la conversación | Cuando quieres una respuesta rápida sin desviar tu tarea actual |
| `/clear` | Borra la conversación y comienza de nuevo | Al cambiar de tema |
| `/help` | Muestra todos los comandos disponibles | Cuando olvidas un comando |
| `/model` | Muestra o cambia el modelo de IA | Cuando quieres cambiar el modelo de IA |
| `/plan` | Planifica tu trabajo antes de codificar | Para características más complejas |
| `/refine` | Reescribe un prompt bruto o de flujo de conciencia en uno claro y enfocado | Cuando tu prompt se siente desordenado y quieres mejores resultados |
| `/research` | Investigación profunda utilizando GitHub y fuentes web | Cuando necesitas investigar un tema antes de codificar |
| `/exit` | Finaliza la sesión | Cuando has terminado |


> 💡 **`/ask` vs chat normal**: Normalmente cada mensaje que envías pasa a formar parte de la conversación en curso y afecta a respuestas futuras. `/ask` es un atajo "fuera de registro" — perfecto para preguntas rápidas y puntuales como `/ask What does YAML mean?` sin contaminar el contexto de tu sesión.

> 💡 **`/refine` para mejores prompts**: ¿No estás seguro de si tu prompt es lo suficientemente claro? Escríbelo tal como te venga a la mente, luego ejecuta `/refine` para que Copilot lo reescriba en un prompt preciso y bien estructurado antes de enviarlo. Esto es especialmente útil cuando eres nuevo en las herramientas de IA y aún estás aprendiendo a redactar prompts efectivos.

> 💡 **Autocompletar con Tab**: Al escribir un comando con barra, presiona **Tab** para autocompletar el nombre del comando o recorrer los subcomandos y argumentos disponibles. Esto es especialmente útil cuando no recuerdas el nombre exacto de un comando.

¡Eso es todo para empezar! A medida que te familiarices, puedes explorar comandos adicionales.

> 📚 **Documentación oficial**: [CLI command reference](https://docs.github.com/copilot/reference/cli-command-reference) para la lista completa de comandos y banderas.

<details>
<summary>📚 <strong>Comandos adicionales</strong> (haz clic para expandir)</summary>

> 💡 Los comandos esenciales anteriores cubren gran parte de lo que harás en el uso diario. Esta referencia está aquí para cuando estés listo para explorar más.

### Entorno del agente

| Comando | Qué hace |
|---------|--------------|
| `/agent` | Examinar y seleccionar entre los agentes disponibles |
| `/env` | Mostrar detalles del entorno cargado — qué instrucciones, servidores MCP, habilidades, agentes y complementos están activos |
| `/init` | Inicializar las instrucciones de Copilot para tu repositorio |
| `/mcp` | Gestionar la configuración del servidor MCP |
| `/settings` | Abrir un diálogo interactivo para explorar y editar todos los ajustes de usuario en un solo lugar |
| `/skills` | Gestionar habilidades para capacidades mejoradas |

> 💡 Los agentes se tratan en [Capítulo 04](../04-agents-custom-instructions/README.md), las habilidades se tratan en [Capítulo 05](../05-skills/README.md), y los servidores MCP se tratan en [Capítulo 06](../06-mcp-servers/README.md).

### Modelos y subagentes

| Comando | Qué hace |
|---------|--------------|
| `/delegate` | Delegar la tarea a un agente en la nube de GitHub Copilot |
| `/fleet` | Dividir una tarea compleja en subtareas paralelas para completarla más rápido |
| `/model` | Mostrar o cambiar el modelo de IA |
| `/tasks` | Ver subagentes en segundo plano y sesiones de shell separadas |

### Código

| Comando | Qué hace |
|---------|--------------|
| `/diff` | Revisar los cambios realizados en el directorio actual |
| `/pr` | Operar sobre pull requests para la rama actual |
| `/research` | Realizar una investigación profunda usando GitHub y fuentes web |
| `/review` | Ejecutar el agente de revisión de código para analizar cambios |
| `/terminal-setup` | Habilitar soporte de entrada multilínea (shift+enter y ctrl+enter) |

### Permisos

| Comando | Qué hace |
|---------|--------------|
| `/add-dir <directory>` | Agregar un directorio a la lista permitida |
| `/allow-all [on\|off\|show]` | Aprueba automáticamente todas las solicitudes de permisos; usa `on` para habilitar, `off` para deshabilitar, `show` para comprobar el estado actual |
| `/yolo` | Alias rápido para `/allow-all on` — aprueba automáticamente todas las solicitudes de permisos. |
| `/cwd`, `/cd [directory]` | Ver o cambiar el directorio de trabajo |
| `/list-dirs` | Mostrar todos los directorios permitidos |

> ⚠️ **Usar con precaución**: `/allow-all` y `/yolo` omiten los cuadros de confirmación. Genial para proyectos de confianza, pero ten cuidado con código no confiable.

### Sesión

| Comando | Qué hace |
|---------|--------------|
| `/clear` | Abandona la sesión actual (no se guarda historial) y comienza una conversación nueva |
| `/compact` | Resumir la conversación para reducir el uso de contexto (opcionalmente agrega instrucciones de enfoque, p. ej. `/compact focus on the bug list`) |
| `/context` | Mostrar uso de tokens de la ventana de contexto y visualización |
| `/keep-alive` | Evitar que tu sistema entre en suspensión mientras Copilot CLI está activo — útil para tareas de larga duración en un portátil |
| `/memory [on\|off\|show]` | Habilitar, deshabilitar o ver la memoria persistente — hechos y preferencias recordados en todas las sesiones |
| `/new` | Termina la sesión actual (guardándola en el historial para búsqueda/reaanudación) y comienza una conversación nueva. |
| `/resume` | Cambiar a una sesión diferente (opcionalmente especifica session ID o nombre) |
| `/rename` | Renombrar la sesión actual (omitir el nombre para generar uno automáticamente) |
| `/rewind` | Abrir un selector de línea de tiempo para retroceder a cualquier punto anterior de la conversación |
| `/usage` | Mostrar métricas y estadísticas de uso de la sesión, incluyendo barras de progreso de cuota |
| `/session` | Mostrar información de la sesión y resumen del espacio de trabajo; usa `/session delete`, `/session delete <id>`, o `/session delete-all` para eliminar sesiones |
| `/share` | Exportar sesión como un archivo markdown, GitHub gist, o archivo HTML autocontenido |
| `/every <interval> <prompt>` | Programar un prompt para que se ejecute en un intervalo recurrente (por ejemplo, `/every 1h summarize new commits`). Usa lenguaje natural para el intervalo. `/loop` es un alias de `/every`. |
| `/after <time> <prompt>` | Programar un prompt para que se ejecute una vez después de un retraso (p. ej., `/after 30m run tests`). Usa lenguaje natural para el tiempo. |

### Visualización

| Comando | Qué hace |
|---------|--------------|
| `/statusline` (or `/footer`) | Personalizar qué ítems aparecen en la barra de estado en la parte inferior de la sesión (directorio, rama, esfuerzo, ventana de contexto, cuota) |
| `/theme` | Ver o establecer el tema del terminal |
| `/voice` | Dicta tu prompt usando reconocimiento de voz local — habla de forma natural en lugar de escribir |

### Ayuda y comentarios

| Comando | Qué hace |
|---------|--------------|
| `/app` | Abrir la app de GitHub (o fallback en el navegador) directamente desde la CLI |
| `/changelog` | Mostrar el registro de cambios de las versiones de la CLI |
| `/feedback` | Enviar comentarios a GitHub |
| `/help` | Mostrar todos los comandos disponibles |

### Comandos rápidos de shell

Ejecuta comandos de shell directamente sin IA anteponiendo `!`:

```bash
copilot

> !git status
# Ejecuta git status directamente, sin pasar por la IA

> !python -m pytest tests/
# Ejecuta pytest directamente
```

### Cambiar modelos

Copilot CLI admite múltiples modelos de IA de OpenAI, Anthropic, Google y otros. Los modelos disponibles para ti dependen de tu nivel de suscripción y región. Usa `/model` para ver tus opciones y cambiar entre ellos:

```bash
copilot
> /model

# Muestra los modelos disponibles y te permite elegir uno. Selecciona Sonnet 4.5.
```

> 💡 **Consejo**: Algunos modelos consumen más "solicitudes premium" que otros. Los modelos marcados **1x** (como Claude Sonnet 4.5) son una excelente opción por defecto. Son capaces y eficientes. Los modelos con multiplicadores más altos usan tu cuota de solicitudes premium más rápido, así que reserva esos para cuando realmente los necesites.

> 💡 **¿No sabes qué modelo elegir?** Selecciona **`Auto`** en el selector de modelos para que Copilot elija automáticamente el mejor modelo disponible para cada sesión. Es una excelente opción por defecto si estás comenzando y no quieres preocuparte por la selección de modelo.

> 💡 **Atajos por familia de modelos**: También puedes escribir un alias corto de familia — como `opus`, `sonnet`, `haiku`, `gpt` o `gemini` — directamente en el selector `/model` en lugar de desplazarte por la lista completa. Copilot elegirá el mejor modelo disponible de esa familia por ti.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Disposición acogedora de escritorio con monitor que muestra código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

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

Usa `/plan` para que Copilot CLI planifique una implementación antes de escribir código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revisar el plan
# Aprobar o modificar
# Observar su implementación paso a paso
```

### Automatizar con el modo programático

La bandera `-p` te permite ejecutar Copilot CLI directamente desde tu terminal sin entrar en modo interactivo. Copia y pega el siguiente script en tu terminal (no dentro de Copilot) desde la raíz del repositorio para revisar todos los archivos Python en la app de libros.

```bash
# Revisar todos los archivos Python en la aplicación de libros
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

2. **Desafío en modo Plan**: Ejecuta `/plan Add rating and review features to the book app`. Lee el plan con atención. ¿Tiene sentido?

3. **Desafío programático**: Ejecuta `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. ¿Funcionó en el primer intento?

---

## 💡 Consejo: Controla tu sesión de CLI desde la web o el móvil

GitHub Copilot CLI admite **sesiones remotas**, que te permiten monitorizar e interactuar con una sesión CLI en ejecución desde un navegador web (en escritorio o móvil) o la app GitHub Mobile sin estar físicamente en tu terminal.

Inicia una sesión remota con la bandera `--remote`:

```bash
copilot --remote
```

Copilot CLI mostrará un enlace y proporcionará acceso a un código QR. Abre el enlace en tu teléfono o en una pestaña del navegador de escritorio para ver la sesión en tiempo real, enviar prompts de seguimiento, revisar planes y guiar al agente de forma remota. Las sesiones son específicas por usuario, por lo que solo puedes acceder a tus propias sesiones de Copilot CLI.

También puedes habilitar el acceso remoto desde el interior de una sesión activa en cualquier momento:

```
> /remote
```

Detalles adicionales sobre sesiones remotas se pueden encontrar en la [documentación de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Tarea

### Desafío principal: Mejorar las utilidades de la app de libros

Los ejemplos prácticos se centraron en revisar y refactorizar `book_app.py`. Ahora practica las mismas habilidades en un archivo diferente, `utils.py`:

1. Inicia una sesión interactiva: `copilot`
2. Pídele a Copilot CLI que resuma el archivo: "Resume @samples/book-app-project/utils.py y explica qué hace cada función en este archivo"
3. Pídele que agregue validación de entrada: "Agrega validación a `get_user_choice()` para que maneje entradas vacías y entradas no numéricas"
4. Pídele que mejore el manejo de errores: "¿Qué ocurre si `get_book_details()` recibe una cadena vacía para el título? Agrega validaciones para eso."
5. Pídele una docstring: "Agrega una docstring completa a `get_book_details()` con descripciones de los parámetros y valores de retorno"
6. Observa cómo el contexto se mantiene entre prompts. Cada mejora se construye sobre la anterior
7. Sal con `/exit`

**Criterios de éxito**: Deberías tener un `utils.py` mejorado con validación de entrada, manejo de errores y una docstring, todo construido mediante una conversación de varias interacciones.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Prompts de ejemplo para probar:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**Problemas comunes:**
- Si Copilot CLI hace preguntas aclaratorias, respóndelas de forma natural
- El contexto se conserva, por lo que cada prompt se basa en el anterior
- Usa `/clear` si quieres empezar de nuevo

</details>

### Desafío extra: Compara los modos

Los ejemplos usaron `/plan` para una función de búsqueda y `-p` para revisiones por lotes. Ahora prueba los tres modos en una sola tarea nueva: agregar un método `list_by_year()` a la clase `BookCollection`:

1. **Interactivo**: `copilot` → pídele que diseñe y construya el método paso a paso
2. **Modo Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programático**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**Reflexión**: ¿Qué modo resultó más natural? ¿Cuándo usarías cada uno?

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Escribir `exit` en lugar de `/exit` | Copilot CLI trata "exit" como un prompt, no como un comando | Los comandos con barra siempre comienzan con `/` |
| Usar `-p` para conversaciones de múltiples turnos | Cada llamada con `-p` está aislada y no recuerda llamadas anteriores | Usa el modo interactivo (`copilot`) para conversaciones que construyan contexto |
| Olvidar las comillas alrededor de prompts con `$` o `!` | El shell interpreta caracteres especiales antes de que Copilot CLI los vea | Encierra los prompts entre comillas simples: `copilot -p 'What does $HOME mean?'` |

| Presionar Esc una vez para cancelar una tarea en ejecución | Un solo Esc ya no cancela el trabajo en curso (para evitar accidentes) | Presiona **Esc dos veces** para cancelar mientras Copilot CLI está procesando |

### Resolución de problemas

**"Model not available"** - Es posible que tu suscripción no incluya todos los modelos. Usa `/model` para ver qué está disponible.

**"Context too long"** - Tu conversación ha usado la ventana de contexto completa. Usa `/clear` para restablecer, o inicia una nueva sesión.

**"Rate limit exceeded"** - Espera unos minutos e inténtalo de nuevo. Considera usar el modo programático para operaciones por lotes con pausas.

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Interactive mode** es para exploración e iteración - el contexto se mantiene. Es como tener una conversación con alguien que recuerda lo que has dicho hasta ese momento.
2. **Plan mode** normalmente es para tareas más complejas. Revisa antes de implementar.
3. **Programmatic mode** es para automatización. No se necesita interacción.
4. **Essential commands** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`) cubren la mayoría de los usos diarios.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para obtener una lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Ahora que entiendes los tres modos, aprendamos cómo dar contexto a Copilot CLI sobre tu código.

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