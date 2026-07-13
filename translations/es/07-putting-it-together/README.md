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

![Capítulo 07: Integrándolo todo](../../../07-putting-it-together/assets/chapter-header.png)

> **Todo lo que aprendiste se combina aquí. Pasa de la idea a un PR fusionado en una sola sesión.**

En este capítulo, reunirás todo lo que has aprendido en flujos de trabajo completos. Construirás funcionalidades usando colaboración multi-agente, configurarás hooks de pre-commit que detecten problemas de seguridad antes de que se hagan commits, integrarás Copilot en pipelines de CI/CD, y pasarás de la idea de una funcionalidad a un PR fusionado en una sola sesión. Aquí es donde GitHub Copilot CLI se convierte en un auténtico multiplicador de fuerza.

> 💡 **Nota**: Este capítulo muestra cómo combinar todo lo que has aprendido. **No necesitas agentes, skills o MCP para ser productivo (aunque pueden ser muy útiles).** El flujo de trabajo básico — describir, planear, implementar, probar, revisar, desplegar — funciona solo con las funciones integradas de los Capítulos 00-03.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Combinar agentes, skills y MCP (Model Context Protocol) en flujos de trabajo unificados
- Desarrollar funciones completas usando enfoques de múltiples herramientas
- Configurar automatización básica con hooks
- Aplicar mejores prácticas para el desarrollo profesional

> ⏱️ **Tiempo estimado**: ~75 minutos (15 min lectura + 60 min práctica)

---

## 🧩 Analogía del mundo real: La orquesta

<img src="../../../07-putting-it-together/assets/orchestra-analogy.png" alt="Analogía de orquesta - Flujo de trabajo unificado" width="800"/>

Una orquesta sinfónica tiene muchas secciones:
- **Cuerdas** proporcionan la base (como tus flujos de trabajo principales)
- **Metales** añaden potencia (como agentes con experiencia especializada)
- **Maderas** añaden color (como skills que amplían capacidades)
- **Percusión** mantiene el ritmo (como MCP conectando con sistemas externos)

Individualmente, cada sección suena limitada. Juntas, bien dirigidas, crean algo magnífico.

**¡Eso es lo que enseña este capítulo!**<br>
*Como un director con una orquesta, orquestas agentes, skills y MCP en flujos de trabajo unificados*

Comencemos recorriendo un escenario que modifica código, genera pruebas, lo revisa y crea un PR - todo en una sola sesión.

---

## De la idea al PR fusionado en una sola sesión

