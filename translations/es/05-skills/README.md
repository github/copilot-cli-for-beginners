![Chapter 05: Skills System](../../../05-skills/images/chapter-header.png)

> **¿Y si Copilot pudiera aplicar automáticamente las mejores prácticas de tu equipo sin que tengas que explicarlas cada vez?**

En este capítulo aprenderás sobre Agent Skills: carpetas de instrucciones que Copilot carga automáticamente cuando son relevantes para tu tarea. Mientras que los agentes cambian *cómo* piensa Copilot, las skills le enseñan *formas específicas de completar tareas*. Crearás una skill de auditoría de seguridad que Copilot aplicará siempre que preguntes sobre seguridad, construirás criterios de revisión estándar del equipo que garanticen calidad de código coherente y aprenderás cómo funcionan las skills en Copilot CLI, VS Code y el agente en la nube de GitHub Copilot.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Entender cómo funcionan las Agent Skills y cuándo usarlas
- Crear skills personalizadas con archivos SKILL.md
- Usar skills comunitarias desde repositorios compartidos
- Saber cuándo usar skills vs agentes vs MCP

> ⏱️ **Tiempo estimado**: ~55 minutos (20 min lectura + 35 min práctica)

---

## 🧩 Analogía del Mundo Real: Herramientas Eléctricas

Un taladro de uso general es útil, pero los accesorios especializados lo hacen potente. 
<img src="../../../05-skills/images/power-tools-analogy.png" alt="Herramientas eléctricas - Las habilidades amplían las capacidades de Copilot" width="800"/>

Las skills funcionan de la misma manera. Igual que cambiar brocas para diferentes trabajos, puedes añadir skills a Copilot para distintas tareas:

| Skill Attachment | Purpose |
|------------|---------|
| `commit` | Generar mensajes de commit consistentes |
| `security-audit` | Comprobar vulnerabilidades OWASP |
| `generate-tests` | Crear pruebas pytest exhaustivas |
| `code-checklist` | Aplicar estándares de calidad de código del equipo |



*Las skills son accesorios especializados que amplían lo que Copilot puede hacer*

---

# Cómo funcionan las Skills

<img src="../../../05-skills/images/how-skills-work.png" alt="Iconos de habilidades estilo RPG brillando conectados por senderos de luz sobre un fondo estrellado que representan las habilidades de Copilot" width="800"/>

Aprende qué son las skills, por qué importan y en qué se diferencian de los agentes y MCP.

---

## *¿Nuevo en Skills?* Comienza aquí!

1. **Ve qué skills ya están disponibles:**
   ```bash
   copilot
   > /skills list
   ```
   Esto muestra todas las skills que Copilot puede encontrar, incluidas las **skills integradas** que vienen con la propia CLI, además de las skills de tu proyecto y de las carpetas personales.

   > 💡 **Skills integradas**: La Copilot CLI viene con skills preinstaladas desde el inicio. Por ejemplo, la skill `customizing-copilot-cloud-agents-environment` ofrece una guía para personalizar el entorno del agente en la nube de Copilot. No necesitas crear ni instalar nada para usarlas. Ejecuta `/skills list` para ver qué hay disponible.

2. **Mira un archivo de skill real:** Consulta nuestro [code-checklist SKILL.md](../../../.github/skills/code-checklist/SKILL.md) para ver el patrón. Es solo frontmatter YAML más instrucciones en markdown.

3. **Entiende el concepto principal:** Las skills son instrucciones específicas de tareas que Copilot carga *automáticamente* cuando tu prompt coincide con la descripción de la skill. No necesitas activarlas, solo pregunta de forma natural.

## Entendiendo las Skills

Agent Skills son carpetas que contienen instrucciones, scripts y recursos que Copilot **carga automáticamente cuando son relevantes** para tu tarea. Copilot lee tu prompt, comprueba si alguna skill coincide y aplica las instrucciones relevantes automáticamente.

