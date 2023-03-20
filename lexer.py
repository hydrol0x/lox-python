
class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def to_string(self):
        return f"<{self.type}:{self.value}>"


class Pos:
    def __init__(self, index, line, col, code):
        self.index = index
        self.line = line
        self.col = col
        self.code = code

    # def advance(self, n):
    #     # advance by n characters and keep track of position in file
    #     for i in range(n):
    #         self.index += 1
    #         self.col += 1
    #         if (self.code[self.index] == '\n'):
    #             self.col = 0
    #             self.line += 1
    def advance(self, n):
        # advance by n characters and keep track of position in file
        for i in range(n):
            self.index += 1
            self.col += 1
            if self.code[self.index] == '\n':
                self.col = 0
                self.line += 1
            print(f"Index: {self.index} Col: {self.col} Line: {self.line}")

    def clone(self):
        return Pos(self.index, self.line, self.col, self.code)


TOKEN_TYPES = {
    'number': "1234567890",
    'operator': ["*", "**", "/", "+", "-"],
    'lparen': "(",
    'rparen': ")",
}


class Lexer:
    def __init__(self, code, TOKEN_TYPES):
        self.code = code
        self.TOKEN_TYPES = TOKEN_TYPES
        self.tokens = []
        self.slice = code
        self.pos = Pos(0, 0, 0, code)

    def advance(self, n):
        # advance by n and advance over any white space or tabs
        self.pos.advance(n)
        self.slice = self.code[self.pos.index:]
        while self.slice[0].isspace():
            self.advance(1)

    def create_tokens(self):
        while self.slice:
            token = ""
            next_char = ""
            found_token = False
            for i, char in enumerate(self.slice):
                token += char
                if i < len(self.slice) - 1:
                    # not at end
                    next_char = self.slice[i + 1]
                print(
                    f"DEBUG: Processing slice '{self.slice}' at position {i}, token '{token}', next char '{next_char}'")
                if not next_char.isspace() and next_char is not '':
                    continue
                for _type, pattern in self.TOKEN_TYPES.items():
                    if token in pattern:
                        self.tokens.append(Token(_type, token))
                        if next_char is not '':
                            self.advance(len(token))
                        else:
                            self.slice = ''
                        print(f"DEBUG: Added token {_type}:{token}")
                        found_token = True
                        break
                    else:
                        print(f"DEBUG: Invalid token {token}")
                        print(f"DEBUG: Tokens so far: {self.tokens}")
                        token = ""
                        return f"ERR: INVALID TOKEN {self.tokens}"
                if found_token:
                    break

        print(f"DEBUG: Final tokens: {self.tokens}")
        return self.tokens

    # def create_tokens(self):
    #     while self.slice:
    #         token = ""
    #         next_char = ""
    #         for i, char in enumerate(self.slice):
    #             token += char
    #             if i < len(self.slice) - 1:
    #                 # not at end
    #                 next_char = self.slice[i + 1]
    #             if not next_char.isspace():
    #                 continue
    #             for _type, pattern in self.TOKEN_TYPES.items():
    #                 if token in pattern:
    #                     self.tokens.append(Token(_type, token))
    #                     self.slice.advance(len(token))
    #                     break
    #                 else:
    #                     return f"ERR: INVALID TOKEN {self.tokens}"

    #     return self.tokens


def create_tokens(code):
    lexer = Lexer(code, TOKEN_TYPES)
    return lexer.create_tokens()
