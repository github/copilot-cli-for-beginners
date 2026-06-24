# Definiciones de agentes de ejemplo

Esta carpeta contiene algunas plantillas de agente simples para GitHub Copilot CLI pensadas para ayudarte a empezar a usar agentes.

## Inicio rápido

```bash
# Copia un agente en tu carpeta personal de agentes
cp hello-world.agent.md ~/.copilot/agents/

# O cópialo en tu proyecto para compartirlo con el equipo
cp python-reviewer.agent.md .github/agents/
```

## Archivos de ejemplo en esta carpeta

| Archivo | Descripción | Ideal para |
|------|-------------|----------|
| `hello-world.agent.md` | Ejemplo mínimo (11 líneas) | Aprender el formato |
| `python-reviewer.agent.md` | Revisor de calidad de código Python | Revisiones de código, PEP 8, sugerencias de tipos |
| `pytest-helper.agent.md` | Especialista en pruebas Pytest | Generación de pruebas, fixtures, casos límite |

## Encontrar más agentes

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - Recursos oficiales de GitHub con agentes comunitarios e instrucciones

---

## Formato de archivo de agente

Cada archivo de agente requiere frontmatter YAML con al menos un campo `description`:

```markdown
---
name: my-agent
description: Brief description of what this agent does
tools: ["read", "edit", "search"]  # Optional: limit available tools
---

# Agent Name

Agent instructions go here...
```

**Propiedades YAML disponibles:**

| Propiedad | Requerido | Descripción |
|----------|----------|-------------|
| `description` | **Sí** | Lo que hace el agente |
| `name` | No | Nombre para mostrar (por defecto, el nombre del archivo) |
| `tools` | No | Lista de herramientas permitidas (omitir = todas). Ver alias abajo. |
| `target` | No | Limitar a `vscode` o `github-copilot` únicamente |

**Alias de herramientas**: `read`, `edit`, `search`, `execute` (shell), `web`, `agent`

> 💡 **Nota**: La propiedad `model` funciona en VS Code pero aún no es compatible con Copilot CLI.
>
> 📖 **Documentación oficial**: [Configuración de agentes personalizados](https://docs.github.com/copilot/reference/custom-agents-configuration)

## Ubicaciones de archivos de agentes

Los agentes pueden almacenarse en:
- `~/.copilot/agents/` - Agentes globales disponibles en todos los proyectos
- `.github/agents/` - Agentes específicos del proyecto
- `.agent.md` files - Formato compatible con VS Code

Cada agente es un archivo separado con la extensión `.agent.md`.

---

## Ejemplos de uso

```bash
# Comienza con un agente específico
copilot --agent python-reviewer

# O selecciona un agente de forma interactiva durante una sesión
copilot
> /agent
# Selecciona "python-reviewer" de la lista

# La experiencia del agente se aplica a tus solicitudes
> @samples/book-app-project/books.py Review this code for quality issues

# Cambia a un agente diferente
> /agent
# Selecciona "pytest-helper"

> @samples/book-app-project/tests/test_books.py What additional tests should we add?
```

---

## Crear tus propios agentes

1. Crea un nuevo archivo en `~/.copilot/agents/` con la extensión `.agent.md`
2. Añade frontmatter YAML con al menos un campo `description`
3. Añade un encabezado descriptivo (p. ej., `# Security Agent`)
4. Define la experiencia, estándares y comportamientos del agente
5. Usa el agente con `/agent` o `--agent <name>`

**Consejos para agentes efectivos:**
- Sé específico sobre las áreas de experiencia
- Incluye estándares y patrones de código
- Define qué comprueba el agente
- Incluye preferencias de formato de salida

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->