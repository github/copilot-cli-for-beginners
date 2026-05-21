# Sample Agent Definitions

This folder contains some simple agent templates for GitHub Copilot CLI intended to help you get started using agents.

## Quick Start

```bash
# Copia un agente en tu carpeta personal de agentes
cp hello-world.agent.md ~/.copilot/agents/

# O cópialo en tu proyecto para compartirlo con el equipo
cp python-reviewer.agent.md .github/agents/
```

## Sample Files in This Folder

| File | Description | Best For |
|------|-------------|----------|
| `hello-world.agent.md` | Minimal example (11 lines) | Learning the format |
| `python-reviewer.agent.md` | Python code quality reviewer | Code reviews, PEP 8, type hints |
| `pytest-helper.agent.md` | Pytest testing specialist | Test generation, fixtures, edge cases |

## Finding More Agents

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - Recursos oficiales de GitHub con agentes comunitarios e instrucciones

---

## Agent File Format

Each agent file requires YAML frontmatter with at least a `description` field:

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

| Property | Required | Description |
|----------|----------|-------------|
| `description` | **Sí** | Lo que hace el agente |
| `name` | No | Nombre a mostrar (por defecto, el nombre de archivo) |
| `tools` | No | Lista de herramientas permitidas (omitir = todas). Ver alias abajo. |
| `target` | No | Limitar solo a `vscode` o `github-copilot` |

**Alias de herramientas**: `read`, `edit`, `search`, `execute` (shell), `web`, `agent`

> 💡 **Nota**: La propiedad `model` funciona en VS Code pero aún no es compatible con Copilot CLI.
>
> 📖 **Documentación oficial**: [Configuración de agentes personalizados](https://docs.github.com/copilot/reference/custom-agents-configuration)

## Agent File Locations

Los agentes pueden almacenarse en:
- `~/.copilot/agents/` - Agentes globales disponibles en todos los proyectos
- `.github/agents/` - Agentes específicos del proyecto
- `.agent.md` archivos - Formato compatible con VS Code

Each agent is a separate file with the `.agent.md` extension.

---

## Usage Examples

```bash
# Comienza con un agente específico
copilot --agent python-reviewer

# O selecciona un agente de forma interactiva durante una sesión
copilot
> /agent
# Selecciona "python-reviewer" de la lista

# La experiencia del agente se aplica a tus indicaciones
> @samples/book-app-project/books.py Review this code for quality issues

# Cambia a un agente diferente
> /agent
# Selecciona "pytest-helper"

> @samples/book-app-project/tests/test_books.py What additional tests should we add?
```

---

## Creating Your Own Agents

1. Create a new file in `~/.copilot/agents/` with `.agent.md` extension
2. Add YAML frontmatter with at least a `description` field
3. Add a descriptive header (e.g., `# Security Agent`)
4. Define the agent's expertise, standards, and behaviors
5. Use the agent with `/agent` or `--agent <name>`

**Consejos para agentes efectivos:**
- Sé específico respecto a las áreas de especialización
- Incluye estándares y patrones de código
- Define qué debe comprobar el agente
- Incluye preferencias del formato de salida

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->