# Habilidades de ejemplo

Plantillas de habilidades listas para usar para GitHub Copilot CLI. Copia cualquier carpeta de habilidades para empezar a usarla de inmediato.

## Inicio rápido

```bash
# Copiar una habilidad a tu carpeta personal de habilidades
cp -r hello-world ~/.copilot/skills/

# O copiar a tu proyecto para compartir con el equipo
cp -r code-checklist .github/skills/
```

## Habilidades disponibles

| Habilidad | Descripción | Ideal para |
|-------|-------------|----------|
| `hello-world` | Ejemplo mínimo (aprender el formato) | Creadores de skills primerizos |
| `code-checklist` | Lista de verificación de calidad de código en Python (PEP 8, anotaciones de tipo, validación) | Comprobaciones de calidad consistentes |
| `pytest-gen` | Generar pruebas exhaustivas con pytest | Generación de pruebas estructurada |
| `commit-message` | Mensajes de commit convencionales | Historial de git estandarizado |

## Cómo funcionan las habilidades

Las habilidades se activan **automáticamente** cuando tu prompt coincide con el campo `description` de la skill. No necesitas invocarlas manualmente.

```bash
copilot

> Check this code for quality issues
# Copilot detecta que esto coincide con la skill "code-checklist" y la carga automáticamente

> Generate a commit message
# Copilot carga la skill "commit-message"
```

También puedes invocar las habilidades directamente:
```bash
> /code-checklist Check books.py
> /pytest-gen Generate tests for BookCollection
> /commit-message
```

## Estructura de la skill

Cada skill es una carpeta que contiene un archivo `SKILL.md`:

```
skill-name/
└── SKILL.md    # Required: Contains frontmatter + instructions
```

El archivo `SKILL.md` tiene un frontmatter YAML con `name` y `description` (ambos obligatorios):

```markdown
---
name: my-skill
description: What this skill does and when to use it
---

# Skill Instructions

Your instructions here...
```

## Encontrar más habilidades

- **[github/awesome-copilot](https://github.com/github/awesome-copilot)** - Recursos oficiales de GitHub con skills de la comunidad
- **`/plugin marketplace`** - Explora e instala skills desde Copilot CLI

## Crear la tuya

1. Crea una carpeta: `mkdir ~/.copilot/skills/my-skill`
2. Crea `SKILL.md` con frontmatter
3. Agrega tus instrucciones
4. Prueba pidiéndole a Copilot algo que coincida con tu descripción

Consulta [Capítulo 05: Habilidades](../../05-skills/README.md) para obtener una guía detallada.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->