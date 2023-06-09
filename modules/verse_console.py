from nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter
import sys

sys.setrecursionlimit(1000000)

print("=========================================")
print(" ")
print(" ")
print("This is an interpreter written in python for the upcoming programming language Verse. Feel free to test verse features to your hearts content")
print("Authors: Kariyampalli Christy, Turobin-Ort Marcel")
print("License: MIT")
print(" ")
print(" ")
print("=========================================")
print(" ")
print(" ██▒   █▓▓█████  ██▀███    ██████ ▓█████ ")
print("▓██░   █▒▓█   ▀ ▓██ ▒ ██▒▒██    ▒ ▓█   ▀ ")
print(" ▓██  █▒░▒███   ▓██ ░▄█ ▒░ ▓██▄   ▒███   ")
print("  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄    ▒   ██▒▒▓█  ▄ ")
print("   ▒▀█░  ░▒████▒░██▓ ▒██▒▒██████▒▒░▒████▒")
print("   ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░░░ ▒░ ░")
print("   ░ ░░   ░ ░  ░  ░▒ ░ ▒░░ ░▒  ░ ░ ░ ░  ░")
print("     ░░     ░     ░░   ░ ░  ░  ░     ░   ")
print("      ░     ░  ░   ░           ░     ░  ░")
print("     ░                                   ")
print("                                         ")      
print("=========================================")
print(" ")
print("To quit the interpreter console, just enter QUIT or EXIT")
print(" ")
text = " "
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)

while True:
    text = input("[verse]>>> ")
    if text.lower() == "quit" or text.lower() == "exit":
        break
    lexer.input = text
    interpreter.reset()
    result = interpreter.interpret()
    print(repr(result))