En lugar de cambiar entre tu editor, terminal, ejecutor de pruebas, documentación y la interfaz de GitHub y perder contexto cada vez, puedes combinar todas tus herramientas en una sesión de terminal. Desglosaremos este patrón en la sección [Patrón de integración](#the-integration-pattern-for-power-users) más abajo.

```bash
# Iniciar Copilot en modo interactivo
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot crea un plan de alto nivel...

# CAMBIAR AL AGENTE PYTHON-REVIEWER
> /agent
# Seleccionar "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# El agente python-reviewer produce:
# - Firma del método y tipo de retorno
# - Implementación del filtro usando comprensión de listas
# - Manejo de casos límite para colecciones vacías

# CAMBIAR AL AGENTE PYTEST-HELPER
> /agent
# Seleccionar "pytest-helper"

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
# - Casos límite (4 pruebas) — colección vacía, todos leídos, ninguno leído, un solo libro
# - Parametrizados (5 casos) — variando las proporciones leídos/no leídos mediante @pytest.mark.parametrize
# - Integración (4 pruebas) — interacción con mark_as_read, remove_book, add_book y la integridad de datos

# Revisar los cambios
> /review

# Si la revisión pasa, use /pr para operar sobre la solicitud de extracción (pull request) de la rama actual
> /pr [view|create|fix|auto]

# O pida de forma natural si desea que Copilot lo redacte desde la terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**Enfoque tradicional**: Cambiar entre editor, terminal, ejecutor de pruebas, docs y la interfaz de GitHub. Cada cambio provoca pérdida de contexto y fricción.

**La idea clave**: Tú dirigiste especialistas como un arquitecto. Ellos se ocuparon de los detalles. Tú te encargaste de la visión.

> 💡 **Para ir más lejos**: Para planes multicapa grandes como este, prueba `/fleet` para permitir que Copilot ejecute subtareas independientes en paralelo. Consulta la [documentación oficial](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet) para más detalles.

---

# Flujos de trabajo adicionales

<img src="../../../07-putting-it-together/assets/combined-workflows.png" alt="Personas armando un rompecabezas gigante colorido con engranajes, representando cómo agentes, skills y MCP se combinan en flujos de trabajo unificados" width="800"/>

Para usuarios avanzados que completaron los Capítulos 04-06, estos flujos de trabajo muestran cómo agentes, skills y MCP multiplican tu eficacia.

## El patrón de integración

Aquí está el modelo mental para combinar todo:

<img src="../../../07-putting-it-together/assets/integration-pattern.png" alt="El patrón de integración - Un flujo de trabajo de 4 fases: Recopilar contexto (MCP), Analizar y planificar (Agentes), Ejecutar (Skills + Manual), Completar (MCP)" width="800"/>

---

## Flujo de trabajo 1: Investigación y corrección de errores

Corrección de errores en el mundo real con integración completa de herramientas:

```bash
copilot

# FASE 1: Entender el fallo en GitHub (MCP lo proporciona)
> Get the details of issue #1

# Aprender: "find_by_author no funciona con nombres parciales"

# FASE 2: Investigar las mejores prácticas (investigación profunda con fuentes web y de GitHub)
> /research Best practices for Python case-insensitive string matching

# FASE 3: Encontrar código relacionado
> @samples/book-app-project/books.py Show me the find_by_author method

# FASE 4: Obtener análisis de expertos
> /agent
# Seleccionar "python-reviewer"

> Analyze this method for issues with partial name matching

# El agente identifica: el método usa igualdad exacta en lugar de coincidencia por subcadena

# FASE 5: Corregir con la guía del agente
> Implement the fix using lowercase comparison and 'in' operator

# FASE 6: Generar pruebas
> /agent
# Seleccionar "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# FASE 7: Realizar commit y solicitud de extracción
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## Flujo de trabajo 2: Automatización de revisión de código (Opcional)

> 💡 **Esta sección es opcional.** Los hooks de pre-commit son útiles para equipos pero no son necesarios para ser productivo. Omítelo si recién estás comenzando.
>
> ⚠️ **Nota sobre rendimiento**: Este hook llama a `copilot -p` para cada archivo en staging, lo que toma varios segundos por archivo. Para commits grandes, considera limitarlo a archivos críticos o ejecutar las revisiones manualmente con `/review` en su lugar.

Un **git hook** es un script que Git ejecuta automáticamente en ciertos momentos. Por ejemplo, justo antes de un commit. Puedes usar esto para ejecutar comprobaciones automatizadas en tu código. Aquí se explica cómo configurar una revisión automatizada de Copilot en tus commits:

```bash
# Crear un hook de pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Obtener archivos preparados (solo archivos Python)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Usar timeout para evitar que se quede colgado (60 segundos por archivo)
    # --allow-all aprueba automáticamente las lecturas/escrituras de archivos para que el hook pueda ejecutarse sin supervisión.
    # Usar esto solo en scripts automatizados. En sesiones interactivas, deje que Copilot pida permiso.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Comprobar si ocurrió un timeout
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

> ⚠️ **Usuarios de macOS**: El comando `timeout` no está incluido por defecto en macOS. Instálalo con `brew install coreutils` o reemplaza `timeout 60` por una invocación simple sin guardia de tiempo.

> 📚 **Documentación oficial**: [Uso de hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) y [Referencia de configuración de hooks](https://docs.github.com/copilot/reference/hooks-configuration) para la API completa de hooks.
>
> 💡 **Alternativa integrada**: Copilot CLI también tiene un sistema de hooks integrado (`copilot hooks`) que puede ejecutarse automáticamente en eventos como pre-commit. El git hook manual anterior te da control total, mientras que el sistema integrado es más fácil de configurar. Consulta la documentación arriba para decidir qué enfoque se adapta a tu flujo de trabajo.

Ahora cada commit recibe una revisión de seguridad rápida:

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Salida:
# Ejecutando la revisión de Copilot en los archivos preparados...
# Revisando samples/book-app-project/books.py...
# Se encontraron problemas críticos en samples/book-app-project/books.py:
# - Línea 15: Vulnerabilidad de inyección de ruta de archivo en load_from_file
#
# Corrige el problema y vuelve a intentarlo.
```

---

## Flujo de trabajo 3: Incorporación a una nueva base de código

Al unirte a un proyecto nuevo, combina contexto, agentes y MCP para ponerte al día rápidamente:

```bash
# Iniciar Copilot en modo interactivo
copilot

# FASE 1: Obtener la visión general con contexto
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# FASE 2: Entender un flujo específico
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# FASE 3: Obtener análisis experto con un agente
> /agent
# Seleccionar "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# FASE 4: Encontrar algo en qué trabajar (MCP proporciona acceso a GitHub)
> List open issues labeled "good first issue"

# FASE 5: Empezar a contribuir
> Pick the simplest open issue and outline a plan to fix it
```

Este flujo de trabajo combina `@` contexto, agentes y MCP en una única sesión de incorporación, exactamente el patrón de integración visto anteriormente en este capítulo.

---

# Mejores prácticas y automatización

Patrones y hábitos que hacen tus flujos de trabajo más eficaces.

---

## Mejores prácticas

### 1. Comienza con el contexto antes del análisis

Siempre reúne contexto antes de pedir un análisis:

```bash
# Bien
> Get the details of issue #42
> /agent
# Seleccionar python-reviewer
> Analyze this issue

# Menos eficaz
> /agent
# Seleccionar python-reviewer
> Fix login bug
# El agente no tiene contexto del problema
```

### 2. Conoce la diferencia: Agentes, Skills e instrucciones personalizadas

Cada herramienta tiene su punto fuerte:

```bash
# Agentes: Personas especializadas que activas explícitamente
> /agent
# Selecciona python-reviewer
> Review this authentication code for security issues

# Habilidades: Capacidades modulares que se activan automáticamente cuando tu indicación
# coincide con la descripción de la habilidad (debes crearlas primero — ver Cap. 05)
> Generate comprehensive tests for this code
# Si tienes una habilidad de pruebas configurada, se activa automáticamente

# Instrucciones personalizadas (.github/copilot-instructions.md): Siempre activas
# orientación que se aplica a cada sesión sin necesidad de cambiarla o activarla
```

> 💡 **Punto clave**: Los agentes y los skills pueden tanto analizar COMO generar código. La diferencia real es **cómo se activan** — los agentes son explícitos (`/agent`), los skills son automáticos (coinciden con el prompt), y las instrucciones personalizadas están siempre activas.

### 3. Mantén las sesiones enfocadas

Usa `/rename` para etiquetar tu sesión (hace que sea fácil encontrarla en el historial) y `/exit` para terminarla correctamente:

```bash
# Bien: una característica por sesión
> /rename list-unread-feature
# Trabajar en la lista de elementos no leídos
> /exit

copilot
> /rename export-csv-feature
# Trabajar en la exportación a CSV
> /exit

# Menos efectivo: todo en una sesión larga
```

### 4. Haz los flujos de trabajo reutilizables con Copilot

En lugar de solo documentar flujos de trabajo en una wiki, codifícalos directamente en tu repo donde Copilot pueda utilizarlos:

- **Instrucciones personalizadas** (`.github/copilot-instructions.md`): Orientación siempre activa para estándares de codificación, reglas de arquitectura y pasos de build/test/deploy. Cada sesión las sigue automáticamente.
- **Archivos de prompts** (`.github/prompts/`): Prompts reutilizables y parametrizados que tu equipo puede compartir — como plantillas para revisiones de código, generación de componentes o descripciones de PR.
- **Agentes personalizados** (`.github/agents/`): Codifica personalidades especializadas (p. ej., un revisor de seguridad o un redactor de documentación) que cualquier persona del equipo puede activar con `/agent`.
- **Skills personalizados** (`.github/skills/`): Empaqueta instrucciones paso a paso de flujos de trabajo que se activan automáticamente cuando son relevantes.

> 💡 **La recompensa**: Los nuevos miembros del equipo obtienen tus flujos de trabajo gratis — están integrados en el repo, no encerrados en la cabeza de alguien.

---

## Bonus: Patrones para producción

Estos patrones son opcionales pero valiosos para entornos profesionales.

### Generador de descripción de PR

```bash
# Generar descripciones completas de pull requests
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

> 📖 **Más información**: Ve [Integración CI/CD](../appendices/ci-cd-integration.md) para flujos de trabajo completos de GitHub Actions, opciones de configuración y consejos para solucionar problemas.

---

# Práctica

<img src="../../../assets/practice.png" alt="Configuración de escritorio acogedora con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica" width="800"/>

Ponte a practicar el flujo de trabajo completo.

---

## ▶️ Pruébalo tú mismo

Después de completar las demos, prueba estas variaciones:

1. **Desafío de extremo a extremo**: Elige una pequeña funcionalidad (p. ej., "listar libros no leídos" o "exportar a CSV"). Usa el flujo de trabajo completo:
   - Planifica con `/plan`
   - Diseña con agentes (python-reviewer, pytest-helper)
   - Implementa
   - Genera pruebas
   - Crea PR

2. **Desafío de automatización**: Configura el hook de pre-commit del flujo de trabajo de Automatización de revisión de código. Haz un commit con una vulnerabilidad intencional en la ruta de archivo. ¿Se bloquea?

3. **Tu flujo de trabajo de producción**: Diseña tu propio flujo para una tarea común que realices. Escríbelo como una lista de verificación. ¿Qué partes podrían automatizarse con skills, agentes o hooks?

**Autoevaluación**: Has completado el curso cuando puedas explicar a un colega cómo agentes, skills y MCP funcionan juntos - y cuándo usar cada uno.

---

## 📝 Tarea

### Desafío principal: Funcionalidad de extremo a extremo

Los ejemplos prácticos recorrieron la construcción de la funcionalidad "listar libros no leídos". Ahora practica el flujo completo en una funcionalidad diferente: **buscar libros por rango de años**:

1. Inicia Copilot y reúne contexto: `@samples/book-app-project/books.py`
2. Planifica con `/plan Add a "search by year" command that lets users find books published between two years`
3. Implementa un método `find_by_year_range(start_year, end_year)` en `BookCollection`
4. Agrega una función `handle_search_year()` en `book_app.py` que solicite al usuario los años de inicio y fin
5. Genera pruebas: `@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. Revisa con `/review`
7. Actualiza el README: `@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. Genera un mensaje de commit

Documenta tu flujo de trabajo mientras avanzas.

**Criterios de éxito**: Has completado la funcionalidad desde la idea hasta el commit usando Copilot CLI, incluyendo planificación, implementación, pruebas, documentación y revisión.

> 💡 **Bonus**: Si tienes agentes configurados del Capítulo 04, prueba crear y usar agentes personalizados. Por ejemplo, un agente manejador de errores para la revisión de implementación y un agente redactor de docs para la actualización del README.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Sigue el patrón del ejemplo ["De la idea al PR fusionado"](#de-la-idea-al-pr-fusionado-en-una-sola-sesión) en la parte superior de este capítulo. Los pasos clave son:**

1. Reúne contexto con `@samples/book-app-project/books.py`
2. Planifica con `/plan Add a "search by year" command`
3. Implementa el método y el handler del comando
4. Genera pruebas con casos límite (entrada inválida, resultados vacíos, rango invertido)
5. Revisa con `/review`
6. Actualiza el README con `@samples/book-app-project/README.md`
7. Genera el mensaje de commit con `-p`

**Casos límite a considerar:**
- ¿Qué pasa si el usuario introduce "2000" y "1990" (rango invertido)?
- ¿Qué pasa si ningún libro coincide con el rango?
- ¿Qué pasa si el usuario introduce entrada no numérica?

**La clave es practicar el flujo de trabajo completo** desde idea → contexto → plan → implementar → probar → documentar → commit.

</details>

---

<details>
<summary>🔧 <strong>Errores comunes</strong> (haz clic para expandir)</summary>

| Error | Qué sucede | Solución |
|---------|--------------|-----|
| Saltar directamente a la implementación | Se pasan por alto problemas de diseño que son costosos de arreglar más tarde | Usa `/plan` primero para pensar en el enfoque |
| Usar una sola herramienta cuando varias ayudarían | Resultados más lentos y menos exhaustivos | Combina: Agente para análisis → Skill para ejecución → MCP para integración |
| No revisar antes de hacer commit | Problemas de seguridad o errores se filtran | Ejecuta siempre `/review` o usa un [pre-commit hook](#codeblock1) |
| Olvidar compartir los flujos de trabajo con el equipo | Cada persona reinventa la rueda | Documenta los patrones en agentes, skills e instrucciones compartidas |

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Integración > Aislamiento**: Combina herramientas para máximo impacto
2. **Contexto primero**: Siempre recopila el contexto requerido antes del análisis
3. **Los agentes analizan, los Skills ejecutan**: Usa la herramienta adecuada para el trabajo
4. **Automatiza la repetición**: Hooks y scripts multiplican tu efectividad
5. **Documenta los flujos de trabajo**: Los patrones compartibles benefician a todo el equipo


> 📋 **Referencia rápida**: Consulta la [Referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## 🎓 ¡Curso completado!

¡Felicidades! Has aprendido:

| Capítulo | Qué aprendiste |
|---------|-------------------|
| 00 | Instalación de Copilot CLI y inicio rápido |
| 01 | Tres modos de interacción |
| 02 | Gestión del contexto con la sintaxis @ |
| 03 | Flujos de trabajo de desarrollo |
| 04 | Agentes especializados |
| 05 | Habilidades extensibles |
| 06 | Conexiones externas con MCP |
| 07 | Flujos de trabajo de producción unificados |

Ahora estás equipado para usar GitHub Copilot CLI como un auténtico multiplicador de fuerza en tu flujo de trabajo de desarrollo.

## ➡️ ¿Qué sigue?

Tu aprendizaje no termina aquí:

1. **Practica a diario**: Usa Copilot CLI para trabajo real
2. **Desarrolla herramientas personalizadas**: Crea agentes y habilidades para tus necesidades específicas
3. **Comparte conocimientos**: Ayuda a tu equipo a adoptar estos flujos de trabajo
4. **Mantente actualizado**: Sigue las actualizaciones de GitHub Copilot para nuevas funciones

### Recursos

- [Documentación de GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [Registro de servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Habilidades de la comunidad](https://github.com/topics/copilot-skill)

---

**¡Buen trabajo! Ahora ve y crea algo increíble.**

**[← Volver al Capítulo 06](../06-mcp-servers/README.md)** | **[Volver al inicio del curso →](../README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->