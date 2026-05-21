![Capítulo 01: Primeros Pasos](../../../01-setup-and-first-steps/images/chapter-header.png)

> **Mira cómo la IA encuentra errores al instante, explica código confuso y genera scripts que funcionan. Luego aprende tres maneras diferentes de usar GitHub Copilot CLI.**

¡Este capítulo es donde comienza la magia! Experimentarás de primera mano por qué los desarrolladores describen a GitHub Copilot CLI como tener a un ingeniero sénior en marcación rápida. Verás a la IA encontrar fallos de seguridad en segundos, obtener explicaciones de código complejo en lenguaje sencillo y generar scripts funcionales al instante. Luego dominarás los tres modos de interacción (Interactivo, Plan y Programático) para saber exactamente cuál usar en cada tarea.

> ⚠️ **Prerequisitos**: Asegúrate de haber completado primero **[Capítulo 00: Inicio Rápido](../00-quick-start/README.md)**. Necesitarás tener GitHub Copilot CLI instalado y autenticado antes de ejecutar las demostraciones a continuación.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Experimentar el aumento de productividad que ofrece GitHub Copilot CLI mediante demostraciones prácticas
- Elegir el modo correcto (Interactivo, Plan o Programático) para cualquier tarea
- Usar comandos slash para controlar tus sesiones

> ⏱️ **Tiempo estimado**: ~45 minutos (15 min lectura + 30 min práctica)

---

# Tu primera experiencia con Copilot CLI

<img src="../../../01-setup-and-first-steps/images/first-copilot-experience.png" alt="Desarrollador sentado en un escritorio con código en el monitor y partículas brillantes que representan la asistencia de la IA" width="800"/>

Sumérgete y descubre lo que Copilot CLI puede hacer.

---

## Familiarízate: Tus primeros prompts

Antes de sumergirte en las demostraciones impresionantes, comencemos con algunos prompts sencillos que puedes probar ahora mismo. **No se necesita un repositorio de código**. Simplemente abre una terminal y inicia Copilot CLI:

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

**La idea clave**: GitHub Copilot CLI es conversacional. No necesitas una sintaxis especial para empezar. Solo pregunta en lenguaje natural.

## Verlo en acción

Ahora veamos por qué los desarrolladores dicen que esto es "tener a un ingeniero senior en marcación rápida".

> 📖 **Lectura de los ejemplos**: Las líneas que empiezan con `>` son prompts que escribes dentro de una sesión interactiva de Copilot CLI. Las líneas sin el prefijo `>` son comandos de shell que ejecutas en tu terminal.

> 💡 **Sobre los resultados de ejemplo**: Las salidas de ejemplo mostradas a lo largo de este curso son ilustrativas. Como las respuestas de Copilot CLI varían cada vez, tus resultados diferirán en redacción, formato y nivel de detalle. Enfócate en el *tipo* de información devuelta, no en el texto exacto.

### Demostración 1: Revisión de código en segundos

El curso incluye archivos de ejemplo con problemas intencionales de calidad de código. Si estás trabajando en tu máquina local y aún no has clonado el repositorio, por favor ejecuta el comando `git clone` que aparece abajo, navega a la carpeta `copilot-cli-for-beginners` y luego ejecuta el comando `copilot`.

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

