from tokens import Token
from tokenType import TokenType as T

global had_error
had_error = False

global had_runtime_error
had_runtime_error = False


def report(line: int, where: str, message: str):
    # TODO: maybe make this have a 'type' parameter so that it can be used to convey error type, e.g RuntimeError vs ParseError (or in future more specific errors)
    print(f"[line {line};{where}] ERROR: {message}")
    had_error = True


def error(message: str, line=None, token: Token | None = None):
    if line:
        report(line, "", message)
    elif token == T.EOF:
        report(token.LINE, "", message)
    elif token:
        report(token.LINE, "", f"`{token.LEXEME}` {message}")
    else:
        # TODO: Figure out how to handle token is None
        pass


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        self.RuntimeError = RuntimeError(message)


def runtime_error(error: LoxRuntimeError):
    print(f'[line {error.token.LINE};] RuntimeError: {error.message}')
    had_runtime_error = True


class BreakException(SyntaxError):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        self.SyntaxError = SyntaxError(message)

# These are not actual errors but instead used to jump around call stack. However, to avoid circular imports they are in this file and not `interpreter.py`

class BreakException(RuntimeError): # Used to jump if `break` encountered.
    pass

class ReturnException(RuntimeError):
    def __init__(self, value: object):
        self.value = value
