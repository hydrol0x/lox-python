from __future__ import annotations
from tokens import Token
from error_handler import LoxRuntimeError


class Environment():

    def __init__(self, enclosing: Environment | None = None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def get(self, name: Token) -> None:
        if name.LEXEME in self.values:
            return self.values[name.LEXEME]

        if self.enclosing:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f'Undefined variable {name.LEXEME}.')

    def assign(self, name: Token, value: object) -> None:
        if name.LEXEME in self.values:
            self.values[name.LEXEME] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable {name.LEXEME}.")
