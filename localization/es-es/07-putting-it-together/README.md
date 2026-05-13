![Capítulo 07: Combinando todo](../../../07-putting-it-together/images/chapter-header.png)

> **Todo lo que has aprendido se combina aquí. Pasa de la idea al PR fusionado en una sola sesión.**

En este capítulo unirás todo lo que has aprendido en flujos de trabajo completos. Construirás funcionalidades usando colaboración multiagente, configurarás hooks de pre-commit que detectan problemas de seguridad antes de que se confirmen, integrarás Copilot en pipelines de CI/CD, e irás de la idea de una funcionalidad al PR fusionado en una sola sesión de terminal. Aquí es donde GitHub Copilot CLI se convierte en un auténtico multiplicador de fuerza.

> 💡 **Nota**: Este capítulo muestra cómo combinar todo lo que has aprendido. **No necesitas agentes, skills ni MCP para ser productivo (aunque pueden resultar muy útiles).** El flujo de trabajo central — describir, planificar, implementar, probar, revisar, enviar — funciona solo con las funcionalidades integradas de los Capítulos 00-03.

## 🎯 Objetivos de aprendizaje

Al finalizar este capítulo, serás capaz de:

- Combinar agentes, skills y MCP (Model Context Protocol) en flujos de trabajo unificados
- Construir funcionalidades completas usando enfoques multi-herramienta
- Configurar automatización básica con hooks
- Aplicar buenas prácticas para el desarrollo profesional

> ⏱️ **Tiempo estimado**: ~75 minutos (15 min de lectura + 60 min práctica)

---

## 🧩 Analogía del mundo real: la orquesta

<img src="../../../07-putting-it-together/images/orchestra-analogy.png" alt="Analogía de la orquesta - Flujo de trabajo unificado" width="800"/>

Una orquesta sinfónica tiene muchas secciones:
- **Las cuerdas** aportan la base (como tus flujos de trabajo principales)
- **Los metales** añaden potencia (como los agentes con experiencia especializada)
- **Las maderas** añaden color (como los skills que amplían capacidades)
- **La percusión** marca el ritmo (como MCP conectando con sistemas externos)

Por separado, cada sección suena limitada. Juntas y bien dirigidas, crean algo magnífico.

**¡Eso es lo que enseña este capítulo!**<br>
*Como un director con su orquesta, tú orquestas agentes, skills y MCP en flujos de trabajo unificados*

Empecemos recorriendo un escenario que modifica código, genera pruebas, lo revisa y crea un PR - todo en una sola sesión.

---

## De la idea al PR fusionado en una sola sesión

