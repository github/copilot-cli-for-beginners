<!--
---
id: CopilotCLI-06
title: !translate Connect to GitHub, Databases, and APIs
description: !translate Configure MCP servers so GitHub Copilot CLI can connect to GitHub, local files, documentation, databases, and other live data sources.
audience: Developers / Students / Terminal users
slug: connect-to-github-databases-and-apis
weight: 7
---
-->

![Capítulo 06: Servidores MCP](../../../06-mcp-servers/assets/chapter-header.png)

> **¿Y si Copilot pudiera leer tus issues de GitHub, revisar tu base de datos y crear PRs... todo desde la terminal?**

Hasta ahora, Copilot solo puede trabajar con lo que le proporcionas directamente: archivos que referencias con `@`, el historial de la conversación y sus propios datos de entrenamiento. Pero ¿y si pudiera conectarse por sí mismo para revisar tu repositorio de GitHub, explorar los archivos de tu proyecto o buscar la documentación más reciente de una biblioteca?

Eso es lo que hace MCP (Model Context Protocol). Es una forma de conectar Copilot con servicios externos para que tenga acceso a datos en vivo y del mundo real. A cada servicio al que Copilot se conecta se le llama "servidor MCP". En este capítulo, configurarás algunas de estas conexiones y verás cómo hacen que Copilot sea mucho más útil.

