#!/usr/bin/env python3

import sys
import random
from lexer import Lexer
from error_handler import had_error
from prompts import PROMPT_LIST


def run(program):
    if had_error:
        sys.exit(65)

    # tokens = program.split()
    # for token in tokens:
        # print(token)
    lex = Lexer(program)
    print([token.to_string() for token in lex.scan_tokens()])

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

