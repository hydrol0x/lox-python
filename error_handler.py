from token import Token
from tokenType import TokenType as T
global had_error
had_error = False

def report(line: int, where: str, message: str):
    print(f"[line {line};{where}] ERROR: {message}")
    had_error = True

def error(message: str, line=None, token: Token=None):
    if line:
        report(line,"",message)
    elif token == T.EOF: 
        report(token.LINE, "", message)
    else:
        report(token.LINE, "", f"`{token.LEXEME}` {message}")