```bash
copilot

> Check books.py against our quality checklist
# Copilot detecta que esto coincide con tu habilidad "code-checklist"
# y aplica automáticamente su lista de verificación de calidad para Python

> Generate tests for the BookCollection class
# Copilot carga tu habilidad "pytest-gen"
# y aplica tu estructura de pruebas preferida

> What are the code quality issues in this file?
# Copilot carga tu habilidad "code-checklist"
# y verifica frente a los estándares de tu equipo
```

> 💡 **Idea clave**: Las skills se **activan automáticamente** en función de que tu prompt coincida con la descripción de la skill. Solo pregunta de forma natural y Copilot aplica las skills relevantes en segundo plano. También puedes invocar skills directamente, lo cual aprenderás a continuación.

> 🧰 **Plantillas listas para usar**: Revisa la carpeta [.github/skills](../../../.github/skills) para skills simples que puedes copiar y probar.

### Invocación directa con comando slash

Aunque el auto-disparo es la forma principal en que funcionan las skills, también puedes **invocarlas directamente** usando su nombre como comando slash:

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

Esto te da control explícito cuando quieres asegurarte de que se use una skill específica.

#### Combinar múltiples skills en un solo mensaje

Puedes invocar **más de una skill en un solo mensaje**, y el comando slash de la skill puede aparecer en cualquier parte de tu prompt — no solo al principio. Esto es útil cuando quieres que se realicen dos comprobaciones distintas de una vez:

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot aplicará cada skill nombrada en la misma respuesta, ahorrándote enviar varios mensajes separados.

> 💡 **Consejo**: Coloca los comandos slash de las skills donde se sientan más naturales en tu frase. Puedes ponerlos al inicio, en medio o al final de tu mensaje.

> 📝 **Invocación: Skills vs Agentes**: No confundas la invocación de una skill con la invocación de un agente:
> - **Skills**: `/skill-name <prompt>`, p. ej., `/code-checklist Check this file`
> - **Agentes**: `/agent` (seleccionar de la lista) o `copilot --agent <name>` (línea de comandos)
>
> Si tienes tanto una skill como un agente con el mismo nombre (por ejemplo, "code-reviewer"), escribir `/code-reviewer` invoca la **skill**, no el agente.

### ¿Cómo sé que se usó una skill?

Puedes preguntarle a Copilot directamente:

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### Skills vs Agents vs MCP

Las skills son solo una pieza del modelo de extensibilidad de GitHub Copilot. Aquí se explica cómo se comparan con los agentes y los servidores MCP.

> *No te preocupes aún por MCP. Lo cubriremos en [Chapter 06](../../../06-mcp-servers). Se incluye aquí para que veas cómo las skills encajan en el panorama general.*

<img src="../../../05-skills/images/skills-agents-mcp-comparison.png" alt="Diagrama comparativo que muestra las diferencias entre Agents, Skills y MCP Servers y cómo se combinan en tu flujo de trabajo" width="800"/>

| Feature | What It Does | When to Use |
|---------|--------------|-------------|
| **Agents** | Changes how AI thinks | Need specialized expertise across many tasks |
| **Skills** | Provides task-specific instructions | Specific, repeatable tasks with detailed steps |
| **MCP** | Connects external services | Need live data from APIs |

Usa agentes para experiencia amplia, skills para instrucciones específicas de tareas y MCP para datos externos. Un agente puede usar una o más skills durante una conversación. Por ejemplo, cuando le pides a un agente que revise tu código, puede aplicar tanto una skill `security-audit` como una `code-checklist` automáticamente.

> 📚 **Aprende más**: Consulta la documentación oficial [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) para la referencia completa sobre formatos de skill y buenas prácticas.

---

## Desde prompts manuales hasta experiencia automática

Antes de profundizar en cómo crear skills, veamos *por qué* vale la pena aprenderlas. Una vez que veas las ganancias en coherencia, el "cómo" tendrá más sentido.

### Antes de las Skills: Revisiones inconsistentes

En cada revisión de código, podrías olvidar algo:

