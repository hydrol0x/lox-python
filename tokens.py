from tokenType import TokenType


class Token:
    def __init__(self, _type: TokenType, lexeme: str, literal: object, line: int):
        self.TYPE = _type
        self.LEXEME = lexeme
        self.LITERAL = literal
        self.LINE = line

    def to_string(self):
        return (f"<{self.TYPE.name}, `{self.LEXEME}`, {self.LITERAL}>")
