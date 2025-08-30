import operator
import ast


class CalculationError(Exception):
    pass


_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


class _Calculator(ast.NodeVisitor):
    def visit_BinOp(self, n):
        return _OP_MAP[type(n.op)](self.visit(n.left), self.visit(n.right))

    def visit_Constant(self, n):
        return n.value

    def visit_Expr(self, n):
        return self.visit(n.value)

    @classmethod
    def evaluate(cls, expr):
        return cls().visit(ast.parse(expr, mode="eval").body)


def calculate(expression: str):
    """
    Safely evaluates a Python-style mathematical expression.

    For the model: Use this for any request requiring calculation. It supports
    addition (+), subtraction (-), multiplication (*), division (/), and
    exponentiation (**). The expression must be a standard mathematical string.
    The result is a raw number.

    Args:
        expression (str): The mathematical expression to evaluate.
                          Example: "5 * (10 + 2)"

    Returns:
        float: The numerical result of the calculation.

    Raises:
        CalculationError: If the expression is invalid, unsafe, or cannot be evaluated.
    """
    try:
        return _Calculator.evaluate(expression)
    except (TypeError, KeyError, SyntaxError, ZeroDivisionError) as e:
        raise CalculationError(f"Invalid mathematical expression: {e}")
    except Exception as e:
        raise CalculationError(f"An unexpected error occurred: {e}")
