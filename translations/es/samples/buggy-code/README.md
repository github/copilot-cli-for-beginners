# Ejemplos de código con errores

Esta carpeta contiene código con errores intencionales para practicar revisión de código y depuración con GitHub Copilot CLI.

## Estructura de la carpeta

```
buggy-code/
├── js/                    # JavaScript examples
│   ├── userService.js     # User management with 8 bugs
│   └── paymentProcessor.js # Payment handling with 8 bugs
└── python/                # Python examples
    ├── user_service.py    # User management with 10 bugs
    └── payment_processor.py # Payment handling with 12 bugs
```

## Inicio rápido

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

# Encontrar todos los errores
> Find all bugs in @samples/buggy-code/python/payment_processor.py
```

## Categorías de errores

### Común a ambos lenguajes

| Tipo de error | Descripción |
|----------|-------------|
| SQL Injection | Entrada de usuario directamente en consultas SQL |
| Hardcoded Secrets | Secretos en el código |
| Race Conditions | Estado compartido sin sincronización adecuada |
| Sensitive Data Logging | Contraseñas y números de tarjeta en los registros |
| Missing Input Validation | Sin comprobaciones en los datos proporcionados por el usuario |
| No Error Handling | Faltan bloques try/catch o try/except |
| Weak Password Comparison | Texto plano o comparaciones vulnerables a ataques de temporización |
| Missing Auth Checks | Operaciones sin verificación de autorización |

### Errores específicos de Python

| Tipo de error | Descripción |
|----------|-------------|
| Pickle Deserialization | `pickle.loads()` en datos no confiables |
| eval() Injection | Entrada de usuario pasada a `eval()` |
| Unsafe YAML Loading | `yaml.load()` sin un cargador seguro |
| Shell Injection | Entrada de usuario en llamadas a `os.system()` |
| Weak Hashing | MD5 para el hashing de contraseñas |
| Insecure Random | módulo `random` para propósitos de seguridad |

## Ejercicios prácticos

1. **Auditoría de seguridad**: Realiza una revisión de seguridad exhaustiva y enumera todas las vulnerabilidades por severidad
2. **Arreglar un error**: Elige un error crítico, obtén la corrección de Copilot y entiende por qué funciona
3. **Generar pruebas**: Crea pruebas que detecten estos errores antes del despliegue
4. **Refactorizar de forma segura**: Corrige los errores de inyección SQL manteniendo la funcionalidad

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->