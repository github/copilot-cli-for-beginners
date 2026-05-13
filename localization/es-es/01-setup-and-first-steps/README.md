![Capítulo 01: Primeros pasos](../../../01-setup-and-first-steps/images/chapter-header.png)

> **Mira cómo la IA encuentra bugs al instante, explica código confuso y genera scripts funcionales. Después aprende tres formas distintas de usar GitHub Copilot CLI.**

¡En este capítulo empieza la magia! Vivirás de primera mano por qué los desarrolladores describen GitHub Copilot CLI como tener a un ingeniero senior en marcación rápida. Verás cómo la IA encuentra bugs de seguridad en segundos, te explica código complejo en lenguaje sencillo y genera scripts funcionales al instante. Después dominarás los tres modos de interacción (Interactivo, Plan y Programático) para que sepas exactamente cuál usar en cada tarea.

> ⚠️ **Requisitos previos**: Asegúrate de haber completado primero **[Capítulo 00: Inicio rápido](../00-quick-start/README.md)**. Necesitarás GitHub Copilot CLI instalado y autenticado antes de ejecutar las demos siguientes.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Experimentar el aumento de productividad que ofrece GitHub Copilot CLI mediante demos prácticas
- Elegir el modo correcto (Interactivo, Plan o Programático) para cualquier tarea
- Usar comandos slash para controlar tus sesiones

> ⏱️ **Tiempo estimado**: ~45 minutos (15 min de lectura + 30 min de práctica)

---

# Tu primera experiencia con Copilot CLI

<img src="../../../01-setup-and-first-steps/images/first-copilot-experience.png" alt="Desarrollador sentado en un escritorio con código en el monitor y partículas brillantes que representan la asistencia de la IA" width="800"/>

Lánzate de lleno y descubre lo que Copilot CLI puede hacer.

---

## Tomando confianza: tus primeros prompts

Antes de meterte en las demos impresionantes, empecemos con algunos prompts sencillos que puedes probar ahora mismo. **¡No necesitas ningún repositorio de código!** Solo abre una terminal e inicia Copilot CLI:

```bash
copilot
```

Prueba estos prompts aptos para principiantes:

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

¿No usas Python? ¡No hay problema! Solo haz preguntas sobre el lenguaje que prefieras.

Fíjate en lo natural que se siente. Solo haz preguntas como se las harías a un colega. Cuando termines de explorar, escribe `/exit` para salir de la sesión.

**La idea clave**: GitHub Copilot CLI es conversacional. No necesitas ninguna sintaxis especial para empezar. Solo haz preguntas en lenguaje natural.

## Míralo en acción

Ahora veamos por qué los desarrolladores lo llaman "tener a un ingeniero senior en marcación rápida".

> 📖 **Cómo leer los ejemplos**: Las líneas que empiezan con `>` son prompts que escribes dentro de una sesión interactiva de Copilot CLI. Las líneas sin el prefijo `>` son comandos de shell que ejecutas en tu terminal.

> 💡 **Sobre los ejemplos de salida**: Los ejemplos de salida que se muestran en este curso son ilustrativos. Como las respuestas de Copilot CLI varían cada vez, tus resultados serán distintos en redacción, formato y nivel de detalle. Concéntrate en el *tipo* de información devuelta, no en el texto exacto.

### Demo 1: revisión de código en segundos

El curso incluye archivos de ejemplo con problemas intencionales de calidad de código. Si trabajas en tu máquina local y aún no has clonado el repositorio, ejecuta el comando `git clone` que aparece abajo, navega a la carpeta `copilot-cli-for-beginners` y luego ejecuta el comando `copilot`.

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

