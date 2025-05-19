import sys
import os

# Agregar ruta al paquete src para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from nachlang.transpiler import transpile_code


def test_transpile_simple_call():
    code = (
        'funcion saludo() dice:\n'
        '    imprime("Hola")\n'
    )
    result = transpile_code(code)
    expected = (
        'def saludo():\n'
        '    imprime("Hola")\n'
    )
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    'code, expected',
    [
        (
            'funcion test() dice:\n'
            '    foo(123, bar, "abc")\n',
            'def test():\n'
            '    foo(123, bar, "abc")\n',
        ),
        (
            'funcion a() dice:\n'
            '    x()\n'
            'funcion b() dice:\n'
            '    y()\n',
            'def a():\n'
            '    x()\n'
            '\n'
            'def b():\n'
            '    y()\n',
        ),
    ],
)
def test_transpile_various(code, expected):
    assert transpile_code(code).strip() == expected.strip()


@pytest.mark.parametrize(
    'code, expected',
    [
        ('x = 5\n', 'x = 5'),
        ('mostrar "Hola"\n', 'print("Hola")'),
        ('print "Hello"\n', 'print("Hello")'),
        (
            'si x == 1:\n'
            '    mostrar "uno"\n',
            'if x == 1:\n'
            '    print("uno")',
        ),
        (
            'if x > 2:\n'
            '    print("gt")\n'
            'else:\n'
            '    print("not gt")\n',
            'if (x > 2):\n'
            '    print("gt")\n'
            'else:\n'
            '    print("not gt")',
        ),
        (
            'repetir 2 veces:\n'
            '    mostrar "Hola"\n',
            'for _ in range(2):\n'
            '    print("Hola")',
        ),
        (
            'repeat 3 times:\n'
            '    print("Hi")\n',
            'for _ in range(3):\n'
            '    print("Hi")',
        ),
        ('terminar\n', 'import sys\nsys.exit()'),
        ('exit\n', 'import sys\nsys.exit()'),
        ('cantidad = 1 + 2\n', 'cantidad = (1 + 2)'),
    ],
)
def test_transpile_new_features(code, expected):
    assert transpile_code(code).strip() == expected.strip()