> 💡 **¿Ya conoces MCP?** [Ir al inicio rápido](#-use-the-built-in-github-mcp) para confirmar que funciona y empezar a configurar servidores.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, podrás:

- Entender qué es MCP y por qué importa
- Gestionar servidores MCP usando los comandos `/mcp`
- Configurar servidores MCP para GitHub, sistema de archivos y documentación
- Usar flujos de trabajo potenciados por MCP con el proyecto de la app del libro
- Saber cuándo y cómo construir un servidor MCP personalizado (opcional)

> ⏱️ **Tiempo estimado**: ~50 minutos (15 min lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: Extensiones del navegador

<img src="../../../06-mcp-servers/assets/browser-extensions-analogy.png" alt="Los servidores MCP son como extensiones del navegador" width="800"/>

Piensa en los servidores MCP como extensiones del navegador. Tu navegador por sí solo puede mostrar páginas web, pero las extensiones lo conectan a servicios adicionales:

| Extensión del navegador | A qué se conecta | Equivalente MCP |
|-------------------|---------------------|----------------|
| Gestor de contraseñas | Tu bóveda de contraseñas | **GitHub MCP** → tus repos, issues, PRs |
| Grammarly | Servicio de análisis de escritura | **Context7 MCP** → documentación de bibliotecas |
| Administrador de archivos | Almacenamiento en la nube | **Filesystem MCP** → archivos locales del proyecto |

Sin extensiones, tu navegador sigue siendo útil, pero con ellas se convierte en una potencia. Los servidores MCP hacen lo mismo por Copilot. Lo conectan a fuentes de datos reales y en vivo para que pueda leer tus issues de GitHub, explorar tu sistema de archivos, obtener documentación actualizada y más.

***Los servidores MCP conectan Copilot con el mundo exterior: GitHub, repositorios, documentación y más***

> 💡 **Idea clave**: Sin MCP, Copilot solo puede ver archivos que compartes explícitamente con `@`. Con MCP, puede explorar proactivamente tu proyecto, revisar tu repositorio de GitHub y consultar documentación, todo automáticamente.

---

<img src="../../../06-mcp-servers/assets/quick-start-mcp.png" alt="Cable de alimentación con una chispa eléctrica brillante rodeada de iconos tecnológicos que representan conexiones de servidores MCP" width="800"/>

# Inicio rápido: MCP en 30 segundos

## Comienza con el servidor MCP de GitHub incorporado
Veamos MCP en acción ahora mismo, antes de configurar nada.
El servidor MCP de GitHub está incluido por defecto. Prueba esto:

```bash
copilot
> List the recent commits in this repository
```

Si Copilot devuelve datos reales de commits, acabas de ver MCP en acción. Ese es el servidor MCP de GitHub contactando a GitHub en tu nombre. Pero GitHub es solo *un* servidor. Este capítulo te muestra cómo agregar más (acceso al sistema de archivos, documentación actualizada y otros) para que Copilot pueda hacer aún más.

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

> 💡 **¿Solo ves el servidor de GitHub?** ¡Eso es normal! Si aún no has agregado servidores MCP adicionales, GitHub es el único que aparece. Agregarás más en la siguiente sección.

> 📚 **¿Quieres ver todos los comandos de gestión de MCP?** Puedes administrar servidores con los comandos slash `/mcp` dentro del chat, o con `copilot mcp` directamente desde tu terminal. Consulta la [referencia completa de comandos](#-additional-mcp-commands) al final de este capítulo.

<details>
<summary>🎬 ¡Míralo en acción!</summary>

![Demostración del estado de MCP](../../../06-mcp-servers/assets/mcp-status-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas serán diferentes a lo que se muestra aquí.*

</details>

---

## ¿Qué cambia con MCP?

Esta es la diferencia que hace MCP en la práctica:

**Sin MCP:**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**Con MCP:**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: El inicio de sesión falla con caracteres especiales
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP hace que Copilot sea consciente de tu entorno de desarrollo real.

> 📚 **Documentación oficial**: [Acerca de MCP](https://docs.github.com/copilot/concepts/context/mcp) para una mirada más profunda a cómo MCP funciona con GitHub Copilot.

---

# Configuración de servidores MCP

<img src="../../../06-mcp-servers/assets/configuring-mcp-servers.png" alt="Manos ajustando perillas y deslizadores en una mesa de mezcla profesional que representan la configuración de servidores MCP" width="800"/>

Ahora que has visto MCP en acción, vamos a configurar servidores adicionales. Puedes agregar servidores de dos maneras: **desde el registro integrado** (lo más fácil: configuración guiada directamente en la CLI) o editando el archivo de configuración manualmente (más flexible). Comienza con la opción del registro si no estás seguro de cuál elegir.

---

## Instalación de servidores MCP desde el registro

La CLI tiene un registro de servidores MCP integrado que te permite descubrir e instalar servidores populares con una configuración guiada — no se requiere editar JSON.

```bash
copilot

> /mcp search
```

Copilot abre un selector interactivo que muestra los servidores disponibles. Selecciona uno, y la CLI te guía a través de la configuración requerida (claves API, rutas, etc.) y lo añade a tu configuración automáticamente.

> 💡 **¿Por qué usar el registro?** Es la forma más fácil de empezar: no necesitas conocer el nombre del paquete npm, los argumentos del comando o la estructura JSON. La CLI se encarga de todo eso por ti.

---

## Archivo de configuración de MCP

Los servidores MCP pueden configurarse a nivel de usuario en `~/.copilot/mcp-config.json`, lo cual aplica a través de proyectos; a nivel de proyecto en `.mcp.json`; o en el archivo de configuración del workspace `.github/mcp.json`. `.github/mcp.json` se carga automáticamente junto con `.mcp.json`. Si usaste `/mcp search`, la CLI creó o actualizó tu `~/.copilot/mcp-config.json` a nivel de usuario, pero entender el formato JSON es útil cuando quieras personalizar o compartir la configuración MCP a nivel de proyecto.

> ⚠️ **Nota**: `.vscode/mcp.json` ya no es compatible como fuente de configuración MCP. Si tienes un `.vscode/mcp.json` existente, migra su contenido a `.mcp.json` en la raíz de tu proyecto. La CLI mostrará una sugerencia de migración si detecta un archivo de configuración antiguo.

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

*La mayoría de los servidores MCP se distribuyen como paquetes npm y se ejecutan mediante el comando `npx`.*

<details>
<summary>💡 <strong>¿Nuevo en JSON?</strong> Haz clic aquí para aprender qué significa cada campo</summary>

| Campo | Qué significa |
|-------|---------------|
| `"mcpServers"` | Contenedor para todas tus configuraciones de servidores MCP |
| `"server-name"` | Un nombre que elijas (p. ej., "github", "filesystem") |
| `"type": "local"` | El servidor se ejecuta en tu máquina |
| `"command": "npx"` | El programa a ejecutar (npx ejecuta paquetes npm) |
| `"args": [...]` | Argumentos pasados al comando |
| `"tools": ["*"]` | Permitir todas las herramientas de este servidor |

**Reglas importantes de JSON:**
- Usa comillas dobles `"` para las cadenas (no comillas simples)
- No usar comas finales después del último elemento
- El archivo debe ser un JSON válido (usa un [validador JSON](https://jsonlint.com/) si no estás seguro)

</details>

---

## Agregar servidores MCP

El servidor MCP de GitHub está integrado y no requiere configuración. A continuación hay servidores adicionales que puedes agregar. **Elige lo que te interese o trabaja con ellos en orden.**

| Quiero... | Ir a |
|---|---|
| Permitir que Copilot explore los archivos de mi proyecto | [Servidor de sistema de archivos](#servidor-de-sistema-de-archivos) |
| Obtener documentación de biblioteca actualizada | [Servidor Context7](#servidor-context7-documentación) |
| Explorar extras opcionales (servidores personalizados, web_fetch) | [Más allá de lo básico](#más-allá-de-lo-básico) |

<details>
<summary><strong>Servidor de sistema de archivos</strong> - Permitir que Copilot explore los archivos de tu proyecto</summary>
<a id="filesystem-server"></a>

### Servidor de sistema de archivos

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

> 💡 **La ruta `.`**: El `.` significa "directorio actual". Copilot puede acceder a archivos relativos al lugar donde lo iniciaste. En un Codespace, esto es la raíz de tu espacio de trabajo. También puedes usar una ruta absoluta como `/workspaces/copilot-cli-for-beginners` si lo prefieres.

Agrega esto a tu `~/.copilot/mcp-config.json` y reinicia Copilot.

</details>

<details>
<summary><strong>Servidor Context7</strong> - Obtener documentación de bibliotecas actualizada</summary>
<a id="context7-server-documentation"></a>

### Servidor Context7 (Documentación)

Context7 da a Copilot acceso a documentación actualizada de frameworks y bibliotecas populares. En lugar de confiar en datos de entrenamiento que pueden estar desactualizados, Copilot obtiene la documentación actual vigente.

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

- ✅ **No se requiere clave API** 
- ✅ **No se necesita cuenta** 
- ✅ **Tu código permanece local**

Agrega esto a tu `~/.copilot/mcp-config.json` y reinicia Copilot.

</details>

<details>
<summary><strong>Más allá de lo básico</strong> - Servidores personalizados y acceso web (opcional)</summary>
<a id="beyond-the-basics"></a>

Estos son extras opcionales para cuando te sientas cómodo con los servidores principales anteriores.

### Servidor MCP de Microsoft Learn

Cada servidor MCP que has visto hasta ahora (filesystem, Context7) se ejecuta localmente en tu máquina. Pero los servidores MCP también pueden ejecutarse de forma remota, lo que significa que simplemente apuntas la CLI de Copilot a una URL y ella se encarga del resto. No hace falta `npx` ni `python`, no hay procesos locales ni dependencias que instalar.

El [Microsoft Learn MCP Server](https://github.com/microsoftdocs/mcp) es un buen ejemplo. Le da a la CLI de Copilot acceso directo a la documentación oficial de Microsoft (Azure, Microsoft Foundry y otros temas de IA, .NET, Microsoft 365 y mucho más) para que pueda buscar en la documentación, obtener páginas completas y encontrar ejemplos de código oficiales en lugar de depender de los datos de entrenamiento del modelo.

- ✅ **No se requiere clave API** 
- ✅ **No se necesita cuenta** 
- ✅ **No se requiere instalación local**

**Instalación rápida con `/plugin install`:**

En lugar de editar manualmente tu archivo de configuración JSON, puedes instalarlo con un solo comando:

```bash
copilot

> /plugin install microsoftdocs/mcp
```

Esto añade el servidor y sus habilidades de agente asociadas automáticamente. Las habilidades instaladas incluyen:

- **microsoft-docs**: Conceptos, tutoriales y búsquedas factuales
- **microsoft-code-reference**: Búsquedas de API, ejemplos de código y resolución de problemas
- **microsoft-skill-creator**: Una meta-habilidad para generar habilidades personalizadas sobre tecnologías Microsoft

**Uso:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 Aprende más: [Descripción general del Microsoft Learn MCP Server](https://learn.microsoft.com/training/support/mcp-get-started)

### Acceso web con `web_fetch`

La CLI de Copilot incluye una herramienta integrada `web_fetch` que puede obtener contenido de cualquier URL. Esto es útil para traer READMEs, documentación de API o notas de lanzamiento sin salir de tu terminal. No se necesita un servidor MCP.

Puedes controlar qué URLs son accesibles mediante `~/.copilot/config.json` (configuración general de Copilot), que es independiente de `~/.copilot/mcp-config.json` (definiciones de servidores MCP).

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

¿Quieres conectar Copilot a tus propias APIs, bases de datos o herramientas internas? Puedes construir un servidor MCP personalizado en Python. Esto es completamente opcional, ya que los servidores preconstruidos (GitHub, filesystem, Context7) cubren la mayoría de los casos de uso.

📖 Consulta la [Guía de servidores MCP personalizados](mcp-custom-server.md) para un recorrido completo usando la app del libro como ejemplo.

📚 Para más información, consulta el [curso MCP para principiantes](https://github.com/microsoft/mcp-for-beginners).

</details>

<a id="complete-configuration-file"></a>

### Archivo de configuración completo

Aquí tienes un `mcp-config.json` completo con servidores filesystem y Context7:

> 💡 **Nota:** El MCP de GitHub está integrado. No necesitas agregarlo a tu archivo de configuración.


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

Guarda esto como `~/.copilot/mcp-config.json` para acceso global o como `.mcp.json` en la raíz del proyecto para configuración específica del proyecto.

---

# Uso de servidores MCP

Ahora que tienes configurados los servidores MCP, veamos lo que pueden hacer.

<img src="../../../06-mcp-servers/assets/using-mcp-servers.png" alt="Uso de servidores MCP - Diagrama hub-and-spoke que muestra una CLI de desarrollador conectada a GitHub, Filesystem, Context7 y servidores personalizados/web_fetch" width="800" />

---

## Ejemplos de uso de servidores

**Elige un servidor para explorar o recórrelos en orden.**

| Quiero intentar... | Ir a |
|---|---|
| Repositorios, incidencias y PRs de GitHub | [Servidor de GitHub](#servidor-de-github-incluido) |
| Explorar archivos del proyecto | [Uso del servidor Filesystem](#filesystem-server-usage) |
| Búsqueda de documentación de librerías | [Uso del servidor Context7](#context7-server-usage) |
| Servidor personalizado, Microsoft Learn MCP y uso de web_fetch | [Más allá de lo básico](#más-allá-de-lo-básico) |

<details>
<summary><strong>Servidor de GitHub (incluido)</strong> - Accede a repositorios, incidencias, PRs y más</summary>
<a id="github-server-built-in"></a>

### Servidor de GitHub (incluido)

El servidor MCP de GitHub está **incluido**. Si iniciaste sesión en Copilot (lo hiciste durante la configuración inicial), ya funciona. ¡No se necesita configuración!

> 💡 **¿No funciona?** Ejecuta `/login` para volver a autenticarte con GitHub.

<details>
<summary><strong>Autenticación en Dev Containers</strong></summary>

- **GitHub Codespaces** (recomendado): La autenticación es automática. La CLI `gh` hereda tu token de Codespace. No se requiere acción.
- **Contenedor de desarrollo local (Docker)**: Ejecuta `gh auth login` después de que el contenedor se inicie, luego reinicia Copilot.

**Solución de problemas de autenticación:**
```bash
# Comprueba si estás autenticado
gh auth status

# Si no, inicia sesión
gh auth login

# Verifica que GitHub MCP esté conectado
copilot
> /mcp show
```

</details>

| Funcionalidad | Ejemplo |
|---------|----------|
| **Información del repositorio** | Ver commits, ramas y colaboradores |
| **Incidencias** | Listar, crear, buscar y comentar incidencias |
| **Pull requests** | Ver PRs, diffs, crear PRs, comprobar el estado |
| **Búsqueda de código** | Buscar código en repositorios |
| **Actions** | Consultar ejecuciones de workflows y su estado |

```bash
copilot

# Ver la actividad reciente en este repositorio
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# Explorar la estructura del repositorio
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# Buscar patrones de código en todo el repositorio
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **¿Trabajando en tu propio fork?** Si bifurcaste este repositorio del curso, también puedes probar operaciones de escritura como crear incidencias y pull requests. Practicaremos eso en los ejercicios a continuación.

> ⚠️ **¿No ves resultados?** El MCP de GitHub opera sobre el remoto del repositorio (en github.com), no solo sobre archivos locales. Asegúrate de que tu repo tenga un remoto: ejecuta `git remote -v` para comprobarlo.

</details>

<details>
<summary><strong>Servidor Filesystem</strong> - Explora y analiza archivos del proyecto</summary>
<a id="filesystem-server-usage"></a>

### Servidor Filesystem

Una vez configurado, el MCP Filesystem proporciona herramientas que Copilot puede usar automáticamente:

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
<summary><strong>Servidor Context7</strong> - Buscar documentación de librerías</summary>
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
        # fixture se pasa automáticamente como argumento
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot ahora conoce los patrones oficiales de pytest
# y puede aplicarlos a samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>Más allá de lo básico</strong> - Servidor personalizado y uso de web_fetch</summary>
<a id="beyond-the-basics-usage"></a>

### Más allá de lo básico

**Servidor MCP personalizado**: Si construiste el servidor de búsqueda de libros a partir de la [Guía de servidor MCP personalizado](mcp-custom-server.md), puedes consultar tu colección de libros directamente:

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**: Si instalaste el [servidor Microsoft Learn MCP](#servidor-mcp-de-microsoft-learn), puedes consultar la documentación oficial de Microsoft directamente:

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**: Usa la herramienta integrada `web_fetch` para obtener contenido de cualquier URL:

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## Flujos de trabajo multi-servidor

Estos flujos de trabajo muestran por qué los desarrolladores dicen «Nunca volveré a trabajar sin esto». Cada ejemplo combina múltiples servidores MCP en una sola sesión.

<img src="../../../06-mcp-servers/assets/issue-to-pr-workflow.png" alt="Flujo de trabajo de issue a PR usando MCP - Muestra el flujo completo desde obtener una incidencia de GitHub hasta crear un pull request" width="800"/>

*Flujo completo de MCP: el MCP de GitHub recupera datos del repositorio, el MCP Filesystem encuentra el código, el MCP Context7 proporciona las mejores prácticas y Copilot realiza el análisis*

Cada ejemplo a continuación es autónomo. **Elige uno que te interese o léelos todos.**

| Quiero ver... | Ir a |
|---|---|
| Múltiples servidores trabajando juntos | [Exploración multi-servidor](#multi-server-exploration) |
| Pasar de issue a PR en una sesión | [Flujo de trabajo issue a PR](#issue-to-pr-workflow) |
| Un chequeo rápido de la salud del proyecto | [Panel de salud](#panel-de-salud-de-la-app-de-libros) |

<details>
<summary><strong>Exploración multi-servidor</strong> - Combina Filesystem, GitHub y Context7 en una sesión</summary>
<a id="multi-server-exploration"></a>

#### Explorando la app de libros con múltiples servidores MCP

```bash
copilot

# Paso 1: Usa el MCP del sistema de archivos para explorar la aplicación de libros
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Paso 2: Usa el MCP de GitHub para comprobar los cambios recientes
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Paso 3: Usa el MCP Context7 para las mejores prácticas
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Paso 4: Sintetiza una recomendación
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 ¡Mira el flujo de trabajo MCP en acción!</summary>

![Demostración del flujo MCP](../../../06-mcp-servers/assets/mcp-workflow-demo.gif)

*La salida de la demo puede variar. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

</details>

**El resultado**: Exploración de código → revisión del historial → consulta de mejores prácticas → plan de mejoras. **Todo desde una sola sesión de terminal, usando tres servidores MCP juntos.**

</details>

<details>
<summary><strong>Flujo de trabajo Issue a PR</strong> - Pasa de una incidencia de GitHub a un pull request sin salir del terminal</summary>
<a id="issue-to-pr-workflow"></a>

#### El flujo Issue a PR (en tu propio repo)

Esto funciona mejor en tu propio fork o repositorio donde tengas acceso de escritura:

> 💡 **No te preocupes si no puedes probar esto ahora mismo.** Si estás en un clon de solo lectura, practicarás esto en la tarea. Por ahora, solo léelo para entender el flujo.

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Agregar validación de entrada para el año del libro
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Agregar validación del año a la aplicación de libros
```

**Cero copiar-pegar. Cero cambios de contexto. Una sesión de terminal.**

</details>

<details>
<summary><strong>Panel de salud</strong> - Obtén un chequeo rápido de la salud del proyecto usando múltiples servidores</summary>
<a id="health-dashboard"></a>

#### Panel de salud de la app de libros

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

**El resultado**: Múltiples fuentes de datos agregadas en segundos. Manualmente, esto significaría ejecutar grep, contar líneas, revisar git log y recorrer archivos de pruebas. Fáciles 15+ minutos de trabajo.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Escritorio acogedor con monitor mostrando código, lámpara, taza de café y auriculares listos para practicar" width="800"/>

**🎉 ¡Ahora conoces lo esencial!** Entiendes MCP, has visto cómo configurar servidores y has visto flujos de trabajo reales en acción. Ahora es momento de intentarlo tú mismo.

---

## ▶️ Pruébalo tú mismo

¡Ahora es tu turno! Completa estos ejercicios para practicar el uso de servidores MCP con el proyecto de la app de libros.

### Ejercicio 1: Comprueba el estado de MCP

Comienza viendo qué servidores MCP están disponibles:

```bash
copilot

> /mcp show
```

Deberías ver el servidor de GitHub listado como habilitado. Si no, ejecuta `/login` para autenticarte.

---

### Ejercicio 2: Explora la app de libros con MCP Filesystem

Si has configurado el servidor Filesystem, úsalo para explorar la app de libros:

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**Resultado esperado**: Copilot lista `book_app.py`, `books.py` y `utils.py` con sus funciones.

> 💡 **¿No tienes MCP Filesystem configurado todavía?** Crea el archivo de configuración desde la sección [Archivo de configuración completo](#archivo-de-configuración-completo) arriba. Luego reinicia Copilot.

---

### Ejercicio 3: Consulta el historial del repositorio con MCP GitHub

Usa el MCP de GitHub incluido para explorar este repositorio del curso:

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**Resultado esperado**: Copilot muestra mensajes de commits recientes y nombres de ramas del remoto de GitHub.

> ⚠️ **¿En un Codespace?** Esto funciona automáticamente. La autenticación se hereda. Si estás en un clon local, asegúrate de que `gh auth status` muestra que has iniciado sesión.

---

### Ejercicio 4: Combina múltiples servidores MCP

Ahora combina MCP Filesystem y GitHub en una sola sesión:

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**Resultado esperado**: Copilot lee el archivo JSON (MCP Filesystem), lista los 5 libros incluyendo "The Hobbit", "1984", "Dune", "To Kill a Mockingbird" y "Mysterious Book", luego consulta GitHub por el historial de commits.

**Autoevaluación**: Comprendes MCP cuando puedes explicar por qué "Check my repo's commit history" es mejor que ejecutar manualmente `git log` y pegar la salida en tu prompt.

---

## 📝 Tarea

### Desafío principal: Exploración MCP de la app de libros

Practica usando servidores MCP juntos en el proyecto de la app de libros. Completa estos pasos en una sola sesión de Copilot:

1. **Verifica que MCP funcione**: Ejecuta `/mcp show` y confirma que al menos el servidor de GitHub esté habilitado
2. **Configura MCP Filesystem** (si aún no lo hiciste): Crea `~/.copilot/mcp-config.json` con la configuración del servidor Filesystem
3. **Explora el código**: Pide a Copilot que use el servidor Filesystem para:
   - Listar todas las funciones en `samples/book-app-project/books.py`
   - Comprobar qué funciones en `samples/book-app-project/utils.py` carecen de anotaciones de tipo
   - Leer `samples/book-app-project/data.json` e identificar problemas de calidad de datos (pista: mira la última entrada)
4. **Comprueba la actividad del repositorio**: Pide a Copilot que use MCP de GitHub para:
   - Listar commits recientes que tocaron archivos en `samples/book-app-project/`
   - Comprobar si hay incidencias o pull requests abiertos
5. **Combina servidores**: En un solo prompt, pídele a Copilot que:
   - Leer el archivo de pruebas en `samples/book-app-project/tests/test_books.py`
   - Comparar las funciones probadas con todas las funciones en `books.py`
   - Resumir qué cobertura de pruebas falta

**Criterios de éxito**: Puedes combinar sin problemas los datos de MCP Filesystem y GitHub en una sola sesión de Copilot, y puedes explicar qué contribuyó cada servidor MCP a la respuesta.

<details>
<summary>💡 Pistas (haz clic para expandir)</summary>

**Paso 1: Verificar MCP**
```bash
copilot
> /mcp show
# Debe mostrar "github" como habilitado
# Si no, ejecute: /login
```

**Paso 2: Crear el archivo de configuración**

Usa el JSON de la sección [Archivo de configuración completo](#archivo-de-configuración-completo) arriba y guárdalo como `~/.copilot/mcp-config.json`.

**Paso 3: Problema de calidad de datos a buscar**

El último libro en `data.json` es:
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
Un autor vacío y año igual a 0. ¡Ese es el problema de calidad de datos!

**Paso 5: Comparación de cobertura de pruebas**

Las pruebas en `test_books.py` cubren: `add_book`, `mark_as_read`, `remove_book`, `get_unread_books` y `find_book_by_title`. Funciones como `load_books`, `save_books` y `list_books` no tienen pruebas directas. Las funciones CLI en `book_app.py` y los ayudantes en `utils.py` no tienen pruebas en absoluto.

**Si MCP no funciona:** Reinicia Copilot después de editar el archivo de configuración.

</details>

### Desafío extra: Construye un servidor MCP personalizado

¿Listo para profundizar? Sigue la [Guía de servidor MCP personalizado](mcp-custom-server.md) para construir tu propio servidor MCP en Python que se conecte a cualquier API.

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para expandir)</summary>

### Errores comunes

| Error | Qué ocurre | Solución |
|---------|--------------|-----|
| No saber que el MCP de GitHub está incluido | Intentar instalar/configurarlo manualmente | El MCP de GitHub está incluido por defecto. Simplemente prueba: "List the recent commits in this repo" |
| Buscar la configuración en la ubicación equivocada | No se pueden encontrar o editar los ajustes de MCP | La configuración a nivel de usuario está en `~/.copilot/mcp-config.json`, la del proyecto es `.mcp.json` en la raíz del proyecto |
| JSON inválido en el archivo de configuración | Los servidores MCP no se cargan | Usa `/mcp show` para comprobar la configuración; valida la sintaxis JSON |
| Olvidar autenticar los servidores MCP | Errores 'Authentication failed' | Algunos MCP requieren autenticación separada. Revisa los requisitos de cada servidor |

### Solución de problemas

**"MCP server not found"** - Comprueba que:
1. El paquete npm existe: `npm view @modelcontextprotocol/server-github`
2. Tu configuración es JSON válido
3. El nombre del servidor coincide con tu configuración

Usa `/mcp show` para ver la configuración actual.


**"Error de autenticación de GitHub"** - El MCP de GitHub integrado usa tus credenciales de `/login`. Intenta:

```bash
copilot
> /login
```

Esto volverá a autenticarte con GitHub. Si los problemas persisten, comprueba que tu cuenta de GitHub tenga los permisos necesarios para el repositorio al que intentas acceder.

**"Error al iniciar el servidor MCP"** - Revisa los registros del servidor:
```bash
# Ejecute el comando del servidor manualmente para ver los errores
npx -y @modelcontextprotocol/server-github
```

**Herramientas MCP no disponibles** - Asegúrate de que el servidor esté habilitado:
```bash
copilot

> /mcp show
# Comprobar si el servidor está listado y habilitado
```

Si un servidor está deshabilitado, consulta los [comandos `/mcp` adicionales](#-additional-mcp-commands) a continuación para saber cómo volver a habilitarlo.

</details>

---

<details>
<summary>📚 <strong>Comandos MCP adicionales</strong> (haga clic para expandir)</summary>
<a id="-additional-mcp-commands"></a>

Puedes gestionar servidores MCP de dos maneras: usando **comandos slash dentro de una sesión de chat**, o usando el **comando `copilot mcp` directamente en tu terminal** (no se necesita iniciar una sesión de chat).

### Opción 1: Comandos slash (dentro de una sesión de chat)

Estos funcionan cuando ya estás dentro de `copilot`:

| Comando | Qué hace |
|---------|--------------|
| `/mcp show` | Muestra todos los servidores MCP configurados y su estado |
| `/mcp list` | Muestra los servidores MCP actualmente adjuntos y su estado; se puede ejecutar mientras Copilot está trabajando |
| `/mcp add` | Configuración interactiva para añadir un nuevo servidor |
| `/mcp edit <server-name>` | Editar la configuración de un servidor existente |
| `/mcp enable <server-name>` | Habilitar un servidor deshabilitado (persiste entre sesiones) |
| `/mcp disable <server-name>` | Deshabilitar un servidor (persiste entre sesiones) |
| `/mcp delete <server-name>` | Eliminar un servidor permanentemente |
| `/mcp auth <server-name>` | Volver a autenticarse con un servidor MCP que usa OAuth (por ejemplo, tras cambiar de cuenta) |

### Opción 2: comando `copilot mcp` (desde tu terminal)

También puedes gestionar servidores MCP directamente desde tu terminal sin iniciar primero una sesión de chat:

```bash
# Listar todos los servidores MCP configurados
copilot mcp list

# Habilitar un servidor
copilot mcp enable filesystem

# Deshabilitar un servidor
copilot mcp disable context7
```

> 💡 **¿Cuándo usar cada uno?** Usa los comandos slash `/mcp` cuando ya estés en una sesión de chat. Usa `copilot mcp` desde la terminal cuando quieras comprobar o cambiar rápidamente la configuración de tu servidor antes de iniciar una sesión.

Para la mayor parte de este curso, `/mcp show` es todo lo que necesitas. Los otros comandos resultan útiles a medida que gestionas más servidores con el tiempo.

</details>

---

# Resumen

## 🔑 Puntos clave

1. **MCP** conecta Copilot a servicios externos (GitHub, filesystem, documentación)
2. **El MCP de GitHub está integrado** - no se necesita configuración, solo `/login`
3. **Filesystem y Context7** se configuran mediante `~/.copilot/mcp-config.json`
4. **Flujos de trabajo multi-servidor** combinan datos de múltiples fuentes en una única sesión
5. **Gestiona servidores de dos maneras**: usa los comandos slash `/mcp` dentro del chat, o `copilot mcp` desde la terminal
6. **Servidores personalizados** te permiten conectar cualquier API (opcional, cubierto en la guía del apéndice)

> 📋 **Referencia rápida**: Consulta la [Referencia de comandos de GitHub Copilot CLI](https://docs.github.com/en/copilot/reference/cli-command-reference) para obtener una lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Ahora tienes todos los bloques de construcción: modos, contexto, flujos de trabajo, agentes, habilidades y MCP. Es hora de juntarlos todos.

En **[Capítulo 07: Integrándolo todo](../07-putting-it-together/README.md)**, aprenderás:

- Combinar agentes, habilidades y MCP en flujos de trabajo unificados
- Desarrollo completo de una funcionalidad desde la idea hasta el PR fusionado
- Automatización con hooks
- Mejores prácticas para entornos de equipo

---

**[← Volver al Capítulo 05](../05-skills/README.md)** | **[Continuar al Capítulo 07 →](../07-putting-it-together/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->