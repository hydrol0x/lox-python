class Token:
    def __init__(self, _type, lexeme, literal, line):
        self.TYPE = _type
        self.LEXEME = lexeme
        self.LITERAL = literal
        self.LINE = line
    
    def to_string(self):
        return(f"<{self.TYPE.name}, `{self.LEXEME}`, {self.LITERAL}>")