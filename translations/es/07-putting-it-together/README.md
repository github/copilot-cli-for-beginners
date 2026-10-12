<!--
---
id: CopilotCLI-07
title: !translate Poniéndolo todo junto
description: !translate Combina contexto, flujos de trabajo, agentes, habilidades y MCP en flujos de trabajo completos de desarrollo de funcionalidades desde la idea hasta el pull request.
audience: Desarrolladores / Estudiantes / Usuarios de terminal
slug: putting-it-all-together
weight: 8
---
-->

![Capítulo 07: Poniéndolo todo junto](../../../07-putting-it-together/assets/chapter-header.png)

> **Todo lo que aprendiste se combina aquí. Pasa de la idea a un PR fusionado en una sola sesión.**

En este capítulo, reunirás todo lo que has aprendido en flujos de trabajo completos. Construirás funcionalidades usando colaboración multiagente, configurarás hooks de pre-commit que detectan problemas de seguridad antes de que se cometan, integrarás Copilot en pipelines de CI/CD y pasarás de la idea de una funcionalidad a un PR fusionado en una sola sesión de terminal. Aquí es donde GitHub Copilot CLI se convierte en un verdadero multiplicador de fuerza.

> 💡 **Nota**: Este capítulo muestra cómo combinar todo lo que aprendiste. **No necesitas agentes, habilidades ni MCP para ser productivo (aunque pueden ser muy útiles).** El flujo de trabajo central — describir, planificar, implementar, probar, revisar, publicar — funciona solo con las funciones integradas de los Capítulos 00-03.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Combinar agentes, habilidades y MCP (Model Context Protocol) en flujos de trabajo unificados
- Crear funcionalidades completas utilizando enfoques multi-herramienta
- Configurar automatización básica con hooks
- Aplicar buenas prácticas para el desarrollo profesional

> ⏱️ **Tiempo estimado**: ~75 minutos (15 min lectura + 60 min práctica)

---

## 🧩 Analogía del mundo real: La orquesta

<img src="../../../07-putting-it-together/assets/orchestra-analogy.png" alt="Analogía de orquesta - Flujo de trabajo unificado" width="800"/>

Una orquesta sinfónica tiene muchas secciones:
- **Cuerdas** proporcionan la base (como tus flujos de trabajo principales)
- **Metales** añaden potencia (como agentes con experiencia especializada)
- **Vientos de madera** añaden color (como habilidades que amplían las capacidades)
- **Percusión** mantiene el ritmo (como MCP conectándose a sistemas externos)

Individualmente, cada sección suena limitada. Juntas, bien dirigidas, crean algo magnífico.

**¡Eso es lo que enseña este capítulo!**<br>
*Como un director con una orquesta, orquestas agentes, habilidades y MCP en flujos de trabajo unificados*

Comencemos recorriendo un escenario que modifica código, genera pruebas, lo revisa y crea un PR - todo en una sola sesión.

---

## De la idea a un PR fusionado en una sola sesión

En lugar de cambiar entre tu editor, terminal, ejecutor de pruebas y la UI de GitHub y perder contexto cada vez, puedes combinar todas tus herramientas en una sola sesión de terminal. Desglosaremos este patrón en la sección [Patrón de integración](#the-integration-pattern-for-power-users) más abajo.

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
# - Casos de prueba con libros leídos/no leídos mezclados
# - Casos de prueba con todos los libros leídos

# IMPLEMENTAR
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# PROBAR
> Generate comprehensive tests for the new feature

# Se generan múltiples pruebas similares a las siguientes:
# - Camino feliz (3 pruebas) — filtra correctamente, excluye los leídos, incluye los no leídos
# - Casos límite (4 pruebas) — colección vacía, todos leídos, ninguno leído, libro único
# - Parametrizados (5 casos) — variando las proporciones leído/no leído mediante @pytest.mark.parametrize
# - Integración (4 pruebas) — interacción con mark_as_read, remove_book, add_book y la integridad de los datos

# Revisa los cambios
> /review

# Si la revisión es aprobada, usa /pr para operar sobre la pull request de la rama actual
> /pr [view|create|fix|auto]

# O pide de forma natural si quieres que Copilot la redacte desde la terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**Enfoque tradicional**: Cambiar entre el editor, la terminal, el ejecutor de pruebas, la documentación y la interfaz de GitHub. Cada cambio provoca pérdida de contexto y fricción.

**La idea clave**: Tú dirigiste a los especialistas como un arquitecto. Ellos se encargaron de los detalles. Tú te encargaste de la visión.

> 💡 **Para profundizar**: Para planes grandes con múltiples pasos como este, prueba `/fleet` para permitir que Copilot ejecute subtareas independientes en paralelo. Consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet) para más detalles.

