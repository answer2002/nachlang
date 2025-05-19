"""
Transpilador de NachLang a Python.
"""

from typing import Any
from .parser import parse
from .ast import FunctionDef, Call, BinaryOp, Number, String, Var, Assignment, Print, If, Repeat, Terminate
from lark import Transformer, Token

class ASTBuilder(Transformer):
    """Transforma el Parse Tree de Lark en nodos AST de NachLang."""
    def ID(self, token):
        return Var(token.value)

    def NUMBER(self, token):
        return Number(token.value)

    def STRING(self, token):
        return String(token.value)


    def arg_list(self, children):
        return children

    def call_stmt(self, children):
        name_node = children[0]
        args = children[1] if len(children) > 1 else []
        return Call(name_node.name, args)

    def stmt(self, children):
        return children[0]

    def func_def(self, children):
        name = None
        body: list[Any] = []
        for child in children:
            if isinstance(child, Var):
                name = child.name
            elif isinstance(child, Call):
                body.append(child)
        return FunctionDef(name or '', [], body)

    def start(self, children):
        return children

    def assign_stmt(self, children):
        var_node = children[0]
        value = children[-1]
        return Assignment(var_node.name, value)

    def print_stmt(self, children):
        expr_node = children[-1]
        return Print(expr_node)

    def then_block(self, children):
        return [c for c in children if not isinstance(c, Token)]

    def else_block(self, children):
        return [c for c in children if not isinstance(c, Token)]

    def if_stmt(self, children):
        ast_children = [c for c in children if not isinstance(c, Token)]
        cond = ast_children[0]
        then_branch = ast_children[1] if len(ast_children) > 1 else []
        else_branch = ast_children[2] if len(ast_children) > 2 else []
        return If(cond, then_branch, else_branch)

    def repeat_stmt(self, children):
        ast_children = [c for c in children if not isinstance(c, Token)]
        count = ast_children[0]
        body = ast_children[1:]
        return Repeat(count, body)

    def terminate_stmt(self, children):
        return Terminate()

    def eq(self, children):
        left, right = children
        return BinaryOp('==', left, right)

    def gt(self, children):
        left, right = children
        return BinaryOp('>', left, right)

    def add(self, children):
        left, right = children
        return BinaryOp('+', left, right)

    def atom(self, children):
        return children[0]

def ast_from_tree(tree):
    """Construye el AST a partir del árbol de parseo."""
    return ASTBuilder().transform(tree)

def transpile(ast_nodes):
    """Genera código Python a partir de la lista de nodos AST."""
    def _transpile_expr(node):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, String):
            return node.value
        if isinstance(node, Var):
            return node.name
        if isinstance(node, BinaryOp):
            left = _transpile_expr(node.left)
            right = _transpile_expr(node.right)
            return f"({left} {node.op} {right})"
        if isinstance(node, Call):
            args = ', '.join(_transpile_expr(arg) for arg in node.args)
            return f"{node.name}({args})"
        raise NotImplementedError(f"Expression type not supported: {node}")

    lines: list[str] = []

    def _transpile_node(node, indent_level=0):
        indent = '    ' * indent_level
        if isinstance(node, FunctionDef):
            params = ', '.join(node.params)
            lines.append(f"{indent}def {node.name}({params}):")
            for stmt in node.body:
                _transpile_node(stmt, indent_level + 1)
            lines.append('')

        elif isinstance(node, If):
            cond = _transpile_expr(node.condition)
            lines.append(f"{indent}if {cond}:")
            for stmt in node.then_branch:
                _transpile_node(stmt, indent_level + 1)
            if node.else_branch:
                lines.append(f"{indent}else:")
                for stmt in node.else_branch:
                    _transpile_node(stmt, indent_level + 1)

        elif isinstance(node, Repeat):
            count = _transpile_expr(node.count)
            lines.append(f"{indent}for _ in range({count}):")
            for stmt in node.body:
                _transpile_node(stmt, indent_level + 1)

        elif isinstance(node, Assignment):
            value = _transpile_expr(node.value)
            lines.append(f"{indent}{node.name} = {value}")

        elif isinstance(node, Print):
            expr = _transpile_expr(node.expr)
            lines.append(f"{indent}print({expr})")

        elif isinstance(node, Terminate):
            lines.append(f"{indent}sys.exit()")

        elif isinstance(node, Call):
            expr = _transpile_expr(node)
            lines.append(f"{indent}{expr}")

        else:
            raise NotImplementedError(f"Statement type not supported: {node}")

    for node in ast_nodes:
        _transpile_node(node)
    return '\n'.join(lines)

def _contains_terminate(nodes):
    for node in nodes:
        if isinstance(node, Terminate):
            return True
        if isinstance(node, FunctionDef):
            if _contains_terminate(node.body):
                return True
        if isinstance(node, If):
            if _contains_terminate(node.then_branch) or _contains_terminate(node.else_branch):
                return True
        if isinstance(node, Repeat):
            if _contains_terminate(node.body):
                return True
    return False

def transpile_code(code: str) -> str:
    """Parsea el código NachLang y devuelve el equivalente en Python."""
    tree = parse(code)
    ast_nodes = ast_from_tree(tree)
    py_code = transpile(ast_nodes)
    if _contains_terminate(ast_nodes):
        py_code = 'import sys\n' + py_code
    return py_code