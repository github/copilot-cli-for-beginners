# Características adicionales de contexto

> 📖 **Requisito previo**: Completa el [Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md) antes de leer este apéndice.

Este apéndice cubre dos características adicionales de contexto: trabajar con imágenes y gestionar permisos en múltiples directorios.

---

## Trabajar con imágenes

Puedes incluir imágenes en tus conversaciones usando la sintaxis `@`. Copilot puede analizar capturas de pantalla, maquetas, diagramas y otro contenido visual.

### Referencia básica de imagen

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analyzes the image and responds

> @mockup.png @current-design.png Compare these two designs

# You can also drag and drop images or paste from clipboard
```

### Formatos de imagen compatibles

| Formato | Ideal para |
|---------|-----------|
| PNG | Capturas de pantalla, maquetas de UI, diagramas |
| JPG/JPEG | Fotos, imágenes complejas |
| GIF | Diagramas simples (solo el primer fotograma) |
| WebP | Capturas de pantalla web |

### Casos de uso prácticos para imágenes

**1. Depuración de UI**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. Implementación de diseño**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. Análisis de errores**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. Revisión de arquitectura**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. Comparación antes/después**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### Combinar imágenes con código

Las imágenes se vuelven aún más poderosas cuando se combinan con contexto de código:

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### Consejos para imágenes

- **Recorta las capturas de pantalla** para mostrar solo las partes relevantes (ahorra tokens de contexto)
- **Usa alto contraste** para los elementos de UI que quieres analizar
- **Anota si es necesario**: rodea con un círculo o resalta las áreas problemáticas antes de subir
- **Una imagen por concepto**: múltiples imágenes funcionan, pero sé específico

---

## Patrones de permisos

Por defecto, Copilot puede acceder a los archivos del directorio actual. Para archivos en otras ubicaciones, necesitas conceder acceso.

### Añadir directorios

```bash
# Add a directory to the allowed list
copilot --add-dir /path/to/other/project

# Add multiple directories
copilot --add-dir ~/workspace --add-dir /tmp
```

### Permitir todas las rutas

```bash
# Disable path restrictions entirely (use with caution)
copilot --allow-all-paths
```

### Dentro de una sesión

```bash
copilot

> /add-dir /path/to/other/project
# Now you can reference files from that directory

> /list-dirs
# See all allowed directories

> /yolo
# Quick alias for /allow-all on — auto-approves all permission prompts
```

### Para automatización

```bash
# Allow all permissions for non-interactive scripts
copilot -p "Review @src/" --allow-all

# Or use the memorable alias
copilot -p "Review @src/" --yolo
```

### Cuándo necesitas acceso a múltiples directorios

Escenarios comunes donde necesitarás estos permisos:

1. **Trabajo en monorepo**: Comparar código entre paquetes
2. **Refactorización entre proyectos**: Actualizar bibliotecas compartidas
3. **Proyectos de documentación**: Referenciar múltiples bases de código
4. **Trabajo de migración**: Comparar implementaciones antiguas y nuevas

---

[**← Volver al Capítulo 02**](../02-context-conversations/README.md) | [**Volver a los apéndices**](README.md)
