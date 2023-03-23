from expr import Visitor, Expr, Binary, Grouping, Literal, Unary
from token import Token 
from tokenType import TokenType as T
from ast_printer import AST_printer

printer = AST_printer()

class Convert_RPN(Visitor):
    def rpn_print(self, expr: Expr):
        return f"Original: {printer.ast_print(expr)} RPN: {expr.accept(self)}"

    def visitBinaryExpr(self, expr: Binary):
        return self.RPN(expr.operator.LEXEME, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping):
        return expr.expression.accept(self)

    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.RPN(expr.operator.LEXEME, expr.right)

    def RPN(self, operator, *exprs: Expr):
        op_stack = []
        output = ""
        precedence = {
            "+":1,
            "-":1,
            "*":2,
            "/":2
        }
        # op_stack.append(operator)
        for expr in exprs:
            output+=(str(expr.accept(self))) + " "
        output+=operator
        # output.append(op_stack)
        return output
    
if __name__ == "__main__":
    group = Grouping(Binary(Literal(2),Token(T.PLUS, "+", None,1),Literal(3)))
    binary_left = Binary(Literal(1), Token(T.PLUS, "+", None,1),group)
    expression = Binary(binary_left,  Token(T.PLUS, "+", None,1),Literal(4))
        # [1 + (2+3)] + 4
        # IDK if this works but it looks ok. I am not sure if that is valid RPN
        # Seems fair since you push [1,2,3] into stack, add [2,3] and then add [1,5] 
    

    to_rpn = Convert_RPN()
    print(to_rpn.rpn_print(expression))