> 💡 **¿Para qué sirve el símbolo `@`?** El símbolo `@` le indica a Copilot CLI que lea un archivo. Aprenderás todo sobre esto en el Capítulo 02. Por ahora, solo copia el comando exactamente como se muestra.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de revisión de código](../../../01-setup-and-first-steps/images/code-review-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán distintos a los que se muestran aquí.*

</details>

---

**La conclusión**: una revisión de código profesional en segundos. Una revisión manual tardaría... bueno... bastante más que eso.

---

### Demo 2: explicar código confuso

¿Alguna vez te has quedado mirando código preguntándote qué hace? Prueba esto en tu sesión de Copilot CLI:

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de explicación de código](../../../01-setup-and-first-steps/images/explain-code-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán distintos a los que se muestran aquí.*

</details>

---

**Lo que ocurre**: (tu salida será distinta) Copilot CLI lee el archivo, entiende el código y lo explica en lenguaje natural.

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

**La conclusión**: código complejo explicado como lo haría un mentor paciente.

---

### Demo 3: generar código funcional

¿Necesitas una función para la que normalmente pasarías 15 minutos buscando en Google? Sigue en tu sesión:

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de generación de código](../../../01-setup-and-first-steps/images/generate-code-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán distintos a los que se muestran aquí.*

</details>

---

**Lo que ocurre**: una función completa y funcional en segundos que puedes copiar, pegar y ejecutar.

Cuando termines de explorar, sal de la sesión:

```
> /exit
```

**La conclusión**: gratificación instantánea, y has permanecido en una sola sesión continua todo el tiempo.

---

# Modos y comandos

<img src="../../../01-setup-and-first-steps/images/modes-and-commands.png" alt="Panel de control futurista con pantallas brillantes, mandos y ecualizadores que representan los modos y comandos de Copilot CLI" width="800"/>

Acabas de ver lo que Copilot CLI puede hacer. Ahora entendamos *cómo* usar estas capacidades de forma efectiva. La clave está en saber cuál de los tres modos de interacción usar en cada situación.

> 💡 **Nota**: Copilot CLI también tiene un modo **Autopilot** en el que trabaja en las tareas sin esperar tu intervención. Es potente, pero requiere conceder permisos completos y consume premium requests de forma autónoma. Este curso se centra en los tres modos siguientes. Te indicaremos cuándo pasar a Autopilot una vez que te sientas cómodo con lo básico.

---

## 🧩 Analogía con el mundo real: salir a comer

Piensa en usar GitHub Copilot CLI como salir a comer. Desde planificar la salida hasta hacer tu pedido, distintas situaciones piden distintos enfoques:

| Modo | Analogía gastronómica | Cuándo usarlo |
|------|----------------|-------------|
| **Plan** | Ruta de GPS hasta el restaurante | Tareas complejas: traza la ruta, revisa las paradas, acuerda el plan y luego conduce |
| **Interactivo** | Hablar con el camarero | Exploración e iteración: haz preguntas, personaliza, recibe feedback en tiempo real |
| **Programático** | Pedir en el autoservicio | Tareas rápidas y específicas: quédate en tu entorno, obtén un resultado rápido |

Igual que cuando sales a comer, irás aprendiendo de forma natural cuándo cada enfoque encaja mejor.

<img src="../../../01-setup-and-first-steps/images/ordering-food-analogy.png" alt="Tres formas de usar GitHub Copilot CLI - Modo Plan (ruta GPS al restaurante), Modo Interactivo (hablar con el camarero), Modo Programático (autoservicio)" width="800"/>

*Elige tu modo según la tarea: Plan para trazar el camino primero, Interactivo para colaboración de ida y vuelta, Programático para resultados rápidos de un solo disparo*

### ¿Con qué modo debería empezar?

**Empieza con el modo Interactivo.** 
- Puedes experimentar y hacer preguntas de seguimiento
- El contexto se va construyendo de forma natural a través de la conversación
- Los errores son fáciles de corregir con `/clear`

Cuando te sientas cómodo, prueba:
- **Modo Programático** (`copilot -p "<tu prompt>"`) para preguntas rápidas y puntuales
- **Modo Plan** (`/plan`) cuando necesites planificar las cosas con más detalle antes de programar

---

## Los tres modos

### Modo 1: Modo Interactivo (empieza aquí)

<img src="../../../01-setup-and-first-steps/images/interactive-mode.png" alt="Modo Interactivo - Como hablar con un camarero que puede responder preguntas y ajustar el pedido" width="250"/>

**Mejor para**: exploración, iteración, conversaciones de varios turnos. Como hablar con un camarero que puede responder preguntas, recibir feedback y ajustar el pedido sobre la marcha.

Inicia una sesión interactiva:

```bash
copilot
```

Como has visto hasta ahora, verás un prompt donde puedes escribir de forma natural. Para obtener ayuda sobre los comandos disponibles, simplemente escribe:

```
> /help
```

**Idea clave**: el modo Interactivo mantiene el contexto. Cada mensaje se construye sobre los anteriores, igual que en una conversación real.

#### Ejemplo del modo Interactivo

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

Fíjate cómo cada prompt se apoya en la respuesta anterior. Estás manteniendo una conversación, no empezando de cero cada vez.

---

### Modo 2: Modo Plan

<img src="../../../01-setup-and-first-steps/images/plan-mode.png" alt="Modo Plan - Como planificar una ruta antes de un viaje usando GPS" width="250"/>

**Mejor para**: tareas complejas en las que quieres revisar el enfoque antes de la ejecución. Similar a planificar una ruta antes de un viaje usando el GPS.

El modo Plan te ayuda a crear un plan paso a paso antes de escribir cualquier código. Usa el comando `/plan` o pulsa **Shift+Tab** para alternar al modo Plan:

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **Tip**: **Shift+Tab** alterna entre modos: Interactivo → Plan → Autopilot. Púlsalo en cualquier momento durante una sesión interactiva para cambiar de modo sin escribir un comando.

También puedes lanzar Copilot CLI directamente en modo Plan usando el flag `--plan`:

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

**Idea clave**: el modo Plan te permite revisar y modificar el enfoque antes de que se escriba cualquier código. Una vez que un plan esté completo, incluso puedes pedirle a Copilot CLI que lo guarde en un archivo para futuras consultas. Por ejemplo, "Save this plan to `mark_as_read_plan.md`" crearía un archivo Markdown con los detalles del plan.

> 💡 **¿Quieres algo más complejo?** Prueba: `/plan Add search and filter capabilities to the book app`. El modo Plan escala desde funcionalidades simples hasta aplicaciones completas.

> 📚 **Modo Autopilot**: Quizá hayas notado que Shift+Tab pasa por un tercer modo llamado **Autopilot**. En el modo Autopilot, Copilot trabaja en un plan completo sin esperar tu intervención después de cada paso, como entregarle una tarea a un colega y decirle "avísame cuando termines". El flujo de trabajo típico es planificar → aceptar → autopilot, lo que significa que primero debes ser bueno escribiendo planes. También puedes lanzar directamente en autopilot con `copilot --autopilot`. Familiarízate primero con los modos Interactivo y Plan, y después consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot) cuando estés listo.

