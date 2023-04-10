from syntaxtree.scopetable import ScopeTable
from syntaxtree.nodes import *
from structure.token import Token
from structure.tokenTypes import TokenTypes
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter


# text = "for{i:int; i=3; i>7}"
text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)"
# text = "x:int; x=7; if(x<20) then x else 333"
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))