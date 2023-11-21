"""
not currently in use, figuring out if I can simplify so i don't have to import everything and can just import Expr and have the rest of the types be sub
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass

    class _Binary:
        pass

    class _Grouping:
        pass

    class _Literal:
        pass

    class _Unary:
        pass


class Binary(Expr._Binary, Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr._Grouping, Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr._Literal, Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr._Unary, Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpr(self)


class Visitor:
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary): pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping): pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal): pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary): pass


Expr._Binary = Binary
Expr._Grouping = Grouping
Expr._Literal = Literal
Expr._Unary = Unary
