#!/usr/bin/env python3

import sys
import random
from lexer import Lexer
from error_handler import had_error, had_runtime_error
from parser import ParseError
from prompts import PROMPT_LIST
from expr import Expr
from parser import Parser
from ast_printer import AST_printer
from interpreter import Interpreter
import logging

logging.basicConfig(level=logging.ERROR)


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
    stmts = []
    try:
        stmts = parser.parse()
    except ParseError:
        print("Parsing error")
    if stmts:
        interpreter.interpret(stmts)


def runFile(path):
    with open(path, "r") as file:
        program = file.read()
        interpreter = Interpreter()
        run(program, interpreter)


def runPrompt():
    while (True):
        # prompt = PROMPT_LIST[random.randint(0, len(PROMPT_LIST)-1)]
        prompt = '[plox]'
        user_in = input(f"{prompt} -> ")
        if not user_in and user_in != '':
            break
        interpreter = Interpreter()
        # TODO: add a 'REPL' bool to interpreter that, if enabled, has extra logic to process raw expressions as well
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
