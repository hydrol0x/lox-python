from expr import Visitor, Expr, Binary, Grouping, Literal, Unary
from tokens import Token
from tokenType import TokenType as T


class AST_printer(Visitor):
    def ast_print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.LEXEME, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.LEXEME, expr.right)

    def parenthesize(self, name: str, *exprs: Expr):
        output = f"({name}"
        for expr in exprs:
            output = output + " " + str(expr.accept(self))
        output += ")"

        return output


if __name__ == "__main__":
    expression = Binary(
        Unary(Token(T.MINUS, "-", None, 1), Literal(123)),
        Token(T.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )
    printer = AST_printer()
    print(printer.ast_print(expression))
