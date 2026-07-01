<!--
---
id: CopilotCLI-04
title: !translate Create Specialized AI Assistants
description: !translate Use built-in agents, create custom agents, and write custom instructions that guide GitHub Copilot CLI for specialized tasks.
audience: Developers / Students / Terminal users
slug: create-specialized-ai-assistants
weight: 5
---
-->

![Capítulo 04: Agentes e Instrucciones Personalizadas](../../../04-agents-custom-instructions/assets/chapter-header.png)

> **¿Qué pasaría si pudieras contratar a un revisor de código Python, un experto en pruebas y un revisor de seguridad... todo en una sola herramienta?**

En el Capítulo 03, dominaste los flujos de trabajo esenciales: revisión de código, refactorización, depuración, generación de pruebas e integración con git. Esos te hacen muy productivo con GitHub Copilot CLI. Ahora, llevémoslo más allá.

Hasta ahora, has estado usando Copilot CLI como un asistente de propósito general. Los agentes te permiten darle una persona específica con estándares incorporados, como un revisor de código que aplica type hints y PEP 8, o un ayudante de pruebas que escribe casos de pytest. Verás cómo el mismo prompt obtiene resultados notablemente mejores cuando lo maneja un agente con instrucciones orientadas.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Usar agentes integrados: Plan (`/plan`), Code-review (`/review`), y comprender los agentes automáticos (Explore, Task)
- Crear agentes especializados usando archivos de agente (`.agent.md`)
- Usar agentes para tareas específicas del dominio
- Cambiar entre agentes usando `/agent` y `--agent`
- Escribir archivos de instrucciones personalizados para estándares específicos del proyecto