---

### Modo 3: Modo Programático

<img src="../../../01-setup-and-first-steps/images/programmatic-mode.png" alt="Modo Programático - Como usar el autoservicio para un pedido rápido" width="250"/>

**Mejor para**: automatización, scripts, CI/CD, comandos de un solo disparo. Como usar el autoservicio para un pedido rápido sin necesidad de hablar con el camarero.

Usa el flag `-p` para comandos puntuales que no necesitan interacción:

```bash
# Generar código
copilot -p "Write a function that checks if a number is even or odd"

# Obtener ayuda rápida
copilot -p "How do I read a JSON file in Python?"
```

**Idea clave**: el modo Programático te da una respuesta rápida y sale. Sin conversación, solo entrada → salida.

<details>
<summary>📚 <strong>Yendo más allá: usar el modo Programático en scripts</strong> (haz clic para expandir)</summary>

Una vez que te sientas cómodo, puedes usar `-p` en scripts de shell:

```bash
#!/bin/bash

# Generar mensajes de commit automáticamente
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# Revisar un archivo
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **Sobre `--allow-all`**: este flag salta todos los avisos de permisos, permitiendo que Copilot CLI lea archivos, ejecute comandos y acceda a URLs sin preguntar primero. Esto es necesario para el modo programático (`-p`) porque no hay una sesión interactiva que apruebe las acciones. Usa `--allow-all` solo con prompts que hayas escrito tú mismo y en directorios en los que confíes. Nunca lo uses con entrada no confiable o en directorios sensibles.

</details>

---

## Comandos slash esenciales

Estos comandos son perfectos para aprender al principio mientras te familiarizas con Copilot CLI:

| Comando | Qué hace | Cuándo usarlo |
|---------|--------------|-------------|
| `/ask` | Hace una pregunta rápida sin que afecte al historial de tu conversación | Cuando quieres una respuesta rápida sin desviar la tarea actual |
| `/clear` | Limpia la conversación y empieza de cero | Cuando cambias de tema |
| `/help` | Muestra todos los comandos disponibles | Cuando olvidas un comando |
| `/model` | Muestra o cambia el modelo de IA | Cuando quieres cambiar el modelo de IA |
| `/plan` | Planifica tu trabajo antes de programar | Para funcionalidades más complejas |
| `/research` | Investigación profunda usando GitHub y fuentes web | Cuando necesitas investigar un tema antes de programar |
| `/exit` | Termina la sesión | Cuando hayas terminado |

> 💡 **`/ask` vs el chat normal**: normalmente cada mensaje que envías pasa a formar parte de la conversación en curso y afecta a las respuestas futuras. `/ask` es un atajo "off the record": perfecto para preguntas rápidas y puntuales como `/ask What does YAML mean?` sin contaminar el contexto de tu sesión.

> 💡 **Autocompletado con Tab**: cuando estés escribiendo un comando slash, pulsa **Tab** para autocompletar el nombre del comando o pasar por los subcomandos y argumentos disponibles. Resulta especialmente útil cuando no recuerdas el nombre exacto de un comando.

¡Eso es todo para empezar! Conforme te sientas cómodo, podrás explorar comandos adicionales.

> 📚 **Documentación oficial**: [Referencia de comandos del CLI](https://docs.github.com/copilot/reference/cli-command-reference) para la lista completa de comandos y flags.

<details>
<summary>📚 <strong>Comandos adicionales</strong> (haz clic para expandir)</summary>

> 💡 Los comandos esenciales de arriba cubren gran parte de lo que harás en el día a día. Esta referencia está aquí para cuando estés listo para explorar más.

### Entorno del agente

| Comando | Qué hace |
|---------|--------------|
| `/agent` | Explora y selecciona entre los agentes disponibles |
| `/env` | Muestra los detalles del entorno cargado: qué instrucciones, servidores MCP, skills, agentes y plugins están activos |
| `/init` | Inicializa instrucciones de Copilot para tu repositorio |
| `/mcp` | Gestiona la configuración del servidor MCP |
| `/skills` | Gestiona skills para capacidades ampliadas |

> 💡 Los agentes se cubren en el [Capítulo 04](../04-agents-custom-instructions/README.md), los skills en el [Capítulo 05](../05-skills/README.md) y los servidores MCP en el [Capítulo 06](../06-mcp-servers/README.md).

### Modelos y subagentes

| Comando | Qué hace |
|---------|--------------|
| `/delegate` | Delega la tarea al agente en la nube de GitHub Copilot |
| `/fleet` | Divide una tarea compleja en subtareas paralelas para completarla más rápido |
| `/model` | Muestra o cambia el modelo de IA |
| `/tasks` | Muestra los subagentes en segundo plano y las sesiones de shell desacopladas |

### Código

| Comando | Qué hace |
|---------|--------------|
| `/diff` | Revisa los cambios realizados en el directorio actual |
| `/pr` | Opera sobre los pull requests de la rama actual |
| `/research` | Ejecuta una investigación profunda usando GitHub y fuentes web |
| `/review` | Ejecuta el agente de code-review para analizar los cambios |
| `/terminal-setup` | Habilita la entrada multilínea (shift+enter y ctrl+enter) |

### Permisos

| Comando | Qué hace |
|---------|--------------|
| `/add-dir <directory>` | Añade un directorio a la lista de permitidos |
| `/allow-all [on\|off\|show]` | Autoaprueba todos los avisos de permisos; usa `on` para activarlo, `off` para desactivarlo, `show` para ver el estado actual |
| `/yolo` | Alias rápido para `/allow-all on`: autoaprueba todos los avisos de permisos. |
| `/cwd`, `/cd [directory]` | Muestra o cambia el directorio de trabajo |
| `/list-dirs` | Muestra todos los directorios permitidos |

> ⚠️ **Usar con precaución**: `/allow-all` y `/yolo` saltan los avisos de confirmación. Excelentes para proyectos de confianza, pero ten cuidado con código no confiable.

### Sesión

| Comando | Qué hace |
|---------|--------------|
| `/clear` | Abandona la sesión actual (sin guardar historial) y empieza una conversación nueva |
| `/compact` | Resume la conversación para reducir el uso de contexto |
| `/context` | Muestra el uso de tokens de la ventana de contexto y su visualización |
| `/keep-alive` | Evita que tu sistema entre en suspensión mientras Copilot CLI esté activo: práctico para tareas largas en un portátil |
| `/new` | Termina la sesión actual (guardándola en el historial para búsqueda/resume) y empieza una conversación nueva. |
| `/resume` | Cambia a una sesión distinta (opcionalmente puedes especificar el ID o nombre de la sesión) |
| `/rename` | Renombra la sesión actual (omite el nombre para autogenerar uno) |
| `/rewind` | Abre un selector de línea de tiempo para volver a un punto anterior de la conversación |
| `/usage` | Muestra métricas y estadísticas de uso de la sesión |
| `/session` | Muestra información de la sesión y un resumen del workspace; usa `/session delete`, `/session delete <id>` o `/session delete-all` para eliminar sesiones |
| `/share` | Exporta la sesión como un archivo Markdown, un gist de GitHub o un archivo HTML autocontenido |

### Visualización

| Comando | Qué hace |
|---------|--------------|
| `/statusline` (o `/footer`) | Personaliza qué elementos aparecen en la barra de estado al final de la sesión (directorio, rama, esfuerzo, ventana de contexto, cuota) |
| `/theme` | Visualiza o establece el tema del terminal |

### Ayuda y feedback

| Comando | Qué hace |
|---------|--------------|
| `/changelog` | Muestra el changelog de las versiones del CLI |
| `/feedback` | Envía feedback a GitHub |
| `/help` | Muestra todos los comandos disponibles |

### Comandos de shell rápidos

Ejecuta comandos de shell directamente sin pasar por la IA prefijándolos con `!`:

```bash
copilot

