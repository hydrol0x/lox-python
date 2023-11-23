from __future__ import annotations
from abc import ABC, abstractmethod
from tokens import Token
from expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass

    @abstractmethod
    def to_string(self) -> str: pass


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: Visitor):
        return visitor.visitBlockStmt(self)

    def to_string(self) -> str:
        return f"Block({[statement.to_string() for statement in self.statements]})"


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitExpressionStmt(self)

    def to_string(self) -> str:
        return f"ExprStmt({self.expression.to_string()})"


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt | None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: Visitor):
        return visitor.visitIfStmt(self)

    def to_string(self) -> str:
        return f"If({self.condition.to_string()}, {self.then_branch.to_string()}, {None if not self.else_branch else self.else_branch.to_string()})"


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visitPrintStmt(self)

    def to_string(self) -> str:
        return f"Print({self.expression.to_string()})"


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr | None):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Visitor):
        return visitor.visitVarStmt(self)

    def to_string(self) -> str:
        return f"VarDec({self.name.to_string()}, {None if not self.initializer else self.initializer.to_string()})"


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt | None):
        self.condition = condition
        self.body = body

    def accept(self, visitor: Visitor):
        return visitor.visitWhileStmt(self)

    def to_string(self) -> str:
        return f"While({self.condition.to_string()}, {None if not self.body else self.body.to_string()})"


class Break(Stmt):
    def accept(self, visitor: Visitor):
        return visitor.visitBreakStmt(self)

    def to_string(self) -> str:
        return f"Break()"


class Visitor:
    @abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt): pass

    @abstractmethod
    def visitPrintStmt(self, stmt: Print): pass

    @abstractmethod
    def visitVarStmt(self, stmt: Var): pass

    @abstractmethod
    def visitBlockStmt(self, stmt: Block): pass

    @abstractmethod
    def visitIfStmt(self, stmt: If): pass

    @abstractmethod
    def visitWhileStmt(self, stmt: While): pass

    @abstractmethod
    def visitBreakStmt(self, stmt: Break): pass
