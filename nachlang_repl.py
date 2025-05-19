#!/usr/bin/env python3
"""
NachLang REPL interactivo.

Uso:
    python3 nachlang_repl.py
"""

import sys
import os
# Agregar src al path para importar el paquete nachlang desde el directorio de desarrollo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from nachlang.repl import run_repl


if __name__ == '__main__':
    run_repl()