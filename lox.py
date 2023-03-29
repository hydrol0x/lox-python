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

    printer = AST_printer
    lex = Lexer(program)
    tokens = lex.scan_tokens()
    parser = Parser(tokens)
    expr = parser.parse()
    if expr:
        print(expr.to_string())
    else:
        print("Error in parsing")

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

