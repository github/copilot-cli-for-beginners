![Capítulo 04: Agentes e instrucciones personalizadas](../../../04-agents-custom-instructions/images/chapter-header.png)

> **¿Y si pudieras contratar a un revisor de código Python, a un experto en testing y a un revisor de seguridad… todos en una sola herramienta?**

En el Capítulo 03 dominaste los flujos de trabajo esenciales: revisión de código, refactorización, depuración, generación de pruebas e integración con git. Eso te hace muy productivo con GitHub Copilot CLI. Ahora vamos a llevarlo más lejos.

Hasta ahora has usado Copilot CLI como un asistente de propósito general. Los agentes te permiten asignarle una persona específica con estándares incorporados, como un revisor de código que aplica type hints y PEP 8, o un asistente de testing que escribe casos pytest. Verás cómo el mismo prompt obtiene resultados notablemente mejores cuando lo gestiona un agente con instrucciones dirigidas.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, serás capaz de:

- Usar agentes integrados: Plan (`/plan`), Code-review (`/review`), y entender los agentes automáticos (Explore, Task)
- Crear agentes especializados usando archivos de agente (`.agent.md`)
- Usar agentes para tareas específicas de un dominio
- Cambiar entre agentes usando `/agent` y `--agent`
- Escribir archivos de instrucciones personalizadas para estándares específicos del proyecto

