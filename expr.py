from __future__ import annotations
from abc import ABC, abstractmethod
from tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass

    @abstractmethod
    def to_string(self): pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visitAssignExpr(self)

    def to_string(self):
        return f"Assign({self.name.to_string()}, {self.value.to_string()})"


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)

    def to_string(self):
        return f"Binary({self.left.to_string()}, {self.operator.to_string()}, {self.right.to_string()})"


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)

    def to_string(self):
        return f"Grouping({self.expression.to_string()})"


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)

    def to_string(self):
        return f"Literal({self.value})"


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpr(self)

    def to_string(self):
        return f"Unary({self.operator.to_string()}, {self.right.to_string()})"


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: Visitor):
        return visitor.visitVariableExpr(self)

    def to_string(self):
        return f"Variable({self.name})"


class Visitor:
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary): pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping): pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal): pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary): pass

    @abstractmethod
    def visitVariableExpr(self, expr: Variable): pass

    @abstractmethod
    def visitAssignExpr(self, expr: Assign): pass
