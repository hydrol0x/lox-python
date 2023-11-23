from tokenType import TokenType as T
from tokens import Token
from error_handler import error, report


class Lexer:
    global KEYWORDS
    KEYWORDS = {
        "and": T.AND,
        "class": T.CLASS,
        "else": T.ELSE,
        "false": T.FALSE,
        "for": T.FOR,
        "fun": T.FUN,
        "if": T.IF,
        "nil": T.NIL,
        "or": T.OR,
        "print": T.PRINT,
        "return": T.RETURN,
        "super": T.SUPER,
        "this": T.THIS,
        "true": T.TRUE,
        "var": T.VAR,
        "break": T.BREAK,
        "while": T.WHILE,
    }

    def __init__(self, source: str):
        self.source = source  # Source code
        self.TOKENS = []  # List of tokens
        self.start = 0  # first char of lexeme
        self.current = 0  # current char in lexeme
        self.line = 1  # current line
        self.col = 0  # current column in line

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        consumed_char = self.source[self.current]
        self.current += 1
        return consumed_char

    def add_token(self, type: T, literal: object = None):
        text = self.source[self.start:self.current]
        self.TOKENS.append(Token(type, text, literal, self.line))

    def match_next(self, character: str):
        if (self.is_at_end()):
            return False
        if self.source[self.current] != character:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            report(self.line, f"{self.start}-{self.current}",
                   "Unterminated string.")
            return

        self.advance()  # closing "

        string = self.source[self.start+1:self.current-1]
        self.add_token(T.STRING, string)

    def number(self):
        while self.peek().isnumeric():
            self.advance()

        if self.peek() == '.' and self.peek_next().isnumeric():
            self.advance()  # consume '.'
            while self.peek().isnumeric():
                self.advance()

        number = self.source[self.start:self.current]
        self.add_token(T.NUMBER, float(number))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        current_token = self.source[self.start:self.current]
        if current_token in KEYWORDS:
            self.add_token(KEYWORDS[current_token])
        else:
            self.add_token(T.IDENTIFIER)

    def multi_comment(self):
        counter = 1
        first_comment_line = self.line
        while counter != 0 and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            elif self.peek() == '/' and self.peek_next() == '*':
                counter += 1
            elif self.peek() == '*' and self.peek_next() == '/':
                counter -= 1

            self.advance()
        if counter != 0:
            report(first_comment_line,
                   f"{self.start}-{self.current}", "Unterminated multiline comment.")
            return

        # consume final `/`
        self.advance()

    def scan_tokens(self):
        while (not self.is_at_end()):
            self.start = self.current
            self.scan_token()

        self.TOKENS.append(Token(T.EOF, "", None, self.line))
        return self.TOKENS

    def scan_token(self):
        char = self.advance()
        match (char):
            case '(': self.add_token(T.LEFT_PAREN)
            case ')': self.add_token(T.RIGHT_PAREN)
            case '{': self.add_token(T.LEFT_BRACE)
            case '}': self.add_token(T.RIGHT_BRACE)
            case ',': self.add_token(T.COMMA)
            case '.': self.add_token(T.DOT)
            case '-': self.add_token(T.MINUS)
            case '+': self.add_token(T.PLUS)
            case ';': self.add_token(T.SEMICOLON)
            case '*':
                if self.match_next('/'):
                    error(line=self.line, message="Unexpected close comment `*/`")
                else:
                    self.add_token(T.STAR)

            case '!': self.add_token(T.BANG_EQUAL if self.match_next('=') else T.BANG)
            case '=': self.add_token(T.EQUAL_EQUAL if self.match_next('=') else T.EQUAL)
            case '<': self.add_token(T.LESS_EQUAL if self.match_next('=') else T.LESS)
            case '>': self.add_token(T.GREATER_EQUAL if self.match_next('=') else T.GREATER)
            case '/':
                if self.match_next('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                elif self.match_next('*'):
                    self.multi_comment()
                else:
                    self.add_token(T.SLASH)

            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self.line += 1

            case '"': self.string()

            case _:
                if char.isnumeric():
                    self.number()
                elif char.isalpha():
                    self.identifier()
                else:
                    report(
                        self.line, f"{self.start}-{self.current}", f"Unexpected character {char}")
