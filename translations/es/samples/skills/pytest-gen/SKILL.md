---
name: pytest-gen
description: Generar pruebas pytest completas - usar al generar pruebas, al crear
  suites de pruebas o al probar código Python
---
# Habilidad de generación de Pytest

Al generar pruebas, siga esta estructura.

## Organización de las pruebas

- Agrupe las pruebas por la función bajo prueba
- Use `@pytest.mark.parametrize` para múltiples entradas
- Use fixtures para la configuración compartida
- Siga el patrón arrange/act/assert

## Requisitos de cobertura

- Camino feliz (uso esperado)
- Casos límite (cadenas vacías, None, valores límite)
- Casos de error (entrada inválida, archivo no encontrado, tipos incorrectos)
- Integración (funciones que trabajan juntas)

## Plantilla

```python
import pytest
from module_under_test import function_to_test


@pytest.fixture
def sample_data():
    """Provide shared test data."""
    return {"key": "value"}


class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self, sample_data):
        result = function_to_test(valid_input)
        assert result == expected_output

    def test_empty_input(self):
        result = function_to_test("")
        assert result == expected_for_empty

    @pytest.mark.parametrize("input_val,expected", [
        ("valid", True),
        ("", False),
        (None, False),
    ])
    def test_various_inputs(self, input_val, expected):
        assert function_to_test(input_val) == expected
```

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->