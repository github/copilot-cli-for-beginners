# AGENTS.md

Curso amigable para principiantes que enseña GitHub Copilot CLI. Contenido educativo, no software.

## Estructura

| Path | Propósito |
|------|---------|
| `00-07/` | Capítulos: analogía → conceptos → práctico → tarea → siguiente |
| `samples/book-app-project/` | **Muestra principal**: Aplicación CLI en Python para colección de libros utilizada en todos los capítulos |
| `samples/book-app-project-cs/` | Versión en C# de la aplicación de colección de libros |
| `samples/book-app-project-js/` | Versión en JavaScript de la aplicación de colección de libros |
| `samples/book-app-buggy/` | **Errores intencionales** para ejercicios de depuración (Ch 03) |
| `samples/agents/` | Ejemplos de plantillas de agentes (python-reviewer, pytest-helper, hello-world) |
| `samples/skills/` | Ejemplos de plantillas de skills (code-checklist, pytest-gen, commit-message, hello-world) |
| `samples/mcp-configs/` | Ejemplos de configuración del servidor MCP |
| `samples/buggy-code/` | **Extra opcional**: Código con errores enfocado en seguridad (JS y Python) |
| `samples/src/` | **Extra opcional**: Ejemplos heredados de JS/React de una versión anterior del curso |
| `appendices/` | Material de referencia suplementario |

## Hacer

- Mantén las explicaciones aptas para principiantes; explica la jerga de IA/ML cuando se use
- Asegúrate de que los ejemplos de bash estén listos para copiar y pegar
- Tono: amigable, alentador, práctico
- Usa las rutas `samples/book-app-project/` en todos los ejemplos principales
- Usa el contexto Python/pytest para los ejemplos de código

## No

- No arregles los errores en `samples/book-app-buggy/` o `samples/buggy-code/` — son intencionales
- No añadas capítulos sin actualizar la tabla del curso en README.md
- No asumas que los lectores conocen la terminología de IA/ML

## Construir

```bash
npm install && npm run release
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->