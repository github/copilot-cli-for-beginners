<!--
---
id: CopilotCLI-07
title: !translate Putting It All Together
description: !translate Combine context, workflows, agents, skills, and MCP into complete feature development workflows from idea to pull request.
audience: Developers / Students / Terminal users
slug: putting-it-all-together
weight: 8
---
-->

![Capítulo 07: Poniéndolo todo junto](../../../07-putting-it-together/assets/chapter-header.png)

> **Todo lo que aprendiste se combina aquí. Pasa de la idea a un PR fusionado en una sola sesión.**

En este capítulo, reunirás todo lo que has aprendido en flujos de trabajo completos. Construirás funciones usando colaboración multi-agente, configurarás hooks de pre-commit que detectan problemas de seguridad antes de que se cometan, integrarás Copilot en pipelines de CI/CD y pasarás de la idea de una función a un PR fusionado en una sola sesión de terminal. Aquí es donde GitHub Copilot CLI se convierte en un verdadero multiplicador de fuerza.

> 💡 **Nota**: Este capítulo muestra cómo combinar todo lo que has aprendido. **No necesitas agents, skills o MCP para ser productivo (aunque pueden ser muy útiles).** El flujo de trabajo central — describir, planear, implementar, probar, revisar, lanzar — funciona solo con las funciones integradas de los Capítulos 00-03.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, serás capaz de:

- Combinar agents, skills y MCP (Model Context Protocol) en flujos de trabajo unificados
- Construir funciones completas usando enfoques multi-herramienta
- Configurar automatización básica con hooks
- Aplicar buenas prácticas para desarrollo profesional

> ⏱️ **Tiempo estimado**: ~75 minutos (15 min de lectura + 60 min prácticos)

---

## 🧩 Analogía del mundo real: La orquesta

<img src="../../../07-putting-it-together/assets/orchestra-analogy.png" alt="Analogía de la orquesta - Flujo de trabajo unificado" width="800"/>

Una orquesta sinfónica tiene muchas secciones:
- **Cuerdas** proporcionan la base (como tus flujos de trabajo principales)
- **Metales** añaden potencia (como agents con experiencia especializada)
- **Vientos** añaden color (como skills que amplían capacidades)
- **Percusión** marca el ritmo (como MCP que conecta con sistemas externos)

Individualmente, cada sección suena limitada. Juntas, dirigidas adecuadamente, crean algo magnífico.

**¡Esto es lo que enseña este capítulo!**<br>
*Como un director con una orquesta, orquestas agents, skills y MCP en flujos de trabajo unificados*

Empecemos recorriendo un escenario que modifica código, genera pruebas, lo revisa y crea un PR — todo en una sesión.

---

## Idea a PR fusionado en una sola sesión

