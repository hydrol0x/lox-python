from abc import ABC, abstractmethod
from stmt import Function
from environment import Environment
from error_handler import ReturnException

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int: pass

    @abstractmethod
    def call(self, interpreter, arguments: list[object]) -> object: pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration
    
    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments: list[object]) -> None | object:
        environment = Environment(interpreter.globals)
        for i, param in enumerate(self.declaration.params):
            environment.define(param.LEXEME, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_val:
            return return_val.value
        return None
    
    def to_string(self) -> str:
        return f"<function {self.declaration.name.LEXEME}>"
