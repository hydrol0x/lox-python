
# Native fns

import time
from lox_callable import LoxCallable

class Clock(LoxCallable):
    def __init__(self):
        pass
    
    def arity(self) -> int:
        return 0
    
    def call(self, interpreter, arguments: list[object]) -> object:
        now = time.time() 
        return now
    
    def to_string(self) -> str:
        return "<native fn>"
