---
name: commit-message
description: Generar mensajes de commit convencionales - usar al crear commits, escribir
  mensajes de commit o al pedir ayuda con commits de git
---
# Habilidad de mensajes de commit

Genera mensajes de commit siguiendo la especificación Conventional Commits.

## Formato

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Tipos

| Tipo | Cuándo usar |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de errores |
| `docs` | Solo documentación |
| `style` | Formateo (sin cambios en el código) |
| `refactor` | Cambio de código que no corrige ni añade |
| `perf` | Mejora de rendimiento |
| `test` | Añadir o actualizar pruebas |
| `chore` | Tareas de mantenimiento |

## Reglas

1. Línea de asunto de máximo 72 caracteres
2. Usa el modo imperativo ("add" en vez de "added" o "adds")
3. No usar punto al final de la línea de asunto
4. Separa el asunto del cuerpo con una línea en blanco
5. El cuerpo explica **qué** y **por qué**, no cómo

## Ejemplos

Simple:
```
fix(auth): prevent redirect loop on expired sessions
```

Con cuerpo:
```
feat(api): add rate limiting to public endpoints

- Limits requests to 100/minute per IP
- Returns 429 status with retry-after header
- Configurable via RATE_LIMIT_MAX env variable

Closes #234
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->