> !git status
# Ejecuta git status directamente, saltándose la IA

> !python -m pytest tests/
# Ejecuta pytest directamente
```

### Cambiar de modelo

Copilot CLI soporta varios modelos de IA de OpenAI, Anthropic, Google y otros. Los modelos disponibles para ti dependen de tu nivel de suscripción y de la región. Usa `/model` para ver tus opciones y cambiar entre ellas:

```bash
copilot
> /model

# Muestra los modelos disponibles y te deja elegir uno. Selecciona Sonnet 4.5.
```

> 💡 **Tip**: algunos modelos cuestan más "premium requests" que otros. Los modelos marcados como **1x** (como Claude Sonnet 4.5) son una opción por defecto excelente. Son capaces y eficientes. Los modelos con multiplicador más alto consumen tu cuota de premium requests más rápido, así que resérvalos para cuando realmente los necesites.

> 💡 **¿No sabes qué modelo elegir?** Selecciona **`Auto`** en el selector de modelos para que Copilot elija automáticamente el mejor modelo disponible para cada sesión. Es una opción por defecto excelente si estás empezando y no quieres pensar en la selección de modelos.

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Escritorio acogedor con un monitor mostrando código, una lámpara, una taza de café y unos auriculares listos para la práctica" width="800"/>

Es hora de poner en práctica lo que has aprendido.

---

## ▶️ Pruébalo tú mismo

### Exploración interactiva

Inicia Copilot y usa prompts de seguimiento para mejorar la app de libros de forma iterativa:

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### Planifica una funcionalidad

Usa `/plan` para que Copilot CLI trace una implementación antes de escribir código:

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# Revisa el plan
# Apruébalo o modifícalo
# Mira cómo lo implementa paso a paso
```