> 💡 **¿Para qué se usa el símbolo `@`?** El símbolo `@` le indica a Copilot CLI que lea un archivo. Aprenderás todo sobre esto en el Capítulo 02. Por ahora, copia el comando exactamente como se muestra.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración de revisión de código](../../../01-setup-and-first-steps/images/code-review-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

---

**Conclusión**: Una revisión de código profesional en segundos. Una revisión manual tomaría... bueno... mucho más tiempo que eso.

---

### Demostración 2: Explicar código confuso

¿Alguna vez te has quedado mirando código preguntándote qué hace? Prueba esto en tu sesión de Copilot CLI:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración - Explicar código](../../../01-setup-and-first-steps/images/explain-code-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

---

**Qué sucede**: (tu salida variará) Copilot CLI lee el archivo, comprende el código y lo explica en un lenguaje sencillo.

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

¿Necesitas una función por la que de otro modo pasarías 15 minutos buscando en Google? Sigue en tu sesión:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración - Generar código](../../../01-setup-and-first-steps/images/generate-code-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

---

**Qué sucede**: Una función completa y funcional en segundos que puedes copiar-pegar-ejecutar.

Cuando termines de explorar, sal de la sesión:

```
> /exit
```

**Conclusión**: Gratificación instantánea, y te mantuviste en una sesión continua todo el tiempo.

---

# Modos y comandos

<img src="../../../01-setup-and-first-steps/images/modes-and-commands.png" alt="Panel de control futurista con pantallas luminosas, diales y ecualizadores que representan los modos y comandos de Copilot CLI" width="800"/>

Acabas de ver lo que Copilot CLI puede hacer. Ahora entendamos *cómo* usar estas capacidades de forma efectiva. La clave es saber cuál de los tres modos de interacción usar según la situación.

> 💡 **Nota**: Copilot CLI también tiene un modo **Autopilot** donde trabaja las tareas sin esperar tu entrada. Es poderoso pero requiere conceder permisos completos y usa solicitudes premium de forma autónoma. Este curso se centra en los tres modos que aparecen abajo. Te guiaremos hacia Autopilot una vez que estés cómodo con lo básico.

---

## 🧩 Analogía del mundo real: Salir a comer

Piensa en usar GitHub Copilot CLI como salir a comer. Desde planear el viaje hasta hacer el pedido, diferentes situaciones requieren diferentes enfoques:

| Modo | Analogía gastronómica | Cuándo usarlo |
|------|-----------------------|---------------|
| **Plan** | Ruta GPS al restaurante | Tareas complejas: traza la ruta, revisa las paradas, acuerda el plan y luego conduce |
| **Interactive** | Hablar con el camarero | Exploración e iteración: haz preguntas, personaliza, recibe retroalimentación en tiempo real |
| **Programmatic** | Pedido por ventanilla (drive-through) | Tareas rápidas y específicas: quédate en tu entorno y obtén un resultado rápido |

Al igual que al salir a comer, aprenderás de forma natural cuándo se siente mejor cada enfoque.

<img src="../../../01-setup-and-first-steps/images/ordering-food-analogy.png" alt="Tres maneras de usar GitHub Copilot CLI - Modo Plan (ruta GPS al restaurante), Modo Interactivo (hablar con el camarero), Modo Programático (drive-through)" width="800"/>

*Elige tu modo según la tarea: Plan para mapear primero, Interactivo para colaboración bidireccional, Programático para resultados rápidos de una sola vez*

### ¿Con qué modo debo empezar?

**Comienza con el modo Interactivo.**
- Puedes experimentar y hacer preguntas de seguimiento
- El contexto se construye naturalmente a través de la conversación
- Los errores son fáciles de corregir con `/clear`

Una vez que te sientas cómodo, prueba:
- **Modo Programático** (`copilot -p "<your prompt>"`) para preguntas rápidas y puntuales
- **Modo Plan** (`/plan`) cuando necesites planificar en detalle antes de codificar

---

## Los tres modos

### Modo 1: Modo interactivo (comienza aquí)

<img src="../../../01-setup-and-first-steps/images/interactive-mode.png" alt="Modo interactivo - Como hablar con un camarero que puede responder preguntas y ajustar el pedido" width="250"/>

**Ideal para**: Exploración, iteración, conversaciones de múltiples turnos. Como hablar con un camarero que puede responder preguntas, recibir feedback y ajustar el pedido sobre la marcha.

Inicia una sesión interactiva:

```bash
copilot
```

Como has visto hasta ahora, verás un prompt donde puedes escribir de forma natural. Para obtener ayuda sobre los comandos disponibles, simplemente escribe:

```
> /help
```

**Idea clave**: El modo interactivo mantiene el contexto. Cada mensaje se construye sobre los previos, como en una conversación real.

#### Ejemplo de modo interactivo

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Fíjate en cómo cada prompt se basa en la respuesta anterior. Estás teniendo una conversación, no empezando de cero cada vez.

---

### Modo 2: Modo Plan

<img src="../../../01-setup-and-first-steps/images/plan-mode.png" alt="Modo Plan - Como planear una ruta antes de un viaje usando GPS" width="250"/>

**Ideal para**: Tareas complejas donde quieres revisar el enfoque antes de ejecutarlo. Similar a planear una ruta antes de un viaje usando GPS.

El modo Plan te ayuda a crear un plan paso a paso antes de escribir cualquier código. Usa el comando `/plan`, presiona **Shift+Tab** para cambiar al Modo Plan:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Consejo**: **Shift+Tab** cicla entre modos: Interactivo → Plan → Autopilot. Púlsalo en cualquier momento durante una sesión interactiva para cambiar de modo sin escribir un comando.

También puedes iniciar Copilot CLI directamente en modo plan usando la bandera `--plan`:

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

**Idea clave**: El modo Plan te permite revisar y modificar el enfoque antes de que se escriba código. Una vez que un plan está completo, incluso puedes pedirle a Copilot CLI que lo guarde en un archivo para referencia posterior. Por ejemplo, "Guardar este plan en `mark_as_read_plan.md`" crearía un archivo markdown con los detalles del plan.

> 💡 **¿Quieres algo más complejo?** Prueba: `/plan Añadir capacidades de búsqueda y filtrado a la aplicación de libros`. El modo Plan escala desde funciones simples hasta aplicaciones completas.

> 📚 **Modo Autopilot**: Puede que hayas notado que Shift+Tab cicla por un tercer modo llamado **Autopilot**. En el modo autopilot, Copilot ejecuta todo un plan sin esperar tu entrada después de cada paso — como delegarle una tarea a un colega y decir "avísame cuando termines". El flujo típico es plan → aceptar → autopilot, lo que significa que necesitas saber escribir buenos planes primero. También puedes iniciar directamente en autopilot con `copilot --autopilot`. Familiarízate primero con los modos Interactivo y Plan, y luego consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) cuando estés listo.

