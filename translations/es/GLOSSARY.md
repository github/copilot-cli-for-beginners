# Glosario

Referencia rápida para términos técnicos usados a lo largo de este curso. No te preocupes por memorizarlos ahora - consúltalos según sea necesario.

---

## A

### Agente

Una personalidad de IA especializada con experiencia en un dominio (p. ej., frontend, seguridad). Definida en archivos `.agent.md` con frontmatter YAML que contienen al menos un campo `description`.

### API

Interfaz de Programación de Aplicaciones. Una forma para que los programas se comuniquen entre sí.

---

## C

### CI/CD

Integración Continua/Despliegue Continuo. Canalizaciones automatizadas de pruebas y despliegue.

### CLI

Interfaz de Línea de Comandos. Una forma basada en texto de interactuar con el software (¡como esta herramienta!).

### Ventana de contexto

La cantidad de texto que una IA puede considerar a la vez. Como un escritorio que solo puede contener tanto. Cuando agregas archivos, historial de conversaciones y mensajes del sistema, todos ocupan espacio en esta ventana.

### Administrador de contexto

Una construcción de Python que usa la sentencia `with` que maneja automáticamente la preparación y la limpieza (como abrir y cerrar archivos). Ejemplo: `with open("file.txt") as f:` garantiza que el archivo se cierre incluso si ocurre un error.

### Commit convencional

Un formato de mensaje de commit que sigue una estructura estandarizada: `type(scope): description`. Los tipos comunes incluyen `feat` (nueva característica), `fix` (corrección de errores), `docs` (documentación), `refactor`, y `test`. Ejemplo: `feat(auth): add password reset flow`.

### Dataclass

Un decorador de Python (`@dataclass`) que genera automáticamente `__init__`, `__repr__`, y otros métodos para clases que almacenan principalmente datos. Usado en la aplicación del libro para definir la clase `Book` con campos como `title`, `author`, `year`, y `read`.

---

## F

### Frontmatter

Metadatos en la parte superior de un archivo Markdown encerrados entre delimitadores `---`. Usados en archivos de agent y skill para definir propiedades como `description` y `name` en formato YAML.

---

## G

### Patrón Glob

Un patrón que utiliza comodines para coincidir con rutas de archivos (p. ej., `*.py` coincide con todos los archivos Python, `*.js` coincide con todos los archivos JavaScript).

---

## J

### JWT

JSON Web Token. Una forma segura de transmitir información de autenticación entre sistemas.

---

## M

### MCP

Model Context Protocol. Un estándar para conectar asistentes de IA a fuentes de datos externas.

---

### Memoria (Copilot CLI)

Una característica que permite a Copilot CLI recordar hechos y preferencias *a través de todas las sesiones*, no solo dentro de una sola. A diferencia del historial de sesión (que guarda una conversación específica), la memoria persiste globalmente y se aplica automáticamente en sesiones futuras. Se gestiona con el comando slash `/memory` (`/memory on`, `/memory off`, `/memory show`). La memoria puede limitarse a tu cuenta de usuario (visible en todos los repositorios) o a un repositorio específico (compartida con colaboradores).

---

## N

### npx

Una herramienta de Node.js que ejecuta paquetes npm sin instalarlos globalmente. Usada en configuraciones de servidor MCP para lanzar servidores (p. ej., `npx @modelcontextprotocol/server-filesystem`).

---

## O

### OWASP

Open Web Application Security Project. Una organización que publica buenas prácticas de seguridad y mantiene la lista "OWASP Top 10" de los riesgos de seguridad de aplicaciones web más críticos.

---

## P

### PEP 8

Python Enhancement Proposal 8. La guía de estilo oficial para el código Python, que abarca convenciones de nomenclatura (snake_case para funciones, PascalCase para clases), indentación (4 espacios) y disposición del código. Seguir PEP 8 hace que el código Python sea consistente y legible.

### Pre-commit Hook

Un script que se ejecuta automáticamente antes de cada `git commit`. Puede usarse para ejecutar revisiones de seguridad de Copilot o comprobaciones de calidad de código antes de que el código se confirme.

### pytest

Un popular framework de pruebas para Python conocido por su sintaxis sencilla, potentes fixtures y un ecosistema de plugins rico. Usado a lo largo de este curso para probar la aplicación del libro. Las pruebas se ejecutan con `python -m pytest tests/`.

### Programmatic Mode

Ejecutar Copilot con la bandera `-p` para comandos únicos sin interacción.

---

## R

### Rate Limiting

Restricciones sobre cuántas solicitudes puedes realizar a una API dentro de un período de tiempo. Copilot puede limitar temporalmente las respuestas si excedes la cuota de uso de tu plan.

---

## S

### Session

Una conversación con Copilot que mantiene contexto y puede reanudarse más tarde.

### Skill

Una carpeta con instrucciones que Copilot carga automáticamente cuando son relevantes para tu solicitud. Definidas en archivos `SKILL.md` con frontmatter YAML.

### Slash Command

Comandos que comienzan con `/` que controlan Copilot (p. ej., `/help`, `/clear`, `/model`).

---

## T

### Token

Una unidad de texto que los modelos de IA procesan. Aproximadamente 4 caracteres o 0,75 palabras. Se usa para medir tanto la entrada (tus prompts y contexto) como la salida (respuestas de la IA).

### Type Hints

Anotaciones de Python que indican los tipos esperados de los parámetros de función y los valores de retorno (p. ej., `def add_book(title: str, year: int) -> Book:`). No imponen tipos en tiempo de ejecución pero ayudan con la claridad del código, el soporte de IDE y herramientas de análisis estático como mypy.

---

## W

### WCAG

Web Content Accessibility Guidelines. Estándares publicados por el W3C para hacer el contenido web accesible a personas con discapacidades. WCAG 2.1 AA es un objetivo de cumplimiento común.

---

## Y

### YAML

YAML Ain't Markup Language. Un formato de datos legible por humanos usado para configuración. En este curso, YAML aparece en el frontmatter de agent y skill (el bloque delimitado por `---` en la parte superior de los archivos `.agent.md` y `SKILL.md`).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->