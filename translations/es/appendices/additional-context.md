# Características adicionales de contexto

> 📖 **Requisito previo**: Completa [Capítulo 02: Contexto y conversaciones](../02-context-conversations/README.md) antes de leer este apéndice.

Este apéndice cubre dos características adicionales de contexto: trabajar con imágenes y gestionar permisos en múltiples directorios.

---

## Trabajar con imágenes

Puedes incluir imágenes en tus conversaciones usando la sintaxis `@`. Copilot puede analizar capturas de pantalla, maquetas, diagramas y otro contenido visual.

### Referencia básica de imagen

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analiza la imagen y responde

> @mockup.png @current-design.png Compare these two designs

# También puedes arrastrar y soltar imágenes o pegar desde el portapapeles
```

### Formatos de imagen compatibles

| Format | Best For |
|--------|----------|
| PNG | Capturas de pantalla, maquetas de UI, diagramas |
| JPG/JPEG | Fotos, imágenes complejas |
| GIF | Diagramas simples (solo primer fotograma) |
| WebP | Capturas de pantalla web |

### Casos prácticos de uso de imágenes

**1. Depuración de IU**
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

### Consejos sobre imágenes

- **Recorta las capturas de pantalla** para mostrar solo las porciones relevantes (ahorra tokens de contexto)
- **Usa alto contraste** para los elementos de la interfaz que quieres analizar
- **Anota si es necesario** - circunda o resalta las áreas problemáticas antes de subir
- **Una imagen por concepto** - varias imágenes funcionan, pero mantente enfocado

---

## Patrones de permisos

Por defecto, Copilot puede acceder a archivos en tu directorio actual. Para archivos en otras ubicaciones, necesitas otorgar acceso.

### Agregar directorios

```bash
# Agregar un directorio a la lista permitida
copilot --add-dir /path/to/other/project

# Agregar varios directorios
copilot --add-dir ~/workspace --add-dir /tmp
```

### Permitir todas las rutas

```bash
# Desactivar por completo las restricciones de rutas (usar con precaución)
copilot --allow-all-paths
```

### Dentro de una sesión

```bash
copilot

> /add-dir /path/to/other/project
# Ahora puedes hacer referencia a archivos de ese directorio

> /list-dirs
# Ver todos los directorios permitidos

> /yolo
# Alias rápido para /allow-all activado — aprueba automáticamente todas las solicitudes de permiso
```

### Para automatización

```bash
# Permitir todos los permisos para scripts no interactivos
copilot -p "Review @src/" --allow-all

# O usa el alias memorable
copilot -p "Review @src/" --yolo
```

### Cuando necesitas acceso a múltiples directorios

Escenarios comunes donde necesitarás estos permisos:

1. **Trabajo en monorepo** - Comparando código entre paquetes
2. **Refactorización entre proyectos** - Actualizando bibliotecas compartidas
3. **Proyectos de documentación** - Referenciando múltiples bases de código
4. **Trabajo de migración** - Comparando implementaciones antiguas y nuevas

---

**[← Volver al Capítulo 02](../02-context-conversations/README.md)** | **[Volver a los apéndices](README.md)**

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->