---

### Modo 3: Modo programático

<img src="../../../01-setup-and-first-steps/images/programmatic-mode.png" alt="Modo programático - Como usar un drive-through para un pedido rápido" width="250"/>

**Ideal para**: Automatización, scripts, CI/CD, comandos de una sola ejecución. Como usar un drive-through para un pedido rápido sin necesidad de hablar con un camarero.

Usa la bandera `-p` para comandos puntuales que no requieren interacción:

```bash
# Generar código
copilot -p "Write a function that checks if a number is even or odd"

# Obtener ayuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Idea clave**: El modo programático te da una respuesta rápida y sale. Sin conversación, solo entrada → salida.

<details>
<summary>📚 <strong>Ir más allá: Usar el modo programático en scripts</strong> (haz clic para expandir)</summary>

Una vez que estés cómodo, puedes usar `-p` en scripts de shell:

```bash
#!/bin/bash

# Generar mensajes de commit automáticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar un archivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Sobre `--allow-all`**: Esta bandera omite todas las solicitudes de permisos, permitiendo que Copilot CLI lea archivos, ejecute comandos y acceda a URLs sin preguntar primero. Esto es necesario para el modo programático (`-p`) ya que no hay una sesión interactiva para aprobar acciones. Usa `--allow-all` solo con prompts que hayas escrito tú mismo y en directorios de confianza. Nunca lo uses con entrada no confiable o en directorios sensibles.

</details>

---

## Comandos slash esenciales

Estos comandos son buenos para aprender al principio mientras te familiarizas con Copilot CLI:

| Comando | Qué hace | Cuándo usarlo |
|---------|----------|---------------|
| `/ask` | Hacer una pregunta rápida sin que afecte tu historial de conversación | Cuando quieres una respuesta rápida sin desviarte de tu tarea actual |
| `/clear` | Borrar la conversación y empezar de cero | Al cambiar de tema |
| `/help` | Mostrar todos los comandos disponibles | Cuando olvidas un comando |
| `/model` | Mostrar o cambiar el modelo de IA | Cuando quieres cambiar el modelo de IA |
| `/plan` | Planear tu trabajo antes de codificar | Para características más complejas |
| `/research` | Investigación profunda usando GitHub y fuentes web | Cuando necesitas investigar un tema antes de codificar |
| `/exit` | Terminar la sesión | Cuando hayas terminado |