---

# Flujos de trabajo adicionales

<img src="../../../07-putting-it-together/assets/combined-workflows.png" alt="Personas ensamblando un gran rompecabezas colorido con engranajes, representando cómo agentes, habilidades y MCP se combinan en flujos de trabajo unificados" width="800"/>

Para usuarios avanzados que completaron los Capítulos 04-06, estos flujos muestran cómo agentes, habilidades y MCP multiplican tu efectividad.

## El patrón de integración

Aquí está el modelo mental para combinar todo:

<img src="../../../07-putting-it-together/assets/integration-pattern.png" alt="El patrón de integración - Un flujo de trabajo de 4 fases: Reunir contexto (MCP), Analizar y planificar (Agentes), Ejecutar (Habilidades + Manual), Completar (MCP)" width="800"/>

---

## Flujo de trabajo 1: Investigación y corrección de errores

Corrección de errores en el mundo real con integración completa de herramientas:

```bash
copilot

# FASE 1: Entender el error desde GitHub (MCP proporciona esto)
> Get the details of issue #1

# Aprender: "find_by_author no funciona con nombres parciales"

# FASE 2: Investigar las mejores prácticas (investigación profunda con fuentes web y GitHub)
> /research Best practices for Python case-insensitive string matching

# FASE 3: Encontrar el código relacionado
> @samples/book-app-project/books.py Show me the find_by_author method

# FASE 4: Obtener análisis experto
> /agent
# Seleccionar "python-reviewer"

> Analyze this method for issues with partial name matching

# El agente identifica: el método usa igualdad exacta en lugar de coincidencia de subcadenas

# FASE 5: Corregir con la guía del agente
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

## Flujo de trabajo 2: Automatización de revisión de código (Opcional)

> 💡 **Esta sección es opcional.** Los hooks de pre-commit son útiles para equipos, pero no son necesarios para ser productivo. Omite esto si recién estás empezando.
>
> ⚠️ **Nota de rendimiento**: Este hook llama a `copilot -p` para cada archivo en staging, lo que toma varios segundos por archivo. Para commits grandes, considera limitarlo a archivos críticos o ejecutar las revisiones manualmente con `/review` en su lugar.

Un **git hook** es un script que Git ejecuta automáticamente en ciertos puntos. Por ejemplo, justo antes de un commit. Puedes usar esto para ejecutar comprobaciones automáticas en tu código. Aquí tienes cómo configurar una revisión automática de Copilot en tus commits:

```bash
# Crear un hook de pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Obtener archivos indexados (solo archivos Python)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Usar timeout para evitar que se quede colgado (60 segundos por archivo)
    # --allow-all aprueba automáticamente las lecturas/escrituras de archivos para que el hook pueda ejecutarse sin supervisión.
    # Usa esto solo en scripts automatizados. En sesiones interactivas, deja que Copilot pida permiso.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Comprobar si se produjo un timeout
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

> ⚠️ **Usuarios de macOS**: El comando `timeout` no está incluido por defecto en macOS. Instálalo con `brew install coreutils` o reemplaza `timeout 60` por una invocación simple sin el límite de tiempo.

