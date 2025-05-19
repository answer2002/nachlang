"""
Definición de nodos del AST (Abstract Syntax Tree) de NachLang.
"""

from dataclasses import dataclass
from typing import Any, List


@dataclass
class FunctionDef:
    name: str
    params: List[str]
    body: List[Any]


@dataclass
class Call:
    name: str
    args: List[Any]


@dataclass
class BinaryOp:
    op: str
    left: Any
    right: Any


@dataclass
class Number:
    value: str


@dataclass
class String:
    value: str


@dataclass
class Var:
    name: str


@dataclass
class Assignment:
    name: str
    value: Any


@dataclass
class Print:
    expr: Any


@dataclass
class If:
    condition: Any
    then_branch: List[Any]
    else_branch: List[Any]


@dataclass
class Repeat:
    count: Any
    body: List[Any]


@dataclass
class Terminate:
    pass
