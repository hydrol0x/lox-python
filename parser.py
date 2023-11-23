import logging
from expr import Expr, Binary, Grouping, Literal, Unary, Variable as VarExpr, Assign, Logical
from stmt import Stmt, Print, ExpressionStmt, Var as VarStmt, Block, If, While, Break
from tokens import Token
from tokenType import TokenType as T
from error_handler import error as lox_error, BreakException


class ParseError(RuntimeError):
    # TODO: possibly move to error_handler
    pass


class Parser:
    def __init__(self, tokens: list):
        logging.debug(f"Tokens: {[token.LEXEME for token in tokens]}")
        logging.debug(f"Token Types: {[token.TYPE for token in tokens]}")
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while (not self.is_at_end()):
            statements.append(self.declaration())
        return statements

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().TYPE == T.EOF

    def check(self, expected: T) -> bool:
        return False if self.is_at_end() else self.peek().TYPE == expected

    def previous(self) -> Token:
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

    def declaration(self, in_loop: bool = False) -> Stmt | None:
        try:
            if self.match(T.VAR):
                return self.var_declaration()

            return self.statement(in_loop)
        except ParseError as error:
            self.synchronize()
            return None

    def var_declaration(self) -> Stmt:
        name = self.consume(T.IDENTIFIER, "Expected variable name.")

        initializer = None
        if self.match(T.EQUAL):
            initializer = self.expression()

        self.consume(T.SEMICOLON, "Expected ';' after variable declaration.")
        return VarStmt(name, initializer)

    def statement(self, in_loop: bool) -> Stmt:
        if self.check(T.BREAK):
            return self.break_statement(in_loop)
        if self.match(T.FOR):
            return self.for_statement()
        if self.match(T.IF):
            return self.if_statement(in_loop)
        if self.match(T.PRINT):
            return self.print_statement()
        if self.match(T.WHILE):
            return self.while_statement()
        if self.match(T.LEFT_BRACE):
            return Block(self.block(in_loop))

        return self.expression_statement()

    def break_statement(self, in_loop: bool) -> Stmt:
        if not in_loop:
            raise self.error(
                self.peek(), "Expected 'break' to be inside of a loop.")
        self.consume(
            T.BREAK, "Unreachable; should have already checked for `break` with self.check()")
        self.consume(T.SEMICOLON, "Expected ';' after 'break'.")

        return Break()

    def for_statement(self) -> Stmt:
        self.consume(
            T.LEFT_PAREN, "Expected '(' to enclose conditional expression after 'for'."
        )
        initializer = None
        if self.match(T.SEMICOLON):
            pass
        elif self.match(T.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(T.SEMICOLON):
            condition = self.expression()
        self.consume(T.SEMICOLON, "Expected ';' after for loop condition.")

        increment = None
        if not self.check(T.RIGHT_PAREN):
            increment = self.expression()
        self.consume(T.RIGHT_PAREN, "Expected ')' after for loop clauses.")

        body = self.statement(in_loop=True)

        if increment:
            body = Block([body, ExpressionStmt(increment)])

        if condition == None:
            condition = Literal(True)

        body = While(condition, body)

        if initializer:
            body = Block([initializer, body])

        return body

    def while_statement(self) -> Stmt:

        self.consume(
            T.LEFT_PAREN, "Expected '(' to enclose conditional expression after 'while'."
        )
        condition = self.expression()
        self.consume(
            T.RIGHT_PAREN, "Expected ')' after 'while' condition"
        )

        body = self.statement(in_loop=True)

        return While(condition, body)

    def if_statement(self, in_loop: bool) -> Stmt:
        self.consume(
            T.LEFT_PAREN, "Expected '(' to enclose conditional expression after 'if'.")
        condition = self.expression()
        self.consume(
            T.RIGHT_PAREN, "Expected ')' after 'if' condition.")
        then_branch = self.statement(in_loop)
        else_branch = None
        if self.match(T.ELSE):
            else_branch = self.statement(in_loop)

        return If(condition, then_branch, else_branch)

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(T.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        value = self.expression()
        self.consume(T.SEMICOLON, "Expect ';' after value.")
        return ExpressionStmt(value)

    def block(self, in_loop: bool) -> list[Stmt]:
        statements = []
        while not self.check(T.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration(in_loop))

        self.consume(T.RIGHT_BRACE, "Expect '}' to close block.")
        return statements

    def expression(self) -> Expr:
        # expression -> equality
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.or_expr()

        if self.match(T.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, VarExpr):
                name = expr.name
                return Assign(name, value)

            self.error(
                equals, "Invalid assignment target; expected variable expression.")

        return expr

    def or_expr(self) -> Expr:
        expr = self.and_expr()

        while self.match(T.OR):
            or_op = self.previous()
            right = self.and_expr()
            expr = Logical(expr, or_op, right)

        return expr

    def and_expr(self) -> Expr:
        expr = self.expr_list()

        while self.match(T.AND):
            and_op = self.previous()
            right = self.expr_list()
            expr = Logical(expr, and_op, right)

        return expr

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

        if self.match(T.IDENTIFIER):
            return VarExpr(self.previous())

        if self.match(T.LEFT_PAREN):
            expr = self.expression()
            self.consume(T.RIGHT_PAREN, "Expect `)` after expression.")
            return Grouping(expr)

        raise (self.error(self.peek(), "Expect expression"))
