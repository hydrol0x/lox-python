#!/usr/bin/env python3

from lexer import create_tokens

code = "( 5 + 2 ) - 6 / 3 * 4"

tokens = create_tokens(code)
print([token.to_string() for token in tokens])