> 📚 **Documentación oficial**: [Usar hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) y [Referencia de configuración de Hooks](https://docs.github.com/copilot/reference/hooks-configuration) para la API completa de hooks.
>
> 💡 **Alternativa integrada**: Copilot CLI también tiene un sistema de hooks integrado (`copilot hooks`) que puede ejecutarse automáticamente en eventos como pre-commit. El git hook manual anterior te da control total, mientras que el sistema integrado es más sencillo de configurar. Consulta la documentación anterior para decidir qué enfoque se ajusta a tu flujo de trabajo.

Ahora cada commit recibe una revisión rápida de seguridad:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Salida:
# Ejecutando revisión de Copilot en los archivos preparados...
# Revisando samples/book-app-project/books.py...
# Se encontraron problemas críticos en samples/book-app-project/books.py:
# - Línea 15: Vulnerabilidad de inyección de ruta de archivo en load_from_file
#
# Corrige el problema e inténtalo de nuevo.
```

---

## Flujo de trabajo 3: Incorporación a una nueva base de código

Al unirte a un nuevo proyecto, combina contexto, agentes y MCP para integrarte rápidamente:

```bash
# Iniciar Copilot en modo interactivo
copilot

# FASE 1: Obtener la visión general con contexto
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# FASE 2: Comprender un flujo específico
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# FASE 3: Obtener análisis experto con un agente
> /agent
# Seleccionar "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# FASE 4: Encontrar algo en lo que trabajar (MCP proporciona acceso a GitHub)
> List open issues labeled "good first issue"

# FASE 5: Comenzar a contribuir
> Pick the simplest open issue and outline a plan to fix it
```

Este flujo de trabajo combina contexto `@`, agentes y MCP en una sola sesión de incorporación, exactamente el patrón de integración mencionado anteriormente en este capítulo.

---

# Mejores prácticas y automatización

Patrones y hábitos que hacen tus flujos de trabajo más efectivos.

---

## Mejores prácticas

### 1. Comienza con contexto antes del análisis

Siempre recopila contexto antes de pedir análisis:

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

### 2. Conoce la diferencia: Agentes, Habilidades e Instrucciones personalizadas

Cada herramienta tiene un punto fuerte:

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
# orientación que se aplica a cada sesión sin necesidad de cambiar o activar
```

> 💡 **Punto clave**: Agentes y habilidades pueden tanto analizar COMO generar código. La verdadera diferencia es **cómo se activan** — los agentes son explícitos (`/agent`), las habilidades son automáticas (coincidencia por prompt), y las instrucciones personalizadas están siempre activas.

### 3. Mantén las sesiones enfocadas

Usa `/rename` para etiquetar tu sesión (facilita encontrarla en el historial) y `/exit` para terminarla de forma limpia:

```bash
# Bien: una característica por sesión
> /rename list-unread-feature
# Trabajar en la lista de no leídos
> /exit

copilot
> /rename export-csv-feature
# Trabajar en la exportación a CSV
> /exit

# Menos eficaz: todo en una sesión larga
```

### 4. Haz los flujos de trabajo reutilizables con Copilot

En lugar de solo documentar los flujos de trabajo en una wiki, encódelos directamente en tu repo donde Copilot pueda usarlos:

- **Instrucciones personalizadas** (`.github/copilot-instructions.md`): Guía siempre activa para estándares de codificación, reglas de arquitectura y pasos de build/test/despliegue. Cada sesión las sigue automáticamente.
- **Archivos de prompt** (`.github/prompts/`): Prompts reutilizables y parametrizados que tu equipo puede compartir — como plantillas para revisiones de código, generación de componentes o descripciones de PR.
- **Agentes personalizados** (`.github/agents/`): Codifica personas especializadas (p. ej., un revisor de seguridad o un redactor de documentación) que cualquiera en el equipo puede activar con `/agent`.
- **Habilidades personalizadas** (`.github/skills/`): Empaqueta instrucciones paso a paso del flujo de trabajo que se activan automáticamente cuando son relevantes.

> 💡 **El beneficio**: Los nuevos miembros del equipo obtienen tus flujos de trabajo gratis — están integrados en el repo, no encerrados en la cabeza de alguien.

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

Para equipos con pipelines CI/CD existentes, puedes automatizar las revisiones de Copilot en cada pull request usando GitHub Actions. Esto incluye publicar comentarios de revisión automáticamente y filtrar problemas críticos.

> 📖 **Más información**: Consulta [Integración CI/CD](../appendices/ci-cd-integration.md) para flujos completos de trabajo de GitHub Actions, opciones de configuración y consejos de solución de problemas.

---

# Práctica

<img src="../../../assets/practice.png" alt="Configuración acogedora de escritorio con un monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Pon en práctica el flujo de trabajo completo.

---

## ▶️ Pruébalo tú mismo

Después de completar las demos, prueba estas variaciones:

1. **Desafío de extremo a extremo**: Elige una pequeña funcionalidad (p. ej., "listar libros no leídos" o "exportar a CSV"). Usa el flujo de trabajo completo:
   - Planifica con `/plan`
   - Diseña con agentes (python-reviewer, pytest-helper)
   - Implementa
   - Genera pruebas
   - Crea el PR

2. **Desafío de automatización**: Configura el hook de pre-commit del flujo de Automatización de revisión de código. Haz un commit con una vulnerabilidad intencional en la ruta de un archivo. ¿Se bloquea?

3. **Tu flujo de trabajo de producción**: Diseña tu propio flujo de trabajo para una tarea común que realizas. Escríbelo como una lista de verificación. ¿Qué partes podrían automatizarse con habilidades, agentes o hooks?

**Autoevaluación**: Has completado el curso cuando puedas explicarle a un colega cómo agentes, habilidades y MCP funcionan juntos - y cuándo usar cada uno.

---

## 📝 Tarea

### Desafío principal: Funcionalidad de extremo a extremo

Los ejemplos prácticos mostraron cómo construir una funcionalidad de "listar libros no leídos". Ahora practica el flujo de trabajo completo con una funcionalidad diferente: **buscar libros por rango de años**:

1. Inicia Copilot y recopila contexto: `@samples/book-app-project/books.py`
2. Planea con `/plan Add a "search by year" command that lets users find books published between two years`
3. Implementa un método `find_by_year_range(start_year, end_year)` en `BookCollection`
4. Agrega una función `handle_search_year()` en `book_app.py` que solicite al usuario los años de inicio y fin
5. Genera pruebas: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. Revisa con `/review`
7. Actualiza el README: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. Genera un mensaje de commit

Documenta tu flujo de trabajo a medida que avanzas.

**Criterios de éxito**: Has completado la funcionalidad desde la idea hasta el commit usando Copilot CLI, incluyendo planificación, implementación, pruebas, documentación y revisión.

> 💡 **Bonus**: Si tienes agentes configurados del Capítulo 04, intenta crear y usar agentes personalizados. Por ejemplo, un agente manejador de errores para la revisión de la implementación y un agente redactor de documentación para la actualización del README.

<details>
<summary>💡 Consejos (haz clic para expandir)</summary>

**Sigue el patrón del ejemplo ["De la idea a un PR fusionado"](#de-la-idea-a-un-pr-fusionado-en-una-sola-sesión) en la parte superior de este capítulo. Los pasos clave son:**

1. Reúne contexto con `@samples/book-app-project/books.py`
2. Planea con `/plan Add a "search by year" command`
3. Implementa el método y el manejador de comando
4. Genera pruebas con casos límite (entrada inválida, resultados vacíos, rango invertido)
5. Revisa con `/review`
6. Actualiza el README con `@samples/book-app-project/README.md`
7. Genera el mensaje de commit con `-p`

**Casos límite para considerar:**
- ¿Qué pasa si el usuario ingresa "2000" y "1990" (rango invertido)?
- ¿Qué pasa si ningún libro coincide con el rango?
- ¿Qué pasa si el usuario ingresa una entrada no numérica?

**La clave es practicar el flujo de trabajo completo** de idea → contexto → plan → implementar → probar → documentar → commit.

</details>

---

<details>
<summary>🔧 <strong>Errores comunes</strong> (haz clic para expandir)</summary>

| Error | Qué sucede | Solución |
|---------|--------------|-----|
| Saltar directamente a la implementación | Se pasan por alto problemas de diseño que son costosos de arreglar más tarde | Usa `/plan` primero para pensar en el enfoque |
| Usar una sola herramienta cuando varias ayudarían | Resultados más lentos y menos exhaustivos | Combina: Agente para análisis → Habilidad para ejecución → MCP para integración |
| No revisar antes de commitear | Pasan problemas de seguridad o bugs | Ejecuta siempre `/review` o usa un [pre-commit hook](#codeblock1) |
| Olvidar compartir los flujos de trabajo con el equipo | Cada persona reinventa la rueda | Documenta patrones en agentes, habilidades e instrucciones compartidas |

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Integración > Aislamiento**: Combina herramientas para un impacto máximo
2. **Contexto primero**: Siempre recopila el contexto requerido antes del análisis
3. **Los agentes analizan, las habilidades ejecutan**: Usa la herramienta adecuada para la tarea
4. **Automatiza la repetición**: Los hooks y scripts multiplican tu efectividad
5. **Documenta los flujos de trabajo**: Los patrones compartibles benefician a todo el equipo

> 📋 **Referencia rápida**: Consulta la [Referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver la lista completa de comandos y atajos.

---

## 🎓 ¡Curso completado!

¡Felicidades! Has aprendido:

| Chapter | Qué aprendiste |
|---------|-------------------|
| 00 | Instalación de Copilot CLI y inicio rápido |
| 01 | Tres modos de interacción |
| 02 | Gestión de contexto con la sintaxis @ |
| 03 | Flujos de trabajo de desarrollo |
| 04 | Agentes especializados |
| 05 | Habilidades extensibles |
| 06 | Conexiones externas con MCP |
| 07 | Flujos de trabajo de producción unificados |

Ahora estás preparado para usar GitHub Copilot CLI como un auténtico multiplicador de fuerza en tu flujo de trabajo de desarrollo.

## ➡️ ¿Qué sigue?

Tu aprendizaje no se detiene aquí:

1. **Practica diariamente**: Usa Copilot CLI para trabajo real
2. **Crea herramientas personalizadas**: Crea agentes y habilidades para tus necesidades específicas
3. **Comparte conocimiento**: Ayuda a tu equipo a adoptar estos flujos de trabajo
4. **Mantente actualizado**: Sigue las actualizaciones de GitHub Copilot para nuevas funciones

### Recursos

- [Documentación de GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Registro de servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Habilidades de la comunidad](https://github.com/topics/copilot-skill)

---

**¡Gran trabajo! Ahora ve y crea algo increíble.**

**[← Volver al Capítulo 06](../06-mcp-servers/README.md)** | **[Volver al inicio del curso →](../README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->