> 💡 **`/ask` vs chat normal**: Normalmente cada mensaje que envías pasa a formar parte de la conversación en curso y afecta las respuestas futuras. `/ask` es un atajo "off the record" — perfecto para preguntas rápidas y puntuales como `/ask ¿Qué significa YAML?` sin contaminar el contexto de tu sesión.

> 💡 **Autocompletado con Tab**: Al escribir un comando slash, pulsa **Tab** para autocompletar el nombre del comando o para ciclar entre subcomandos y argumentos disponibles. Esto es especialmente útil cuando no recuerdas el nombre exacto de un comando.

¡Eso es todo para empezar! A medida que te sientas cómodo, puedes explorar comandos adicionales.
> 📚 **Documentación oficial**: [Referencia de comandos de la CLI](https://docs.github.com/copilot/reference/cli-command-reference) para la lista completa de comandos y banderas.

<details>
<summary>📚 <strong>Comandos adicionales</strong> (hacer clic para expandir)</summary>

> 💡 Los comandos esenciales anteriores cubren gran parte de lo que harás en el uso diario. Esta referencia está aquí para cuando estés listo para explorar más.

### Entorno de agentes

| Command | Qué hace |
|---------|--------------|
| `/agent` | Explorar y seleccionar entre los agentes disponibles |
| `/env` | Mostrar detalles del entorno cargado — qué instrucciones, servidores MCP, habilidades, agentes y complementos están activos |
| `/init` | Inicializar las instrucciones de Copilot para tu repositorio |
| `/mcp` | Gestionar la configuración del servidor MCP |
| `/skills` | Gestionar habilidades para capacidades mejoradas |

> 💡 Los agentes se tratan en [Capítulo 04](../04-agents-custom-instructions/README.md), las habilidades en [Capítulo 05](../05-skills/README.md) y los servidores MCP en [Capítulo 06](../06-mcp-servers/README.md).

### Modelos y subagentes

| Command | Qué hace |
|---------|--------------|
| `/delegate` | Delegar la tarea al agente en la nube de GitHub Copilot |
| `/fleet` | Dividir una tarea compleja en subtareas paralelas para completarla más rápido |
| `/model` | Mostrar o cambiar el modelo de IA |
| `/tasks` | Ver subagentes en segundo plano y sesiones de shell separadas |

### Código

| Command | Qué hace |
|---------|--------------|
| `/diff` | Revisar los cambios realizados en el directorio actual |
| `/pr` | Operar sobre pull requests de la rama actual |
| `/research` | Realizar investigación profunda utilizando GitHub y fuentes web |
| `/review` | Ejecutar el agente de revisión de código para analizar cambios |
| `/terminal-setup` | Habilitar soporte de entrada multilínea (shift+enter y ctrl+enter) |

### Permisos

| Command | Qué hace |
|---------|--------------|
| `/add-dir <directory>` | Agregar un directorio a la lista permitida |
| `/allow-all [on\|off\|show]` | Aprobar automáticamente todos los avisos de permisos; usa `on` para habilitar, `off` para deshabilitar, `show` para verificar el estado actual |
| `/yolo` | Alias rápido de `/allow-all on` — aprueba automáticamente todos los avisos de permisos. |
| `/cwd`, `/cd [directory]` | Ver o cambiar el directorio de trabajo |
| `/list-dirs` | Mostrar todos los directorios permitidos |

> ⚠️ **Usar con precaución**: `/allow-all` y `/yolo` omiten las solicitudes de confirmación. Genial para proyectos de confianza, pero ten cuidado con código no confiable.

### Sesión

| Command | Qué hace |
|---------|--------------|
| `/clear` | Abandona la sesión actual (no se guarda el historial) y inicia una conversación nueva |
| `/compact` | Resumir la conversación para reducir el uso del contexto |
| `/context` | Mostrar el uso de tokens de la ventana de contexto y su visualización |
| `/keep-alive` | Evitar que tu sistema entre en suspensión mientras Copilot CLI está activo — útil para tareas de larga duración en un portátil |
| `/new` | Finaliza la sesión actual (guardándola en el historial para búsqueda/continuación) e inicia una conversación nueva. |
| `/resume` | Cambiar a una sesión diferente (opcionalmente especificar ID o nombre de la sesión) |
| `/rename` | Renombrar la sesión actual (omite el nombre para autogenerarlo) |
| `/rewind` | Abrir un selector de línea de tiempo para retroceder a cualquier punto anterior de la conversación |
| `/usage` | Mostrar métricas y estadísticas de uso de la sesión |
| `/session` | Mostrar información de la sesión y resumen del espacio de trabajo; usa `/session delete`, `/session delete <id>`, o `/session delete-all` para eliminar sesiones |
| `/share` | Exportar la sesión como archivo markdown, gist de GitHub o archivo HTML autocontenido |

### Visualización

| Command | Qué hace |
|---------|--------------|
| `/statusline` (or `/footer`) | Personalizar qué elementos aparecen en la barra de estado en la parte inferior de la sesión (directorio, rama, esfuerzo, ventana de contexto, cuota) |
| `/theme` | Ver o establecer el tema del terminal |

### Ayuda y comentarios

| Command | Qué hace |
|---------|--------------|
| `/changelog` | Mostrar el registro de cambios de las versiones de la CLI |
| `/feedback` | Enviar comentarios a GitHub |
| `/help` | Mostrar todos los comandos disponibles |

### Comandos rápidos de shell

Ejecuta comandos de shell directamente sin IA anteponiendo `!`:

```bash
copilot

> !git status
# Ejecuta git status directamente, sin usar la IA

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

> 💡 **Consejo**: Algunos modelos cuestan más "premium requests" que otros. Los modelos marcados **1x** (como Claude Sonnet 4.5) son una excelente opción por defecto. Son capaces y eficientes. Los modelos con multiplicadores más altos usan tu cuota de solicitudes premium más rápido, así que guárdalos para cuando realmente los necesites.

> 💡 **¿No estás seguro de qué modelo elegir?** Selecciona **`Auto`** en el selector de modelos para permitir que Copilot elija automáticamente el mejor modelo disponible para cada sesión. Esto es un excelente valor predeterminado si recién comienzas y no quieres pensar en la selección de modelos.

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración de escritorio acogedora con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

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

### Planificar una función

Usa `/plan` para que Copilot CLI trace una implementación antes de escribir código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revisar el plan
# Aprobar o modificar
# Observar su implementación paso a paso
```

### Automatizar con el modo programático

La bandera `-p` te permite ejecutar Copilot CLI directamente desde tu terminal sin entrar en modo interactivo. Copia y pega el siguiente script en tu terminal (no dentro de Copilot) desde la raíz del repositorio para revisar todos los archivos Python de la aplicación de libros.

```bash
# Revisar todos los archivos Python en la aplicación book
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

1. **Desafío interactivo**: Inicia `copilot` y explora la aplicación de libros. Pregunta sobre `@samples/book-app-project/books.py` y solicita mejoras 3 veces seguidas.

2. **Desafío en modo Plan**: Ejecuta `/plan Add rating and review features to the book app`. Lee el plan cuidadosamente. ¿Tiene sentido?

3. **Desafío programático**: Ejecuta `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. ¿Funcionó a la primera?

---

## 💡 Consejo: Controla tu sesión de CLI desde la web o el móvil

GitHub Copilot CLI admite **sesiones remotas**, que te permiten monitorizar e interactuar con una sesión de CLI en ejecución desde un navegador web (en escritorio o móvil) o la app GitHub Mobile sin estar físicamente en tu terminal.

Inicia una sesión remota con la bandera `--remote`:

```bash
copilot --remote
```

Copilot CLI mostrará un enlace y proporcionará acceso a un código QR. Abre el enlace en tu teléfono o en una pestaña del navegador de escritorio para ver la sesión en tiempo real, enviar indicaciones de seguimiento, revisar planes y dirigir el agente de forma remota. Las sesiones son específicas por usuario, por lo que solo puedes acceder a tus propias sesiones de Copilot CLI.

También puedes habilitar el acceso remoto desde dentro de una sesión activa en cualquier momento:

```
> /remote
```

Detalles adicionales sobre sesiones remotas se pueden encontrar en la [documentación de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Tarea

### Desafío principal: Mejorar las utilidades de la aplicación de libros

Los ejemplos prácticos se centraron en revisar y refactorizar `book_app.py`. Ahora practica las mismas habilidades en un archivo diferente, `utils.py`:

1. Inicia una sesión interactiva: `copilot`
2. Pide a Copilot CLI que resuma el archivo: "Summarize @samples/book-app-project/utils.py and explain what each function in this file does"
3. Pídele que agregue validación de entrada: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. Pídele que mejore el manejo de errores: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. Pídele un docstring: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. Observa cómo el contexto se mantiene entre las indicaciones. Cada mejora se basa en la anterior
7. Sal con `/exit`

**Criterios de éxito**: Deberías tener un `utils.py` mejorado con validación de entrada, manejo de errores y un docstring, todo construido mediante una conversación de múltiples turnos.

<details>
<summary>💡 Pistas (hacer clic para expandir)</summary>

**Ejemplos de indicaciones para probar:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**Problemas comunes:**
- Si Copilot CLI hace preguntas de aclaración, simplemente respóndelas de forma natural
- El contexto se mantiene, por lo que cada indicación se basa en la anterior
- Usa `/clear` si quieres empezar de nuevo

</details>

### Desafío adicional: Compara los modos

Los ejemplos usaron `/plan` para una función de búsqueda y `-p` para revisiones por lotes. Ahora prueba los tres modos en una única nueva tarea: agregar un método `list_by_year()` a la clase `BookCollection`:

1. **Interactivo**: `copilot` → pídele que diseñe y construya el método paso a paso
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programático**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**Reflexión**: ¿Qué modo te pareció más natural? ¿Cuándo usarías cada uno?

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (hacer clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Escribir `exit` en lugar de `/exit` | Copilot CLI trata "exit" como una indicación, no como un comando | Los comandos con barra siempre comienzan con `/` |
| Usar `-p` para conversaciones de múltiples turnos | Cada llamada con `-p` está aislada sin memoria de llamadas previas | Usa el modo interactivo (`copilot`) para conversaciones que se basen en el contexto |
| Olvidar las comillas alrededor de indicaciones con `$` o `!` | El shell interpreta caracteres especiales antes de que Copilot CLI los vea | Encierra las indicaciones entre comillas: `copilot -p "What does $HOME mean?"` |
| Presionar Esc una vez para cancelar una tarea en ejecución | Un solo Esc ya no cancela el trabajo en curso (para evitar accidentes) | Presiona **Esc dos veces** para cancelar mientras Copilot CLI está procesando |

### Solución de problemas

**"Model not available"** - Es posible que tu suscripción no incluya todos los modelos. Usa `/model` para ver qué está disponible.

**"Context too long"** - Tu conversación ha usado toda la ventana de contexto. Usa `/clear` para reiniciar, o inicia una nueva sesión.

**"Rate limit exceeded"** - Espera unos minutos e inténtalo de nuevo. Considera usar el modo programático para operaciones por lotes con retrasos.

</details>

---

# Resumen

## 🔑 Puntos clave

1. **El modo interactivo** es para exploración e iteración: el contexto se conserva. Es como tener una conversación con alguien que recuerda lo que has dicho hasta ese momento.
2. **El modo Plan** suele ser para tareas más complejas. Revisa antes de implementar.
3. **El modo programático** es para automatización. No se necesita interacción.
4. **Comandos esenciales** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`) cubren la mayoría del uso diario.

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ahora que entiendes los tres modos, aprendamos cómo proporcionar contexto sobre tu código a Copilot CLI.

En **[Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md)**, aprenderás:

- La sintaxis `@` para referenciar archivos y directorios
- Gestión de sesiones con `--resume` y `--continue`
- Cómo la gestión de contexto hace que Copilot CLI sea realmente potente

---

**[← Volver a la página principal del curso](../README.md)** | **[Continuar al Capítulo 02 →](../02-context-conversations/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->