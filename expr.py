from __future__ import annotations
from abc import ABC, abstractmethod
from token import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass


class Binary(Expr):
    def __init__(self,left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):
    def __init__(self,expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    def __init__(self,value: object):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)

class Unary(Expr):
    def __init__(self,operator: Token, right: Expr):
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