### Automatiza con el modo Programático

El flag `-p` te permite ejecutar Copilot CLI directamente desde tu terminal sin entrar en modo interactivo. Copia y pega el siguiente script en tu terminal (no dentro de Copilot) desde la raíz del repositorio para revisar todos los archivos Python de la app de libros.

```bash
# Revisa todos los archivos Python en la app de libros
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# Revisa todos los archivos Python en la app de libros
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

Después de completar las demos, prueba estas variaciones:

1. **Reto interactivo**: inicia `copilot` y explora la app de libros. Pregunta sobre `@samples/book-app-project/books.py` y solicita mejoras 3 veces seguidas.

2. **Reto en modo Plan**: ejecuta `/plan Add rating and review features to the book app`. Lee el plan con atención. ¿Tiene sentido?

3. **Reto programático**: ejecuta `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"`. ¿Funcionó al primer intento?

---

## 💡 Tip: controla tu sesión del CLI desde la web o el móvil

GitHub Copilot CLI soporta **sesiones remotas**, que te permiten monitorizar e interactuar con una sesión del CLI en ejecución desde un navegador web (en escritorio o móvil) o desde la app GitHub Mobile sin estar físicamente delante de tu terminal.

Inicia una sesión remota con el flag `--remote`:

```bash
copilot --remote
```

