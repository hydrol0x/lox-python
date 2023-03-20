#!/usr/bin/env python3

from lexer_debug import create_tokens

code = "5 2 3 6"

tokens = create_tokens(code)
print([token.to_string() for token in tokens])
