<!--
---
id: CopilotCLI-Appendix-Additional-Context
title: !translate Additional Context Features
description: !translate Learn how to use image context and manage permissions across multiple directories in GitHub Copilot CLI.
audience: Developers / Students / Terminal users
slug: additional-context-features
weight: 92
---
-->

# Additional Context Features

> 📖 **Prerequisito**: Completa [Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md) antes de leer este apéndice.

Este apéndice cubre dos características adicionales de contexto: trabajar con imágenes y gestionar permisos en múltiples directorios.

---

## Working with Images

Puedes incluir imágenes en tus conversaciones usando la sintaxis `@`. Copilot puede analizar capturas de pantalla, maquetas, diagramas y otro contenido visual.

### Basic Image Reference

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analiza la imagen y responde

> @mockup.png @current-design.png Compare these two designs

# También puedes arrastrar y soltar imágenes o pegar desde el portapapeles
```

### Supported Image Formats

| Format | Best For |
|--------|----------|
| PNG | Screenshots, UI mockups, diagrams |
| JPG/JPEG | Photos, complex images |
| GIF | Simple diagrams (first frame only) |
| WebP | Web screenshots |

### Practical Image Use Cases

**1. UI Debugging**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. Design Implementation**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. Error Analysis**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. Architecture Review**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. Before/After Comparison**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### Combining Images with Code

Las imágenes son aún más potentes cuando se combinan con el contexto de código:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### Image Tips

- **Recorta las capturas de pantalla** para mostrar solo las porciones relevantes (ahorra tokens de contexto)
- **Usa alto contraste** para los elementos de la interfaz que quieras analizar
- **Anota si es necesario** - rodea o resalta las áreas problemáticas antes de subir
- **Una imagen por concepto** - varias imágenes funcionan, pero mantente enfocado

---

## Permission Patterns

De forma predeterminada, Copilot puede acceder a los archivos en tu directorio actual. Para archivos en otras ubicaciones, necesitas otorgar acceso.

### Add Directories

```bash
# Agregar un directorio a la lista permitida
copilot --add-dir /path/to/other/project

# Agregar varios directorios
copilot --add-dir ~/workspace --add-dir /tmp
```

### Allow All Paths

```bash
# Deshabilitar por completo las restricciones de ruta (usar con precaución)
copilot --allow-all-paths
```

### Inside a Session

```bash
copilot

> /add-dir /path/to/other/project
# Ahora puedes hacer referencia a archivos desde ese directorio

> /list-dirs
# Ver todos los directorios permitidos

> /yolo
# Alias rápido para /allow-all activado — aprueba automáticamente todas las solicitudes de permisos
```

### For Automation

```bash
# Permitir todos los permisos para scripts no interactivos
copilot -p "Review @src/" --allow-all

# O usa el alias memorable
copilot -p "Review @src/" --yolo
```

### When You Need Multi-Directory Access

Escenarios comunes en los que necesitarás estos permisos:

1. **Monorepo work** - Comparing code across packages
2. **Cross-project refactoring** - Updating shared libraries
3. **Documentation projects** - Referencing multiple codebases
4. **Migration work** - Comparing old and new implementations

---

**[← Volver al Capítulo 02](../02-context-conversations/README.md)** | **[Volver a los apéndices](README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->