Copilot CLI mostrará un enlace y dará acceso a un código QR. Abre el enlace en tu teléfono o en una pestaña del navegador del escritorio para ver la sesión en tiempo real, enviar prompts de seguimiento, revisar planes y guiar al agente de forma remota. Las sesiones son específicas de cada usuario, así que solo puedes acceder a tus propias sesiones de Copilot CLI.

También puedes habilitar el acceso remoto desde dentro de una sesión activa en cualquier momento:

```
> /remote
```

Encontrarás más detalles sobre las sesiones remotas en la [documentación de Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely).

---

## 📝 Tarea

### Reto principal: mejora las utilidades de la app de libros

Los ejemplos prácticos se centraron en revisar y refactorizar `book_app.py`. Ahora practica las mismas habilidades sobre un archivo distinto, `utils.py`:

1. Inicia una sesión interactiva: `copilot`
2. Pide a Copilot CLI que resuma el archivo: "Summarize @samples/book-app-project/utils.py and explain what each function in this file does"
3. Pídele que añada validación de entrada: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. Pídele que mejore el manejo de errores: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. Pide un docstring: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. Observa cómo el contexto se mantiene entre prompts. Cada mejora se construye sobre la anterior
7. Sal con `/exit`

**Criterios de éxito**: deberías acabar con un `utils.py` mejorado con validación de entrada, manejo de errores y un docstring, todo construido a través de una conversación de varios turnos.

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
- Si Copilot CLI hace preguntas aclaratorias, simplemente respóndelas con naturalidad
- El contexto se mantiene, así que cada prompt se construye sobre el anterior
- Usa `/clear` si quieres empezar de nuevo

</details>

### Reto extra: compara los modos

Los ejemplos usaron `/plan` para una funcionalidad de búsqueda y `-p` para revisiones en lote. Ahora prueba los tres modos sobre una nueva tarea: añadir un método `list_by_year()` a la clase `BookCollection`:

1. **Interactivo**: `copilot` → pídele que diseñe y construya el método paso a paso
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programático**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**Reflexión**: ¿qué modo te resultó más natural? ¿Cuándo usarías cada uno?

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué pasa | Cómo arreglarlo |
|---------|--------------|-----|
| Escribir `exit` en vez de `/exit` | Copilot CLI trata "exit" como un prompt, no como un comando | Los comandos slash siempre empiezan por `/` |
| Usar `-p` para conversaciones de varios turnos | Cada llamada a `-p` está aislada y no recuerda llamadas anteriores | Usa el modo interactivo (`copilot`) para conversaciones que se construyan sobre el contexto |
| Olvidar las comillas en prompts con `$` o `!` | El shell interpreta los caracteres especiales antes de que Copilot CLI los vea | Envuelve los prompts entre comillas: `copilot -p "What does $HOME mean?"` |
| Pulsar Esc una vez para cancelar una tarea en ejecución | Una sola pulsación de Esc ya no cancela el trabajo en curso (para evitar accidentes) | Pulsa **Esc dos veces** para cancelar mientras Copilot CLI está procesando |

### Solución de problemas

**"Model not available"**: tu suscripción puede no incluir todos los modelos. Usa `/model` para ver lo que está disponible.

**"Context too long"**: tu conversación ha consumido toda la ventana de contexto. Usa `/clear` para reiniciar, o inicia una nueva sesión.

**"Rate limit exceeded"**: espera unos minutos e inténtalo de nuevo. Considera usar el modo programático para operaciones en lote con retardos.

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **El modo Interactivo** es para exploración e iteración: el contexto se mantiene. Es como tener una conversación con alguien que recuerda lo que has dicho hasta ese momento.
2. **El modo Plan** se usa normalmente para tareas más complejas. Revisa antes de implementar.
3. **El modo Programático** es para automatización. No requiere interacción.
4. **Los comandos esenciales** (`/ask`, `/help`, `/clear`, `/plan`, `/research`, `/model`, `/exit`) cubren la mayor parte del uso diario.

> 📋 **Referencia rápida**: consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ahora que entiendes los tres modos, vamos a aprender a darle a Copilot CLI contexto sobre tu código.

En **[Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md)** aprenderás:

- La sintaxis `@` para referenciar archivos y directorios
- Gestión de sesiones con `--resume` y `--continue`
- Cómo la gestión de contexto hace que Copilot CLI sea verdaderamente potente

---

**[← Volver al inicio del curso](../README.md)** | **[Continuar al Capítulo 02 →](../02-context-conversations/README.md)**
