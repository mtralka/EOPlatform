# type: ignore
import ast
from ast import AST
import math
import operator
from typing import Any
from typing import Dict
from typing import Union


def safe_eval(s, **kwargs) -> Any:
    """Safely parse input formula string

    Modified from Jason M @ SO
    """

    def checkmath(x: str, *args) -> Any:
        if x not in [x for x in dir(math) if not "__" in x]:
            raise SyntaxError(f"Unknown func {x}()")
        fun = getattr(math, x)
        return fun(*args)

    binOps: Dict[type, Union[function, type]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.Call: checkmath,
        ast.BinOp: ast.BinOp,
    }

    unOps: Dict[type, Union[function, type]] = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.UnaryOp: ast.UnaryOp,
    }

    ops = tuple(binOps) + tuple(unOps)

    tree: AST = ast.parse(s, mode="eval")

    def _eval(node, **kwargs):
        if isinstance(node, ast.Expression):
            return _eval(node.body, **kwargs)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            if isinstance(node.left, ops):
                left = _eval(node.left, **kwargs)
            else:
                left = kwargs[node.left.id]
            if isinstance(node.right, ops):
                right = _eval(node.right, **kwargs)
            else:
                right = kwargs[node.right.id]
            return binOps[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.operand, ops):
                operand = _eval(node.operand, **kwargs)
            else:
                operand = node.operand.n
            return unOps[type(node.op)](operand)
        elif isinstance(node, ast.Call):
            args = [_eval(x, **kwargs) for x in node.args]
            r = checkmath(node.func.id, *args)
            return r
        else:
            raise SyntaxError(f"Bad syntax, {type(node)}")

    return _eval(tree, **kwargs)