En lugar de cambiar entre tu editor, la terminal, el ejecutor de pruebas y la interfaz de GitHub, perdiendo contexto cada vez, puedes combinar todas tus herramientas en una sola sesión de terminal. Desglosaremos este patrón en la sección [Patrón de integración](#the-integration-pattern-for-power-users) más abajo.

```bash
# Start Copilot in interactive mode
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot creates high-level plan...

# SWITCH TO PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# SWITCH TO PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# IMPLEMENT
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TEST
> Generate comprehensive tests for the new feature

# Multiple tests are generated similar to the following:
# - Happy path (3 tests) — filters correctly, excludes read, includes unread
# - Edge cases (4 tests) — empty collection, all read, none read, single book
# - Parametrized (5 cases) — varying read/unread ratios via @pytest.mark.parametrize
# - Integration (4 tests) — interplay with mark_as_read, remove_book, add_book, and data integrity

# Review the changes
> /review

# If review passes, use /pr to operate on the pull request for the current branch
> /pr [view|create|fix|auto]

# Or ask naturally if you want Copilot to draft it from the terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**Enfoque tradicional**: Cambiar entre editor, terminal, ejecutor de pruebas, documentación y la interfaz de GitHub. Cada cambio provoca pérdida de contexto y fricción.

**La idea clave**: Diriges a especialistas como un arquitecto. Ellos se encargan de los detalles. Tú te encargas de la visión.

> 💡 **Yendo más allá**: Para planes grandes y multi-paso como este, prueba `/fleet` para que Copilot ejecute subtareas independientes en paralelo. Consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet) para más detalles.

---

# Flujos de trabajo adicionales

<img src="../../../07-putting-it-together/images/combined-workflows.png" alt="Personas montando un puzzle gigante de colores con engranajes, que representa cómo agentes, skills y MCP se combinan en flujos de trabajo unificados" width="800"/>

Para usuarios avanzados que han completado los Capítulos 04-06, estos flujos de trabajo muestran cómo agentes, skills y MCP multiplican tu eficacia.

## El patrón de integración

Aquí tienes el modelo mental para combinarlo todo:

<img src="../../../07-putting-it-together/images/integration-pattern.png" alt="El patrón de integración - Un flujo de trabajo de 4 fases: Reunir contexto (MCP), Analizar y planificar (Agentes), Ejecutar (Skills + Manual), Completar (MCP)" width="800"/>

---

## Flujo de trabajo 1: Investigación y corrección de bugs

Corrección de bugs reales con integración completa de herramientas:

```bash
copilot

# PHASE 1: Understand the bug from GitHub (MCP provides this)
> Get the details of issue #1

# Learn: "find_by_author doesn't work with partial names"

# PHASE 2: Research best practice (deep research with web + GitHub sources)
> /research Best practices for Python case-insensitive string matching

# PHASE 3: Find related code
> @samples/book-app-project/books.py Show me the find_by_author method

# PHASE 4: Get expert analysis
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching

# Agent identifies: Method uses exact equality instead of substring matching

# PHASE 5: Fix with agent guidance
> Implement the fix using lowercase comparison and 'in' operator

# PHASE 6: Generate tests
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# PHASE 7: Commit and PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## Flujo de trabajo 2: Automatización de revisión de código (opcional)

> 💡 **Esta sección es opcional.** Los hooks de pre-commit son útiles para equipos pero no son imprescindibles para ser productivo. Sáltatela si estás empezando.
>
> ⚠️ **Nota de rendimiento**: Este hook llama a `copilot -p` por cada archivo en staged, lo que tarda varios segundos por archivo. Para commits grandes, considera limitarlo a archivos críticos o ejecutar las revisiones manualmente con `/review`.

Un **git hook** es un script que Git ejecuta automáticamente en determinados puntos, por ejemplo, justo antes de un commit. Puedes usarlo para ejecutar comprobaciones automatizadas sobre tu código. Aquí tienes cómo configurar una revisión automatizada de Copilot en tus commits:

```bash
# Create a pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    # --allow-all auto-approves file reads/writes so the hook can run unattended.
    # Only use this in automated scripts. In interactive sessions, let Copilot ask for permission.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **Usuarios de macOS**: El comando `timeout` no viene incluido por defecto en macOS. Instálalo con `brew install coreutils` o sustituye `timeout 60` por una invocación simple sin protección de tiempo.

> 📚 **Documentación oficial**: [Usar hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) y [Referencia de configuración de hooks](https://docs.github.com/copilot/reference/hooks-configuration) para la API completa de hooks.
>
> 💡 **Alternativa integrada**: Copilot CLI también tiene un sistema de hooks integrado (`copilot hooks`) que puede ejecutarse automáticamente en eventos como pre-commit. El git hook manual de arriba te da control total, mientras que el sistema integrado es más sencillo de configurar. Consulta la documentación de arriba para decidir qué enfoque encaja con tu flujo de trabajo.

Ahora cada commit recibe una rápida revisión de seguridad:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Output:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## Flujo de trabajo 3: Onboarding en una nueva base de código

Al incorporarte a un nuevo proyecto, combina contexto, agentes y MCP para ponerte al día rápido:

```bash
# Start Copilot in interactive mode
copilot

# PHASE 1: Get the big picture with context
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# PHASE 2: Understand a specific flow
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# PHASE 3: Get expert analysis with an agent
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# PHASE 4: Find something to work on (MCP provides GitHub access)
> List open issues labeled "good first issue"

# PHASE 5: Start contributing
> Pick the simplest open issue and outline a plan to fix it
```

Este flujo de trabajo combina contexto con `@`, agentes y MCP en una sola sesión de onboarding, exactamente el patrón de integración de antes en este capítulo.

---

# Buenas prácticas y automatización

Patrones y hábitos que hacen que tus flujos de trabajo sean más eficaces.

---

## Buenas prácticas

### 1. Empieza con contexto antes del análisis

Reúne siempre contexto antes de pedir un análisis:

```bash
# Good
> Get the details of issue #42
> /agent
# Select python-reviewer
> Analyze this issue

# Less effective
> /agent
# Select python-reviewer
> Fix login bug
# Agent doesn't have issue context
```

### 2. Conoce la diferencia: agentes, skills e instrucciones personalizadas

Cada herramienta tiene su punto fuerte:

```bash
# Agents: Specialized personas you explicitly activate
> /agent
# Select python-reviewer
> Review this authentication code for security issues

# Skills: Modular capabilities that auto-activate when your prompt
# matches the skill's description (you must create them first — see Ch 05)
> Generate comprehensive tests for this code
# If you have a testing skill configured, it activates automatically

# Custom instructions (.github/copilot-instructions.md): Always-on
# guidance that applies to every session without switching or triggering
```

> 💡 **Punto clave**: Los agentes y los skills pueden tanto analizar como generar código. La diferencia real es **cómo se activan** — los agentes son explícitos (`/agent`), los skills son automáticos (se activan según el prompt) y las instrucciones personalizadas están siempre activas.

### 3. Mantén las sesiones enfocadas

Usa `/rename` para etiquetar tu sesión (facilita encontrarla en el historial) y `/exit` para terminarla limpiamente:

```bash
# Good: One feature per session
> /rename list-unread-feature
# Work on list unread
> /exit

copilot
> /rename export-csv-feature
# Work on CSV export
> /exit

# Less effective: Everything in one long session
```

### 4. Haz que los flujos de trabajo sean reutilizables con Copilot

En lugar de simplemente documentar los flujos de trabajo en una wiki, codifícalos directamente en tu repo donde Copilot pueda usarlos:

- **Instrucciones personalizadas** (`.github/copilot-instructions.md`): Guía siempre activa para estándares de codificación, reglas de arquitectura y pasos de build/test/deploy. Cada sesión las sigue automáticamente.
- **Archivos de prompts** (`.github/prompts/`): Prompts reutilizables y parametrizables que tu equipo puede compartir — como plantillas para revisiones de código, generación de componentes o descripciones de PR.
- **Agentes personalizados** (`.github/agents/`): Codifica personas especializadas (p. ej., un revisor de seguridad o un redactor de documentación) que cualquiera del equipo pueda activar con `/agent`.
- **Skills personalizados** (`.github/skills/`): Empaqueta instrucciones de flujo de trabajo paso a paso que se activan automáticamente cuando son relevantes.

> 💡 **El beneficio**: Las nuevas personas del equipo obtienen tus flujos de trabajo gratis — están integrados en el repo, no encerrados en la cabeza de alguien.

---

## Extra: Patrones de producción

Estos patrones son opcionales pero valiosos para entornos profesionales.

### Generador de descripciones de PR

```bash
# Generate comprehensive PR descriptions
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### Integración CI/CD

Para equipos con pipelines de CI/CD existentes, puedes automatizar las revisiones de Copilot en cada pull request usando GitHub Actions. Esto incluye publicar comentarios de revisión automáticamente y filtrar problemas críticos.

> 📖 **Más información**: Consulta [Integración CI/CD](../appendices/ci-cd-integration.md) para flujos de trabajo de GitHub Actions completos, opciones de configuración y consejos de solución de problemas.

---

# Práctica

<img src="../../../images/practice.png" alt="Espacio de escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Pon en práctica el flujo de trabajo completo.

---

## ▶️ Inténtalo tú mismo

Después de completar las demos, prueba estas variantes:

1. **Reto end-to-end**: Elige una pequeña funcionalidad (p. ej., "list unread books" o "export to CSV"). Usa el flujo de trabajo completo:
   - Planifica con `/plan`
   - Diseña con agentes (python-reviewer, pytest-helper)
   - Implementa
   - Genera pruebas
   - Crea un PR

2. **Reto de automatización**: Configura el hook de pre-commit del flujo de Automatización de revisión de código. Haz un commit con una vulnerabilidad intencionada de ruta de archivo. ¿Se bloquea?

3. **Tu flujo de trabajo de producción**: Diseña tu propio flujo de trabajo para una tarea común que hagas. Escríbelo como una checklist. ¿Qué partes podrían automatizarse con skills, agentes o hooks?

**Autoevaluación**: Has completado el curso cuando puedes explicarle a un compañero cómo funcionan juntos agentes, skills y MCP - y cuándo usar cada uno.

---

## 📝 Tarea

### Reto principal: Funcionalidad end-to-end

Los ejemplos prácticos recorrieron la construcción de una funcionalidad "list unread books". Ahora practica el flujo de trabajo completo en una funcionalidad distinta: **buscar libros por rango de años**:

1. Inicia Copilot y reúne contexto: `@samples/book-app-project/books.py`
2. Planifica con `/plan Add a "search by year" command that lets users find books published between two years`
3. Implementa un método `find_by_year_range(start_year, end_year)` en `BookCollection`
4. Añade una función `handle_search_year()` en `book_app.py` que pregunte al usuario por los años de inicio y fin
5. Genera pruebas: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. Revisa con `/review`
7. Actualiza el README: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. Genera un mensaje de commit

Documenta tu flujo de trabajo a medida que avances.

**Criterios de éxito**: Has completado la funcionalidad de la idea al commit usando Copilot CLI, incluyendo planificación, implementación, pruebas, documentación y revisión.

> 💡 **Extra**: Si tienes agentes configurados desde el Capítulo 04, prueba a crear y usar agentes personalizados. Por ejemplo, un agente error-handler para revisión de la implementación y un agente doc-writer para la actualización del README.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Sigue el patrón del ejemplo ["De la idea al PR fusionado"](#idea-to-merged-pr-in-one-session)** del inicio de este capítulo. Los pasos clave son:

1. Reúne contexto con `@samples/book-app-project/books.py`
2. Planifica con `/plan Add a "search by year" command`
3. Implementa el método y el manejador del comando
4. Genera pruebas con casos límite (entrada inválida, resultados vacíos, rango invertido)
5. Revisa con `/review`
6. Actualiza el README con `@samples/book-app-project/README.md`
7. Genera un mensaje de commit con `-p`

**Casos límite a tener en cuenta:**
- ¿Qué pasa si el usuario introduce "2000" y "1990" (rango invertido)?
- ¿Qué pasa si ningún libro coincide con el rango?
- ¿Qué pasa si el usuario introduce datos no numéricos?

**La clave es practicar el flujo de trabajo completo** desde idea → contexto → plan → implementar → probar → documentar → commit.

</details>

---

<details>
<summary>🔧 <strong>Errores comunes</strong> (haz clic para expandir)</summary>

| Error | Qué pasa | Solución |
|---------|--------------|-----|
| Saltar directamente a la implementación | Te pierdes problemas de diseño que cuesta corregir más tarde | Usa primero `/plan` para reflexionar sobre el enfoque |
| Usar una sola herramienta cuando varias ayudarían | Resultados más lentos y menos completos | Combina: agente para análisis → skill para ejecución → MCP para integración |
| No revisar antes de hacer commit | Se cuelan problemas de seguridad o bugs | Ejecuta siempre `/review` o usa un [hook de pre-commit](#workflow-2-code-review-automation-optional) |
| Olvidar compartir flujos de trabajo con el equipo | Cada persona reinventa la rueda | Documenta los patrones en agentes, skills e instrucciones compartidas |

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **Integración > Aislamiento**: Combina herramientas para un máximo impacto
2. **Contexto primero**: Reúne siempre el contexto necesario antes del análisis
3. **Los agentes analizan, los skills ejecutan**: Usa la herramienta adecuada para cada tarea
4. **Automatiza la repetición**: Los hooks y scripts multiplican tu eficacia
5. **Documenta los flujos de trabajo**: Los patrones compartibles benefician a todo el equipo

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver una lista completa de comandos y atajos.

---

## 🎓 ¡Curso completado!

¡Enhorabuena! Has aprendido:

| Capítulo | Lo que has aprendido |
|---------|-------------------|
| 00 | Instalación de Copilot CLI e inicio rápido |
| 01 | Tres modos de interacción |
| 02 | Gestión de contexto con la sintaxis @ |
| 03 | Flujos de trabajo de desarrollo |
| 04 | Agentes especializados |
| 05 | Skills extensibles |
| 06 | Conexiones externas con MCP |
| 07 | Flujos de trabajo unificados de producción |

Ahora estás equipado para usar GitHub Copilot CLI como un auténtico multiplicador de fuerza en tu flujo de trabajo de desarrollo.

## ➡️ Qué sigue

Tu aprendizaje no termina aquí:

1. **Practica a diario**: Usa Copilot CLI para trabajo real
2. **Construye herramientas personalizadas**: Crea agentes y skills para tus necesidades específicas
3. **Comparte conocimiento**: Ayuda a tu equipo a adoptar estos flujos de trabajo
4. **Mantente al día**: Sigue las novedades de GitHub Copilot para nuevas funcionalidades

### Recursos

- [Documentación de GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Registro de servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Skills de la comunidad](https://github.com/topics/copilot-skill)

---

**¡Buen trabajo! Ahora ve a construir algo increíble.**

[**← Volver al Capítulo 06**](../06-mcp-servers/README.md) | [**Volver al inicio del curso →**](../README.md)
