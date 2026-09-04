# AGENTS.md

Curso pensado para principiantes que enseña GitHub Copilot CLI. Contenido educativo, no software.

## Estructura

| Path | Purpose |
|------|---------|
| `00-07/` | Capítulos: analogía → conceptos → práctico → tarea → siguiente |
| `samples/book-app-project/` | **Ejemplo principal**: Aplicación CLI en Python para gestionar una colección de libros usada a lo largo de todos los capítulos |
| `samples/book-app-project-cs/` | Versión en C# de la aplicación de colección de libros |
| `samples/book-app-project-js/` | Versión en JavaScript de la aplicación de colección de libros |
| `samples/book-app-buggy/` | **Errores intencionados** para ejercicios de depuración (Cap. 03) |
| `samples/agents/` | Ejemplos de plantillas de agentes (python-reviewer, pytest-helper, hello-world) |
| `samples/skills/` | Ejemplos de plantillas de skills (code-checklist, pytest-gen, commit-message, hello-world) |
| `samples/mcp-configs/` | Ejemplos de configuración del servidor MCP |
| `samples/buggy-code/` | **Extra opcional**: Código con errores centrado en seguridad (JS y Python) |
| `samples/src/` | **Extra opcional**: Ejemplos heredados de JS/React de una versión anterior del curso |
| `appendices/` | Material de referencia complementario |

## Hacer

- Mantener las explicaciones aptas para principiantes; explicar la jerga de IA/ML cuando se use
- Asegurarse de que los ejemplos de bash estén listos para copiar y pegar
- Tono: amistoso, alentador, práctico
- Usar `samples/book-app-project/` paths en todos los ejemplos principales
- Usar el contexto de Python/pytest para los ejemplos de código

## No hacer

- No arreglar errores en `samples/book-app-buggy/` o `samples/buggy-code/` — son intencionales
- No añadir capítulos sin actualizar README.md (tabla del curso)
- No asumir que los lectores conocen la terminología de IA/ML

## Compilar

```bash
npm install && npm run release
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->