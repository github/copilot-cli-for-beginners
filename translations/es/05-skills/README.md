![Capítulo 05: Sistema de Skills](../../../05-skills/images/chapter-header.png)

> **¿Y si Copilot pudiera aplicar automáticamente las mejores prácticas de tu equipo sin que tengas que explicarlas cada vez?**

En este capítulo aprenderás sobre las Agent Skills: carpetas de instrucciones que Copilot carga automáticamente cuando son relevantes para tu tarea. Mientras que los agentes cambian *cómo* piensa Copilot, las skills le enseñan *formas concretas de completar tareas*. Crearás una skill de auditoría de seguridad que Copilot aplicará siempre que preguntes sobre seguridad, construirás criterios de revisión estándar del equipo que aseguren una calidad de código consistente y aprenderás cómo funcionan las skills en Copilot CLI, VS Code y el agente en la nube de GitHub Copilot.


## 🎯 Objetivos de aprendizaje

Al final de este capítulo, serás capaz de:

- Entender cómo funcionan las Agent Skills y cuándo usarlas
- Crear skills personalizadas con archivos SKILL.md
- Usar skills de la comunidad desde repositorios compartidos
- Saber cuándo usar skills, agentes o MCP

> ⏱️ **Tiempo estimado**: ~55 minutos (20 min de lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: herramientas eléctricas

Un taladro de propósito general es útil, pero los accesorios especializados lo hacen potente. 
<img src="../../../05-skills/images/power-tools-analogy.png" alt="Herramientas eléctricas - Las skills amplían las capacidades de Copilot" width="800"/>


Las skills funcionan igual. Igual que cambias las brocas del taladro para distintos trabajos, puedes añadir skills a Copilot para diferentes tareas:

| Accesorio (Skill) | Propósito |
|------------|---------|
| `commit` | Generar mensajes de commit consistentes |
| `security-audit` | Comprobar vulnerabilidades OWASP |
| `generate-tests` | Crear pruebas pytest exhaustivas |
| `code-checklist` | Aplicar estándares de calidad de código del equipo |



*Las skills son accesorios especializados que amplían lo que Copilot puede hacer*

---

# Cómo funcionan las skills

<img src="../../../05-skills/images/how-skills-work.png" alt="Iconos de skill estilo RPG brillantes conectados por estelas de luz sobre un fondo estelar que representan las skills de Copilot" width="800"/>

Aprende qué son las skills, por qué importan y en qué se diferencian de los agentes y MCP.

---

## *¿Nuevo en skills?* ¡Empieza aquí!

1. **Mira qué skills ya están disponibles:**
   ```bash
   copilot
   > /skills list
   ```
   Esto muestra todas las skills que Copilot puede encontrar, incluidas las **skills integradas** que vienen con la propia CLI, además de las skills de tu proyecto y de tus carpetas personales.

   > 💡 **Skills integradas**: Copilot CLI viene con skills preinstaladas listas para usar. Por ejemplo, la skill `customizing-copilot-cloud-agents-environment` proporciona una guía para personalizar el entorno del agente en la nube de Copilot. No necesitas crear ni instalar nada para usarlas. Ejecuta `/skills list` para ver lo que está disponible.

2. **Mira un archivo de skill real:** Echa un vistazo a nuestro ejemplo [code-checklist SKILL.md](../../../.github/skills/code-checklist/SKILL.md) para ver el patrón. Es solo frontmatter YAML más instrucciones en Markdown.

3. **Entiende el concepto clave:** Las skills son instrucciones específicas de tarea que Copilot carga *automáticamente* cuando tu prompt coincide con la descripción de la skill. No necesitas activarlas; basta con preguntar de forma natural.


## Entender las skills

Las Agent Skills son carpetas que contienen instrucciones, scripts y recursos que Copilot **carga automáticamente cuando son relevantes** para tu tarea. Copilot lee tu prompt, comprueba si alguna skill coincide y aplica las instrucciones pertinentes automáticamente.

```bash
copilot

> Check books.py against our quality checklist
# Copilot detects this matches your "code-checklist" skill
# and automatically applies its Python quality checklist

> Generate tests for the BookCollection class
# Copilot loads your "pytest-gen" skill
# and applies your preferred test structure

> What are the code quality issues in this file?
# Copilot loads your "code-checklist" skill
# and checks against your team's standards
```

> 💡 **Idea clave**: Las skills se **disparan automáticamente** cuando tu prompt coincide con la descripción de la skill. Solo pregunta de forma natural y Copilot aplicará las skills relevantes en segundo plano. También puedes invocar skills directamente, como verás a continuación.

> 🧰 **Plantillas listas para usar**: Echa un vistazo a la carpeta [.github/skills](../../../.github/skills/) para ver skills sencillas que puedes copiar, pegar y probar.

### Invocación directa con slash command

Aunque el autodisparo es la forma principal en que funcionan las skills, también puedes **invocar skills directamente** usando su nombre como un slash command:

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

Esto te da control explícito cuando quieres asegurarte de que se use una skill concreta.

#### Combinar varias skills en un mismo mensaje

Puedes invocar **más de una skill en un solo mensaje**, y el slash command de la skill puede aparecer en cualquier parte de tu prompt, no solo al principio. Esto es práctico cuando quieres realizar dos comprobaciones distintas de una sola vez:

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot aplicará cada skill nombrada en la misma respuesta, ahorrándote tener que enviar varios mensajes por separado.

> 💡 **Consejo**: Coloca los slash commands de skill donde resulte más natural en tu frase. Puedes ponerlos al principio, en medio o al final de tu mensaje.

> 📝 **Invocación de skills vs agentes**: No confundas la invocación de skills con la invocación de agentes:
> - **Skills**: `/skill-name <prompt>`, por ejemplo, `/code-checklist Check this file`
> - **Agentes**: `/agent` (selecciona de la lista) o `copilot --agent <name>` (línea de comandos)
>
> Si tienes una skill y un agente con el mismo nombre (por ejemplo, "code-reviewer"), escribir `/code-reviewer` invoca la **skill**, no el agente.

### ¿Cómo sé que se ha usado una skill?

Puedes preguntárselo directamente a Copilot:

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### Skills vs agentes vs MCP

Las skills son solo una pieza del modelo de extensibilidad de GitHub Copilot. Aquí tienes cómo se comparan con los agentes y los servidores MCP.

> *No te preocupes por MCP todavía. Lo cubriremos en el [Capítulo 06](../06-mcp-servers/). Se incluye aquí para que veas cómo encajan las skills en el cuadro general.*

<img src="../../../05-skills/images/skills-agents-mcp-comparison.png" alt="Diagrama comparativo que muestra las diferencias entre Agentes, Skills y servidores MCP y cómo se combinan en tu flujo de trabajo" width="800"/>

| Característica | Qué hace | Cuándo usarla |
|---------|--------------|-------------|
| **Agentes** | Cambian cómo piensa la IA | Necesitas experiencia especializada en muchas tareas |
| **Skills** | Proporcionan instrucciones específicas de tarea | Tareas específicas y repetibles con pasos detallados |
| **MCP** | Conecta servicios externos | Necesitas datos en vivo desde APIs |

Usa agentes para experiencia amplia, skills para instrucciones de tareas concretas, y MCP para datos externos. Un agente puede usar una o varias skills durante una conversación. Por ejemplo, cuando le pides a un agente que revise tu código, podría aplicar automáticamente tanto una skill `security-audit` como una skill `code-checklist`.

> 📚 **Aprende más**: Consulta la documentación oficial [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) para la referencia completa sobre formatos de skills y mejores prácticas.

---

## De los prompts manuales a la experiencia automática

Antes de profundizar en cómo crear skills, veamos *por qué* merece la pena aprenderlas. Una vez que veas las ganancias en consistencia, el "cómo" tendrá más sentido.

### Antes de las skills: revisiones inconsistentes

En cada revisión de código, podrías olvidar algo:

```bash
copilot

> Review this code for issues
# Generic review - might miss your team's specific concerns
```

O escribes un prompt largo cada vez:

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

Tiempo: **más de 30 segundos** para teclear. Consistencia: **depende de la memoria**.

### Después de las skills: mejores prácticas automáticas

Con una skill `code-checklist` instalada, basta con preguntar de forma natural:

```bash
copilot

> Check the book collection code for quality issues
```

**Lo que pasa entre bastidores**:
1. Copilot ve "code quality" e "issues" en tu prompt
2. Comprueba las descripciones de las skills, encuentra que tu skill `code-checklist` coincide
3. Carga automáticamente la checklist de calidad de tu equipo
4. Aplica todas las comprobaciones sin que tú las enumeres

<img src="../../../05-skills/images/skill-auto-discovery-flow.png" alt="Cómo se autodisparan las skills - Flujo de 4 pasos que muestra cómo Copilot empareja automáticamente tu prompt con la skill adecuada" width="800"/>

*Solo pregunta de forma natural. Copilot empareja tu prompt con la skill adecuada y la aplica automáticamente.*

**Salida**:
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**La diferencia**: Los estándares de tu equipo se aplican automáticamente, cada vez, sin tener que escribirlos.

---

<details>
<summary>🎬 ¡Mira la demo!</summary>

![Demo de disparo de skill](../../../05-skills/images/skill-trigger-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán distintas a las que se muestran aquí.*

</details>

---

## Consistencia a escala: skill de revisión de PR del equipo

Imagina que tu equipo tiene una checklist de PR de 10 puntos. Sin una skill, cada desarrollador debe recordar los 10 puntos, y siempre alguien olvida uno. Con una skill `pr-review`, todo el equipo recibe revisiones consistentes:

```bash
copilot

> Can you review this PR?
```

Copilot carga automáticamente la skill `pr-review` de tu equipo y comprueba los 10 puntos:

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**El poder**: Cada miembro del equipo aplica los mismos estándares automáticamente. Las nuevas incorporaciones no necesitan memorizar la checklist porque la skill se encarga.

---

# Crear skills personalizadas

<img src="../../../05-skills/images/creating-managing-skills.png" alt="Manos humanas y robóticas construyendo un muro de bloques tipo LEGO brillantes que representan la creación y gestión de skills" width="800"/>

Construye tus propias skills a partir de archivos SKILL.md.

---

## Ubicaciones de las skills

Las skills se almacenan en `.github/skills/` (específicas del proyecto) o `~/.copilot/skills/` (a nivel de usuario).

### Cómo encuentra Copilot las skills

Copilot escanea automáticamente estas ubicaciones en busca de skills:

| Ubicación | Ámbito |
|----------|-------|
| `.github/skills/` | Específica del proyecto (compartida con el equipo vía git) |
| `~/.copilot/skills/` | Específica del usuario (tus skills personales) |

### Estructura de una skill

Cada skill vive en su propia carpeta con un archivo `SKILL.md`. Opcionalmente puedes incluir scripts, ejemplos u otros recursos:

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Required: Skill definition and instructions
    ├── examples/          # Optional: Example files Copilot can reference
    │   └── sample.py
    └── scripts/           # Optional: Scripts the skill can use
        └── validate.sh
```

> 💡 **Consejo**: El nombre del directorio debería coincidir con el `name` del frontmatter de tu SKILL.md (minúsculas con guiones).

### Formato de SKILL.md

Las skills usan un formato Markdown sencillo con frontmatter YAML:

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**Propiedades YAML:**

| Propiedad | Obligatoria | Descripción |
|----------|----------|-------------|
| `name` | **Sí** | Identificador único (minúsculas, guiones para los espacios) |
| `description` | **Sí** | Lo que hace la skill y cuándo debería usarla Copilot |
| `license` | No | Licencia que se aplica a esta skill |

> 📖 **Documentación oficial**: [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### Crea tu primera skill

Vamos a construir una skill de auditoría de seguridad que comprueba las vulnerabilidades del OWASP Top 10:

```bash
# Create skill directory
mkdir -p .github/skills/security-audit

# Create the SKILL.md file
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Test your skill (skills load automatically based on your prompt)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot detects "security vulnerabilities" matches your skill
# and automatically applies its OWASP checklist
```

**Salida esperada** (tus resultados pueden variar):

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## Escribir buenas descripciones de skill

¡El campo `description` en tu SKILL.md es crucial! Es como Copilot decide si cargar tu skill:

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **Consejo**: Incluye palabras clave que coincidan con cómo haces las preguntas de forma natural. Si dices "security review", incluye "security review" en la descripción.

### Combinar skills con agentes

Skills y agentes funcionan juntos. El agente aporta la experiencia, la skill aporta las instrucciones específicas:

```bash
# Start with a code-reviewer agent
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer agent's expertise combines
# with your code-checklist skill's checklist
```

---

# Gestionar y compartir skills

Descubre las skills instaladas, encuentra skills de la comunidad y comparte las tuyas.

<img src="../../../05-skills/images/managing-sharing-skills.png" alt="Gestionar y compartir skills - mostrando el ciclo descubrir, usar, crear y compartir para skills de la CLI" width="800" />

---

## Gestionar skills con el comando `/skills`

Usa el comando `/skills` para gestionar tus skills instaladas:

| Comando | Qué hace |
|---------|--------------|
| `/skills list` | Muestra todas las skills instaladas |
| `/skills info <name>` | Obtiene detalles sobre una skill concreta |
| `/skills add <name>` | Habilita una skill (desde un repositorio o marketplace) |
| `/skills remove <name>` | Desactiva o desinstala una skill |
| `/skills reload` | Recarga las skills tras editar archivos SKILL.md |

> 💡 **Recuerda**: No necesitas "activar" las skills para cada prompt. Una vez instaladas, las skills se **disparan automáticamente** cuando tu prompt coincide con su descripción. Estos comandos sirven para gestionar qué skills están disponibles, no para usarlas.

### Ejemplo: ver tus skills

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>¡Mira la demo!</summary>

![Demo de listar skills](../../../05-skills/images/list-skills-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán distintas a las que se muestran aquí.*

</details>

---

### Cuándo usar `/skills reload`

Después de crear o editar el archivo SKILL.md de una skill, ejecuta `/skills reload` para incorporar los cambios sin reiniciar Copilot:

```bash
# Edit your skill file
# Then in Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **Bueno saberlo**: Las skills siguen siendo efectivas incluso después de usar `/compact` para resumir tu historial de conversación. No es necesario recargar tras compactar.

---

## Encontrar y usar skills de la comunidad

### Usar plugins para instalar skills

> 💡 **¿Qué son los plugins?** Los plugins son paquetes instalables que pueden agrupar skills, agentes y configuraciones de servidores MCP. Piénsalos como extensiones de "tienda de aplicaciones" para Copilot CLI.

El comando `/plugin` te permite explorar e instalar estos paquetes:

```bash
copilot

> /plugin list
# Shows installed plugins

> /plugin marketplace
# Browse available plugins

> /plugin install <plugin-name>
# Install a plugin from the marketplace
```

Para mantener al día tu catálogo local de plugins, actualízalo con:

```bash
copilot plugin marketplace update
```

Los plugins pueden agrupar varias capacidades. Un único plugin puede incluir skills relacionadas, agentes y configuraciones de servidores MCP que funcionen juntos.

### Repositorios de skills de la comunidad

También hay skills prefabricadas disponibles en repositorios de la comunidad:

- [**Awesome Copilot**](https://github.com/github/awesome-copilot) - Recursos oficiales de GitHub Copilot incluyendo documentación y ejemplos de skills

### Instalar una skill de la comunidad con GitHub CLI

La forma más sencilla de instalar una skill desde un repositorio de GitHub es usar el comando `gh skill install` (requiere [GitHub CLI v2.90.0+](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)):

```bash
# Browse and interactively select a skill from awesome-copilot
gh skill install github/awesome-copilot

# Or install a specific skill directly
gh skill install github/awesome-copilot code-checklist

# Install for personal use across all projects (user scope)
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **Revisa antes de instalar**: Lee siempre el `SKILL.md` de una skill antes de instalarla. Las skills controlan lo que hace Copilot, y una skill maliciosa podría indicarle que ejecute comandos dañinos o que modifique código de formas inesperadas.

---

# Práctica

<img src="../../../images/practice.png" alt="Escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

Aplica lo que has aprendido construyendo y probando tus propias skills.

---

## ▶️ Inténtalo tú mismo

### Construye más skills

Aquí tienes dos skills más que muestran patrones diferentes. Sigue el mismo flujo `mkdir` + `cat` de "Crea tu primera skill" más arriba o copia y pega las skills en la ubicación correcta. Hay más ejemplos disponibles en [.github/skills](../../../.github/skills).

### Skill de generación de tests pytest

Una skill que asegura una estructura pytest consistente en todo tu codebase:

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### Skill de revisión de PR del equipo

Una skill que aplica estándares de revisión de PR consistentes en tu equipo:

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### Ve más allá

1. **Reto de creación de skill**: Crea una skill `quick-review` que haga una checklist de 3 puntos:
   - Cláusulas bare except
   - Type hints faltantes
   - Nombres de variables poco claros

   Pruébala preguntando: "Do a quick review of books.py"

2. **Comparativa de skill**: Cronométrate escribiendo manualmente un prompt detallado de revisión de seguridad. Después, simplemente pregunta "Check for security issues in this file" y deja que tu skill `security-audit` se cargue automáticamente. ¿Cuánto tiempo te ha ahorrado la skill?

3. **Reto de skill de equipo**: Piensa en la checklist de revisión de código de tu equipo. ¿Podrías codificarla como una skill? Anota 3 cosas que la skill debería comprobar siempre.

**Autocomprobación**: Entiendes las skills cuando puedes explicar por qué importa el campo `description` (es como Copilot decide si cargar tu skill).

---

## 📝 Tarea

### Reto principal: construir una skill de resumen de libros

Los ejemplos anteriores crearon las skills `pytest-gen` y `pr-review`. Ahora practica creando un tipo de skill completamente diferente: una para generar salida con formato a partir de datos.

1. Lista tus skills actuales: ejecuta Copilot y pásale `/skills list`. También puedes usar `ls .github/skills/` para ver las skills del proyecto o `ls ~/.copilot/skills/` para las personales.
2. Crea una skill `book-summary` en `.github/skills/book-summary/SKILL.md` que genere un resumen Markdown formateado de la colección de libros
3. Tu skill debería tener:
   - Un nombre y descripción claros (¡la descripción es crucial para el matching!)
   - Reglas de formato concretas (por ejemplo, una tabla Markdown con título, autor, año, estado de lectura)
   - Convenciones de salida (por ejemplo, usar ✅/❌ para el estado de lectura, ordenar por año)
4. Prueba la skill: `@samples/book-app-project/data.json Summarize the books in this collection`
5. Verifica que la skill se autodispara comprobando `/skills list`
6. Prueba a invocarla directamente con `/book-summary Summarize the books in this collection`

**Criterio de éxito**: Tienes una skill `book-summary` funcional que Copilot aplica automáticamente cuando preguntas sobre la colección de libros.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Plantilla inicial**: Crea `.github/skills/book-summary/SKILL.md`:

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**Pruébalo:**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# The skill should auto-trigger based on the description match
```

**Si no se dispara:** Prueba `/skills reload` y vuelve a preguntar.

</details>

### Reto bonus: skill de mensaje de commit

1. Crea una skill `commit-message` que genere mensajes de commit convencionales con un formato consistente
2. Pruébala dejando un cambio en stage y preguntando: "Generate a commit message for my staged changes"
3. Documenta tu skill y compártela en GitHub con el topic `copilot-skill`

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué pasa | Solución |
|---------|--------------|-----|
| Nombrar el archivo de otra forma que no sea `SKILL.md` | La skill no se reconocerá | El archivo debe llamarse exactamente `SKILL.md` |
| Campo `description` vago | La skill nunca se cargará automáticamente | La descripción es el mecanismo PRIMARIO de descubrimiento. Usa palabras clave concretas |
| Falta `name` o `description` en el frontmatter | La skill no carga | Añade ambos campos en el frontmatter YAML |
| Ubicación de carpeta incorrecta | Skill no encontrada | Usa `.github/skills/skill-name/` (proyecto) o `~/.copilot/skills/skill-name/` (personal) |

### Solución de problemas

**La skill no se utiliza** - Si Copilot no usa tu skill cuando lo esperas:

1. **Comprueba la descripción**: ¿Coincide con cómo lo estás preguntando?
   ```markdown
   # Bad: Too vague
   description: Reviews code

   # Good: Includes trigger words
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **Verifica la ubicación del archivo**:
   ```bash
   # Project skills
   ls .github/skills/

   # User skills
   ls ~/.copilot/skills/
   ```

3. **Comprueba el formato de SKILL.md**: El frontmatter es obligatorio:
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**La skill no aparece** - Verifica la estructura de carpetas:
```
.github/skills/
└── my-skill/           # Folder name
    └── SKILL.md        # Must be exactly SKILL.md (case-sensitive)
```

Ejecuta `/skills reload` después de crear o editar skills para asegurarte de que los cambios se incorporan.

**Probar si una skill se carga** - Pregúntale directamente a Copilot:
```bash
> What skills do you have available for checking code quality?
# Copilot will describe relevant skills it found
```

**¿Cómo sé que mi skill realmente está funcionando?**

1. **Comprueba el formato de salida**: Si tu skill especifica un formato de salida (como las etiquetas `[CRITICAL]`), búscalo en la respuesta
2. **Pregunta directamente**: Tras recibir una respuesta, pregunta "Did you use any skills for that?"
3. **Compara con/sin**: Prueba el mismo prompt con `--no-custom-instructions` para ver la diferencia:
   ```bash
   # With skills
   copilot --allow-all -p "Review @file.py for security issues"

   # Without skills (baseline comparison)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **Busca comprobaciones específicas**: Si tu skill incluye comprobaciones específicas (como "functions over 50 lines"), comprueba si aparecen en la salida

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **Las skills son automáticas**: Copilot las carga cuando tu prompt coincide con la descripción de la skill
2. **Invocación directa**: También puedes invocar skills directamente con `/skill-name` como un slash command
3. **Formato SKILL.md**: Frontmatter YAML (name, description, license opcional) más instrucciones en Markdown
4. **La ubicación importa**: `.github/skills/` para compartir en proyecto/equipo, `~/.copilot/skills/` para uso personal
5. **La descripción es clave**: Escribe descripciones que coincidan con cómo preguntas de forma natural

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Las skills amplían lo que Copilot puede hacer con instrucciones cargadas automáticamente. Pero, ¿qué pasa con conectarse a servicios externos? Ahí es donde entra MCP.

En el [**Capítulo 06: Servidores MCP**](../06-mcp-servers/README.md), aprenderás:

- Qué es MCP (Model Context Protocol)
- Conectar a GitHub, sistema de archivos y servicios de documentación
- Configurar servidores MCP
- Flujos de trabajo con varios servidores

---

[**← Volver al Capítulo 04**](../04-agents-custom-instructions/README.md) | [**Continuar al Capítulo 06 →**](../06-mcp-servers/README.md)
