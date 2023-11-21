from __future__ import annotations
from abc import ABC, abstractmethod
from tokens import Token
from expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: Visitor):
        return visitor.visitBlockStmt(self)


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitPrintStmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Visitor):
        return visitor.visitVarStmt(self)


class Visitor:
    @abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt): pass

    @abstractmethod
    def visitPrintStmt(self, stmt: Print): pass

    @abstractmethod
    def visitVarStmt(self, stmt: Var): pass

    @abstractmethod
    def visitBlockStmt(self, stmt: Block): pass