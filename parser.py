import logging
from expr import Expr, Binary, Grouping, Literal, Unary
from tokens import Token
from tokenType import TokenType as T
from error_handler import error as lox_error

logging.basicConfig(level=logging.ERROR)


class ParseError(RuntimeError):
    # TODO: possibly move to error_handler
    pass


class Parser:
    def __init__(self, tokens: list):
        logging.debug(f"Tokens: {[token.LEXEME for token in tokens]}")
        self.tokens = tokens
        self.current = 0

    def parse(self):
        logging.debug(f"Parsing token {self.tokens[self.current].LEXEME}")
        logging.debug(f"Line: {self.tokens[self.current].LINE}")
        try:
            return self.expression()
        except ParseError:
            return None

    # test code
    def parse_multiple(self):
        expressions = []
        while not self.is_at_end():
            try:
                expr = self.expression()
                if expr is not None:
                    expressions.append(expr)
            except ParseError:
                self.synchronize()
        return expressions

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().TYPE == T.EOF

    def check(self, expected: T) -> bool:
        return False if self.is_at_end() else self.peek().TYPE == expected

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *types: T):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def error(self, token: Token, err_message: str) -> ParseError:
        lox_error(token=token, message=err_message)
        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().TYPE == T.SEMICOLON:
                return

            match self.peek().TYPE:
                case T.CLASS: return
                case T.FUN: return
                case T.VAR: return
                case T.FOR: return
                case T.WHILE: return
                case T.IF: return
                case T.PRINT: return
                case T.RETURN: return

            self.advance()

    def consume(self, token_type: T, err_message: str):
        if (self.check(token_type)):
            return self.advance()

        token = self.peek()
        raise (self.error(token, err_message))

    def expression(self) -> Expr:
        # expression -> equality
        return self.expr_list()

    def expr_list(self) -> Expr:
        # expression -> expression "," expression
        # print("Expr_list")
        expr = self.equality()

        while self.match(T.COMMA):
            # print("Generating expr_list")
            op = self.previous()
            expr = Binary(expr, op, self.equality())
        return expr

    def equality(self) -> Expr:
        logging.debug("Equality")
        # equality -> comparison ( ( "!=" | "==" ) comparison )*
        expr = self.comparison()

        while self.match(T.BANG_EQUAL, T.EQUAL_EQUAL):
            logging.debug("Generating Equality")
            op = self.previous()
            expr = Binary(expr, op, self.comparison())
        return expr

    def comparison(self) -> Expr:
        logging.debug("Comparison")
        # comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )*

        expr = self.term()

        while self.match(T.GREATER, T.GREATER_EQUAL, T.LESS, T.LESS_EQUAL):
            logging.debug("Generating Comparison")
            op = self.previous()
            expr = Binary(expr, op, self.term())
        return expr

    def term(self) -> Expr:
        logging.debug("Term")
        # term -> factor ( ( "-" | "+" ) factor )*

        expr = self.factor()

        while self.match(T.PLUS, T.MINUS):
            logging.debug("Generating term")
            op = self.previous()
            expr = Binary(expr, op, self.factor())
        return expr

    def factor(self) -> Expr:
        logging.debug("Factor")

        expr = self.unary()

        while self.match(T.SLASH, T.STAR):
            logging.debug("Generating factor")
            op = self.previous()
            expr = Binary(expr, op, self.unary())
        return expr

    def unary(self):
        logging.debug("Unary")
        if self.match(T.BANG, T.MINUS):
            logging.debug("Generating unary")
            op = self.previous()
            return Unary(op, self.unary())
        return self.primary()

    def primary(self):
        logging.debug("Generated Primary")
        if self.match(T.FALSE):
            return Literal(False)
        if self.match(T.TRUE):
            return Literal(True)
        if self.match(T.NIL):
            return Literal(None)

        if self.match(T.NUMBER, T.STRING):
            return Literal(self.previous().LITERAL)

        if self.match(T.LEFT_PAREN):
            expr = self.expression()
            self.consume(T.RIGHT_PAREN, "Expect `)` after expression.")
            return Grouping(expr)

        raise (self.error(self.peek(), "Expect expression"))
