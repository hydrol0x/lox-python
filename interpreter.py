from tokenType import TokenType as T
from tokens import Token
from expr import Visitor, Expr, Literal, Unary, Binary, Grouping


class LoxRuntimeError(RuntimeError):
    # TODO: possibly will be moved to error_handler or some errors file, along with other errors
    def __init__(self, token: Token, message: str):
        self.token = token
        self.RuntimeError = RuntimeError(message)


class Interpreter(Visitor):

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        error = LoxRuntimeError(operator, "Expected numerical operand")
        raise error

    def _to_float(self, value: object):
        if isinstance(value, (int, float, str)):
            return float(value)
        else:
            # unreachable due to check_number_operand
            raise TypeError(
                f"Value `{value}` cannot be converted to float. Check interpreter; should throw LoxRuntimeException")

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def is_truthy(self, _object: object) -> bool:
        if _object == None:
            return False
        if isinstance(_object, bool):
            return bool(_object)
        return True

    def is_equal(self, a: object, b: object) -> bool:
        # if (a==None and b == None): return True --- this already happens in python
        if (a == None):
            return False
        return a == b

    def visitLiteralExpr(self, expr: Literal) -> object:
        return expr.value

    def visitGroupingExpr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.TYPE:
            case T.BANG:
                return not self.is_truthy(right)
            case T.MINUS:
                self.check_number_operand(expr.operator, right)
                return self._to_float(right)

        # Unreachable
        return None

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.TYPE:
            case T.GREATER:
                return self._to_float(left) > self._to_float(right)
            case T.GREATER_EQUAL:
                return self._to_float(left) >= self._to_float(right)
            case T.LESS:
                return self._to_float(left) < self._to_float(right)
            case T.LESS_EQUAL:
                return self._to_float(left) <= self._to_float(right)
            case T.BANG_EQUAL:
                return not self.is_equal(left, right)
            case T.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case T.MINUS:
                return self._to_float(left) - self._to_float(right)
            case T.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return self._to_float(left) + self._to_float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
            case T.SLASH:
                return self._to_float(left) / self._to_float(right)
            case T.STAR:
                return self._to_float(left) * self._to_float(right)

        # Unreachable
        return None
