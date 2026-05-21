![Capítulo 04: Agentes e instrucciones personalizadas](../../../04-agents-custom-instructions/images/chapter-header.png)

> **¿Qué pasaría si pudieras contratar a un revisor de código en Python, un experto en testing y un revisor de seguridad... todo en una sola herramienta?**

En el Capítulo 03, dominaste los flujos de trabajo esenciales: revisión de código, refactorización, depuración, generación de pruebas e integración con git. Esos te hacen muy productivo con GitHub Copilot CLI. Ahora, llevémoslo más lejos.

Hasta ahora, has estado usando Copilot CLI como un asistente de propósito general. Los agentes te permiten darle una persona específica con estándares incorporados, como un revisor de código que aplica type hints y PEP 8, o un ayudante de testing que escribe casos pytest. Verás cómo el mismo prompt obtiene resultados notablemente mejores cuando lo maneja un agente con instrucciones dirigidas.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Usar agentes integrados: Plan (`/plan`), Code-review (`/review`), y entender agentes automáticos (Explore, Task)
- Crear agentes especializados usando archivos de agente (`.agent.md`)
- Usar agentes para tareas específicas de dominio
- Cambiar entre agentes usando `/agent` y `--agent`
- Escribir archivos de instrucciones personalizados para estándares específicos del proyecto

