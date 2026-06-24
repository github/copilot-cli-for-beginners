# Código fuente de ejemplo (Legado - Referencia opcional)

> **Nota**: La muestra principal para este curso es la **aplicación de colección de libros en Python** en `../book-app-project/`. Estos archivos JS/React son de una versión anterior del curso y se mantienen como material de referencia opcional adicional para estudiantes que quieran ejemplos en JS.

Esta carpeta contiene archivos fuente de ejemplo. Estos son solo ejemplos y no están destinados a ser una aplicación completamente operativa.

## Estructura

```
src/
├── api/           # API route handlers
│   ├── auth.js    # Authentication endpoints
│   └── users.js   # User CRUD endpoints
├── auth/          # Client-side auth handlers
│   ├── login.js   # Login form logic
│   └── register.js # Registration form logic
├── components/    # React components
│   ├── Button.jsx # Reusable button
│   └── Header.jsx # App header with nav
├── models/        # Data models
│   └── User.js    # User model
├── services/      # Business logic
│   ├── productService.js
│   └── userService.js
├── utils/         # Helper functions
│   └── helpers.js
├── index.js       # App entry point
└── refactor-me.js # Beginner refactoring practice (Chapter 03)
```

## Uso

Estos archivos se referencian en los ejemplos del curso usando la sintaxis `@`:

```bash
copilot

> Explain what @samples/src/utils/helpers.js does
> Review @samples/src/api/ for security issues
> Compare @samples/src/auth/login.js and @samples/src/auth/register.js
```

## Práctica de refactorización

El archivo `refactor-me.js` está específicamente diseñado para los ejercicios de refactorización del Capítulo 03:

```bash
copilot

> @samples/src/refactor-me.js Rename the variable 'x' to something more descriptive
> @samples/src/refactor-me.js This function is too long. Split it into smaller functions.
> @samples/src/refactor-me.js Remove any unused variables
```

## Notas

- Los archivos contienen TODOs intencionales y problemas menores para que Copilot los encuentre durante las revisiones
- Este es código de demostración que no está diseñado para ejecutarse realmente. NO apto para producción
- Usado para aprender la sintaxis de referencia de archivos `@`

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->