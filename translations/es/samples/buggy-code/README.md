# Ejemplos de Código con Errores

Esta carpeta contiene código intencionalmente defectuoso para practicar la revisión de código y la depuración con GitHub Copilot CLI.

## Estructura de Carpetas

```
buggy-code/
├── js/                    # JavaScript examples
│   ├── userService.js     # User management with 8 bugs
│   └── paymentProcessor.js # Payment handling with 8 bugs
└── python/                # Python examples
    ├── user_service.py    # User management with 10 bugs
    └── payment_processor.py # Payment handling with 12 bugs
```

## Inicio Rápido

### JavaScript

```bash
copilot

# Auditoría de seguridad
> Review @samples/buggy-code/js/userService.js for security issues

# Encontrar todos los errores
> Find all bugs in @samples/buggy-code/js/paymentProcessor.js
```

### Python

```bash
copilot

# Auditoría de seguridad
> Review @samples/buggy-code/python/user_service.py for security issues

# Encuentra todos los errores
> Find all bugs in @samples/buggy-code/python/payment_processor.py
```

## Categorías de Errores

### Comunes a Ambos Lenguajes

| Tipo de Bug | Descripción |
|----------|-------------|
| Inyección SQL | Entrada de usuario incluida directamente en consultas SQL |
| Secretos incrustados | Claves API y contraseñas en el código fuente |
| Condiciones de carrera | Estado compartido sin sincronización adecuada |
| Registro de datos sensibles | Contraseñas y números de tarjeta en los registros |
| Falta de validación de entrada | Sin comprobaciones sobre datos proporcionados por el usuario |
| Sin manejo de errores | Faltan bloques try/catch o try/except |
| Comparación de contraseñas débil | Comparaciones en texto plano o vulnerables a ataques por temporización |
| Falta de comprobaciones de autorización | Operaciones sin verificación de autorización |

### Bugs específicos de Python

| Tipo de Bug | Descripción |
|----------|-------------|
| Deserialización con pickle | `pickle.loads()` en datos no confiables |
| Inyección con eval() | Entrada de usuario pasada a `eval()` |
| Carga insegura de YAML | `yaml.load()` sin un cargador seguro |
| Inyección de shell | Entrada de usuario en llamadas a `os.system()` |
| Hash débil | MD5 para el hash de contraseñas |
| Random inseguro | Módulo `random` para propósitos de seguridad |

## Ejercicios Prácticos

1. **Auditoría de Seguridad**: Ejecuta una revisión de seguridad completa y enumera todas las vulnerabilidades por severidad
2. **Corregir un bug**: Elige un bug crítico, obtén la solución de Copilot, comprende por qué funciona
3. **Generar pruebas**: Crea pruebas que detecten estos errores antes del despliegue
4. **Refactorizar de forma segura**: Arregla los bugs de inyección SQL manteniendo la funcionalidad

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->