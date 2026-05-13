![Capítulo 06: Servidores MCP](../../../06-mcp-servers/images/chapter-header.png)

> **¿Y si Copilot pudiera leer tus issues de GitHub, consultar tu base de datos y crear PRs... todo desde la terminal?**

Hasta ahora, Copilot solo puede trabajar con lo que le proporcionas directamente: archivos a los que haces referencia con `@`, el historial de conversación y sus propios datos de entrenamiento. Pero ¿y si pudiera consultar por sí mismo tu repositorio de GitHub, explorar los archivos de tu proyecto o buscar la documentación más reciente de una librería?

Eso es lo que hace MCP (Model Context Protocol). Es una manera de conectar Copilot con servicios externos para que tenga acceso a datos reales y en vivo. A cada servicio al que Copilot se conecta se le llama "servidor MCP". En este capítulo configurarás algunas de estas conexiones y verás cómo hacen que Copilot sea muchísimo más útil.

> 💡 **¿Ya conoces MCP?** [Salta al inicio rápido](#-use-the-built-in-github-mcp) para confirmar que funciona y empezar a configurar servidores.

## 🎯 Objetivos de aprendizaje

Al finalizar este capítulo, serás capaz de:

- Entender qué es MCP y por qué importa
- Gestionar servidores MCP con los comandos `/mcp`
- Configurar servidores MCP para GitHub, sistema de archivos y documentación
- Usar flujos de trabajo potenciados por MCP con el proyecto book app
- Saber cuándo y cómo construir un servidor MCP personalizado (opcional)

> ⏱️ **Tiempo estimado**: ~50 minutos (15 min de lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: extensiones del navegador

<img src="../../../06-mcp-servers/images/browser-extensions-analogy.png" alt="Los servidores MCP son como las extensiones del navegador" width="800"/>

Piensa en los servidores MCP como en las extensiones del navegador. Tu navegador, por sí solo, puede mostrar páginas web, pero las extensiones lo conectan con servicios adicionales:

| Extensión del navegador | Con qué se conecta | Equivalente en MCP |
|-------------------|---------------------|----------------|
| Gestor de contraseñas | Tu bóveda de contraseñas | **GitHub MCP** → tus repos, issues, PRs |
| Grammarly | Servicio de análisis de escritura | **Context7 MCP** → documentación de librerías |
| Gestor de archivos | Almacenamiento en la nube | **Filesystem MCP** → archivos locales del proyecto |

Sin extensiones, el navegador sigue siendo útil, pero con ellas se convierte en una herramienta muy potente. Los servidores MCP hacen lo mismo con Copilot. Lo conectan a fuentes de datos reales y en vivo para que pueda leer tus issues de GitHub, explorar tu sistema de archivos, traer documentación actualizada y mucho más.

***Los servidores MCP conectan Copilot con el mundo exterior: GitHub, repositorios, documentación y más***

> 💡 **Idea clave**: Sin MCP, Copilot solo puede ver los archivos que compartes explícitamente con `@`. Con MCP, puede explorar tu proyecto de forma proactiva, consultar tu repositorio de GitHub y buscar documentación, todo de forma automática.

---

<img src="../../../06-mcp-servers/images/quick-start-mcp.png" alt="Cable de alimentación conectándose con una chispa eléctrica brillante rodeado de iconos tecnológicos flotantes que representan las conexiones de los servidores MCP" width="800"/>

# Inicio rápido: MCP en 30 segundos

## Empieza con el servidor MCP de GitHub integrado
Veamos MCP en acción ahora mismo, antes de configurar nada.
El servidor MCP de GitHub viene incluido por defecto. Prueba esto:

```bash
copilot
> List the recent commits in this repository
```

Si Copilot devuelve datos reales de commits, acabas de ver MCP en acción. Eso es el servidor MCP de GitHub conectándose con GitHub en tu nombre. Pero GitHub es solo *un* servidor. Este capítulo te muestra cómo añadir más (acceso al sistema de archivos, documentación actualizada y otros) para que Copilot pueda hacer todavía más.

---

## El comando `/mcp show`

Usa `/mcp show` para ver qué servidores MCP están configurados y si están habilitados:

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **¿Solo ves el servidor de GitHub?** ¡Es lo esperado! Si todavía no has añadido ningún servidor MCP adicional, GitHub es el único que aparece. Añadirás más en la siguiente sección.

> 📚 **¿Quieres ver todos los comandos de gestión de MCP?** Puedes gestionar los servidores con los comandos slash `/mcp` dentro del chat, o con `copilot mcp` directamente desde tu terminal. Consulta la [referencia completa de comandos](#-additional-mcp-commands) al final de este capítulo.

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demo de estado de MCP](../../../06-mcp-servers/images/mcp-status-demo.gif)

*La salida de la demo varía. Tu modelo, tus herramientas y las respuestas serán distintos a lo que se muestra aquí.*

</details>

---

## ¿Qué cambia con MCP?

Esta es la diferencia que MCP marca en la práctica:

**Sin MCP:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**Con MCP:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP hace que Copilot sea consciente de tu entorno de desarrollo real.

> 📚 **Documentación oficial**: [Sobre MCP](https://docs.github.com/copilot/concepts/context/mcp) para profundizar en cómo funciona MCP con GitHub Copilot.

---

# Configurar servidores MCP

<img src="../../../06-mcp-servers/images/configuring-mcp-servers.png" alt="Manos ajustando perillas y deslizadores en una mesa profesional de mezcla de audio que representa la configuración de servidores MCP" width="800"/>

Ahora que has visto MCP en acción, vamos a configurar servidores adicionales. Puedes añadir servidores de dos maneras: **desde el registro integrado** (lo más fácil — configuración guiada directamente en la CLI) o **editando manualmente el archivo de configuración** (más flexible). Empieza por la opción del registro si no estás seguro de cuál elegir.

---

## Instalar servidores MCP desde el registro

La CLI tiene un registro integrado de servidores MCP que te permite descubrir e instalar los más populares con una configuración guiada — sin necesidad de editar JSON.

```bash
copilot

> /mcp search
```

Copilot abre un selector interactivo que muestra los servidores disponibles. Elige uno y la CLI te guiará por la configuración necesaria (claves de API, rutas, etc.) y lo añadirá a tu configuración automáticamente.

> 💡 **¿Por qué usar el registro?** Es la forma más fácil de empezar — no necesitas conocer el nombre del paquete npm, los argumentos del comando ni la estructura JSON. La CLI se encarga de todo eso por ti.

---

## Archivo de configuración de MCP

Los servidores MCP se configuran en `~/.copilot/mcp-config.json` (a nivel de usuario, aplica a todos los proyectos) o `.mcp.json` (a nivel de proyecto, situado en la raíz de tu proyecto). Si has usado `/mcp search` arriba, la CLI ya ha creado o actualizado este archivo por ti, pero es útil entender el formato para poder personalizarlo.

> ⚠️ **Nota**: `.vscode/mcp.json` ya no se admite como fuente de configuración MCP. Si tienes un `.vscode/mcp.json` existente, migra su contenido a `.mcp.json` en la raíz de tu proyecto. La CLI mostrará una sugerencia de migración si detecta un archivo de configuración antiguo.

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*La mayoría de servidores MCP se distribuyen como paquetes de npm y se ejecutan con el comando `npx`.*

<details>
<summary>💡 <strong>¿Eres nuevo en JSON?</strong> Haz clic aquí para ver qué significa cada campo</summary>

| Campo | Qué significa |
|-------|---------------|
| `"mcpServers"` | Contenedor de todas tus configuraciones de servidores MCP |
| `"server-name"` | Un nombre que tú eliges (p. ej., "github", "filesystem") |
| `"type": "local"` | El servidor se ejecuta en tu máquina |
| `"command": "npx"` | El programa a ejecutar (npx ejecuta paquetes de npm) |
| `"args": [...]` | Argumentos pasados al comando |
| `"tools": ["*"]` | Permite todas las herramientas de este servidor |

**Reglas importantes de JSON:**
- Usa comillas dobles `"` para las cadenas (no comillas simples)
- Sin comas finales tras el último elemento
- El archivo debe ser JSON válido (usa un [validador de JSON](https://jsonlint.com/) si tienes dudas)

</details>

---

## Añadir servidores MCP

El servidor MCP de GitHub viene integrado y no requiere configuración. A continuación tienes servidores adicionales que puedes añadir. **Elige el que te interese o ve recorriéndolos en orden.**

| Quiero... | Ir a |
|---|---|
| Dejar que Copilot navegue por los archivos de mi proyecto | [Servidor Filesystem](#filesystem-server) |
| Obtener documentación de librerías actualizada | [Servidor Context7](#context7-server-documentation) |
| Explorar extras opcionales (servidores personalizados, web_fetch) | [Más allá de lo básico](#beyond-the-basics) |

<details>
<summary><strong>Servidor Filesystem</strong> - Deja que Copilot explore los archivos de tu proyecto</summary>
<a id="filesystem-server"></a>

### Servidor Filesystem

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **La ruta `.`**: El `.` significa "directorio actual". Copilot puede acceder a archivos relativos al lugar donde lo has lanzado. En un Codespace, esto es la raíz de tu workspace. También puedes usar una ruta absoluta como `/workspaces/copilot-cli-for-beginners` si lo prefieres.

Añade esto a tu `~/.copilot/mcp-config.json` y reinicia Copilot.

</details>

<details>
<summary><strong>Servidor Context7</strong> - Obtén documentación actualizada de librerías</summary>
<a id="context7-server-documentation"></a>

### Servidor Context7 (documentación)

Context7 da a Copilot acceso a documentación actualizada de frameworks y librerías populares. En lugar de depender de datos de entrenamiento que pueden estar obsoletos, Copilot trae la documentación actual real.

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **No requiere clave de API** 
- ✅ **No necesita cuenta** 
- ✅ **Tu código se queda en local**

Añade esto a tu `~/.copilot/mcp-config.json` y reinicia Copilot.

</details>

<details>
<summary><strong>Más allá de lo básico</strong> - Servidores personalizados y acceso web (opcional)</summary>
<a id="beyond-the-basics"></a>

Estos son extras opcionales para cuando ya te sientas cómodo con los servidores básicos anteriores.

### Servidor MCP de Microsoft Learn

Cada servidor MCP que has visto hasta ahora (filesystem, Context7) se ejecuta localmente en tu máquina. Pero los servidores MCP también pueden ejecutarse de forma remota, lo que significa que tú simplemente apuntas Copilot CLI a una URL y él se encarga del resto. Sin `npx` ni `python`, sin proceso local, sin dependencias que instalar.

El [servidor MCP de Microsoft Learn](https://github.com/microsoftdocs/mcp) es un buen ejemplo. Da a Copilot CLI acceso directo a la documentación oficial de Microsoft (Azure, Microsoft Foundry y otros temas de IA, .NET, Microsoft 365 y mucho más) para que pueda buscar en la documentación, traer páginas completas y encontrar ejemplos de código oficiales en lugar de depender de los datos de entrenamiento de un modelo.

- ✅ **No requiere clave de API** 
- ✅ **No necesita cuenta** 
- ✅ **No requiere instalación local**

**Instalación rápida con `/plugin install`:**

En lugar de editar manualmente tu archivo de configuración JSON, puedes instalarlo con un solo comando:

```bash
copilot

> /plugin install microsoftdocs/mcp
```

Esto añade el servidor y sus skills de agente asociados automáticamente. Los skills instalados incluyen:

- **microsoft-docs**: Conceptos, tutoriales y consultas de información
- **microsoft-code-reference**: Consultas de API, ejemplos de código y solución de problemas
- **microsoft-skill-creator**: Un meta-skill para generar skills personalizados sobre tecnologías de Microsoft

**Uso:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 Más información: [Información general del servidor MCP de Microsoft Learn](https://learn.microsoft.com/training/support/mcp-get-started)

### Acceso web con `web_fetch`

Copilot CLI incluye una herramienta integrada `web_fetch` que puede traer contenido de cualquier URL. Es útil para obtener READMEs, documentación de APIs o notas de versión sin salir de tu terminal. No hace falta ningún servidor MCP.

Puedes controlar a qué URLs se puede acceder mediante `~/.copilot/config.json` (ajustes generales de Copilot), que es distinto a `~/.copilot/mcp-config.json` (definiciones de servidores MCP).

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**Uso:**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### Construir un servidor MCP personalizado

¿Quieres conectar Copilot con tus propias APIs, bases de datos o herramientas internas? Puedes construir un servidor MCP personalizado en Python. Esto es totalmente opcional, ya que los servidores preconstruidos (GitHub, filesystem, Context7) cubren la mayoría de casos de uso.

📖 Consulta la [Guía del servidor MCP personalizado](mcp-custom-server.md) para ver un recorrido completo usando el book app como ejemplo.

📚 Para más contexto, consulta el [curso MCP for Beginners](https://github.com/microsoft/mcp-for-beginners).

</details>

<a id="complete-configuration-file"></a>

### Archivo de configuración completo

Aquí tienes un `mcp-config.json` completo con los servidores filesystem y Context7:

> 💡 **Nota:** El MCP de GitHub viene integrado. No necesitas añadirlo a tu archivo de configuración.

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

Guárdalo como `~/.copilot/mcp-config.json` para acceso global o como `.mcp.json` en la raíz del proyecto para una configuración específica de proyecto.

---

# Usar servidores MCP

Ahora que tienes servidores MCP configurados, veamos lo que pueden hacer.

<img src="../../../06-mcp-servers/images/using-mcp-servers.png" alt="Uso de servidores MCP - Diagrama radial que muestra una CLI de desarrollador conectada a los servidores GitHub, Filesystem, Context7 y Personalizado/Web Fetch" width="800" />

---

## Ejemplos de uso de servidores

**Elige un servidor a explorar o ve recorriéndolos en orden.**

| Quiero probar... | Ir a |
|---|---|
| Repos, issues y PRs de GitHub | [Servidor GitHub](#github-server-built-in) |
| Navegar por archivos del proyecto | [Uso del servidor Filesystem](#filesystem-server-usage) |
| Búsqueda de documentación de librerías | [Uso del servidor Context7](#context7-server-usage) |
| Servidor personalizado, MCP de Microsoft Learn y uso de web_fetch | [Uso de Más allá de lo básico](#beyond-the-basics-usage) |

<details>
<summary><strong>Servidor GitHub (integrado)</strong> - Accede a repos, issues, PRs y más</summary>
<a id="github-server-built-in"></a>

### Servidor GitHub (integrado)

El servidor MCP de GitHub viene **integrado**. Si has iniciado sesión en Copilot (lo hiciste durante la configuración inicial), ya funciona. ¡No hace falta configuración!

> 💡 **¿No funciona?** Ejecuta `/login` para reautenticarte con GitHub.

<details>
<summary><strong>Autenticación en dev containers</strong></summary>

- **GitHub Codespaces** (recomendado): La autenticación es automática. La CLI `gh` hereda el token de tu Codespace. No hay que hacer nada.
- **Dev container local (Docker)**: Ejecuta `gh auth login` después de que arranque el contenedor y reinicia Copilot.

**Solución de problemas de autenticación:**
```bash
# Check if you're authenticated
gh auth status

# If not, log in
gh auth login

# Verify GitHub MCP is connected
copilot
> /mcp show
```

</details>

| Característica | Ejemplo |
|---------|----------|
| **Información del repositorio** | Ver commits, ramas, contribuidores |
| **Issues** | Listar, crear, buscar y comentar issues |
| **Pull requests** | Ver PRs, diffs, crear PRs, comprobar estado |
| **Búsqueda de código** | Buscar código entre repositorios |
| **Actions** | Consultar ejecuciones y estado de workflows |

```bash
copilot

# See recent activity in this repo
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# Explore the repo structure
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# Search for code patterns across the repo
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **¿Trabajas en tu propio fork?** Si has hecho fork de este repositorio del curso, también puedes probar operaciones de escritura como crear issues y pull requests. Lo practicaremos en los ejercicios de abajo.

> ⚠️ **¿No ves resultados?** El MCP de GitHub opera sobre el remoto del repositorio (en github.com), no solo sobre archivos locales. Asegúrate de que tu repo tiene un remoto: ejecuta `git remote -v` para comprobarlo.

</details>

<details>
<summary><strong>Servidor Filesystem</strong> - Navega y analiza archivos del proyecto</summary>
<a id="filesystem-server-usage"></a>

### Servidor Filesystem

Una vez configurado, el MCP de filesystem proporciona herramientas que Copilot puede usar automáticamente:

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Servidor Context7</strong> - Consulta documentación de librerías</summary>
<a id="context7-server-usage"></a>

### Servidor Context7

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot now knows the official pytest patterns
# and can apply them to samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>Más allá de lo básico</strong> - Uso del servidor personalizado y de web_fetch</summary>
<a id="beyond-the-basics-usage"></a>

### Más allá de lo básico

**Servidor MCP personalizado**: Si has construido el servidor book-lookup de la [Guía del servidor MCP personalizado](mcp-custom-server.md), puedes consultar tu colección de libros directamente:

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**MCP de Microsoft Learn**: Si has instalado el [servidor MCP de Microsoft Learn](#microsoft-learn-mcp-server), puedes consultar la documentación oficial de Microsoft directamente:

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**: Usa la herramienta integrada `web_fetch` para traer contenido de cualquier URL:

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## Flujos de trabajo multiservidor

Estos flujos de trabajo muestran por qué hay quien dice "no quiero volver a trabajar sin esto". Cada ejemplo combina varios servidores MCP en una única sesión.

<img src="../../../06-mcp-servers/images/issue-to-pr-workflow.png" alt="Flujo de trabajo de issue a PR usando MCP - Muestra el flujo completo desde obtener un issue de GitHub hasta crear un pull request" width="800"/>

*Flujo completo de MCP: el MCP de GitHub recupera datos del repo, el MCP de Filesystem encuentra el código, el MCP de Context7 aporta buenas prácticas y Copilot se encarga del análisis*

Cada ejemplo de abajo es autónomo. **Elige el que te interese o léelos todos.**

| Quiero ver... | Ir a |
|---|---|
| Varios servidores funcionando juntos | [Exploración multiservidor](#multi-server-exploration) |
| Pasar de issue a PR en una sola sesión | [Flujo de trabajo de issue a PR](#issue-to-pr-workflow) |
| Una rápida revisión de salud del proyecto | [Panel de salud](#health-dashboard) |

<details>
<summary><strong>Exploración multiservidor</strong> - Combina filesystem, GitHub y Context7 en una sesión</summary>
<a id="multi-server-exploration"></a>

#### Explorar el book app con varios servidores MCP

```bash
copilot

# Step 1: Use filesystem MCP to explore the book app
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Step 2: Use GitHub MCP to check recent changes
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Step 3: Use Context7 MCP for best practices
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Step 4: Synthesize a recommendation
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 ¡Ve el flujo de trabajo de MCP en acción!</summary>

![Demo del flujo de trabajo de MCP](../../../06-mcp-servers/images/mcp-workflow-demo.gif)

*La salida de la demo varía. Tu modelo, tus herramientas y las respuestas serán distintos a lo que se muestra aquí.*

</details>

**El resultado**: Exploración del código → revisión del historial → consulta de buenas prácticas → plan de mejora. **Todo desde una sola sesión de terminal, usando tres servidores MCP juntos.**

</details>

<details>
<summary><strong>Flujo de trabajo de issue a PR</strong> - Pasa de un issue de GitHub a un pull request sin salir de la terminal</summary>
<a id="issue-to-pr-workflow"></a>

#### El flujo de trabajo de issue a PR (en tu propio repo)

Esto funciona mejor en tu propio fork o repositorio donde tengas permisos de escritura:

> 💡 **No te preocupes si no puedes probarlo ahora mismo.** Si estás en un clon de solo lectura, lo practicarás en la tarea. Por ahora, basta con leer para entender el flujo.

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**Cero copiar y pegar. Cero cambio de contexto. Una sola sesión de terminal.**

</details>

<details>
<summary><strong>Panel de salud</strong> - Obtén una rápida revisión de salud del proyecto usando varios servidores</summary>
<a id="health-dashboard"></a>

#### Panel de salud del book app

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**El resultado**: Múltiples fuentes de datos agregadas en segundos. De forma manual, esto significaría ejecutar grep, contar líneas, revisar git log y navegar por archivos de pruebas. Fácilmente más de 15 minutos de trabajo.

</details>

---

# Práctica

<img src="../../../images/practice.png" alt="Espacio de escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

**🎉 ¡Ya conoces lo esencial!** Entiendes MCP, has visto cómo configurar servidores y has visto flujos de trabajo reales en acción. Ahora es momento de probarlo tú.

---

## ▶️ Inténtalo tú mismo

¡Te toca! Completa estos ejercicios para practicar el uso de servidores MCP con el proyecto book app.

### Ejercicio 1: Comprueba el estado de tu MCP

Empieza viendo qué servidores MCP están disponibles:

```bash
copilot

> /mcp show
```

Deberías ver el servidor de GitHub listado como habilitado. Si no, ejecuta `/login` para autenticarte.

---

### Ejercicio 2: Explora el book app con el MCP de Filesystem

Si has configurado el servidor de filesystem, úsalo para explorar el book app:

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**Resultado esperado**: Copilot lista `book_app.py`, `books.py` y `utils.py` con sus funciones.

> 💡 **¿Aún no has configurado el MCP de filesystem?** Crea el archivo de configuración a partir de la sección [Configuración completa](#complete-configuration-file) de arriba. Después reinicia Copilot.

---

### Ejercicio 3: Consulta el historial del repositorio con el MCP de GitHub

Usa el MCP integrado de GitHub para explorar este repositorio del curso:

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**Resultado esperado**: Copilot muestra los mensajes recientes de commit y los nombres de las ramas desde el remoto de GitHub.

> ⚠️ **¿Estás en un Codespace?** Esto funciona automáticamente. La autenticación se hereda. Si estás en un clon local, asegúrate de que `gh auth status` muestra que has iniciado sesión.

---

### Ejercicio 4: Combina varios servidores MCP

Ahora combina los MCP de filesystem y GitHub en una sola sesión:

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**Resultado esperado**: Copilot lee el archivo JSON (MCP de filesystem), lista los 5 libros incluidos "The Hobbit", "1984", "Dune", "To Kill a Mockingbird" y "Mysterious Book", y luego consulta GitHub para el historial de commits.

**Autoevaluación**: Entiendes MCP cuando puedes explicar por qué "Comprueba el historial de commits de mi repo" es mejor que ejecutar manualmente `git log` y pegar la salida en tu prompt.

---

## 📝 Tarea

### Reto principal: Exploración del book app con MCP

Practica el uso de servidores MCP juntos en el proyecto book app. Completa estos pasos en una sola sesión de Copilot:

1. **Verifica que MCP funciona**: Ejecuta `/mcp show` y confirma que al menos el servidor de GitHub está habilitado
2. **Configura el MCP de filesystem** (si aún no lo has hecho): Crea `~/.copilot/mcp-config.json` con la configuración del servidor de filesystem
3. **Explora el código**: Pide a Copilot que use el servidor de filesystem para:
   - Listar todas las funciones en `samples/book-app-project/books.py`
   - Comprobar qué funciones de `samples/book-app-project/utils.py` no tienen type hints
   - Leer `samples/book-app-project/data.json` e identificar problemas de calidad de datos (pista: fíjate en la última entrada)
4. **Comprueba la actividad del repositorio**: Pide a Copilot que use el MCP de GitHub para:
   - Listar los commits recientes que tocaron archivos en `samples/book-app-project/`
   - Comprobar si hay issues o pull requests abiertos
5. **Combina servidores**: En un único prompt, pide a Copilot que:
   - Lea el archivo de pruebas en `samples/book-app-project/tests/test_books.py`
   - Compare las funciones probadas con todas las funciones de `books.py`
   - Resuma qué cobertura de pruebas falta

**Criterios de éxito**: Puedes combinar sin fricciones datos de los MCP de filesystem y GitHub en una sola sesión de Copilot, y puedes explicar qué aportó cada servidor MCP a la respuesta.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Paso 1: Verifica MCP**
```bash
copilot
> /mcp show
# Should show "github" as enabled
# If not, run: /login
```

**Paso 2: Crea el archivo de configuración**

Usa el JSON de la sección [Configuración completa](#complete-configuration-file) de arriba y guárdalo como `~/.copilot/mcp-config.json`.

**Paso 3: Problema de calidad de datos a buscar**

El último libro de `data.json` es:
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
Un autor vacío y año 0. ¡Ese es el problema de calidad de datos!

**Paso 5: Comparación de cobertura de pruebas**

Las pruebas en `test_books.py` cubren: `add_book`, `mark_as_read`, `remove_book`, `get_unread_books` y `find_book_by_title`. Funciones como `load_books`, `save_books` y `list_books` no tienen pruebas directas. Las funciones CLI en `book_app.py` y los helpers en `utils.py` no tienen ninguna prueba.

**Si MCP no funciona:** Reinicia Copilot después de editar el archivo de configuración.

</details>

### Reto extra: Construye un servidor MCP personalizado

¿Listo para profundizar más? Sigue la [Guía del servidor MCP personalizado](mcp-custom-server.md) para construir tu propio servidor MCP en Python que se conecte a cualquier API.

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué pasa | Solución |
|---------|--------------|-----|
| No saber que el MCP de GitHub viene integrado | Intentar instalarlo o configurarlo manualmente | El MCP de GitHub viene incluido por defecto. Solo prueba: "List the recent commits in this repo" |
| Buscar la configuración en el lugar equivocado | No encontrar o editar los ajustes de MCP | La configuración a nivel de usuario está en `~/.copilot/mcp-config.json`, la de nivel de proyecto es `.mcp.json` en la raíz del proyecto |
| JSON inválido en el archivo de configuración | Los servidores MCP no se cargan | Usa `/mcp show` para revisar la configuración; valida la sintaxis JSON |
| Olvidar autenticar los servidores MCP | Errores de "Authentication failed" | Algunos MCPs necesitan autenticación aparte. Revisa los requisitos de cada servidor |

### Solución de problemas

**"MCP server not found"** - Comprueba que:
1. El paquete de npm existe: `npm view @modelcontextprotocol/server-github`
2. Tu configuración es JSON válido
3. El nombre del servidor coincide con el de tu configuración

Usa `/mcp show` para ver la configuración actual.

**"GitHub authentication failed"** - El MCP integrado de GitHub usa tus credenciales de `/login`. Prueba:

```bash
copilot
> /login
```

Esto te reautenticará con GitHub. Si los problemas persisten, comprueba que tu cuenta de GitHub tiene los permisos necesarios para el repositorio al que estás accediendo.

**"MCP server failed to start"** - Revisa los logs del servidor:
```bash
# Run the server command manually to see errors
npx -y @modelcontextprotocol/server-github
```

**Las herramientas de MCP no están disponibles** - Asegúrate de que el servidor está habilitado:
```bash
copilot

> /mcp show
# Check if server is listed and enabled
```

Si un servidor está deshabilitado, consulta los [comandos `/mcp` adicionales](#-additional-mcp-commands) de abajo para saber cómo reactivarlo.

</details>

---

<details>
<summary>📚 <strong>Comandos MCP adicionales</strong> (haz clic para expandir)</summary>
<a id="-additional-mcp-commands"></a>

Puedes gestionar los servidores MCP de dos formas: usando **comandos slash dentro de una sesión de chat**, o usando el comando **`copilot mcp` directamente en tu terminal** (sin necesidad de sesión de chat).

### Opción 1: Comandos slash (dentro de una sesión de chat)

Funcionan cuando ya estás dentro de `copilot`:

| Comando | Qué hace |
|---------|--------------|
| `/mcp show` | Muestra todos los servidores MCP configurados y su estado |
| `/mcp add` | Configuración interactiva para añadir un nuevo servidor |
| `/mcp edit <server-name>` | Edita la configuración de un servidor existente |
| `/mcp enable <server-name>` | Habilita un servidor deshabilitado (persiste entre sesiones) |
| `/mcp disable <server-name>` | Deshabilita un servidor (persiste entre sesiones) |
| `/mcp delete <server-name>` | Elimina un servidor permanentemente |
| `/mcp auth <server-name>` | Reautentica con un servidor MCP que use OAuth (p. ej., tras cambiar de cuenta) |

### Opción 2: Comando `copilot mcp` (desde tu terminal)

También puedes gestionar los servidores MCP directamente desde tu terminal sin iniciar antes una sesión de chat:

```bash
# List all configured MCP servers
copilot mcp list

# Enable a server
copilot mcp enable filesystem

# Disable a server
copilot mcp disable context7
```

> 💡 **¿Cuándo usar cada uno?** Usa los comandos slash `/mcp` cuando ya estés en una sesión de chat. Usa `copilot mcp` desde la terminal cuando quieras revisar o cambiar rápidamente los ajustes de tus servidores antes de iniciar una sesión.

Para la mayor parte de este curso, `/mcp show` es todo lo que necesitas. Los demás comandos te resultarán útiles a medida que gestiones más servidores con el tiempo.

</details>

---

# Resumen

## 🔑 Conclusiones clave

1. **MCP** conecta Copilot con servicios externos (GitHub, sistema de archivos, documentación)
2. **El MCP de GitHub viene integrado** - sin configuración necesaria, basta con `/login`
3. **Filesystem y Context7** se configuran mediante `~/.copilot/mcp-config.json`
4. **Los flujos de trabajo multiservidor** combinan datos de múltiples fuentes en una sola sesión
5. **Gestiona los servidores de dos formas**: usa los comandos slash `/mcp` dentro del chat, o `copilot mcp` desde la terminal
6. **Los servidores personalizados** te permiten conectar cualquier API (opcional, cubierto en la guía del apéndice)

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para ver una lista completa de comandos y atajos.

---

## ➡️ Qué sigue

Ya tienes todos los bloques: modos, contexto, flujos de trabajo, agentes, skills y MCP. Es hora de combinarlos.

En el **[Capítulo 07: Combinando todo](../07-putting-it-together/README.md)** aprenderás:

- Combinar agentes, skills y MCP en flujos de trabajo unificados
- Desarrollo completo de funcionalidades de la idea al PR fusionado
- Automatización con hooks
- Buenas prácticas para entornos de equipo

---

**[← Volver al Capítulo 05](../05-skills/README.md)** | **[Continuar al Capítulo 07 →](../07-putting-it-together/README.md)**