En lugar de cambiar entre tu editor, terminal, ejecutor de pruebas y la interfaz de GitHub y perder contexto cada vez, puedes combinar todas tus herramientas en una sesión de terminal. Desglosaremos este patrón en la sección [Patrón de integración](#the-integration-pattern-for-power-users) más abajo.

```bash
# Inicia Copilot en modo interactivo
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot crea un plan de alto nivel...

# CAMBIAR AL AGENTE PYTHON-REVIEWER
> /agent
# Selecciona "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# El agente python-reviewer produce:
# - Firma del método y tipo de retorno
# - Implementación del filtro usando comprensión de listas
# - Manejo de casos límite para colecciones vacías

# CAMBIAR AL AGENTE PYTEST-HELPER
> /agent
# Selecciona "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# El agente pytest-helper produce:
# - Casos de prueba para colecciones vacías
# - Casos de prueba con mezcla de libros leídos y no leídos
# - Casos de prueba con todos los libros leídos

# IMPLEMENTAR
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# PROBAR
> Generate comprehensive tests for the new feature

# Se generan múltiples pruebas similares a las siguientes:
# - Camino feliz (3 pruebas) — filtra correctamente, excluye los leídos, incluye los no leídos
# - Casos límite (4 pruebas) — colección vacía, todos leídos, ninguno leído, un solo libro
# - Parametrizados (5 casos) — variación de proporciones leídos/no leídos vía @pytest.mark.parametrize
# - Integración (4 pruebas) — interacción con mark_as_read, remove_book, add_book y la integridad de los datos

# Revisa los cambios
> /review

# Si la revisión pasa, usa /pr para operar en el pull request de la rama actual
> /pr [view|create|fix|auto]

# O pide de forma natural si quieres que Copilot lo redacte desde la terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**Enfoque tradicional**: Cambiar entre editor, terminal, ejecutor de pruebas, documentación y la interfaz de GitHub. Cada cambio provoca pérdida de contexto y fricción.

**La idea clave**: Dirigiste especialistas como un arquitecto. Ellos manejaron los detalles. Tú manejaste la visión.

> 💡 **Ir más allá**: Para planes grandes con múltiples pasos como este, prueba `/fleet` para dejar que Copilot ejecute subtareas independientes en paralelo. Consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet) para más detalles.

---

# Flujos de trabajo adicionales

<img src="../../../07-putting-it-together/assets/combined-workflows.png" alt="Personas ensamblando un rompecabezas gigante y colorido con engranajes, representando cómo agents, skills y MCP se combinan en flujos de trabajo unificados" width="800"/>

Para usuarios avanzados que completaron los Capítulos 04-06, estos flujos muestran cómo agents, skills y MCP multiplican tu efectividad.

## El patrón de integración

Aquí está el modelo mental para combinar todo:

<img src="../../../07-putting-it-together/assets/integration-pattern.png" alt="El patrón de integración - Un flujo de trabajo de 4 fases: Reunir contexto (MCP), Analizar y planear (Agents), Ejecutar (Skills + Manual), Completar (MCP)" width="800"/>

---

## Flujo 1: Investigación y corrección de bugs

Corrección de bugs en el mundo real con integración completa de herramientas:

```bash
copilot

# FASE 1: Entender el error desde GitHub (MCP proporciona esto)
> Get the details of issue #1

# Aprender: "find_by_author no funciona con nombres parciales"

# FASE 2: Investigar las mejores prácticas (investigación profunda en la web y fuentes de GitHub)
> /research Best practices for Python case-insensitive string matching

# FASE 3: Encontrar código relacionado
> @samples/book-app-project/books.py Show me the find_by_author method

# FASE 4: Obtener análisis experto
> /agent
# Seleccionar "python-reviewer"

> Analyze this method for issues with partial name matching

# El agente identifica: el método usa igualdad exacta en lugar de coincidencia de subcadenas

# FASE 5: Corregir con la orientación del agente
> Implement the fix using lowercase comparison and 'in' operator

# FASE 6: Generar pruebas
> /agent
# Seleccionar "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# FASE 7: Hacer commit y pull request
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## Flujo 2: Automatización de revisión de código (Opcional)

> 💡 **Esta sección es opcional.** Los hooks de pre-commit son útiles para equipos pero no son obligatorios para ser productivo. Omite esto si apenas estás empezando.
>
> ⚠️ **Nota de rendimiento**: Este hook llama a `copilot -p` para cada archivo en staging, lo que toma varios segundos por archivo. Para commits grandes, considera limitarlo a archivos críticos o ejecutar revisiones manualmente con `/review`.

Un **git hook** es un script que Git ejecuta automáticamente en ciertos puntos, por ejemplo, justo antes de un commit. Puedes usar esto para ejecutar comprobaciones automatizadas en tu código. Aquí tienes cómo configurar una revisión automática de Copilot en tus commits:

```bash
# Crear un hook de pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Obtener archivos en el área de preparación (solo archivos Python)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Usar tiempo de espera para evitar que se bloquee (60 segundos por archivo)
    # --allow-all aprueba automáticamente lecturas y escrituras de archivos para que el hook pueda ejecutarse sin supervisión.
    # Usa esto solo en scripts automatizados. En sesiones interactivas, deja que Copilot solicite permiso.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Comprobar si se produjo un tiempo de espera
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

> ⚠️ **Usuarios de macOS**: El comando `timeout` no está incluido por defecto en macOS. Instálalo con `brew install coreutils` o reemplaza `timeout 60` con una invocación simple sin límite de tiempo.

> 📚 **Documentación oficial**: [Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) y [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) para la API completa de hooks.
>
> 💡 **Alternativa integrada**: Copilot CLI también tiene un sistema de hooks integrado (`copilot hooks`) que puede ejecutarse automáticamente en eventos como pre-commit. El git hook manual anterior te da control total, mientras que el sistema integrado es más sencillo de configurar. Revisa la documentación anterior para decidir qué enfoque se ajusta a tu flujo de trabajo.

Ahora cada commit recibe una rápida revisión de seguridad:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Salida:
# Ejecutando la revisión de Copilot en los archivos preparados...
# Revisando samples/book-app-project/books.py...
# Se encontraron problemas críticos en samples/book-app-project/books.py:
# - Línea 15: vulnerabilidad de inyección de ruta de archivo en load_from_file
#
# Corrija el problema y vuelva a intentarlo.
```

---

## Flujo 3: Incorporación a un nuevo codebase

Al unirte a un nuevo proyecto, combina contexto, agents y MCP para incorporarte rápidamente:

```bash
# Iniciar Copilot en modo interactivo
copilot

# FASE 1: Obtén la visión general con contexto
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# FASE 2: Comprende un flujo específico
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# FASE 3: Obtén un análisis experto con un agente
> /agent
# Selecciona "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# FASE 4: Encuentra algo en lo que trabajar (MCP proporciona acceso a GitHub)
> List open issues labeled "good first issue"

# FASE 5: Comienza a contribuir
> Pick the simplest open issue and outline a plan to fix it
```

Este flujo combina el contexto `@`, agents y MCP en una sola sesión de incorporación, exactamente el patrón de integración visto antes en este capítulo.

---

# Buenas prácticas y automatización

Patrones y hábitos que hacen tus flujos de trabajo más efectivos.

---

## Buenas prácticas

### 1. Empieza con contexto antes de analizar

Siempre recopila contexto antes de pedir un análisis:

```bash
# Bueno
> Get the details of issue #42
> /agent
# Seleccionar python-reviewer
> Analyze this issue

# Menos efectivo
> /agent
# Seleccionar python-reviewer
> Fix login bug
# El agente no tiene contexto del problema
```

### 2. Conoce la diferencia: Agents, Skills y Custom Instructions

Cada herramienta tiene su punto fuerte:

```bash
# Agentes: Personas especializadas que activas explícitamente
> /agent
# Selecciona python-reviewer
> Review this authentication code for security issues

# Habilidades: Capacidades modulares que se activan automáticamente cuando tu prompt
# coincide con la descripción de la habilidad (debes crearlas primero — ver Cap. 05)
> Generate comprehensive tests for this code
# Si tienes una habilidad de pruebas configurada, se activa automáticamente

# Instrucciones personalizadas (.github/copilot-instructions.md): Siempre activas
# orientación que se aplica a cada sesión sin cambiar ni activar
```

> 💡 **Punto clave**: Agents y skills pueden tanto analizar COMO generar código. La verdadera diferencia es **cómo se activan** — los agents son explícitos (`/agent`), las skills son automáticas (coincidencia por prompt) y las custom instructions están siempre activas.

### 3. Mantén las sesiones enfocadas

Usa `/rename` para etiquetar tu sesión (facilita encontrarla en el historial) y `/exit` para cerrarla limpiamente:

```bash
# Bueno: Una característica por sesión
> /rename list-unread-feature
# Trabajar en la lista de no leídos
> /exit

copilot
> /rename export-csv-feature
# Trabajar en la exportación a CSV
> /exit

# Menos efectivo: Todo en una sola sesión larga
```

### 4. Haz los flujos de trabajo reutilizables con Copilot

En lugar de solo documentar los flujos en un wiki, incorpóralos directamente en tu repo para que Copilot pueda usarlos:

- **Custom instructions** (`.github/copilot-instructions.md`): Guía siempre activa para estándares de código, reglas de arquitectura y pasos de build/test/deploy. Cada sesión las seguirá automáticamente.
- **Prompt files** (`.github/prompts/`): Prompts reutilizables y parametrizados que tu equipo puede compartir — como plantillas para revisiones de código, generación de componentes o descripciones de PR.
- **Custom agents** (`.github/agents/`): Codifica personajes especializados (p. ej., un revisor de seguridad o un redactor de docs) que cualquiera del equipo puede activar con `/agent`.
- **Custom skills** (`.github/skills/`): Empaqueta instrucciones paso a paso que se auto-activan cuando son relevantes.

> 💡 **El beneficio**: Los nuevos miembros del equipo obtienen tus flujos de trabajo gratis — están integrados en el repo, no atrapados en la cabeza de alguien.

---

## Bonus: Patrones de producción

Estos patrones son opcionales pero valiosos para entornos profesionales.

### Generador de descripción de PR

```bash
# Generar descripciones completas de PR
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### Integración CI/CD

Para equipos con pipelines de CI/CD existentes, puedes automatizar las revisiones de Copilot en cada pull request usando GitHub Actions. Esto incluye publicar comentarios de revisión automáticamente y filtrar por problemas críticos.

> 📖 **Más información**: Consulta [CI/CD Integration](../appendices/ci-cd-integration.md) para flujos de trabajo completos de GitHub Actions, opciones de configuración y consejos para resolver problemas.

---

# Práctica

<img src="../../../assets/practice.png" alt="Escritorio cálido con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Pon el flujo de trabajo completo en práctica.

---

## ▶️ Pruébalo tú mismo

Después de completar las demos, intenta estas variaciones:

1. **Reto de extremo a extremo**: Elige una pequeña función (p. ej., "listar libros no leídos" o "exportar a CSV"). Usa el flujo completo:
   - Planifica con `/plan`
   - Diseña con agents (python-reviewer, pytest-helper)
   - Implementa
   - Genera pruebas
   - Crea PR

2. **Reto de automatización**: Configura el hook de pre-commit del flujo de Automatización de revisión de código. Haz un commit con una vulnerabilidad intencional en la ruta de un archivo. ¿Se bloquea?

3. **Tu flujo de producción**: Diseña tu propio flujo para una tarea común que hagas. Escríbelo como una lista de verificación. ¿Qué partes podrían automatizarse con skills, agents o hooks?

**Autoevaluación**: Has completado el curso cuando puedes explicar a un colega cómo agents, skills y MCP funcionan juntos — y cuándo usar cada uno.

---

## 📝 Tarea

### Desafío principal: Función de extremo a extremo

Los ejemplos prácticos mostraron cómo construir la función "listar libros no leídos". Ahora practica el flujo completo con una función diferente: **buscar libros por rango de años**:

1. Inicia Copilot y reúne contexto: `@samples/book-app-project/books.py`
2. Planifica con `/plan Add a "search by year" command that lets users find books published between two years`
3. Implementa un método `find_by_year_range(start_year, end_year)` en `BookCollection`
4. Añade una función `handle_search_year()` en `book_app.py` que pida al usuario los años de inicio y fin
5. Genera pruebas: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. Revisa con `/review`
7. Actualiza el README: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. Genera un mensaje de commit

Documenta tu flujo mientras avanzas.

**Criterios de éxito**: Has completado la función desde la idea hasta el commit usando Copilot CLI, incluyendo planificación, implementación, pruebas, documentación y revisión.

> 💡 **Bonus**: Si tienes agents configurados desde el Capítulo 04, intenta crear y usar agents personalizados. Por ejemplo, un agent de manejo de errores para la revisión de implementación y un agent redactor de docs para la actualización del README.

<details>
<summary>💡 Sugerencias (haz clic para expandir)</summary>

**Sigue el patrón del ejemplo ["Idea a PR fusionado"](#idea-a-pr-fusionado-en-una-sola-sesión)** al inicio de este capítulo. Los pasos clave son:

1. Reúne contexto con `@samples/book-app-project/books.py`
2. Planifica con `/plan Add a "search by year" command`
3. Implementa el método y el manejador del comando
4. Genera pruebas con casos límite (entrada inválida, resultados vacíos, rango invertido)
5. Revisa con `/review`
6. Actualiza el README con `@samples/book-app-project/README.md`
7. Genera el mensaje de commit con `-p`

**Casos extremos para considerar:**
- ¿Qué pasa si el usuario introduce "2000" y "1990" (rango invertido)?
- ¿Qué pasa si no hay libros que coincidan con el rango?
- ¿Qué pasa si el usuario introduce entrada no numérica?

**La clave es practicar el flujo completo** desde idea → contexto → plan → implementación → pruebas → documentación → commit.

</details>

---

<details>
<summary>🔧 <strong>Errores comunes</strong> (haz clic para expandir)</summary>

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Saltar directamente a la implementación | Se pasan por alto problemas de diseño que son costosos de arreglar más tarde | Usa `/plan` primero para pensar el enfoque |
| Usar una sola herramienta cuando varias ayudarían | Resultados más lentos y menos completos | Combina: Agent para análisis → Skill para ejecución → MCP para integración |
| No revisar antes de commitear | Problemas de seguridad o bugs se filtran | Siempre ejecuta `/review` o usa un [pre-commit hook](#codeblock1) |
| Olvidar compartir los flujos con el equipo | Cada persona reinventa la rueda | Documenta patrones en agents, skills e instrucciones compartidas |

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Integración > Aislamiento**: Combina herramientas para impacto máximo
2. **Contexto primero**: Siempre reúne el contexto requerido antes del análisis
3. **Agents analizan, Skills ejecutan**: Usa la herramienta adecuada para la tarea
4. **Automatiza la repetición**: Hooks y scripts multiplican tu efectividad
5. **Documenta los flujos**: Los patrones compartibles benefician a todo el equipo
> 📋 **Referencia rápida**: Consulta la [Referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para obtener la lista completa de comandos y atajos.

---

## 🎓 ¡Curso completado!

¡Felicidades! Has aprendido:

| Capítulo | Qué aprendiste |
|---------|-------------------|
| 00 | Instalación de Copilot CLI e Inicio rápido |
| 01 | Tres modos de interacción |
| 02 | Gestión de contexto con la sintaxis @ |
| 03 | Flujos de trabajo de desarrollo |
| 04 | Agentes especializados |
| 05 | Habilidades extensibles |
| 06 | Conexiones externas con MCP |
| 07 | Flujos de producción unificados |

Ahora estás preparado para usar GitHub Copilot CLI como un auténtico multiplicador de productividad en tu flujo de trabajo de desarrollo.

## ➡️ ¿Qué sigue?

Tu aprendizaje no termina aquí:

1. **Practica a diario**: Usa Copilot CLI para trabajo real
2. **Crea herramientas personalizadas**: Crea agentes y habilidades para tus necesidades específicas
3. **Comparte conocimientos**: Ayuda a tu equipo a adoptar estos flujos de trabajo
4. **Mantente al día**: Sigue las actualizaciones de GitHub Copilot para nuevas funciones

### Recursos

- [Documentación de GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Registro de servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Habilidades de la comunidad](https://github.com/topics/copilot-skill)

---

**¡Buen trabajo! Ahora crea algo increíble.**

**[← Volver al Capítulo 06](../06-mcp-servers/README.md)** | **[Volver al inicio del curso →](../README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->