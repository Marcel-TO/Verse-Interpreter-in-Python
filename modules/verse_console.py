from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter
import start_text

start_text
print("=========================================")
print(" ")
print("To quit the interpreter console, just enter QUIT or EXIT")
print(" ")
text = " "
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)

while True:
    text = input(">>> ")
    if text.lower() == "quit" or text.lower() == "exit":
        break
    lexer.input = text
    interpreter.reset()
    result = interpreter.interpret()
    print(repr(result))