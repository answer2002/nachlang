"""
Parser de NachLang: carga la gramática y produce un árbol de sintaxis.
"""

from lark import Lark
from lark.indenter import Indenter
from pathlib import Path

_GRAMMAR_PATH = Path(__file__).parent.parent.parent / 'grammar' / 'nachlang.lark'
_GRAMMAR = _GRAMMAR_PATH.read_text(encoding='utf-8')

class PythonIndenter(Indenter):
    """Post-lexical indenter para NachLang basado en indentación tipo Python."""
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

_parser = Lark(
    _GRAMMAR,
    parser='lalr',
    lexer='contextual',
    postlex=PythonIndenter(),
    start='start',
)

def parse(code: str):
    """Devuelve el árbol de sintaxis (Parse Tree) de NachLang para el código dado."""
    return _parser.parse(code)