> ⏱️ **Tiempo estimado**: ~55 minutos (20 min lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: Contratar especialistas

Cuando necesitas ayuda con tu casa, no llamas a un "ayudante general". Llamas a especialistas:

| Problema | Especialista | Por qué |
|---------|------------|-----|
| Leaky pipe | Fontanero | Conoce los códigos de fontanería, tiene herramientas especializadas |
| Rewiring | Electricista | Entiende los requisitos de seguridad, cumple con la normativa |
| New roof | Techador | Conoce los materiales y las consideraciones del clima local |

Los agentes funcionan de la misma manera. En lugar de una IA genérica, usa agentes que se enfocan en tareas específicas y conocen el proceso correcto a seguir. Configura las instrucciones una vez y vuelvelas a usar siempre que necesites esa especialidad: revisión de código, testing, seguridad, documentación.

<img src="../../../04-agents-custom-instructions/images/hiring-specialists-analogy.png" alt="Analogía de contratación de especialistas: Así como llamas a oficios especializados para reparaciones del hogar, los agentes de IA están especializados en tareas como revisión de código, testing, seguridad y documentación" width="800" />

---

# Uso de Agentes

Comienza ya con agentes integrados y personalizados.

---

## *¿Nuevo en agentes?* ¡Comienza aquí!
¿Nunca has usado o creado un agente? Esto es todo lo que necesitas saber para empezar en este curso.

1. **Prueba un agente *integrado* ahora mismo:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   Esto invoca al agente Plan para crear un plan de implementación paso a paso.

2. **Ve uno de nuestros ejemplos de agentes personalizados:** Es sencillo definir las instrucciones de un agente, mira nuestro archivo provisto [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) para ver el patrón.

3. **Entiende el concepto central:** Los agentes son como consultar a un especialista en lugar de a un generalista. Un "agente frontend" se centrará automáticamente en accesibilidad y patrones de componentes, no tienes que recordárselo porque ya está especificado en las instrucciones del agente.


## Agentes integrados

**¡Ya has usado algunos agentes integrados en el Flujo de Trabajo del Capítulo 03!**
<br>`/plan` y `/review` son en realidad agentes integrados. Ahora sabes qué está pasando detrás de escena. Aquí está la lista completa:

| Agente | Cómo invocarlo | Qué hace |
|-------|---------------|--------------|
| **Plan** | `/plan` o `Shift+Tab` (cycle modes) | Crea planes de implementación paso a paso antes de codificar |
| **Code-review** | `/review` | Revisa cambios staged/unstaged con comentarios enfocados y accionables |
| **Init** | `/init` | Genera archivos de configuración del proyecto (instrucciones, agentes) |
| **Explore** | *Automatic* | Se usa internamente cuando le pides a Copilot que explore o analice el código base |
| **Task** | *Automatic* | Ejecuta comandos como pruebas, compilaciones, lint e instalaciones de dependencias |

<br>

**Agentes integrados en acción** - Ejemplos de invocación de Plan, Code-review, Explore y Task

```bash
copilot

# Invoca el agente Plan para crear un plan de implementación
> /plan Add input validation for book year in the book app

# Invoca el agente Code-review sobre tus cambios
> /review

# Los agentes Explore y Task se invocan automáticamente cuando sea relevante:
> Run the test suite        # Usa el agente Task

> Explore how book data is loaded    # Usa el agente Explore
```

¿Qué pasa con el Agente Task? Trabaja entre bastidores para gestionar y hacer seguimiento de lo que ocurre y para reportar de vuelta en un formato claro y limpio:

| Resultado | Lo que ves |
|---------|--------------|
| ✅ **Éxito** | Resumen breve (p. ej., "All 247 tests passed", "Build succeeded") |
| ❌ **Fallo** | Salida completa con stack traces, errores del compilador y logs detallados |


> 📚 **Documentación oficial**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Añadiendo agentes a Copilot CLI

¡Puedes simplemente definir tus propios agentes para que formen parte de tu flujo de trabajo! Define una vez, luego dirige.

<img src="../../../04-agents-custom-instructions/images/using-agents.png" alt="Cuatro robots coloridos de pie juntos, cada uno con diferentes herramientas representando capacidades especializadas de los agentes" width="800"/>

## 🗂️ Añade tus agentes

Los archivos de agente son archivos markdown con la extensión `.agent.md`. Tienen dos partes: frontmatter YAML (metadatos) e instrucciones en markdown.

> 💡 **¿Nuevo en frontmatter YAML?** Es un pequeño bloque de ajustes en la parte superior del archivo, rodeado por marcadores `---`. YAML es simplemente pares `clave: valor`. El resto del archivo es markdown regular.

Aquí hay un agente mínimo:

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

> 💡 **Requerido vs Opcional**: El campo `description` es obligatorio. Otros campos como `name`, `tools` y `model` son opcionales.

## Dónde poner los archivos de agente

| Ubicación | Ámbito | Ideal para |
|----------|-------|----------|
| `.github/agents/` | Específico del proyecto | Agentes compartidos por el equipo con convenciones del proyecto |
| `~/.copilot/agents/` | Global (todos los proyectos) | Agentes personales que usas en todas partes |

**Este proyecto incluye archivos de agente de ejemplo en la carpeta [.github/agents/](../../../.github/agents)**. Puedes escribir los tuyos, o personalizar los que ya vienen.

<details>
<summary>📂 Ver los agentes de ejemplo en este curso</summary>

| Archivo | Descripción |
|------|-------------|
| `hello-world.agent.md` | Ejemplo mínimo - empieza aquí |
| `python-reviewer.agent.md` | Revisor de calidad de código Python |
| `pytest-helper.agent.md` | Especialista en pruebas Pytest |

```bash
# O copia uno en tu carpeta de agentes personales (disponible en cada proyecto)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

Para más agentes de la comunidad, mira [github/awesome-copilot](https://github.com/github/awesome-copilot)

</details>


## 🚀 Dos maneras de usar agentes personalizados

### Modo interactivo
Dentro del modo interactivo, lista agentes usando `/agent` y selecciona el agente para empezar a trabajar. 
Selecciona un agente para continuar tu conversación con él.

```bash
copilot
> /agent
```

Para cambiar a un agente diferente, o para volver al modo predeterminado, usa el comando `/agent` de nuevo.

### Modo programático

Lanza directamente una nueva sesión con un agente.

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **Cambiar de agentes**: Puedes cambiar a un agente diferente en cualquier momento usando `/agent` o `--agent` de nuevo. Para volver a la experiencia estándar de Copilot CLI, usa `/agent` y selecciona **sin agente**.

---

# Profundizando con Agentes

<img src="../../../04-agents-custom-instructions/images/creating-custom-agents.png" alt="Robot siendo ensamblado en un banco de trabajo rodeado de componentes y herramientas que representan la creación de agentes personalizados" width="800"/>

> 💡 **Esta sección es opcional.** Los agentes integrados (`/plan`, `/review`) son suficientemente potentes para la mayoría de los flujos de trabajo. Crea agentes personalizados cuando necesites experiencia especializada que se aplique de forma consistente a tu trabajo.

Cada tema abajo es independiente. **Elige lo que te interese - no necesitas leerlos todos de una vez.**

| Quiero... | Ir a |
|---|---|
| Ver por qué los agentes superan a los prompts genéricos | [Especialista vs Genérico](#especialista-vs-genérico-ve-la-diferencia) |
| Combinar agentes en una funcionalidad | [Trabajar con múltiples agentes](#trabajar-con-múltiples-agentes) |
| Organizar, nombrar y compartir agentes | [Organizar y compartir agentes](#organizar-y-compartir-agentes) |
| Configurar contexto de proyecto siempre activo | [Configurar tu proyecto para Copilot](#configuración-rápida-con-init) |
| Consultar propiedades YAML y herramientas | [Referencia de archivo de agente](#un-ejemplo-más-completo) |

Selecciona un escenario abajo para expandirlo.

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>Especialista vs Genérico: Ve la diferencia</strong> - Por qué los agentes producen mejores resultados que los prompts genéricos</summary>

## Especialista vs Genérico: Ve la diferencia

Aquí es donde los agentes demuestran su valor. Observa la diferencia:

### Sin un Agente (Copilot genérico)

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

Básico. Funciona. Pero falta mucho.

---

### Con el agente Python Reviewer

```bash
copilot

> /agent
# Seleccione "python-reviewer"

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
- ✅ Sugerencias de tipo en todos los parámetros y valores de retorno
- ✅ Docstring completo con Args/Returns/Raises
- ✅ Validación de entrada con manejo de errores adecuado
- ✅ Comprensiones de listas para mejor rendimiento
- ✅ Manejo de casos límite (valores de año faltantes/ inválidos)
- ✅ Formato conforme a PEP 8
- ✅ Prácticas de programación defensiva

**La diferencia**: Mismo prompt, salida drásticamente mejor. El agente aporta la experiencia que olvidarías pedir.

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>Trabajar con múltiples agentes</strong> - Combina especialistas, cambia a mitad de sesión, agente-como-herramientas</summary>

## Trabajar con múltiples agentes

El verdadero poder viene cuando los especialistas trabajan juntos en una funcionalidad.

### Ejemplo: Construyendo una funcionalidad simple

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Usa python-reviewer para el diseño
> /agent
# Selecciona "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Cambia a pytest-helper para el diseño de pruebas
> /agent
# Selecciona "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Sintetiza ambos diseños
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**La idea clave**: Tú eres el arquitecto dirigiendo a los especialistas. Ellos manejan los detalles, tú te encargas de la visión.

<details>
<summary>🎬 ¡Verlo en acción!</summary>

![Demostración del revisor de Python](../../../04-agents-custom-instructions/images/python-reviewer-demo.gif)

*La salida de la demo varía - tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

### Agente como herramientas

Cuando los agentes están configurados, Copilot también puede llamarlos como herramientas durante tareas complejas. Si pides una funcionalidad full-stack, Copilot puede delegar automáticamente partes a los agentes especialistas apropiados.

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>Organizar y compartir agentes</strong> - Nombres, ubicación de archivos, archivos de instrucciones y uso en equipo</summary>

## Organizar y compartir agentes

### Nombrar tus agentes

Cuando creas archivos de agente, el nombre importa. Es lo que escribirás después de `/agent` o `--agent`, y lo que verán tus compañeros en la lista de agentes.

| ✅ Buenos nombres | ❌ Evitar |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**Convenciones de nombres:**
- Usa minúsculas con guiones: `my-agent-name.agent.md`
- Incluye el dominio: `frontend`, `backend`, `devops`, `security`
- Sé específico cuando sea necesario: `react-typescript` vs solo `frontend`

---

### Compartir con tu equipo

Coloca archivos de agente en `.github/agents/` y estarán bajo control de versiones. Haz push a tu repo y todos los miembros del equipo los obtendrán automáticamente. Pero los agentes son solo un tipo de archivo que Copilot lee desde tu proyecto. También soporta **archivos de instrucciones** que se aplican automáticamente a cada sesión, sin que nadie tenga que ejecutar `/agent`.

Piensa en ello así: los agentes son especialistas que llamas, y los archivos de instrucciones son reglas del equipo que están siempre activas.

### Dónde colocar tus archivos

Ya conoces las dos ubicaciones principales (ver [Dónde poner archivos de agente](#dónde-poner-los-archivos-de-agente) arriba). Usa este árbol de decisión para elegir:

<img src="../../../04-agents-custom-instructions/images/agent-file-placement-decision-tree.png" alt="Árbol de decisión para dónde colocar archivos de agente: experimentación → carpeta actual, uso en equipo → .github/agents/, en todos lados → ~/.copilot/agents/" width="800"/>

**Empieza simple:** Crea un único archivo `*.agent.md` en la carpeta de tu proyecto. Muévelo a una ubicación permanente una vez que estés satisfecho con él.

Más allá de los archivos de agente, Copilot también lee **archivos de instrucciones a nivel de proyecto** automáticamente, sin necesidad de `/agent`. Ve [Configurar tu proyecto para Copilot](#configuración-rápida-con-init) abajo para `AGENTS.md`, `.instructions.md`, y `/init`.

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Configurar tu proyecto para Copilot</strong> - AGENTS.md, archivos de instrucciones y configuración con /init</summary>
## Configurando tu proyecto para Copilot

Los agentes son especialistas que invocas bajo demanda. **Los archivos de configuración del proyecto** son diferentes: Copilot los lee automáticamente en cada sesión para entender las convenciones, la pila tecnológica y las reglas de tu proyecto. Nadie necesita ejecutar `/agent`; el contexto siempre está activo para todas las personas que trabajan en el repositorio.

### Configuración rápida con /init

La forma más rápida de comenzar es dejar que Copilot genere archivos de configuración por ti:

```bash
copilot
> /init
```

Copilot escaneará tu proyecto y creará archivos de instrucciones a medida. Puedes editarlos después.

### Formatos de archivos de instrucciones

| Archivo | Ámbito | Notas |
|------|-------|-------|
| `AGENTS.md` | Raíz del proyecto o anidado | **Estándar multiplataforma** - funciona con Copilot y otros asistentes de IA |
| `.github/copilot-instructions.md` | Proyecto | Específico de GitHub Copilot |
| `.github/instructions/*.instructions.md` | Proyecto | Instrucciones granulares y específicas por tema |
| `CLAUDE.md`, `GEMINI.md` | Raíz del proyecto | Soportados para compatibilidad |

> 🎯 **¿Apenas empezando?** Usa `AGENTS.md` para las instrucciones del proyecto. Puedes explorar los otros formatos más tarde según sea necesario.

### AGENTS.md

`AGENTS.md` es el formato recomendado. Es un [estándar abierto](https://agents.md/) que funciona con Copilot y otras herramientas de programación con IA. Colócalo en la raíz de tu repositorio y Copilot lo lee automáticamente. El propio [AGENTS.md](../AGENTS.md) de este proyecto es un ejemplo funcional.

Un `AGENTS.md` típico describe el contexto de tu proyecto, el estilo de código, los requisitos de seguridad y los estándares de pruebas. Escribe el tuyo siguiendo el patrón en nuestro archivo de ejemplo.

### Archivos de instrucciones personalizados (.instructions.md)

Para equipos que quieran un control más granular, divide las instrucciones en archivos por tema. Cada archivo cubre una preocupación y se aplica automáticamente:

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **Nota**: Los archivos de instrucciones funcionan con cualquier lenguaje. Este ejemplo usa Python para coincidir con el proyecto del curso, pero puedes crear archivos similares para TypeScript, Go, Rust o cualquier tecnología que use tu equipo.

#### Delimitando instrucciones con `applyTo`

Por defecto, un archivo de instrucciones se aplica a toda conversación. Para limitarlo a tipos de archivo específicos, añade un campo `applyTo` en el frontmatter YAML (el bloque entre `---` marcadores en la parte superior del archivo):

```markdown
---
applyTo: "**/*.py"
---
# Python Standards
Always follow PEP 8 style conventions.
Use type hints in all function signatures.
```

Con `applyTo: "**/*.py"`, Copilot carga ese archivo de instrucciones solo cuando estás trabajando con archivos Python. Las instrucciones para el estilo de Python nunca saturan una conversación sobre, por ejemplo, un Dockerfile o una consulta SQL.

Aquí hay algunos patrones comunes:

| `applyTo` value | Cuándo se aplica |
|---|---|
| `"**/*.py"` | Cualquier archivo Python |
| `"**/*.{ts,tsx}"` | Archivos TypeScript y TSX |
| `"tests/**"` | Cualquier archivo dentro de una carpeta `tests/` |
| (sin frontmatter) | Toda conversación — por defecto |

> 💡 **Consejo**: Encierra el patrón glob entre comillas (p. ej., `"**/*.py"`) para asegurar que se interprete correctamente en todos los sistemas operativos y shells.

**Encontrar archivos de instrucciones de la comunidad**: Busca en [github/awesome-copilot](https://github.com/github/awesome-copilot) archivos de instrucciones preconfeccionados que cubren .NET, Angular, Azure, Python, Docker y muchas más tecnologías.

### Deshabilitar instrucciones personalizadas

Si necesitas que Copilot ignore todas las configuraciones específicas del proyecto (útil para depurar o comparar comportamientos):

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>Referencia de archivo de agente</strong> - Propiedades YAML, alias de herramientas y ejemplos completos</summary>

## Referencia de archivo de agente

### Un ejemplo más completo

Has visto el [formato de agente minimalista](#-add-your-agents) arriba. Aquí hay un agente más completo que usa la propiedad `tools`. Crea `~/.copilot/agents/python-reviewer.agent.md`:

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

| Propiedad | Requerido | Descripción |
|----------|----------|-------------|
| `name` | No | Nombre para mostrar (por defecto: usa el nombre del archivo) |
| `description` | **Sí** | Lo que hace el agente - ayuda a Copilot a entender cuándo sugerirlo |
| `tools` | No | Lista de herramientas permitidas (omitir = todas las herramientas disponibles). Ver alias de herramientas abajo. |
| `target` | No | Limitar a `vscode` o `github-copilot` únicamente |

### Alias de herramientas

Usa estos nombres en la lista `tools`:
- `read` - Leer el contenido de archivos
- `edit` - Editar archivos
- `search` - Buscar archivos (grep/glob)
- `execute` - Ejecutar comandos de shell (también: `shell`, `Bash`)
- `agent` - Invocar otros agentes personalizados

> 📖 **Documentación oficial**: [Configuración de agentes personalizados](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **Solo VS Code**: La propiedad `model` (para seleccionar modelos de IA) funciona en VS Code pero no es compatible con GitHub Copilot CLI. Puedes incluirla sin problemas en archivos de agentes multiplataforma. GitHub Copilot CLI la ignorará.

### Más plantillas de agentes

> 💡 **Nota para principiantes**: Los ejemplos a continuación son plantillas. **Sustituye las tecnologías específicas por las que use tu proyecto.** Lo importante es la *estructura* del agente, no las tecnologías específicas mencionadas.

Este proyecto incluye ejemplos funcionales en la carpeta [.github/agents/](../../../.github/agents):
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) - Ejemplo mínimo, comienza aquí
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) - Revisor de calidad de código Python
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) - Especialista en pruebas Pytest

Para agentes comunitarios, consulta [github/awesome-copilot](https://github.com/github/awesome-copilot).

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración de escritorio acogedora con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica práctica" width="800"/>

Crea tus propios agentes y míralos en acción.

---

## ▶️ Pruébalo tú mismo

```bash

# Crear el directorio de agentes (si no existe)
mkdir -p .github/agents

# Crear un agente revisor de código
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Agente revisor de código

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

# Crear un agente de documentación
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Agente de documentación

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Úsalos ahora
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# O cambia de agentes
copilot
> /agent
# Selecciona "documentador"
> Document @samples/book-app-project/books.py
```

---

## 📝 Tarea

### Reto principal: Construir un equipo de agentes especializados

El ejemplo práctico creó agentes `reviewer` y `documentor`. Ahora practica creando y usando agentes para una tarea diferente: mejorar la validación de datos en la aplicación de libros:

1. Crea 3 archivos de agente (`.agent.md`) adaptados a la app de libros, uno por agente, colocados en `.github/agents/`
2. Tus agentes:
   - **data-validator**: comprueba `data.json` en busca de datos faltantes o mal formados (autores vacíos, year=0, campos faltantes)
   - **error-handler**: revisa el código Python en busca de manejo de errores inconsistente y sugiere un enfoque unificado
   - **doc-writer**: genera o actualiza docstrings y contenido de README
3. Usa cada agente en la app de libros:
   - `data-validator` → auditar `@samples/book-app-project/data.json`
   - `error-handler` → revisar `@samples/book-app-project/books.py` y `@samples/book-app-project/utils.py`
   - `doc-writer` → añadir docstrings a `@samples/book-app-project/books.py`
4. Colaborar: usa `error-handler` para identificar brechas en el manejo de errores, y luego `doc-writer` para documentar el enfoque mejorado

**Criterios de éxito**: Tienes 3 agentes funcionando que producen resultados coherentes y de alta calidad y puedes alternar entre ellos con `/agent`.

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

> 💡 **Nota:** Deberías ya tener `samples/book-app-project/data.json` en tu copia local de este repositorio. Si falta, descarga la versión original del repositorio fuente:
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Seleccione "data-validator" de la lista
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**Consejo:** El campo `description` en el frontmatter YAML es obligatorio para que los agentes funcionen.

</details>

### Reto adicional: Biblioteca de instrucciones

Has creado agentes que invocas bajo demanda. Ahora prueba el otro lado: **archivos de instrucciones** que Copilot lee automáticamente en cada sesión, sin necesidad de `/agent`.

Crea una carpeta `.github/instructions/` con al menos 3 archivos de instrucciones:
- `python-style.instructions.md` para aplicar PEP 8 y las convenciones de anotaciones de tipo
- `test-standards.instructions.md` para aplicar las convenciones de pytest en archivos de pruebas
- `data-quality.instructions.md` para validar entradas de datos JSON

Prueba cada archivo de instrucciones en el código de la app de libros.

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Falta `description` en el frontmatter del agente | El agente no se cargará o no será detectable | Siempre incluye `description:` en el frontmatter YAML |
| Ubicación incorrecta de los archivos de agentes | El agente no se encuentra cuando intentas usarlo | Colócalo en `~/.copilot/agents/` (personal) o `.github/agents/` (proyecto) |
| Usar `.md` en vez de `.agent.md` | El archivo puede no ser reconocido como un agente | Nombra los archivos como `python-reviewer.agent.md` |
| Prompts de agente demasiado largos | Pueden alcanzar el límite de 30,000 caracteres | Mantén las definiciones de agentes enfocadas; usa skills para instrucciones detalladas |

### Solución de problemas

**Agente no encontrado** - Comprueba que el archivo del agente exista en una de estas ubicaciones:
- `~/.copilot/agents/`
- `.github/agents/`

Lista de agentes disponibles:

```bash
copilot
> /agent
# Muestra todos los agentes disponibles
```

**Agente que no sigue las instrucciones** - Sé explícito en tus prompts y añade más detalle a las definiciones de agentes:
- Frameworks/bibliotecas específicas con versiones
- Convenciones del equipo
- Patrones de código de ejemplo

**Instrucciones personalizadas no se cargan** - Ejecuta `/init` en tu proyecto para configurar instrucciones específicas del proyecto:

```bash
copilot
> /init
```

O verifica si están deshabilitadas:
```bash
# No uses --no-custom-instructions si quieres que se carguen
copilot  # Esto carga instrucciones personalizadas de forma predeterminada
```

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Agentes integrados**: `/plan` y `/review` se invocan directamente; Explore y Task funcionan automáticamente
2. **Agentes personalizados** son especialistas definidos en archivos `.agent.md`
3. **Buenos agentes** tienen experiencia clara, estándares y formatos de salida
4. **Colaboración multiagente** resuelve problemas complejos combinando experiencia
5. **Los archivos de instrucciones** (`.instructions.md`) codifican los estándares del equipo para su aplicación automática
6. **Salida consistente** proviene de instrucciones de agente bien definidas

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Los agentes cambian *cómo Copilot aborda y realiza acciones específicas* en tu código. A continuación, aprenderás sobre **skills** — que cambian *qué pasos* sigue. ¿Te preguntas cómo difieren agentes y skills? El Capítulo 05 trata eso directamente.

En **[Capítulo 05: Sistema de skills](../05-skills/README.md)**, aprenderás:

- Cómo los skills se activan automáticamente a partir de tus indicaciones (no se necesita un comando con barra)
- Cómo instalar skills de la comunidad
- Crear skills personalizados con archivos SKILL.md
- La diferencia entre agentes, skills y MCP
- Cuándo usar cada uno

---

**[← Volver al Capítulo 03](../03-development-workflows/README.md)** | **[Continuar al Capítulo 05 →](../05-skills/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->