---
name: code-checklist
description: Lista de verificación de calidad de código del equipo - usar para comprobar
  la calidad del código Python, errores, problemas de seguridad y mejores prácticas
---
# Lista de verificación de código

Aplica esta lista de verificación al revisar código Python.

## Lista de verificación de calidad de código

- [ ] Todas las funciones tienen anotaciones de tipo
- [ ] No hay cláusulas except sin especificar
- [ ] No hay argumentos por defecto mutables
- [ ] Se usan gestores de contexto para E/S de archivos
- [ ] Las funciones tienen menos de 50 líneas
- [ ] Los nombres de variables y funciones siguen PEP 8 (snake_case)

## Lista de verificación de validación de entrada

- [ ] La entrada del usuario se valida antes de procesarla
- [ ] Se manejan casos límite (cadenas vacías, None, valores fuera de rango)
- [ ] Los mensajes de error son claros y útiles

## Lista de verificación de pruebas

- [ ] El código nuevo tiene pruebas correspondientes con pytest
- [ ] Se cubren los casos límite
- [ ] Las pruebas usan nombres descriptivos

## Formato de salida

Presenta los hallazgos como:

```
## Code Checklist: [filename]

### Code Quality
- [PASS/FAIL] Description of finding

### Input Validation
- [PASS/FAIL] Description of finding

### Testing
- [PASS/FAIL] Description of finding

### Summary
[X] items need attention before merge
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->