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

> **¿Y si Copilot pudiera leer tus issues de GitHub, consultar tu base de datos y crear PRs... todo desde la terminal?**

Hasta ahora, Copilot solo puede trabajar con lo que le das directamente: archivos que referencias con `@`, el historial de la conversación y sus propios datos de entrenamiento. Pero ¿y si pudiera conectarse por su cuenta para comprobar tu repositorio de GitHub, explorar los archivos de tu proyecto o buscar la documentación más reciente de una librería?

Eso es lo que hace MCP (Model Context Protocol). Es una forma de conectar Copilot con servicios externos para que tenga acceso a datos en vivo y del mundo real. A cada servicio al que Copilot se conecta se le llama un "servidor MCP". En este capítulo, configurarás algunas de estas conexiones y verás cómo hacen a Copilot notablemente más útil.

> 💡 **¿Ya conoces MCP?** [Ir al inicio rápido](#-use-the-built-in-github-mcp) para confirmar que funciona y empezar a configurar servidores.

## 🎯 Objetivos de aprendizaje

Al final de este capítulo, serás capaz de:

- Entender qué es MCP y por qué importa
- Gestionar servidores MCP usando los comandos `/mcp`
- Configurar servidores MCP para GitHub, el sistema de archivos y documentación
- Usar flujos de trabajo potenciados por MCP con el proyecto de la app del libro
- Saber cuándo y cómo construir un servidor MCP personalizado (opcional)

> ⏱️ **Tiempo estimado**: ~50 minutos (15 min lectura + 35 min práctica)

---

## 🧩 Analogía del mundo real: Extensiones del navegador

<img src="../../../06-mcp-servers/assets/browser-extensions-analogy.png" alt="Los servidores MCP son como extensiones del navegador" width="800"/>

Piensa en los servidores MCP como extensiones del navegador. Tu navegador por sí solo puede mostrar páginas web, pero las extensiones lo conectan a servicios extra:

| Extensión del navegador | A qué se conecta | Equivalente MCP |
|------------------------|------------------|-----------------|
| Administrador de contraseñas | Tu bóveda de contraseñas | **GitHub MCP** → tus repositorios, incidencias, pull requests |
| Grammarly | Servicio de análisis de redacción | **Context7 MCP** → documentación de librerías |
| Gestor de archivos | Almacenamiento en la nube | **Filesystem MCP** → archivos del proyecto local |

Sin extensiones, tu navegador sigue siendo útil, pero con ellas se convierte en una herramienta poderosa. Los servidores MCP hacen lo mismo por Copilot. Lo conectan a fuentes de datos reales y en vivo para que pueda leer tus issues de GitHub, explorar tu sistema de archivos, obtener documentación actualizada y más.

***Los servidores MCP conectan a Copilot con el mundo exterior: GitHub, repositorios, documentación y más***

> 💡 **Idea clave**: Sin MCP, Copilot solo puede ver archivos que compartes explícitamente con `@`. Con MCP, puede explorar proactivamente tu proyecto, comprobar tu repositorio de GitHub y buscar documentación, todo automáticamente.

---

<img src="../../../06-mcp-servers/assets/quick-start-mcp.png" alt="Cable de alimentación conectándose con chispa eléctrica brillante rodeado por iconos tecnológicos flotantes que representan conexiones de servidores MCP" width="800"/>

# Inicio rápido: MCP en 30 segundos

## Comienza con el servidor MCP de GitHub integrado
Veamos MCP en acción ahora mismo, sin configurar nada.
El servidor MCP de GitHub está incluido por defecto. Prueba esto:

```bash
copilot
> List the recent commits in this repository
```

Si Copilot devuelve datos reales de commits, acabas de ver MCP en acción. Ese es el servidor MCP de GitHub conectándose a GitHub en tu nombre. Pero GitHub es solo *un* servidor. Este capítulo te muestra cómo añadir más (acceso al sistema de archivos, documentación actualizada y otros) para que Copilot pueda hacer todavía más.

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

> 💡 **¿Solo ves el servidor de GitHub?** ¡Es lo esperado! Si no has añadido servidores MCP adicionales todavía, GitHub es el único que aparece. Añadirás más en la siguiente sección.

> 📚 **¿Quieres ver todos los comandos de gestión de MCP?** Puedes gestionar servidores con los comandos slash `/mcp` dentro del chat, o con `copilot mcp` directamente desde tu terminal. Consulta la [referencia completa de comandos](#-additional-mcp-commands) al final de este capítulo.

<details>
<summary>🎬 ¡Mira cómo funciona!</summary>

![Demostración del estado de MCP](../../../06-mcp-servers/assets/mcp-status-demo.gif)

*La salida de la demo varía. Tu modelo, herramientas y respuestas diferirán de lo mostrado aquí.*

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

> 📚 **Documentación oficial**: [About MCP](https://docs.github.com/copilot/concepts/context/mcp) para una mirada más profunda de cómo MCP funciona con GitHub Copilot.

---

# Configuración de servidores MCP

<img src="../../../06-mcp-servers/assets/configuring-mcp-servers.png" alt="Manos ajustando perillas y controles deslizantes en una mesa de mezcla profesional representando la configuración de servidores MCP" width="800"/>

Ahora que has visto MCP en acción, vamos a configurar servidores adicionales. Puedes añadir servidores de dos maneras: **desde el registro integrado** (lo más fácil — configuración guiada directamente en la CLI) o editando el archivo de configuración manualmente (más flexible). Empieza con la opción del registro si no estás seguro de cuál elegir.

---

## Instalar servidores MCP desde el registro

La CLI tiene un registro de servidores MCP incorporado que te permite descubrir e instalar servidores populares con una configuración guiada — sin editar JSON.

```bash
copilot

> /mcp search
```

Copilot abre un selector interactivo mostrando los servidores disponibles. Selecciona uno y la CLI te guiará por la configuración necesaria (claves API, rutas, etc.) y lo añadirá a tu configuración automáticamente.

> 💡 **¿Por qué usar el registro?** Es la forma más fácil de empezar — no necesitas conocer el nombre del paquete npm, los argumentos del comando ni la estructura JSON. La CLI se encarga de todo eso por ti.

---

## Archivo de configuración de MCP

Los servidores MCP pueden configurarse a nivel de usuario en `~/.copilot/mcp-config.json`, lo cual se aplica a todos los proyectos, a nivel de proyecto en `.mcp.json`, o en el archivo de configuración del workspace `.github/mcp.json`. `.github/mcp.json` se carga automáticamente junto con `.mcp.json`. Si usaste `/mcp search`, la CLI creó o actualizó tu `~/.copilot/mcp-config.json` a nivel de usuario, pero entender el formato JSON es útil cuando quieres personalizar o compartir la configuración MCP a nivel de proyecto.

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
| `"server-name"` | Un nombre que eliges (por ejemplo, "github", "filesystem") |
| `"type": "local"` | El servidor se ejecuta en tu máquina |
| `"command": "npx"` | El programa a ejecutar (npx ejecuta paquetes npm) |
| `"args": [...]` | Argumentos pasados al comando |
| `"tools": ["*"]` | Permite todas las herramientas de este servidor |

**Reglas importantes de JSON:**
- Usa comillas dobles `"` para las cadenas (no comillas simples)
- No pongas comas finales después del último elemento
- El archivo debe ser JSON válido (usa un [validador JSON](https://jsonlint.com/) si no estás seguro)

</details>

---

## Añadir servidores MCP

El servidor MCP de GitHub está integrado y no requiere configuración. A continuación hay servidores adicionales que puedes añadir. **Elige lo que te interese o siguelos en orden.**

| Quiero... | Ir a |
|---|---|
| Permitir que Copilot explore mis archivos de proyecto | [Filesystem Server](#servidor-filesystem) |
| Obtener documentación de librerías actualizada | [Context7 Server](#servidor-context7-documentación) |
| Explorar extras opcionales (servidores personalizados, web_fetch) | [Más allá de lo básico](#más-allá-de-lo-básico) |

<details>
<summary><strong>Servidor Filesystem</strong> - Permitir que Copilot explore tus archivos de proyecto</summary>
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

> 💡 **La ruta `.`**: El `.` significa "directorio actual". Copilot puede acceder a archivos relativos a donde lo arrancaste. En un Codespace, esto es la raíz de tu workspace. También puedes usar una ruta absoluta como `/workspaces/copilot-cli-for-beginners` si lo prefieres.

Añádelo a tu `~/.copilot/mcp-config.json` y reinicia Copilot.

</details>

<details>
<summary><strong>Servidor Context7</strong> - Obtener documentación de librerías actualizada</summary>
<a id="context7-server-documentation"></a>

### Servidor Context7 (Documentación)

Context7 da a Copilot acceso a documentación actualizada para frameworks y librerías populares. En lugar de confiar en datos de entrenamiento que pueden estar desactualizados, Copilot obtiene la documentación actual real.

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

Añádelo a tu `~/.copilot/mcp-config.json` y reinicia Copilot.

</details>

<details>
<summary><strong>Más allá de lo básico</strong> - Servidores personalizados y acceso web (opcional)</summary>
<a id="beyond-the-basics"></a>

Estos son extras opcionales para cuando ya te sientas cómodo con los servidores principales anteriores.

### Servidor MCP de Microsoft Learn

Todos los servidores MCP que has visto hasta ahora (filesystem, Context7) se ejecutan localmente en tu máquina. Pero los servidores MCP también pueden ejecutarse de forma remota, lo que significa que solo apuntas la Copilot CLI a una URL y ella se encarga del resto. No hace falta `npx` ni `python`, no hay proceso local ni dependencias que instalar.

El [Servidor MCP de Microsoft Learn](https://github.com/microsoftdocs/mcp) es un buen ejemplo. Da a Copilot CLI acceso directo a la documentación oficial de Microsoft (Azure, Microsoft Foundry y otros temas de IA, .NET, Microsoft 365 y mucho más) para que pueda buscar en la documentación, obtener páginas completas y encontrar ejemplos de código oficiales en lugar de depender de los datos de entrenamiento de un modelo.

- ✅ **No se requiere clave API**
- ✅ **No se necesita cuenta**
- ✅ **No se requiere instalación local**

**Instalación rápida con `/plugin install`:**

En lugar de editar tu archivo JSON de configuración manualmente, puedes instalarlo con un solo comando:

```bash
copilot

> /plugin install microsoftdocs/mcp
```

Esto añade el servidor y sus skills de agente asociados automáticamente. Las skills instaladas incluyen:

- **microsoft-docs**: Conceptos, tutoriales y búsquedas factuales
- **microsoft-code-reference**: Búsquedas de API, ejemplos de código y solución de problemas
- **microsoft-skill-creator**: Una meta-skill para generar skills personalizadas sobre tecnologías de Microsoft

**Uso:**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 Más información: [Descripción general del Servidor MCP de Microsoft Learn](https://learn.microsoft.com/training/support/mcp-get-started)

### Acceso web con `web_fetch`

La Copilot CLI incluye una herramienta integrada `web_fetch` que puede obtener contenido de cualquier URL. Esto es útil para traer README, documentación de API o notas de lanzamiento sin salir de la terminal. No se necesita un servidor MCP.

Puedes controlar qué URLs son accesibles mediante `~/.copilot/config.json` (ajustes generales de Copilot), que está separado de `~/.copilot/mcp-config.json` (definiciones de servidores MCP).

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

### Crear un servidor MCP personalizado

¿Quieres conectar Copilot a tus propias APIs, bases de datos o herramientas internas? Puedes crear un servidor MCP personalizado en Python. Esto es completamente opcional, ya que los servidores preconstruidos (GitHub, filesystem, Context7) cubren la mayoría de los casos de uso.

📖 Consulta la [Guía de servidor MCP personalizado](mcp-custom-server.md) para un recorrido completo usando la app del libro como ejemplo.

📚 Para más contexto, consulta el [curso MCP para principiantes](https://github.com/microsoft/mcp-for-beginners).

</details>

<a id="complete-configuration-file"></a>

### Archivo de configuración completo

Aquí tienes un `mcp-config.json` completo con servidores filesystem y Context7:

> 💡 **Nota:** GitHub MCP está integrado. No necesitas añadirlo a tu archivo de configuración.
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

Guárdalo como `~/.copilot/mcp-config.json` para acceso global o `.mcp.json` en la raíz del proyecto para configuración específica del proyecto.

---

# Uso de servidores MCP

Ahora que tienes los servidores MCP configurados, veamos lo que pueden hacer.

<img src="../../../06-mcp-servers/assets/using-mcp-servers.png" alt="Uso de servidores MCP - Diagrama hub-and-spoke que muestra un Developer CLI conectado a GitHub, Filesystem, Context7 y servidores Custom/Web Fetch" width="800" />

---

## Ejemplos de uso de servidores

**Elige un servidor para explorar, o trabájalos en orden.**

| Quiero probar... | Ir a |
|---|---|
| Repositorios de GitHub, issues y pull requests | [Servidor de GitHub](#servidor-de-github-integrado) |
| Examinar archivos del proyecto | [Uso del servidor Filesystem](#filesystem-server-usage) |
| Búsqueda de documentación de librerías | [Uso del servidor Context7](#context7-server-usage) |
| Servidor personalizado, Microsoft Learn MCP y uso de web_fetch | [Más allá de lo básico](#más-allá-de-lo-básico) |

<details>
<summary><strong>Servidor de GitHub (integrado)</strong> - Accede a repos, issues, PRs y más</summary>
<a id="github-server-built-in"></a>

### Servidor de GitHub (integrado)

El servidor MCP de GitHub está **integrado**. Si iniciaste sesión en Copilot (como lo hiciste durante la configuración inicial), ya funciona. ¡No se necesita configuración!

> 💡 **¿No funciona?** Ejecuta `/login` para volver a autenticarte con GitHub.

<details>
<summary><strong>Autenticación en contenedores de desarrollo</strong></summary>

- **GitHub Codespaces** (recomendado): La autenticación es automática. El CLI `gh` hereda tu token de Codespace. No se requiere acción.
- **Contenedor de desarrollo local (Docker)**: Ejecuta `gh auth login` después de que el contenedor arranque, y luego reinicia Copilot.

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

| Función | Ejemplo |
|---------|----------|
| **Información del repositorio** | Ver commits, ramas y colaboradores |
| **Incidencias (Issues)** | Listar, crear, buscar y comentar incidencias |
| **Pull requests** | Ver PRs, diffs, crear PRs, comprobar estado |
| **Búsqueda de código** | Buscar código a través de repositorios |
| **Acciones** | Consultar ejecuciones de workflows y su estado |

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

> 💡 **¿Trabajando en tu propio fork?** Si hiciste un fork de este repositorio del curso, también puedes probar operaciones de escritura como crear issues y pull requests. Practicaremos eso en los ejercicios abajo.

> ⚠️ **¿No ves resultados?** El MCP de GitHub opera sobre el control remoto del repositorio (en github.com), no solo sobre archivos locales. Asegúrate de que tu repo tenga un remoto: ejecuta `git remote -v` para comprobarlo.

</details>

<details>
<summary><strong>Servidor de sistema de archivos</strong> - Examina y analiza archivos del proyecto</summary>
<a id="filesystem-server-usage"></a>

### Servidor de sistema de archivos

Una vez configurado, el MCP de sistema de archivos proporciona herramientas que Copilot puede usar automáticamente:

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
<summary><strong>Servidor Context7</strong> - Consultar documentación de librerías</summary>
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
<summary><strong>Más allá de lo básico</strong> - Uso de servidor personalizado y web_fetch</summary>
<a id="beyond-the-basics-usage"></a>

### Más allá de lo básico

**Servidor MCP personalizado**: Si creaste el servidor de búsqueda de libros a partir de la [Guía de servidor MCP personalizado](mcp-custom-server.md), puedes consultar tu colección de libros directamente:

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

## Flujos de trabajo con múltiples servidores

Estas secuencias muestran por qué los desarrolladores dicen "No quiero volver a trabajar sin esto". Cada ejemplo combina múltiples servidores MCP en una sola sesión.

<img src="../../../06-mcp-servers/assets/issue-to-pr-workflow.png" alt="Flujo de trabajo Issue a PR usando MCP - Muestra el flujo completo desde obtener un issue de GitHub hasta crear un pull request" width="800"/>

*Flujo MCP completo: MCP de GitHub recupera datos del repo, MCP de Filesystem encuentra el código, MCP de Context7 proporciona mejores prácticas y Copilot realiza el análisis*

Cada ejemplo a continuación es independiente. **Elige el que te interese o léelos todos.**

| Quiero ver... | Ir a |
|---|---|
| Varios servidores trabajando juntos | [Exploración multiserver](#multi-server-exploration) |
| Ir de un issue a un PR en una sesión | [Flujo Issue-a-PR](#issue-to-pr-workflow) |
| Un chequeo rápido del estado del proyecto | [Panel de estado](#panel-de-estado-de-la-app-de-libros) |

<details>
<summary><strong>Exploración multiserver</strong> - Combina filesystem, GitHub y Context7 en una sesión</summary>
<a id="multi-server-exploration"></a>

#### Explorando la app de libros con múltiples servidores MCP

```bash
copilot

# Paso 1: Utilice el MCP del sistema de archivos para explorar la aplicación de libros
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Paso 2: Utilice el MCP de GitHub para comprobar los cambios recientes
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Paso 3: Utilice el MCP Context7 para las mejores prácticas
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Paso 4: Sintetice una recomendación
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 ¡Ve el flujo de trabajo MCP en acción!</summary>

![Demostración del flujo de trabajo MCP](../../../06-mcp-servers/assets/mcp-workflow-demo.gif)

*La salida de la demostración varía. Tu modelo, herramientas y respuestas diferirán de lo que se muestra aquí.*

</details>

**El resultado**: Exploración de código → revisión de historial → consulta de mejores prácticas → plan de mejoras. **Todo desde una sesión de terminal, usando tres servidores MCP juntos.**

</details>

<details>
<summary><strong>Flujo Issue-a-PR</strong> - Pasa de un issue de GitHub a un pull request sin salir del terminal</summary>
<a id="issue-to-pr-workflow"></a>

#### Flujo de trabajo: de issue a PR (en tu propio repositorio)

Esto funciona mejor en tu propio fork o repositorio donde tengas permisos de escritura:

> 💡 **No te preocupes si no puedes probar esto ahora mismo.** Si estás en un clon de solo lectura, practicarás esto en la asignación. Por ahora, solo léelo para entender el flujo.

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

**Cero copiar-pegar. Cero cambio de contexto. Una sola sesión de terminal.**

</details>

<details>
<summary><strong>Panel de estado</strong> - Obtén un chequeo rápido del estado del proyecto usando múltiples servidores</summary>
<a id="health-dashboard"></a>

#### Panel de estado de la app de libros

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

**El resultado**: Múltiples fuentes de datos agregadas en segundos. Manualmente, esto significaría ejecutar grep, contar líneas, revisar git log y examinar archivos de tests. Fácilmente 15+ minutos de trabajo.

</details>

---

# Práctica

<img src="../../../assets/practice.png" alt="Espacio de trabajo cálido con monitor mostrando código, lámpara, taza de café y auriculares listos para la práctica" width="800"/>

**🎉 ¡Ahora conoces lo esencial!** Entiendes MCP, has visto cómo configurar servidores y has visto flujos de trabajo reales en acción. Ahora es momento de intentarlo tú mismo.

---

## ▶️ Pruébalo tú mismo

Ahora te toca a ti. Completa estos ejercicios para practicar el uso de servidores MCP con el proyecto de la app de libros.

### Ejercicio 1: Comprueba el estado de MCP

Comienza viendo qué servidores MCP están disponibles:

```bash
copilot

> /mcp show
```

Deberías ver el servidor de GitHub listado como habilitado. Si no, ejecuta `/login` para autenticarte.

---

### Ejercicio 2: Explora la app de libros con el MCP de sistema de archivos

Si has configurado el servidor de sistema de archivos, úsalo para explorar la app de libros:

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**Resultado esperado**: Copilot lista `book_app.py`, `books.py` y `utils.py` con sus funciones.

> 💡 **¿Aún no tienes configurado el MCP de sistema de archivos?** Crea el archivo de configuración desde la sección [Configuración completa](#archivo-de-configuración-completo) más arriba. Luego reinicia Copilot.

---

### Ejercicio 3: Consulta el historial del repositorio con el MCP de GitHub

Usa el MCP de GitHub integrado para explorar este repositorio del curso:

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**Resultado esperado**: Copilot muestra mensajes de commits recientes y nombres de ramas desde el remoto de GitHub.

> ⚠️ **¿En un Codespace?** Esto funciona automáticamente. La autenticación se hereda. Si estás en un clon local, asegúrate de que `gh auth status` muestre que has iniciado sesión.

---

### Ejercicio 4: Combina varios servidores MCP

Ahora combina filesystem y GitHub MCP en una sola sesión:

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**Resultado esperado**: Copilot lee el archivo JSON (MCP de sistema de archivos), lista los 5 libros incluyendo "The Hobbit", "1984", "Dune", "To Kill a Mockingbird" y "Mysterious Book", y luego consulta GitHub para el historial de commits.

**Autoevaluación**: Entiendes MCP cuando puedes explicar por qué "Comprueba el historial de commits de mi repo" es mejor que ejecutar manualmente `git log` y pegar la salida en tu prompt.

---

## 📝 Asignación

### Desafío principal: Exploración MCP de la app de libros

Practica usar servidores MCP juntos en el proyecto de la app de libros. Completa estos pasos en una sola sesión de Copilot:

1. **Verifica que MCP funciona**: Ejecuta `/mcp show` y confirma que al menos el servidor de GitHub está habilitado
2. **Configura el MCP de sistema de archivos** (si aún no lo hiciste): Crea `~/.copilot/mcp-config.json` con la configuración del servidor de sistema de archivos
3. **Explora el código**: Pide a Copilot que use el servidor de sistema de archivos para:
   - Listar todas las funciones en `samples/book-app-project/books.py`
   - Comprobar qué funciones en `samples/book-app-project/utils.py` no tienen type hints
   - Leer `samples/book-app-project/data.json` e identificar problemas de calidad de datos (pista: mira la última entrada)
4. **Revisa la actividad del repositorio**: Pide a Copilot que use el MCP de GitHub para:
   - Listar commits recientes que afectaron archivos en `samples/book-app-project/`
   - Comprobar si hay issues o pull requests abiertos
5. **Combina servidores**: En un solo prompt, pide a Copilot que:
   - Lea el archivo de tests en `samples/book-app-project/tests/test_books.py`
   - Compare las funciones probadas con todas las funciones en `books.py`
   - Resuma qué cobertura de tests falta

**Criterios de éxito**: Puedes combinar sin problemas datos de MCP de sistema de archivos y GitHub en una sola sesión de Copilot, y puedes explicar qué aportó cada servidor MCP a la respuesta.

<details>
<summary>💡 Pistas (haz clic para ver)</summary>

**Paso 1: Verificar MCP**
```bash
copilot
> /mcp show
# Debería mostrar "github" como habilitado
# Si no, ejecuta: /login
```

**Paso 2: Crear el archivo de configuración**

Usa el JSON de la sección [Configuración completa](#archivo-de-configuración-completo) arriba y guárdalo como `~/.copilot/mcp-config.json`.

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
Un autor vacío y año 0. ¡Ese es el problema de calidad de datos!

**Paso 5: Comparación de cobertura de tests**

Los tests en `test_books.py` cubren: `add_book`, `mark_as_read`, `remove_book`, `get_unread_books` y `find_book_by_title`. Funciones como `load_books`, `save_books` y `list_books` no tienen tests directos. Las funciones CLI en `book_app.py` y los helpers en `utils.py` no tienen tests en absoluto.

**Si MCP no funciona:** Reinicia Copilot después de editar el archivo de configuración.

</details>

### Desafío extra: Construye un servidor MCP personalizado

¿Listo para profundizar? Sigue la [Guía de servidor MCP personalizado](mcp-custom-server.md) para crear tu propio servidor MCP en Python que se conecte a cualquier API.

---

<details>
<summary>🔧 <strong>Errores comunes y solución de problemas</strong> (haz clic para ver)</summary>

### Errores comunes

| Error | Qué sucede | Solución |
|---------|--------------|-----|
| No saber que el MCP de GitHub está integrado | Intentar instalar/configurar manualmente | El MCP de GitHub está incluido por defecto. Simplemente prueba: "Lista los commits recientes en este repo" |
| Buscar la configuración en la ubicación equivocada | No poder encontrar o editar la configuración de MCP | La configuración a nivel de usuario está en `~/.copilot/mcp-config.json`, la a nivel de proyecto está en `.mcp.json` en la raíz del proyecto |
| JSON inválido en el archivo de configuración | Los servidores MCP no se cargan | Usa `/mcp show` para comprobar la configuración; valida la sintaxis JSON |
| Olvidar autenticar servidores MCP | Errores de "Authentication failed" | Algunos MCP requieren autenticación separada. Revisa los requisitos de cada servidor |

### Solución de problemas

**"Servidor MCP no encontrado"** - Comprueba que:
1. El paquete npm exista: `npm view @modelcontextprotocol/server-github`
2. Tu configuración sea JSON válido
3. El nombre del servidor coincida con tu configuración

Usa `/mcp show` para ver la configuración actual.

</details>
**"Autenticación de GitHub fallida"** - El MCP de GitHub incorporado usa tus credenciales de `/login`. Prueba:

```bash
copilot
> /login
```

Esto te volverá a autenticar con GitHub. Si los problemas persisten, verifica que tu cuenta de GitHub tenga los permisos necesarios para el repositorio al que estás accediendo.

**"El servidor MCP no pudo iniciarse"** - Revisa los registros del servidor:
```bash
# Ejecute el comando del servidor manualmente para ver los errores
npx -y @modelcontextprotocol/server-github
```

**"Herramientas MCP no disponibles"** - Asegúrate de que el servidor esté habilitado:
```bash
copilot

> /mcp show
# Verificar si el servidor está listado y habilitado
```

Si un servidor está deshabilitado, consulta los [comandos adicionales `/mcp`](#-additional-mcp-commands) a continuación para saber cómo volver a habilitarlo.

</details>

---

<details>
<summary>📚 <strong>Comandos MCP adicionales</strong> (haz clic para expandir)</summary>
<a id="-additional-mcp-commands"></a>

Puedes administrar servidores MCP de dos maneras: usando **comandos slash dentro de una sesión de chat**, o usando el **comando `copilot mcp` directamente en tu terminal** (no se necesita una sesión de chat).

### Opción 1: Comandos slash (dentro de una sesión de chat)

Estos funcionan cuando ya estás dentro de `copilot`:

| Command | What It Does |
|---------|--------------|
| `/mcp show` | Muestra todos los servidores MCP configurados y su estado |
| `/mcp add` | Configuración interactiva para agregar un nuevo servidor |
| `/mcp edit <server-name>` | Editar la configuración de un servidor existente |
| `/mcp enable <server-name>` | Habilitar un servidor deshabilitado (persiste entre sesiones) |
| `/mcp disable <server-name>` | Deshabilitar un servidor (persiste entre sesiones) |
| `/mcp delete <server-name>` | Eliminar un servidor permanentemente |
| `/mcp auth <server-name>` | Reautenticar con un servidor MCP que utiliza OAuth (por ejemplo, después de cambiar de cuenta) |

### Opción 2: comando `copilot mcp` (desde tu terminal)

También puedes administrar servidores MCP directamente desde tu terminal sin iniciar primero una sesión de chat:

```bash
# Listar todos los servidores MCP configurados
copilot mcp list

# Habilitar un servidor
copilot mcp enable filesystem

# Deshabilitar un servidor
copilot mcp disable context7
```

> 💡 **¿Cuándo usar cada uno?** Usa los comandos slash `/mcp` cuando ya estés en una sesión de chat. Usa `copilot mcp` desde el terminal cuando quieras revisar o cambiar rápidamente la configuración de tus servidores antes de iniciar una sesión.

Para la mayor parte de este curso, `/mcp show` es todo lo que necesitas. Los otros comandos resultan útiles a medida que administras más servidores con el tiempo.

</details>

---

# Resumen

## 🔑 Puntos clave

1. **MCP** conecta Copilot con servicios externos (GitHub, sistema de archivos, documentación)
2. **GitHub MCP está integrado** - no se necesita configuración, solo `/login`
3. **Sistema de archivos y Context7** se configuran a través de `~/.copilot/mcp-config.json`
4. **Los flujos de trabajo multi-servidor** combinan datos de múltiples fuentes en una sola sesión
5. **Gestiona servidores de dos maneras**: usa los comandos slash `/mcp` dentro del chat, o `copilot mcp` desde el terminal
6. **Los servidores personalizados** te permiten conectar cualquier API (opcional, cubierto en la guía del apéndice)

> 📋 **Referencia rápida**: Consulta la [referencia de comandos de la CLI de GitHub Copilot](https://docs.github.com/en/copilot/reference/cli-command-reference) para obtener la lista completa de comandos y atajos.

---

## ➡️ ¿Qué sigue?

Ahora tienes todos los bloques de construcción: modos, contexto, flujos de trabajo, agentes, habilidades y MCP. Es hora de unirlos todos.

En **[Capítulo 07: Poniéndolo todo junto](../07-putting-it-together/README.md)**, aprenderás:

- Combinar agentes, habilidades y MCP en flujos de trabajo unificados
- Desarrollo completo de funcionalidades desde la idea hasta el PR fusionado
- Automatización con hooks
- Mejores prácticas para entornos de equipo

---

**[← Volver al Capítulo 05](../05-skills/README.md)** | **[Continuar al Capítulo 07 →](../07-putting-it-together/README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->