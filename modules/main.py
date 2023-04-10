from syntaxtree.scopetable import ScopeTable
from syntaxtree.nodes import *
from structure.token import Token
from structure.tokenTypes import TokenTypes
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter


# table = ScopeTable()
# table.addScope("y", NumberNode(Token(TokenTypes.INTEGER, 7)), TokenTypes.INT_TYPE)

# table2 = ScopeTable()
# table2.addScope("x", NumberNode(Token(TokenTypes.INTEGER, 4)), TokenTypes.INT_TYPE)

# table.addScopeTable(table2)

# table.__info__()


# lexer = lexicon("x:4; >=; 1..10")

# while lexer.current_char is not None:
#     token = lexer.get_token(lexer.current_char)
#     print(str(token.value) + " is of the tokentype: " + str(token.type))
#     lexer.forward()

text = "for{i:int; i=3; i<7}"
# text = "x,y:int; x=7; y=3; x+y"
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print("\n Result = " + str(result))
print(" ")

# text = "for{i:int; i=3; i<7}"
text = "x,y:int; x=7; y=3; x+y"
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print("\n Result = " + str(result))