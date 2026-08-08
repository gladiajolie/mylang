import sys
from lexer import lex
from myparser import Parser
from interpreter import Interpreter

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    source = f.read()

tokens = lex(source)
ast = Parser(tokens).parse()

interpreter = Interpreter()
interpreter.run(ast)