# NachLang

[![CI](https://github.com/usuario/nachlang/actions/workflows/ci.yml/badge.svg)](https://github.com/usuario/nachlang/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/usuario/nachlang/branch/main/graph/badge.svg)](https://codecov.io/gh/usuario/nachlang)
[![PyPI version](https://badge.fury.io/py/nachlang.svg)](https://badge.fury.io/py/nachlang)

Lenguaje de programación de sintaxis natural.

## Sintaxis básica (v0.1)

- **Asignación**: `variable = expresión`
- **Impresión**: `mostrar expresión` / `print expresión`
- **Condicionales**:
  ```nachlang
  si condición:
      ...
  sino:
      ...
  ```
- **Bucles**:
  ```nachlang
  repetir N veces:
      ...
  repeat N times:
      ...
  ```
- **Terminación**: `terminar` / `exit`
- **Funciones**: `funcion|function nombre() dice|say:` ...
- **Llamadas**: `nombre(args)`
- **Operadores**: `+`, `>`, `==`
- **Strings**: `"texto"`
- **Números**: `123`

Consulta el [Manifiesto](MANIFIESTO.md) para la visión, principios y plan de arranque del proyecto.

## Manual de Uso

### Instalación

**Instalación desde PyPI** (si está publicado):

```bash
pip install nachlang
```

**Instalación desde el repositorio:**

```bash
git clone https://github.com/usuario/nachlang.git  # Reemplaza 'usuario' según corresponda
cd nachlang
pip install .
```

Para soporte IA (opcional):

```bash
pip install nachlang[ai]
```

### Conversión a Python

```bash
python3 nachlang_converter.py entrada.nach salida.py
```

### REPL interactivo

```bash
python3 nachlang_repl.py
```

### Ayuda IA (opcional)

Dentro de la REPL, escribe:

```bash
ia: <tu pregunta o petición>
```
o
```bash
ai: <tu pregunta o petición>
```

y obtendrás respuestas generadas por IA.