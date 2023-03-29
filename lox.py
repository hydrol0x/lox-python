#!/usr/bin/env python3

import sys
import random
from lexer import Lexer
from error_handler import had_error
from prompts import PROMPT_LIST
from expr import Expr
from parser import Parser
from ast_printer import AST_printer


def run(program):
    if had_error:
        sys.exit(65)

    # tokens = program.split()
    # for token in tokens:
        # print(token)
    printer = AST_printer
    lex = Lexer(program)
    tokens = lex.scan_tokens()
    parser = Parser(tokens)
    expr = parser.parse()
    if expr:
        print(expr.to_string())
        print(printer.ast_print(expr))
    else:
        print("Error in parsing")
    # print([token.to_string() for token in lex.scan_tokens()])

# def report(self, line: int, where: str, message: str):
#     raise (f"[line {line} ] Error {where}: {message}")
#     self.had_error = True

# def error(self, line: int, message: str):
#     self.report(line, "", message)

def runFile(path):
    with open(path, "r") as file:
        program = file.read()
        run(program)

def runPrompt():
    while (True):
        prompt = PROMPT_LIST[random.randint(0,len(PROMPT_LIST)-1)]
        user_in = input(f"{prompt} ->")
        if not user_in and user_in != '':
            break
        run(user_in)
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