```bash
copilot

> Review this code for issues
# Revisión genérica - puede pasar por alto las preocupaciones específicas de su equipo
```

O escribes un prompt largo cada vez:

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

Tiempo: **30+ segundos** para escribir. Coherencia: **varía según la memoria**.

### Después de las Skills: Mejores prácticas automáticas

Con una skill `code-checklist` instalada, solo pregunta de forma natural:

```bash
copilot

> Check the book collection code for quality issues
```

**Qué ocurre entre bastidores**:
1. Copilot ve "code quality" y "issues" en tu prompt
2. Comprueba las descripciones de las skills, encuentra que tu skill `code-checklist` coincide
3. Carga automáticamente la lista de verificación de calidad de tu equipo
4. Aplica todas las comprobaciones sin que las enumeres

<img src="../../../05-skills/images/skill-auto-discovery-flow.png" alt="Cómo se activan automáticamente las Skills - flujo de 4 pasos que muestra cómo Copilot empareja automáticamente tu prompt con la skill correcta" width="800"/>

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

**La diferencia**: Los estándares de tu equipo se aplican automáticamente, siempre, sin tener que escribirlos.

---

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Skill Trigger Demo](../../../05-skills/images/skill-trigger-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

---

## Coherencia a escala: Skill de revisión de PR del equipo

Imagina que tu equipo tiene una lista de verificación de PR de 10 puntos. Sin una skill, cada desarrollador debe recordar los 10 puntos, y alguien siempre olvida uno. Con una skill `pr-review`, todo el equipo obtiene revisiones coherentes:

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

**El poder**: Cada miembro del equipo aplica los mismos estándares automáticamente. Las nuevas contrataciones no necesitan memorizar la lista porque la skill se encarga de ello.

---

# Creando Skills Personalizadas

<img src="../../../05-skills/images/creating-managing-skills.png" alt="Manos humanas y robóticas construyendo un muro de bloques brillantes tipo LEGO que representan la creación y gestión de skills" width="800"/>

Crea tus propias skills desde archivos SKILL.md.

---

## Ubicaciones de las Skills

Las skills se almacenan en `.github/skills/` (específicas del proyecto) o `~/.copilot/skills/` (a nivel de usuario).

### Cómo encuentra Copilot las skills

Copilot escanea automáticamente estas ubicaciones en busca de skills:

| Location | Scope |
|----------|-------|
| `.github/skills/` | Project-specific (shared with team via git) |
| `~/.copilot/skills/` | User-specific (your personal skills) |

### Estructura de una Skill

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

> 💡 **Consejo**: El nombre del directorio debe coincidir con el `name` en el frontmatter de tu SKILL.md (minúsculas con guiones).

### Formato SKILL.md

Las skills usan un formato markdown simple con frontmatter YAML:

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

| Property | Required | Description |
|----------|----------|-------------|
| `name` | **Yes** | Identificador único (minúsculas, guiones para espacios) |
| `description` | **Yes** | Qué hace la skill y cuándo Copilot debe usarla |
| `license` | No | Licencia que aplica a esta skill |

> 📖 **Documentación oficial**: [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### Creando tu primera Skill

Vamos a construir una skill de auditoría de seguridad que compruebe las vulnerabilidades OWASP Top 10:

```bash
# Crear el directorio de la habilidad
mkdir -p .github/skills/security-audit

# Crear el archivo SKILL.md
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Auditoría de seguridad

Perform a security audit checking for:

## Vulnerabilidades de inyección
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Problemas de autenticación
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Datos sensibles
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Control de acceso
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Salida
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Prueba tu habilidad (las habilidades se cargan automáticamente según tu indicación)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot detecta "vulnerabilidades de seguridad" que coinciden con tu habilidad
# y aplica automáticamente su lista de verificación OWASP
```

**Salida esperada** (tus resultados variarán):

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

## Escribir buenas descripciones de Skill

El campo `description` en tu SKILL.md ¡es crucial! Es cómo Copilot decide si cargar tu skill:

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **Consejo**: Incluye palabras clave que coincidan con cómo preguntas de forma natural. Si dices "security review", incluye "security review" en la descripción.

### Combinar Skills con Agentes

Las skills y los agentes funcionan juntos. El agente aporta la experiencia, la skill aporta instrucciones específicas:

```bash
# Comience con un agente revisor de código
copilot --agent code-reviewer

> Check the book app for quality issues
# La experiencia del agente revisor de código se combina
# con la lista de verificación de su habilidad code-checklist
```

---

# Gestionar y Compartir Skills

Descubre las skills instaladas, encuentra skills comunitarias y comparte las tuyas.

<img src="../../../05-skills/images/managing-sharing-skills.png" alt="Gestionar y compartir Skills - mostrando el ciclo de descubrir, usar, crear y compartir para skills de la CLI" width="800" />

---

## Gestionar Skills con el comando `/skills`

Usa el comando `/skills` para gestionar tus skills instaladas:

| Command | What It Does |
|---------|--------------|
| `/skills list` | Mostrar todas las skills instaladas |
| `/skills info <name>` | Obtener detalles sobre una skill específica |
| `/skills add <name>` | Habilitar una skill (desde un repositorio o marketplace) |
| `/skills remove <name>` | Deshabilitar o desinstalar una skill |
| `/skills reload` | Recargar skills después de editar archivos SKILL.md |

> 💡 **Recuerda**: No necesitas "activar" las skills para cada prompt. Una vez instaladas, las skills se **activan automáticamente** cuando tu prompt coincide con su descripción. Estos comandos sirven para gestionar qué skills están disponibles, no para usarlas.

### Ejemplo: Ver tus Skills

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
<summary>¡Míralo en acción!</summary>

![List Skills Demo](../../../05-skills/images/list-skills-demo.gif)

*La salida del demo varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

---

### Cuándo usar `/skills reload`

Después de crear o editar el archivo SKILL.md de una skill, ejecuta `/skills reload` para recoger los cambios sin reiniciar Copilot:

```bash
# Edita tu archivo de habilidad
# Luego, en Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **Buen dato**: Las skills siguen siendo efectivas incluso después de usar `/compact` para resumir el historial de la conversación. No es necesario recargar después de compactar.

---

## Encontrar y usar Skills comunitarias

### Usar Plugins para instalar Skills
> 💡 **¿Qué son los plugins?** Los plugins son paquetes instalables que pueden agrupar skills, agents y configuraciones de servidores MCP. Piénsalos como extensiones tipo "app store" para Copilot CLI.

El comando `/plugin` te permite explorar e instalar estos paquetes:

```bash
copilot

> /plugin list
# Muestra los complementos instalados

> /plugin marketplace
# Explorar complementos disponibles

> /plugin install <plugin-name>
# Instalar un complemento desde el mercado
```

Para mantener tu catálogo local de plugins actualizado, renuévalo con:

```bash
copilot plugin marketplace update
```

Los plugins pueden agrupar múltiples capacidades. Un solo plugin puede incluir skills, agents y configuraciones de servidores MCP relacionadas que funcionen en conjunto.

### Repositorios de Skills de la Comunidad

Las skills prefabricadas también están disponibles en repositorios comunitarios:

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - Recursos oficiales de GitHub Copilot que incluyen documentación y ejemplos de skills

### Instalar una Skill de la Comunidad con GitHub CLI

La forma más sencilla de instalar una skill desde un repositorio de GitHub es usar el comando `gh skill install` (requiere [GitHub CLI v2.90.0+](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/)):

```bash
# Explorar y seleccionar de forma interactiva una habilidad de awesome-copilot
gh skill install github/awesome-copilot

# O instalar directamente una habilidad específica
gh skill install github/awesome-copilot code-checklist

# Instalar para uso personal en todos los proyectos (ámbito de usuario)
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **Revisa antes de instalar**: Siempre lee el `SKILL.md` de una skill antes de instalarla. Las skills controlan lo que hace Copilot, y una skill maliciosa podría instruirlo para ejecutar comandos dañinos o modificar el código de maneras inesperadas.

---

# Práctica

<img src="../../../images/practice.png" alt="Configuración de escritorio acogedora con monitor mostrando código, lámpara, taza de café y auriculares listos para práctica" width="800"/>

Aplica lo que has aprendido construyendo y probando tus propias skills.

---

## ▶️ Pruébalo tú mismo

### Crea más skills

Aquí hay dos skills más que muestran distintos patrones. Sigue el mismo flujo de trabajo `mkdir` + `cat` de "Crear tu primera skill" arriba o copia y pega las skills en la ubicación adecuada. Hay más ejemplos disponibles en [.github/skills](../../../.github/skills).

### Skill de generación de tests con pytest

Una skill que garantiza una estructura consistente de pytest en tu base de código:

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# Generación de pruebas con pytest

Generate pytest tests that include:

## Estructura de pruebas
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Cobertura
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Salida
Provide complete, runnable test file with proper imports.
EOF
```

### Skill de revisión de PR del equipo

Una skill que aplica estándares coherentes de revisión de PR en tu equipo:

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# Revisión de PR

Review code changes against team standards:

## Lista de verificación de seguridad
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Calidad del código
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Pruebas
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentación
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Formato de salida
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### Ir más allá

1. **Desafío de creación de skills**: Crea una skill `quick-review` que haga una lista de verificación de 3 puntos:
   - Cláusulas except sin especificar
   - Falta de hints de tipo
   - Nombres de variables poco claros

   Pruébala preguntando: "Haz una revisión rápida de books.py"

2. **Comparación de skills**: Cronometra cuánto tardas en escribir manualmente un prompt detallado de revisión de seguridad. Luego simplemente pregunta "Comprueba si hay problemas de seguridad en este archivo" y deja que tu skill de auditoría de seguridad se cargue automáticamente. ¿Cuánto tiempo ahorró la skill?

3. **Desafío de skill para el equipo**: Piensa en la lista de comprobación de revisión de código de tu equipo. ¿Podrías codificarla como una skill? Anota 3 cosas que la skill debería revisar siempre.

**Autoevaluación**: Entenderás las skills cuando puedas explicar por qué importa el campo `description` (es como Copilot decide si cargar tu skill).

---

## 📝 Tarea

### Desafío principal: Crea una skill de resumen de libros

Los ejemplos anteriores crearon las skills `pytest-gen` y `pr-review`. Ahora practica creando un tipo de skill completamente diferente: una para generar salida formateada a partir de datos.

1. Lista tus skills actuales: Ejecuta Copilot y pásale `/skills list`. También puedes usar `ls .github/skills/` para ver las skills del proyecto o `ls ~/.copilot/skills/` para las personales.
2. Crea una skill `book-summary` en `.github/skills/book-summary/SKILL.md` que genere un resumen en Markdown formateado de la colección de libros
3. Tu skill debe tener:
   - Nombre y descripción claros (¡la descripción es crucial para el emparejamiento!)
   - Reglas de formato específicas (p. ej., tabla en Markdown con título, autor, año, estado de lectura)
   - Convenciones de salida (p. ej., usa ✅/❌ para el estado de lectura, ordenar por año)
4. Prueba la skill: `@samples/book-app-project/data.json Summarize the books in this collection`
5. Verifica que la skill se active automáticamente comprobando `/skills list`
6. Intenta invocarla directamente con `/book-summary Summarize the books in this collection`

**Criterios de éxito**: Tienes una skill `book-summary` funcionando que Copilot aplica automáticamente cuando preguntas sobre la colección de libros.

<details>
<summary>💡 Sugerencias (haz clic para expandir)</summary>

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
# La habilidad debería activarse automáticamente según la coincidencia de la descripción
```

**Si no se activa:** Intenta `/skills reload` y luego pregunta de nuevo.

</details>

### Desafío extra: Skill de mensajes de commit

1. Crea una skill `commit-message` que genere mensajes de commit convencionales con un formato consistente
2. Pruébala poniendo en stage un cambio y preguntando: "Genera un mensaje de commit para mis cambios en stage"
3. Documenta tu skill y compártela en GitHub con el tema `copilot-skill`

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| Nombrar el archivo con otro nombre que no sea `SKILL.md` | La skill no será reconocida | El archivo debe llamarse exactamente `SKILL.md` |
| Campo `description` vago | La skill nunca se carga automáticamente | La descripción es el mecanismo PRINCIPAL de descubrimiento. Usa palabras clave específicas |
| Falta `name` o `description` en el frontmatter | La skill no se carga | Añade ambos campos en el frontmatter YAML |
| Ubicación de carpeta incorrecta | Skill no encontrada | Usa `.github/skills/skill-name/` (proyecto) o `~/.copilot/skills/skill-name/` (personal) |

### Solución de problemas

**Skill no usada** - Si Copilot no está usando tu skill cuando se espera:

1. **Revisa la descripción**: ¿Coincide con la forma en que preguntas?
   ```markdown
   # Bad: Too vague
   description: Reviews code

   # Good: Includes trigger words
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **Verifica la ubicación del archivo**:
   ```bash
   # Habilidades del proyecto
   ls .github/skills/

   # Habilidades del usuario
   ls ~/.copilot/skills/
   ```

3. **Revisa el formato de SKILL.md**: El frontmatter es obligatorio:
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**Skill no aparece** - Verifica la estructura de carpetas:
```
.github/skills/
└── my-skill/           # Folder name
    └── SKILL.md        # Must be exactly SKILL.md (case-sensitive)
```

Ejecuta `/skills reload` tras crear o editar skills para asegurarte de que los cambios se carguen.

**Probar si una skill se carga** - Pregunta a Copilot directamente:
```bash
> What skills do you have available for checking code quality?
# Copilot describirá las habilidades relevantes que encontró
```

**¿Cómo sé si mi skill realmente está funcionando?**

1. **Revisa el formato de salida**: Si tu skill especifica un formato de salida (como etiquetas `[CRITICAL]`), búscalo en la respuesta
2. **Pregunta directamente**: Después de obtener una respuesta, pregunta "¿Usaste alguna skill para eso?"
3. **Compara con/sin**: Prueba el mismo prompt con `--no-custom-instructions` para ver la diferencia:
   ```bash
   # Con habilidades
   copilot --allow-all -p "Review @file.py for security issues"

   # Sin habilidades (comparación de referencia)
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **Revisa comprobaciones específicas**: Si tu skill incluye comprobaciones específicas (como "funciones de más de 50 líneas"), verifica si aparecen en la salida

</details>

---

# Resumen

## 🔑 Puntos clave

1. **Las skills se cargan automáticamente**: Copilot las carga cuando tu prompt coincide con la descripción de la skill
2. **Invocación directa**: También puedes invocar skills directamente con `/skill-name` como comando slash
3. **Formato SKILL.md**: Frontmatter YAML (name, description, licencia opcional) más instrucciones en Markdown
4. **La ubicación importa**: `.github/skills/` para compartir en proyecto/equipo, `~/.copilot/skills/` para uso personal
5. **La descripción es clave**: Escribe descripciones que coincidan con la forma en que preguntas naturalmente

> 📋 **Referencia rápida**: Consulta la [Referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para una lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Las skills amplían lo que Copilot puede hacer con instrucciones que se cargan automáticamente. ¿Pero qué pasa con la conexión a servicios externos? Ahí es donde entra MCP.

En **[Capítulo 06: Servidores MCP](../06-mcp-servers/README.md)**, aprenderás:

- Qué es MCP (Model Context Protocol)
- Conexión a GitHub, sistema de archivos y servicios de documentación
- Configurar servidores MCP
- Flujos de trabajo multi-servidor

---

**[← Volver al Capítulo 04](../04-agents-custom-instructions/README.md)** | **[Continuar al Capítulo 06 →](../06-mcp-servers/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->