> ⏱️ **Tiempo estimado**: ~55 minutos (20 min de lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: contratar especialistas

Cuando necesitas ayuda con tu casa, no llamas a un único "ayudante general". Llamas a especialistas:

| Problema | Especialista | Por qué |
|---------|------------|-----|
| Tubería con fugas | Fontanero | Conoce las normativas de fontanería, dispone de herramientas especializadas |
| Reinstalación eléctrica | Electricista | Comprende los requisitos de seguridad, cumple la normativa |
| Tejado nuevo | Tejador | Conoce los materiales y el clima local |

Los agentes funcionan igual. En lugar de una IA genérica, usa agentes que se centran en tareas concretas y conocen el proceso correcto a seguir. Configura las instrucciones una vez y reutilízalas siempre que necesites esa especialidad: revisión de código, testing, seguridad, documentación.

<img src="../../../04-agents-custom-instructions/images/hiring-specialists-analogy.png" alt="Analogía de contratar especialistas - Igual que llamas a profesionales especializados para reparar tu casa, los agentes de IA están especializados en tareas concretas como revisión de código, testing, seguridad y documentación" width="800" />

---

# Usar agentes

Empieza ya con agentes integrados y personalizados.

---

## *¿Nuevo en agentes?* ¡Empieza aquí!
¿Nunca has usado o creado un agente? Aquí tienes todo lo que necesitas saber para empezar este curso.

1. **Prueba un agente *integrado* ahora mismo:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   Esto invoca al agente Plan para crear un plan de implementación paso a paso.

2. **Mira uno de nuestros ejemplos de agente personalizado:** Es sencillo definir las instrucciones de un agente; revisa el archivo de ejemplo [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) para ver el patrón.

3. **Entiende el concepto clave:** Los agentes son como consultar a un especialista en lugar de a un generalista. Un "agente de frontend" se centrará automáticamente en accesibilidad y patrones de componentes; no tienes que recordárselo porque ya está especificado en las instrucciones del agente.


## Agentes integrados

**¡Ya has usado algunos agentes integrados en el flujo de trabajo de desarrollo del Capítulo 03!**
<br>`/plan` y `/review` son en realidad agentes integrados. Ahora ya sabes lo que ocurre por debajo. Aquí tienes la lista completa:

| Agente | Cómo invocarlo | Qué hace |
|-------|---------------|--------------|
| **Plan** | `/plan` o `Shift+Tab` (cambia entre modos) | Crea planes de implementación paso a paso antes de programar |
| **Code-review** | `/review` | Revisa los cambios en stage o sin stage con feedback enfocado y accionable |
| **Init** | `/init` | Genera archivos de configuración del proyecto (instrucciones, agentes) |
| **Explore** | *Automático* | Se usa internamente cuando le pides a Copilot que explore o analice el código |
| **Task** | *Automático* | Ejecuta comandos como pruebas, builds, lints e instalación de dependencias |

<br>

**Agentes integrados en acción** - Ejemplos de invocación de Plan, Code-review, Explore y Task

```bash
copilot

# Invoke the Plan agent to create an implementation plan
> /plan Add input validation for book year in the book app

# Invoke the Code-review agent on your changes
> /review

# Explore and Task agents are invoked automatically when relevant:
> Run the test suite        # Uses Task agent

> Explore how book data is loaded    # Uses Explore agent
```

¿Y el agente Task? Trabaja entre bastidores para gestionar y registrar lo que está pasando, y reportar de vuelta en un formato limpio y claro:

| Resultado | Lo que ves |
|---------|--------------|
| ✅ **Éxito** | Resumen breve (por ejemplo, "All 247 tests passed", "Build succeeded") |
| ❌ **Fallo** | Salida completa con stack traces, errores del compilador y logs detallados |


> 📚 **Documentación oficial**: [Agentes de GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Añadir agentes a Copilot CLI

¡Puedes definir tus propios agentes para que formen parte de tu flujo de trabajo! Defínelos una vez y luego dirígelos.

<img src="../../../04-agents-custom-instructions/images/using-agents.png" alt="Cuatro robots de IA coloridos juntos, cada uno con herramientas distintas que representan capacidades de agentes especializados" width="800"/>

## 🗂️ Añade tus agentes 

Los archivos de agente son archivos Markdown con la extensión `.agent.md`. Tienen dos partes: el frontmatter YAML (metadatos) y las instrucciones en Markdown.

> 💡 **¿Nuevo con el frontmatter YAML?** Es un pequeño bloque de configuración al principio del archivo, rodeado por marcadores `---`. YAML son simplemente pares `key: value`. El resto del archivo es Markdown normal.

Aquí tienes un agente mínimo:

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **Obligatorio vs opcional**: El campo `description` es obligatorio. Otros campos como `name`, `tools` y `model` son opcionales.

## Dónde colocar los archivos de agente

| Ubicación | Ámbito | Recomendado para |
|----------|-------|----------|
| `.github/agents/` | Específico del proyecto | Agentes compartidos por el equipo con las convenciones del proyecto |
| `~/.copilot/agents/` | Global (todos los proyectos) | Agentes personales que usas en todas partes |

**Este proyecto incluye archivos de agente de ejemplo en la carpeta [.github/agents/](../../../.github/agents/)**. Puedes escribir los tuyos o personalizar los que ya se proporcionan.

<details>
<summary>📂 Ver los agentes de ejemplo de este curso</summary>

| Archivo | Descripción |
|------|-------------|
| `hello-world.agent.md` | Ejemplo mínimo: empieza por aquí |
| `python-reviewer.agent.md` | Revisor de calidad de código Python |
| `pytest-helper.agent.md` | Especialista en testing con pytest |

```bash
# Or copy one to your personal agents folder (available in every project)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

Para más agentes de la comunidad, consulta [github/awesome-copilot](https://github.com/github/awesome-copilot)

</details>


## 🚀 Dos formas de usar agentes personalizados

### Modo interactivo
Dentro del modo interactivo, lista los agentes con `/agent` y selecciona el agente con el que quieras trabajar. 
Selecciona un agente para continuar tu conversación con él.

```bash
copilot
> /agent
```

Para cambiar a un agente diferente o volver al modo por defecto, vuelve a usar el comando `/agent`.

### Modo programático

Lanza directamente una nueva sesión con un agente.

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **Cambiar de agente**: Puedes cambiar a un agente diferente en cualquier momento volviendo a usar `/agent` o `--agent`. Para volver a la experiencia estándar de Copilot CLI, usa `/agent` y selecciona **no agent**.

---

# Profundizando en los agentes

<img src="../../../04-agents-custom-instructions/images/creating-custom-agents.png" alt="Robot siendo ensamblado en un banco de trabajo rodeado de componentes y herramientas que representan la creación de agentes personalizados" width="800"/>

> 💡 **Esta sección es opcional.** Los agentes integrados (`/plan`, `/review`) son lo bastante potentes para la mayoría de los flujos de trabajo. Crea agentes personalizados cuando necesites una experiencia especializada que se aplique de forma consistente a tu trabajo.

Cada tema a continuación es independiente. **Elige lo que te interese: no necesitas leerlos todos a la vez.**

| Quiero... | Ir a |
|---|---|
| Ver por qué los agentes superan a los prompts genéricos | [Especialista vs genérico](#specialist-vs-generic-see-the-difference) |
| Combinar agentes en una funcionalidad | [Trabajar con varios agentes](#working-with-multiple-agents) |
| Organizar, nombrar y compartir agentes | [Organizar y compartir agentes](#organizing--sharing-agents) |
| Configurar contexto de proyecto siempre activo | [Configurar tu proyecto para Copilot](#configuring-your-project-for-copilot) |
| Consultar propiedades YAML y herramientas | [Referencia del archivo de agente](#agent-file-reference) |

Selecciona un escenario abajo para expandirlo.

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>Especialista vs genérico: nota la diferencia</strong> - Por qué los agentes producen mejores resultados que los prompts genéricos</summary>

## Especialista vs genérico: nota la diferencia

Aquí es donde los agentes demuestran su valor. Observa la diferencia:

### Sin un agente (Copilot genérico)

```bash
copilot

> Add a function to search books by year range in the book app
```

**Salida genérica**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

Básico. Funciona. Pero le falta mucho.

---

### Con el agente Python Reviewer

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
```

**Salida del especialista**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**Lo que el agente python-reviewer incluye automáticamente**:
- ✅ Type hints en todos los parámetros y valores de retorno
- ✅ Docstring completa con Args/Returns/Raises
- ✅ Validación de entrada con manejo de errores adecuado
- ✅ Comprensión de listas para mejor rendimiento
- ✅ Manejo de casos límite (valores de año ausentes o no válidos)
- ✅ Formato conforme a PEP 8
- ✅ Prácticas de programación defensiva

**La diferencia**: El mismo prompt, una salida muchísimo mejor. El agente aporta la experiencia que tú olvidarías pedir.

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>Trabajar con varios agentes</strong> - Combina especialistas, cambia a mitad de sesión, agentes como herramientas</summary>

## Trabajar con varios agentes

El verdadero poder llega cuando los especialistas trabajan juntos en una funcionalidad.

### Ejemplo: construir una funcionalidad sencilla

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Use python-reviewer for design
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Switch to pytest-helper for test design
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Synthesize both designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**La idea clave**: tú eres el arquitecto que dirige a los especialistas. Ellos se encargan de los detalles, tú de la visión.

<details>
<summary>🎬 ¡Mira la demo!</summary>

![Demo del Python Reviewer](../../../04-agents-custom-instructions/images/python-reviewer-demo.gif)

*La salida de la demo varía: tu modelo, herramientas y respuestas serán distintas a las que se muestran aquí.*

</details>

### Agentes como herramientas

Cuando hay agentes configurados, Copilot también puede llamarlos como herramientas durante tareas complejas. Si pides una funcionalidad full-stack, Copilot puede delegar automáticamente partes a los agentes especialistas adecuados.

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>Organizar y compartir agentes</strong> - Nombrado, ubicación de archivos, archivos de instrucciones y compartir con el equipo</summary>

## Organizar y compartir agentes

### Nombrar tus agentes

Cuando creas archivos de agente, el nombre importa. Es lo que escribirás después de `/agent` o `--agent`, y lo que tus compañeros verán en la lista de agentes.

| ✅ Buenos nombres | ❌ Evita |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**Convenciones de nombrado:**
- Usa minúsculas con guiones: `my-agent-name.agent.md`
- Incluye el dominio: `frontend`, `backend`, `devops`, `security`
- Sé específico cuando sea necesario: `react-typescript` vs simplemente `frontend`

---

### Compartir con tu equipo

Coloca los archivos de agente en `.github/agents/` y quedarán bajo control de versiones. Súbelos a tu repositorio y cada miembro del equipo los obtiene automáticamente. Pero los agentes son solo un tipo de archivo que Copilot lee de tu proyecto. También admite **archivos de instrucciones** que se aplican automáticamente en cada sesión, sin que nadie tenga que ejecutar `/agent`.

Piénsalo así: los agentes son especialistas a los que llamas, y los archivos de instrucciones son reglas del equipo que están siempre activas.

### Dónde colocar tus archivos

Ya conoces las dos ubicaciones principales (consulta [Dónde colocar los archivos de agente](#where-to-put-agent-files) más arriba). Usa este árbol de decisión para elegir:

<img src="../../../04-agents-custom-instructions/images/agent-file-placement-decision-tree.png" alt="Árbol de decisión sobre dónde colocar los archivos de agente: experimentando → carpeta actual, uso por el equipo → .github/agents/, en todas partes → ~/.copilot/agents/" width="800"/>

**Empieza simple:** Crea un único archivo `*.agent.md` en la carpeta de tu proyecto. Muévelo a una ubicación permanente cuando estés satisfecho con él.

Más allá de los archivos de agente, Copilot también lee **archivos de instrucciones a nivel de proyecto** automáticamente, sin necesidad de `/agent`. Consulta [Configurar tu proyecto para Copilot](#configuring-your-project-for-copilot) más abajo para `AGENTS.md`, `.instructions.md` y `/init`.

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Configurar tu proyecto para Copilot</strong> - AGENTS.md, archivos de instrucciones y configuración con /init</summary>

## Configurar tu proyecto para Copilot

Los agentes son especialistas que invocas a demanda. Los **archivos de configuración del proyecto** son distintos: Copilot los lee automáticamente en cada sesión para entender las convenciones, el stack tecnológico y las reglas de tu proyecto. Nadie tiene que ejecutar `/agent`; el contexto está siempre activo para todos los que trabajan en el repo.

### Configuración rápida con /init

La forma más rápida de empezar es dejar que Copilot genere los archivos de configuración por ti:

```bash
copilot
> /init
```

Copilot escaneará tu proyecto y creará archivos de instrucciones a medida. Puedes editarlos después.

### Formatos de archivo de instrucciones

| Archivo | Ámbito | Notas |
|------|-------|-------|
| `AGENTS.md` | Raíz del proyecto o anidado | **Estándar multiplataforma** - funciona con Copilot y otros asistentes de IA |
| `.github/copilot-instructions.md` | Proyecto | Específico de GitHub Copilot |
| `.github/instructions/*.instructions.md` | Proyecto | Instrucciones granulares específicas por tema |
| `CLAUDE.md`, `GEMINI.md` | Raíz del proyecto | Soportados por compatibilidad |

> 🎯 **¿Empezando ahora?** Usa `AGENTS.md` para las instrucciones del proyecto. Puedes explorar los demás formatos más adelante según los necesites.

### AGENTS.md

`AGENTS.md` es el formato recomendado. Es un [estándar abierto](https://agents.md/) que funciona con Copilot y otras herramientas de IA para programar. Colócalo en la raíz de tu repositorio y Copilot lo leerá automáticamente. El propio [AGENTS.md](../../../AGENTS.md) de este proyecto es un ejemplo funcional.

Un `AGENTS.md` típico describe el contexto de tu proyecto, el estilo de código, los requisitos de seguridad y los estándares de testing. Escribe el tuyo siguiendo el patrón de nuestro archivo de ejemplo.

### Archivos de instrucciones personalizadas (.instructions.md)

Para equipos que quieren un control más granular, divide las instrucciones en archivos específicos por tema. Cada archivo cubre una preocupación y se aplica automáticamente:

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **Nota**: Los archivos de instrucciones funcionan con cualquier lenguaje. Este ejemplo usa Python para encajar con el proyecto del curso, pero puedes crear archivos similares para TypeScript, Go, Rust o cualquier tecnología que use tu equipo.

**Encontrar archivos de instrucciones de la comunidad**: Explora [github/awesome-copilot](https://github.com/github/awesome-copilot) para encontrar archivos de instrucciones prefabricados que cubren .NET, Angular, Azure, Python, Docker y muchas otras tecnologías.

### Desactivar las instrucciones personalizadas

Si necesitas que Copilot ignore todas las configuraciones específicas del proyecto (útil para depurar o comparar comportamientos):

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>Referencia del archivo de agente</strong> - Propiedades YAML, alias de herramientas y ejemplos completos</summary>

## Referencia del archivo de agente

### Un ejemplo más completo

Has visto el [formato de agente mínimo](#-add-your-agents) más arriba. Aquí tienes un agente más completo que usa la propiedad `tools`. Crea `~/.copilot/agents/python-reviewer.agent.md`:

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### Propiedades YAML

| Propiedad | Obligatoria | Descripción |
|----------|----------|-------------|
| `name` | No | Nombre para mostrar (por defecto, el nombre del archivo) |
| `description` | **Sí** | Lo que hace el agente: ayuda a Copilot a entender cuándo sugerirlo |
| `tools` | No | Lista de herramientas permitidas (omitir = todas las herramientas disponibles). Consulta los alias de herramientas más abajo. |
| `target` | No | Limitar a `vscode` o `github-copilot` solamente |

### Alias de herramientas

Usa estos nombres en la lista `tools`:
- `read` - Leer el contenido de archivos
- `edit` - Editar archivos
- `search` - Buscar en archivos (grep/glob)
- `execute` - Ejecutar comandos de shell (también: `shell`, `Bash`)
- `agent` - Invocar otros agentes personalizados

> 📖 **Documentación oficial**: [Configuración de agentes personalizados](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **Solo en VS Code**: La propiedad `model` (para seleccionar modelos de IA) funciona en VS Code pero no es compatible con GitHub Copilot CLI. Puedes incluirla sin problema en archivos de agente multiplataforma. GitHub Copilot CLI la ignorará.

### Más plantillas de agentes

> 💡 **Nota para principiantes**: Los ejemplos de abajo son plantillas. **Reemplaza las tecnologías específicas por las que use tu proyecto.** Lo importante es la *estructura* del agente, no las tecnologías concretas mencionadas.

Este proyecto incluye ejemplos funcionales en la carpeta [.github/agents/](../../../.github/agents/):
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) - Ejemplo mínimo, empieza por aquí
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) - Revisor de calidad de código Python
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) - Especialista en testing con pytest

Para agentes de la comunidad, consulta [github/awesome-copilot](https://github.com/github/awesome-copilot).

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Crea tus propios agentes y míralos en acción.

---

## ▶️ Inténtalo tú mismo

```bash

# Create the agents directory (if it doesn't exist)
mkdir -p .github/agents

# Create a code reviewer agent
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# Create a documentation agent
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Now use them
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# Or switch agents
copilot
> /agent
# Select "documentor"
> Document @samples/book-app-project/books.py
```

---

## 📝 Tarea

### Reto principal: construye un equipo de agentes especializados

El ejemplo práctico creó los agentes `reviewer` y `documentor`. Ahora practica creando y usando agentes para una tarea diferente: mejorar la validación de datos en la app de libros.

1. Crea 3 archivos de agente (`.agent.md`) adaptados a la app de libros, uno por agente, colocados en `.github/agents/`
2. Tus agentes:
   - **data-validator**: comprueba `data.json` en busca de datos faltantes o malformados (autores vacíos, year=0, campos faltantes)
   - **error-handler**: revisa el código Python en busca de manejo de errores inconsistente y sugiere un enfoque unificado
   - **doc-writer**: genera o actualiza docstrings y contenido del README
3. Usa cada agente en la app de libros:
   - `data-validator` → audita `@samples/book-app-project/data.json`
   - `error-handler` → revisa `@samples/book-app-project/books.py` y `@samples/book-app-project/utils.py`
   - `doc-writer` → añade docstrings a `@samples/book-app-project/books.py`
4. Colabora: usa `error-handler` para identificar lagunas en el manejo de errores y luego `doc-writer` para documentar el enfoque mejorado

**Criterio de éxito**: Tienes 3 agentes funcionales que producen una salida consistente y de alta calidad y puedes alternar entre ellos con `/agent`.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Plantillas iniciales**: crea un archivo por agente en `.github/agents/`:

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**Probar tus agentes:**

> 💡 **Nota:** Ya deberías tener `samples/book-app-project/data.json` en tu copia local de este repo. Si falta, descarga la versión original desde el repo origen:
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Select "data-validator" from the list
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**Consejo:** El campo `description` en el frontmatter YAML es obligatorio para que los agentes funcionen.

</details>

### Reto bonus: biblioteca de instrucciones

Has construido agentes que invocas a demanda. Ahora prueba la otra cara: **archivos de instrucciones** que Copilot lee automáticamente en cada sesión, sin necesidad de `/agent`.

Crea una carpeta `.github/instructions/` con al menos 3 archivos de instrucciones:
- `python-style.instructions.md` para aplicar PEP 8 y convenciones de type hints
- `test-standards.instructions.md` para aplicar las convenciones de pytest en archivos de test
- `data-quality.instructions.md` para validar entradas de datos JSON

Prueba cada archivo de instrucciones con el código de la app de libros.

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué pasa | Solución |
|---------|--------------|-----|
| Falta `description` en el frontmatter del agente | El agente no se carga o no es detectable | Incluye siempre `description:` en el frontmatter YAML |
| Ubicación de archivo incorrecta para los agentes | Agente no encontrado al intentar usarlo | Colócalo en `~/.copilot/agents/` (personal) o `.github/agents/` (proyecto) |
| Usar `.md` en lugar de `.agent.md` | El archivo puede no reconocerse como agente | Nombra los archivos como `python-reviewer.agent.md` |
| Prompts de agente excesivamente largos | Puede alcanzar el límite de 30 000 caracteres | Mantén las definiciones de agente enfocadas; usa skills para instrucciones detalladas |

### Solución de problemas

**Agente no encontrado** - Comprueba que el archivo del agente exista en una de estas ubicaciones:
- `~/.copilot/agents/`
- `.github/agents/`

Lista los agentes disponibles:

```bash
copilot
> /agent
# Shows all available agents
```

**El agente no sigue las instrucciones** - Sé explícito en tus prompts y añade más detalle a las definiciones del agente:
- Frameworks/librerías concretas con versiones
- Convenciones del equipo
- Patrones de código de ejemplo

**Las instrucciones personalizadas no se cargan** - Ejecuta `/init` en tu proyecto para configurar instrucciones específicas del proyecto:

```bash
copilot
> /init
```

O comprueba si están desactivadas:
```bash
# Don't use --no-custom-instructions if you want them loaded
copilot  # This loads custom instructions by default
```

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **Agentes integrados**: `/plan` y `/review` se invocan directamente; Explore y Task funcionan automáticamente
2. **Los agentes personalizados** son especialistas definidos en archivos `.agent.md`
3. **Los buenos agentes** tienen experiencia, estándares y formatos de salida claros
4. **La colaboración multiagente** resuelve problemas complejos combinando experiencia
5. **Los archivos de instrucciones** (`.instructions.md`) codifican estándares del equipo para aplicarse automáticamente
6. **La salida consistente** procede de instrucciones de agente bien definidas

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Los agentes cambian *cómo enfoca y ejecuta acciones dirigidas Copilot* en tu código. A continuación aprenderás sobre las **skills**, que cambian *qué pasos* sigue. ¿Te preguntas en qué se diferencian agentes y skills? El Capítulo 05 lo aborda directamente.

En el **[Capítulo 05: Sistema de skills](../05-skills/README.md)**, aprenderás:

- Cómo las skills se autodisparan a partir de tus prompts (sin necesidad de un slash command)
- Instalar skills de la comunidad
- Crear skills personalizadas con archivos SKILL.md
- La diferencia entre agentes, skills y MCP
- Cuándo usar cada uno

---

**[← Volver al Capítulo 03](../03-development-workflows/README.md)** | **[Continuar al Capítulo 05 →](../05-skills/README.md)**
