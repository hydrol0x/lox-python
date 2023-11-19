from tokenType import TokenType as T
from tokens import Token
from expr import Visitor, Expr, Literal, Unary, Binary, Grouping
from error_handler import LoxRuntimeError, runtime_error
import logging


class Interpreter(Visitor):
    def interpret(self, expr: Expr) -> None:
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            runtime_error(error)

    def stringify(self, value: object) -> str:
        if value == None:
            return "nil"

        if isinstance(value, float):
            text = str(value)
            if text.endswith('.0'):
                text = text[0:-2]
            return text

        if isinstance(value, bool):
            # Lox uses lowercase 'true' and 'false' keywords
            if value == True:
                return 'true'
            else:
                return 'false'

        return str(value)

    def check_number_operands(self, operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        error = LoxRuntimeError(operator, "Expected numerical operands")
        raise error

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        error = LoxRuntimeError(operator, "Expected numerical operand")
        raise error

    def _to_float(self, value: object):
        """
        This is necessary due to Pylance/Python type checking, since otherwise Python complains that it is possible for float() to be called on an Object,
        even though check_number_operand ensures that doesn't happen (otherwise error thrown). In the future, I may try to fix this since it is redundant.
        """
        if isinstance(value, (int, float, str)):
            return float(value)
        else:
            # unreachable due to check_number_operand
            raise TypeError(
                f"Value `{value}` cannot be converted to float. Check interpreter; should throw LoxRuntimeException")

    def evaluate(self, expr: Expr) -> object:
        logging.debug(f"Evaluating expression {expr.to_string()}")
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
                return -self._to_float(right)

        # Unreachable
        return None

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.TYPE:
            case T.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return self._to_float(left) > self._to_float(right)
            case T.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return self._to_float(left) >= self._to_float(right)
            case T.LESS:
                self.check_number_operands(expr.operator, left, right)
                return self._to_float(left) < self._to_float(right)
            case T.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return self._to_float(left) <= self._to_float(right)
            case T.BANG_EQUAL:
                return not self.is_equal(left, right)
            case T.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case T.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return self._to_float(left) - self._to_float(right)
            case T.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return self._to_float(left) + self._to_float(right)
                if isinstance(left, str) or isinstance(right, str):
                    # Stringify necessary so that `"string" + 1` isn't interpreted as `"string1.0"`
                    # although, there is an edgecase that if the user enters explicitly 1.0 then it will be presented as 1
                    # There is no way to distinguish this without an under-the-hood int type
                    return self.stringify(left) + self.stringify(right)

                error = LoxRuntimeError(
                    expr.operator, "Expect operands to be two numbers or two strings")
                raise error
            case T.SLASH:
                self.check_number_operands(expr.operator, left, right)
                if right == 0:
                    error = LoxRuntimeError(expr.operator, "Divide by zero")
                    raise error
                return self._to_float(left) / self._to_float(right)
            case T.STAR:
                self.check_number_operands(expr.operator, left, right)
                return self._to_float(left) * self._to_float(right)

        # Unreachable
        return None
