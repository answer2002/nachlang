#!/usr/bin/env python3
"""
NachLang to Python converter.

Usage:
    python3 nachlang_converter.py entrada.nach salida.py
"""
import sys
from pathlib import Path

from nachlang.transpiler import transpile_code


def main():
    if len(sys.argv) != 3:
        print(
            'Uso: python3 nachlang_converter.py entrada.nach salida.py',
            file=sys.stderr,
        )
        sys.exit(1)

    entrada, salida = sys.argv[1], sys.argv[2]
    code = Path(entrada).read_text(encoding='utf-8')
    py_code = transpile_code(code)
    Path(salida).write_text(py_code, encoding='utf-8')
    print(f'Archivo traducido guardado en {salida}')


if __name__ == '__main__':
    main()