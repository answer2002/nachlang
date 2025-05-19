import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import pytest

from nachlang.parser import parse


def test_parse_placeholder():
    code = "funcion saludo() dice:\n" '    imprime("Hola")\n'
    tree = parse(code)
    assert tree is not None


def test_parse_english_keywords():
    code = "function saludo() says:\n" '    print("Hello")\n'
    tree = parse(code)
    assert tree is not None