> ⏱️ **Tiempo estimado**: ~55 minutos (20 min lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: Contratar especialistas

Cuando necesitas ayuda con tu casa, no llamas a un "ayudante general". Llamas a especialistas:

| Problema | Especialista | Por qué |
|---------|------------|-----|
| Tubería con fuga | Fontanero | Conoce las normativas de fontanería, dispone de herramientas especializadas |
| Instalación eléctrica | Electricista | Entiende los requisitos de seguridad, cumple la normativa |
| Tejado nuevo | Techador | Conoce los materiales y las condiciones climáticas locales |

Los agentes funcionan de la misma manera. En lugar de una IA genérica, usa agentes que se enfocan en tareas específicas y conocen el proceso correcto a seguir. Configura las instrucciones una vez, luego reutilízalas siempre que necesites esa especialidad: revisión de código, pruebas, seguridad, documentación.

<img src="../../../04-agents-custom-instructions/assets/hiring-specialists-analogy.png" alt="Analogía de contratación de especialistas - Al igual que llamas a oficios especializados para reparaciones en la casa, los agentes de IA están especializados en tareas específicas como revisión de código, pruebas, seguridad y documentación" width="800" />

---

# Uso de agentes

Comienza con agentes integrados y personalizados de inmediato.

---

## *¿Nuevo en agentes?* ¡Comienza aquí!
¿Nunca has usado o creado un agente? Esto es todo lo que necesitas saber para empezar con este curso.

1. **Prueba un agente *integrado* ahora mismo:**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   Esto invoca al agente Plan para crear un plan de implementación paso a paso.

2. **Mira uno de nuestros ejemplos de agentes personalizados:** Es simple definir las instrucciones de un agente; mira el archivo proporcionado [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) para ver el patrón.

3. **Comprende el concepto principal:** Los agentes son como consultar a un especialista en lugar de a un generalista. Un "frontend agent" se centrará automáticamente en accesibilidad y patrones de componentes; no tienes que recordárselo porque ya está especificado en las instrucciones del agente.

## Agentes integrados

**¡Ya has usado algunos agentes integrados en el Capítulo 03: Flujo de trabajo de desarrollo!**
<br>`/plan` y `/review` son en realidad agentes integrados. Ahora ya sabes qué ocurre internamente. Esta es la lista completa:

| Agente | Cómo invocarlo | Qué hace |
|-------|---------------|--------------|
| **Plan** | `/plan` or `Shift+Tab` (cycle modes) | Crea planes de implementación paso a paso antes de codificar |
| **Code-review** | `/review` | Revisa cambios staged/unstaged con comentarios enfocados y accionables |
| **Init** | `/init` | Genera archivos de configuración del proyecto (instrucciones, agents) |
| **Explore** | *Automático* | Usado internamente cuando le pides a Copilot que explore o analice el código base |
| **Task** | *Automático* | Ejecuta comandos como pruebas, compilaciones, lint e instalaciones de dependencias |

<br>

**Agentes integrados en acción** - Ejemplos de invocación de Plan, Code-review, Explore y Task

```bash
copilot

# Invoca al agente Plan para crear un plan de implementación
> /plan Add input validation for book year in the book app

# Invoca al agente Code-review sobre tus cambios
> /review

# Los agentes Explore y Task se invocan automáticamente cuando proceda:
> Run the test suite        # Usa el agente Task

> Explore how book data is loaded    # Usa el agente Explore
```

¿Qué pasa con el agente Task? Funciona detrás de escena para gestionar y seguir lo que sucede y reportarlo de forma clara y ordenada:

| Resultado | Lo que ves |
|---------|--------------|
| ✅ **Éxito** | Resumen breve (p. ej., "All 247 tests passed", "Build succeeded") |
| ❌ **Fallo** | Salida completa con stack traces, errores del compilador y registros detallados |


> 📚 **Documentación oficial**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Agregar agentes a Copilot CLI

¡Puedes definir fácilmente tus propios agentes para que formen parte de tu flujo de trabajo! Define una vez, ¡luego dirígelos!

<img src="../../../04-agents-custom-instructions/assets/using-agents.png" alt="Four colorful AI robots standing together, each with different tools representing specialized agent capabilities" width="800"/>

## 🗂️ Agrega tus agentes 

Los archivos de agente son archivos markdown con la extensión `.agent.md`. Tienen dos partes: frontmatter YAML (metadatos) e instrucciones en markdown.

> 💡 **¿Nuevo en frontmatter YAML?** Es un pequeño bloque de configuraciones en la parte superior del archivo, rodeado por marcadores `---`. YAML son simplemente pares `key: value`. El resto del archivo es markdown normal.

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

> 💡 **Requerido vs Opcional**: El campo `description` es obligatorio. Otros campos como `name`, `tools`, y `model` son opcionales.

## Dónde colocar los archivos de agente

| Ubicación | Alcance | Ideal para |
|----------|-------|----------|
| `.github/agents/` | Específico del proyecto | Agentes compartidos por el equipo con convenciones del proyecto |
| `~/.copilot/agents/` | Global (todos los proyectos) | Agentes personales que usas en todos tus proyectos |

**Este proyecto incluye archivos de agente de ejemplo en la carpeta [.github/agents/](../../../.github/agents)**. Puedes escribir los tuyos, o personalizar los ya provistos.

<details>
<summary>📂 Ver los agentes de ejemplo en este curso</summary>

| Archivo | Descripción |
|------|-------------|
| `hello-world.agent.md` | Ejemplo mínimo - comienza aquí |
| `python-reviewer.agent.md` | Revisor de calidad de código Python |
| `pytest-helper.agent.md` | Especialista en pruebas con Pytest |

```bash
# O copia uno en tu carpeta de agentes personales (disponible en cada proyecto)
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

Para más agentes de la comunidad, consulta [github/awesome-copilot](https://github.com/github/awesome-copilot)

</details>


## 🚀 Dos maneras de usar agentes personalizados

### Modo interactivo
Dentro del modo interactivo, lista los agentes con `/agent` y selecciona el agente con el que empezar a trabajar. 
Selecciona un agente para continuar tu conversación con él.

```bash
copilot
> /agent
```

Para cambiar a un agente diferente, o para volver al modo predeterminado, usa el comando `/agent` de nuevo.

### Modo programático

Inicia directamente una nueva sesión con un agente.

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **Cambiar de agente**: Puedes cambiar a un agente diferente en cualquier momento usando `/agent` o `--agent` de nuevo. Para volver a la experiencia estándar de Copilot CLI, usa `/agent` y selecciona **no agent**.

> 💡 **El modo agente tiene alcance por sesión**: El agente que selecciones se aplica solo a la sesión actual. Cuando inicies una nueva sesión con `/new`, `/clear`, o abriendo una nueva terminal, Copilot vuelve a su modo predeterminado — la selección de agente no se conserva automáticamente. Esto significa que cada sesión comienza con una pizarra en blanco, lo cual es una buena práctica para mantener tu trabajo enfocado.

---

# Profundizando con agentes

<img src="../../../04-agents-custom-instructions/assets/creating-custom-agents.png" alt="Robot being assembled on a workbench surrounded by components and tools representing custom agent creation" width="800"/>

> 💡 **Esta sección es opcional.** Los agentes integrados (`/plan`, `/review`) son lo suficientemente potentes para la mayoría de los flujos de trabajo. Crea agentes personalizados cuando necesites una experiencia especializada que se aplique de forma consistente en tu trabajo.

Cada tema a continuación es independiente. **Elige lo que te interese: no necesitas leerlos todos de una vez.**

| Quiero... | Ir a |
|---|---|
| Ver por qué los agentes superan a los prompts genéricos | [Specialist vs Generic](#especialista-vs-genérico-ve-la-diferencia) |
| Combinar agentes en una funcionalidad | [Working with Multiple Agents](#trabajando-con-múltiples-agentes) |
| Organizar, nombrar y compartir agentes | [Organizing & Sharing Agents](#organizar-y-compartir-agentes) |
| Configurar contexto de proyecto siempre activo | [Configuring Your Project for Copilot](#configurar-tu-proyecto-para-copilot) |
| Consultar propiedades YAML y herramientas | [Agent File Reference](#referencia-de-archivo-de-agente) |

Selecciona un escenario a continuación para expandirlo.

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>Especialista vs Genérico: Ve la diferencia</strong> - Por qué los agentes producen mejores resultados que los prompts genéricos</summary>

## Especialista vs Genérico: Ve la diferencia

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

Básico. Funciona. Pero falta mucho.

---

### Con el agente python-reviewer

```bash
copilot

> /agent
# Seleccione "python-reviewer"

> Add a function to search books by year range in the book app
```

**Salida especializada**:
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

**Qué incluye automáticamente el agente python-reviewer**:
- ✅ Anotaciones de tipo en todos los parámetros y valores de retorno
- ✅ Docstring completa con Args/Returns/Raises
- ✅ Validación de entrada con manejo de errores adecuado
- ✅ Comprensión de listas para un mejor rendimiento
- ✅ Manejo de casos límite (valores de año faltantes/inválidos)
- ✅ Formato conforme a PEP 8
- ✅ Prácticas de programación defensiva

**La diferencia**: Mismo prompt, salida dramáticamente mejor. El agente aporta la experiencia que olvidarías pedir.

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>Trabajando con múltiples agentes</strong> - Combinar especialistas, cambiar a mitad de sesión, agentes como herramientas</summary>

## Trabajando con múltiples agentes

El verdadero poder surge cuando los especialistas trabajan juntos en una funcionalidad.

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

**La idea clave**: Eres el arquitecto que dirige a los especialistas. Ellos se encargan de los detalles, tú te encargas de la visión.

<details>
<summary>🎬 ¡Verlo en acción!</summary>

![Demostración del revisor de Python](../../../04-agents-custom-instructions/assets/python-reviewer-demo.gif)

*La salida de la demo varía: tu modelo, herramientas y respuestas serán diferentes a lo mostrado aquí.*

</details>

### Agentes como herramientas

Cuando los agentes están configurados, Copilot también puede llamarlos como herramientas durante tareas complejas. Si pides una funcionalidad full-stack, Copilot puede delegar automáticamente partes a los agentes especialistas apropiados.

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>Organizar y compartir agentes</strong> - Nombres, ubicación de archivos, archivos de instrucciones y compartir en equipo</summary>

## Organizar y compartir agentes

### Nombrar tus agentes

Cuando creas archivos de agente, el nombre importa. Es lo que escribirás después de `/agent` o `--agent`, y lo que tus compañeros verán en la lista de agentes.

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

Coloca los archivos de agente en `.github/agents/` y estarán bajo control de versiones. Haz push a tu repo y todos los miembros del equipo los obtendrán automáticamente. Pero los agentes son solo un tipo de archivo que Copilot lee desde tu proyecto. También admite **archivos de instrucciones** que se aplican automáticamente a cada sesión, sin que nadie necesite ejecutar `/agent`.

Piénsalo así: los agentes son especialistas a los que llamas, y los archivos de instrucciones son reglas del equipo que están siempre activas.

### Dónde poner tus archivos

Ya conoces las dos ubicaciones principales (ver [Where to put agent files](#dónde-colocar-los-archivos-de-agente) arriba). Usa este árbol de decisión para elegir:
<img src="../../../04-agents-custom-instructions/assets/agent-file-placement-decision-tree.png" alt="Árbol de decisiones sobre dónde colocar archivos de agente: experimentar → carpeta actual, uso en equipo → .github/agents/, en todas partes → ~/.copilot/agents/" width="800"/>

**Empieza simple:** Crea un único archivo `*.agent.md` en la carpeta de tu proyecto. Muévelo a una ubicación permanente cuando estés satisfecho con él.

Más allá de los archivos de agente, Copilot también lee automáticamente los **archivos de instrucciones a nivel de proyecto**, no se necesita `/agent`. Consulta [Configuring Your Project for Copilot](#configurar-tu-proyecto-para-copilot) abajo para `AGENTS.md`, `.instructions.md` y `/init`.

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Configurar tu proyecto para Copilot</strong> - AGENTS.md, archivos de instrucciones y configuración /init</summary>

## Configurar tu proyecto para Copilot

Los agentes son especialistas que invocas bajo demanda. Los **archivos de configuración del proyecto** son diferentes: Copilot los lee automáticamente en cada sesión para comprender las convenciones, la pila tecnológica y las reglas de tu proyecto. Nadie necesita ejecutar `/agent`; el contexto siempre está activo para todos los que trabajan en el repositorio.

### Configuración rápida con /init

La forma más rápida de empezar es dejar que Copilot genere archivos de configuración por ti:

```bash
copilot
> /init
```

Copilot escaneará tu proyecto y creará archivos de instrucciones adaptados. Puedes editarlos después.

### Formatos de archivos de instrucciones

| Archivo | Ámbito | Notas |
|------|-------|-------|
| `AGENTS.md` | Project root or nested | **Estándar multiplataforma** - funciona con Copilot y otras herramientas de IA |
| `.github/copilot-instructions.md` | Project | Específico de GitHub Copilot |
| `.github/instructions/*.instructions.md` | Project | Instrucciones granulares por tema |
| `~/.copilot/instructions/**/*.instructions.md` | User (all projects) | Instrucciones personales que se aplican en todos los proyectos, en todos tus repos |
| `CLAUDE.md`, `GEMINI.md` | Project root | Compatibles para interoperabilidad |

> 🎯 **¿Apenas empezando?** Usa `AGENTS.md` para instrucciones del proyecto. Puedes explorar los otros formatos más adelante según lo necesites.

### AGENTS.md

`AGENTS.md` es el formato recomendado. Es un [estándar abierto](https://agents.md/) que funciona con Copilot y otras herramientas de asistencia de codificación. Colócalo en la raíz de tu repositorio y Copilot lo lee automáticamente. El propio [AGENTS.md](../AGENTS.md) de este proyecto es un ejemplo funcional.

Un `AGENTS.md` típico describe el contexto del proyecto, el estilo de código, los requisitos de seguridad y los estándares de pruebas. Escribe el tuyo siguiendo el patrón de nuestro archivo de ejemplo.

### Archivos de instrucciones personalizados (.instructions.md)

Para equipos que quieran un control más granular, divide las instrucciones en archivos por tema. Cada archivo cubre una preocupación y se aplica automáticamente:

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **Nota**: Los archivos de instrucciones funcionan con cualquier lenguaje. Este ejemplo usa Python para coincidir con nuestro proyecto del curso, pero puedes crear archivos similares para TypeScript, Go, Rust o cualquier tecnología que use tu equipo.

#### Delimitar el alcance de las instrucciones con `applyTo`

Por defecto, un archivo de instrucciones se aplica a cada conversación. Para limitarlo a tipos de archivos específicos, añade un campo `applyTo` en el frontmatter YAML (el bloque entre marcadores `---` en la parte superior del archivo):

```markdown
---
applyTo: "**/*.py"
---
# Python Standards
Always follow PEP 8 style conventions.
Use type hints in all function signatures.
```

Con `applyTo: "**/*.py"`, Copilot solo carga ese archivo de instrucciones cuando estás trabajando con archivos Python. Las instrucciones para el estilo de Python nunca saturarán una conversación sobre, por ejemplo, un Dockerfile o una consulta SQL.

Aquí hay algunos patrones comunes:

| Valor de `applyTo` | Cuándo se aplica |
|---|---|
| `"**/*.py"` | Cualquier archivo Python |
| `"**/*.{ts,tsx}"` | Archivos TypeScript y TSX |
| `"tests/**"` | Cualquier archivo dentro de una carpeta `tests/` |
| (sin frontmatter) | Cada conversación — el valor por defecto |

> 💡 **Consejo**: Encierra el patrón glob entre comillas (p. ej., `"**/*.py"`) para asegurarte de que se interprete correctamente en todos los sistemas operativos y shells.

**Encontrar archivos de instrucciones de la comunidad**: Busca en [github/awesome-copilot](https://github.com/github/awesome-copilot) archivos de instrucciones predefinidos que cubren .NET, Angular, Azure, Python, Docker y muchas más tecnologías.

### Deshabilitar instrucciones personalizadas

Si necesitas que Copilot ignore todas las configuraciones específicas del proyecto (útil para depuración o comparar comportamientos):

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

Has visto el [formato mínimo de agente](#-add-your-agents) arriba. Aquí hay un agente más completo que usa la propiedad `tools`. Crea `~/.copilot/agents/python-reviewer.agent.md`:

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
| `name` | No | Nombre para mostrar (por defecto el nombre de archivo) |
| `description` | **Sí** | Qué hace el agente - ayuda a Copilot a entender cuándo sugerirlo |
| `tools` | No | Lista de herramientas permitidas (omitir = todas las herramientas disponibles). Ver alias de herramientas abajo. |
| `target` | No | Limitar a `vscode` o `github-copilot` solamente |

### Alias de herramientas

Usa estos nombres en la lista `tools`:
- `read` - Leer el contenido de archivos
- `edit` - Editar archivos
- `search` - Buscar en archivos (grep/glob)
- `execute` - Ejecutar comandos de shell (también: `shell`, `Bash`)
- `agent` - Invocar otros agentes personalizados

> 📖 **Documentación oficial**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **Solo VS Code**: La propiedad `model` (para seleccionar modelos de IA) funciona en VS Code pero no está soportada en GitHub Copilot CLI. Puedes incluirla sin problemas para archivos de agente multiplataforma. GitHub Copilot CLI la ignorará.

### Más plantillas de agentes

> 💡 **Nota para principiantes**: Los ejemplos abajo son plantillas. **Reemplaza las tecnologías específicas por las que use tu proyecto.** Lo importante es la *estructura* del agente, no las tecnologías mencionadas específicamente.

Este proyecto incluye ejemplos funcionales en la carpeta [.github/agents/](../../../.github/agents):
- [hello-world.agent.md](../../../.github/agents/hello-world.agent.md) - Ejemplo mínimo, comienza aquí
- [python-reviewer.agent.md](../../../.github/agents/python-reviewer.agent.md) - Revisor de calidad de código Python
- [pytest-helper.agent.md](../../../.github/agents/pytest-helper.agent.md) - Especialista en pruebas con Pytest

Para agentes de la comunidad, consulta [github/awesome-copilot](https://github.com/github/awesome-copilot).

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Escritorio cálido con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica práctica" width="800"/>

Crea tus propios agentes y ponlos en acción.

---

## ▶️ Pruébalo tú mismo

```bash

# Crear el directorio agents (si no existe)
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

# O cambia de agente
copilot
> /agent
# Selecciona "documentor"
> Document @samples/book-app-project/books.py
```

---

## 📝 Tarea

### Desafío principal: Construye un equipo especializado de agentes

El ejemplo práctico creó los agentes `reviewer` y `documentor`. Ahora practica creando y usando agentes para una tarea diferente: mejorar la validación de datos en la app de libros:

1. Crea 3 archivos de agente (`.agent.md`) adaptados a la app de libros, uno por agente, colocados en `.github/agents/`
2. Tus agentes:
   - **data-validator**: revisa `data.json` en busca de datos faltantes o mal formados (autores vacíos, year=0, campos faltantes)
   - **error-handler**: revisa el código Python en busca de manejo de errores inconsistente y sugiere un enfoque unificado
   - **doc-writer**: genera o actualiza docstrings y contenido del README
3. Usa cada agente en la app de libros:
   - `data-validator` → auditar `@samples/book-app-project/data.json`
   - `error-handler` → revisar `@samples/book-app-project/books.py` y `@samples/book-app-project/utils.py`
   - `doc-writer` → añadir docstrings a `@samples/book-app-project/books.py`
4. Colaboración: usa `error-handler` para identificar brechas en el manejo de errores, luego `doc-writer` para documentar el enfoque mejorado

**Criterios de éxito**: Tienes 3 agentes funcionales que producen resultados consistentes y de alta calidad y puedes alternar entre ellos con `/agent`.

<details>
<summary>💡 Sugerencias (haz clic para ver)</summary>

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

> 💡 **Nota:** Deberías tener ya `samples/book-app-project/data.json` en tu copia local de este repositorio. Si falta, descarga la versión original desde el repositorio fuente:
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Seleccione "data-validator" de la lista
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**Consejo:** El campo `description` en el frontmatter YAML es obligatorio para que los agentes funcionen.

</details>

### Desafío extra: Biblioteca de instrucciones

Has construido agentes que invocas bajo demanda. Ahora prueba el otro lado: **archivos de instrucciones** que Copilot lee automáticamente en cada sesión, sin necesidad de `/agent`.

Crea una carpeta `.github/instructions/` con al menos 3 archivos de instrucciones:
- `python-style.instructions.md` para aplicar PEP 8 y convenciones de type hints
- `test-standards.instructions.md` para aplicar convenciones de pytest en archivos de pruebas
- `data-quality.instructions.md` para validar entradas JSON

Prueba cada archivo de instrucciones en el código de la app de libros.

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para ver)</summary>

### Errores comunes

| Mistake | What Happens | Fix |
|---------|--------------|-----|
| Missing `description` in agent frontmatter | Agent won't load or won't be discoverable | Always include `description:` in YAML frontmatter |
| Wrong file location for agents | Agent not found when you try to use it | Place in `~/.copilot/agents/` (personal) or `.github/agents/` (project) |
| Using `.md` instead of `.agent.md` | File may not be recognized as an agent | Name files like `python-reviewer.agent.md` |
| Overly long agent prompts | May hit the 30,000 character limit | Keep agent definitions focused; use skills for detailed instructions |

### Solución de problemas

**Agent not found** - Comprueba que el archivo del agente exista en una de estas ubicaciones:
- `~/.copilot/agents/`
- `.github/agents/`

Lista los agentes disponibles:

```bash
copilot
> /agent
# Muestra todos los agentes disponibles
```

**Agent not following instructions** - Sé explícito en tus indicaciones y añade más detalle a las definiciones de agente:
- Marcos/bibliotecas específicas con versiones
- Convenciones del equipo
- Patrones de código de ejemplo

**Custom instructions not loading** - Ejecuta `/init` en tu proyecto para configurar instrucciones específicas del proyecto:

```bash
copilot
> /init
```

O comprueba si están deshabilitadas:
```bash
# No uses --no-custom-instructions si quieres que se carguen
copilot  # Esto carga las instrucciones personalizadas por defecto
```

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **Agentes integrados**: `/plan` y `/review` se invocan directamente; Explore y Task funcionan automáticamente
2. **Agentes personalizados** son especialistas definidos en archivos `.agent.md`
3. **Buenos agentes** tienen experiencia clara, estándares y formatos de salida
4. **Colaboración multi-agente** resuelve problemas complejos combinando especialidades
5. **Archivos de instrucciones** (`.instructions.md`) codifican estándares de equipo para su aplicación automática
6. **Salida consistente** proviene de instrucciones de agente bien definidas

> 📋 **Referencia rápida**: Consulta la [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Los agentes cambian *cómo Copilot aborda y realiza acciones concretas* en tu código. A continuación, aprenderás sobre **skills** - que cambian *qué pasos* sigue. ¿Te preguntas cómo difieren agentes y skills? El Capítulo 05 lo aborda directamente.

En **[Capítulo 05: Skills System](../05-skills/README.md)**, aprenderás:

- Cómo los skills se auto-disparan a partir de tus indicaciones (sin comando slash)
- Instalar skills de la comunidad
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