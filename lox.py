#!/usr/bin/env python3

import sys
import random
from lexer import Lexer
from error_handler import had_error, had_runtime_error
from prompts import PROMPT_LIST
from expr import Expr
from parser import Parser
from ast_printer import AST_printer
from interpreter import Interpreter
import logging

logging.basicConfig(level=logging.DEBUG)


def run(program, interpreter: Interpreter):
    # Interpreter accepted as arg so that in REPL, the intepreter will be persistent, keeping variables set in REPL persistent.
    # Indicate error in exit code
    if had_error:
        sys.exit(65)

    if had_runtime_error:
        sys.exit(70)

    # tokens = program.split()
    # for token in tokens:
        # print(token)
    printer = AST_printer()
    lex = Lexer(program)
    tokens = lex.scan_tokens()
    parser = Parser(tokens)
    expr = parser.parse()
    if expr:
        interpreter.interpret(expr)
    else:
        print('Parsing Error')

    # expressions = parser.parse_multiple()

    # print([expr.to_string() for expr in expressions])
    # for expr in expressions:
    #     print(expr.to_string())
    #     print(printer.ast_print(expr))
    #     # printer.ast_print(expr)

    # print([token.to_string() for token in lex.scan_tokens()])

# def report(self, line: int, where: str, message: str):
#     raise (f"[line {line} ] Error {where}: {message}")
#     self.had_error = True

# def error(self, line: int, message: str):
#     self.report(line, "", message)


def runFile(path):
    with open(path, "r") as file:
        program = file.read()
        interpreter = Interpreter()
        run(program, interpreter)


def runPrompt():
    while (True):
        prompt = PROMPT_LIST[random.randint(0, len(PROMPT_LIST)-1)]
        user_in = input(f"{prompt} ->")
        if not user_in and user_in != '':
            break
        interpreter = Interpreter()
        run(user_in, interpreter)
        had_error = False


args = sys.argv
n = len(args)
if n > 2:
    print("Usage: plox [script]")
    sys.exit(64)
elif n == 2:
    print(f"Running file {args[1]}")
    runFile(args[1])
else:
    runPrompt()
