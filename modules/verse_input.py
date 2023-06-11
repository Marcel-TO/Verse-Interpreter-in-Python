import sys
from nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter
import start_text

sys.setrecursionlimit(1000000)

text = 'INPUT VERSE CODE HERE'

start_text
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))